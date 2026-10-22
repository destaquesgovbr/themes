"""Validação estrutural das árvores temáticas (versão 3.2).

Garante que os três YAML do repositório:
- carregam com PyYAML (safe_load);
- têm 24 temas L1 (01–21, 24, 25 e 26), sem códigos duplicados e com pais coerentes;
- estão alinhados entre si e com o banco (tabela ``themes``, carregada a partir de
  ``themes_tree_enriched_full.yaml``);
- aplicam o contrato do tema 26 (DEC-006): 19.03 → 26.01 e 19.04 → 26.02.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
FULL = ROOT / "themes_tree_enriched_full.yaml"
ENRICHED = ROOT / "themes_tree_enriched.yaml"
LEGACY = ROOT / "themes_tree.yaml"
README = ROOT / "README.md"

EXPECTED_L1 = [f"{i:02d}" for i in range(1, 22)] + ["24", "25", "26"]
EXPECTED_COUNTS = {1: 24, 2: 106, 3: 459}
VERSION = "3.2"

THEME_26_LABEL = "Defesa Civil e Gestão de Desastres"
THEME_26_L2 = {"26.01": "Defesa Civil", "26.02": "Situações de Emergência"}
# Contrato: os L3 do 26 são os L3 de 19.03/19.04, com os mesmos labels, renumerados.
THEME_26_L3 = {
    "26.01.01": "Preparação para Desastres",
    "26.01.02": "Planejamento de Evacuação",
    "26.01.03": "Resposta a Desastres",
    "26.01.04": "Monitoramento de Riscos Naturais",
    "26.01.05": "Gestão de Abrigos",
    "26.02.01": "Resgate e Salvamento",
    "26.02.02": "Logística de Emergência",
    "26.02.03": "Ações Humanitárias",
    "26.02.04": "Reconstrução Pós-Desastre",
    "26.02.05": "Assistência a Deslocados Internos",
}
REMOVED_PREFIXES = ("19.03", "19.04", "22", "23")

# Termos de Defesa Civil que não podem mais puxar notícias para 05.02.01 e 15.02.03.
CONTRADICTORY_TERMS = (
    "defesa civil",
    "calamidade",
    "situação de emergência",
    "cemaden",
    "desabrigad",
    "desalojad",
)

CODE_PATTERN = {
    1: re.compile(r"^\d{2}$"),
    2: re.compile(r"^\d{2}\.\d{2}$"),
    3: re.compile(r"^\d{2}\.\d{2}\.\d{2}$"),
}
LEGACY_LINE = re.compile(r"^(\d{2}(?:\.\d{2}){0,2}) - (.+)$")
# Mesmo regex do activitypub-server/scripts/seed-actors.ts (lê só os L1).
ACTIVITYPUB_L1 = re.compile(r"^(\d{2}) - (.+):$")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _load(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _flatten_structured(nodes, level=1, parent=None):
    """Achata a árvore no formato ``themes: [{code, label, children}]``."""
    for node in nodes:
        yield {
            "code": node["code"],
            "label": node["label"],
            "level": level,
            "parent": parent,
            "node": node,
        }
        yield from _flatten_structured(node.get("children") or [], level + 1, node["code"])


def _split_legacy(key: str):
    match = LEGACY_LINE.match(key)
    assert match, f"entrada fora do formato 'NN - Nome': {key!r}"
    return match.group(1), match.group(2)


def _flatten_legacy(tree: dict):
    """Achata o ``themes_tree.yaml`` (formato ``'01 - Nome': {'01.01 - Nome': [...]}``)."""
    for l1_key, l2_map in tree.items():
        l1_code, l1_label = _split_legacy(l1_key)
        yield {"code": l1_code, "label": l1_label, "level": 1, "parent": None}
        for l2_key, l3_list in (l2_map or {}).items():
            l2_code, l2_label = _split_legacy(l2_key)
            yield {"code": l2_code, "label": l2_label, "level": 2, "parent": l1_code}
            for l3_item in l3_list or []:
                l3_code, l3_label = _split_legacy(l3_item)
                yield {"code": l3_code, "label": l3_label, "level": 3, "parent": l2_code}


@pytest.fixture(scope="module")
def full_flat():
    return list(_flatten_structured(_load(FULL)["themes"]))


@pytest.fixture(scope="module")
def full_index(full_flat):
    return {item["code"]: item for item in full_flat}


@pytest.fixture(scope="module")
def legacy_flat():
    return list(_flatten_legacy(_load(LEGACY)))


@pytest.fixture(scope="module")
def enriched_l1():
    return _load(ENRICHED)["themes"]


# --------------------------------------------------------------------------- #
# Estrutura (vale para os dois arquivos com a árvore completa)
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("flat_fixture", ["full_flat", "legacy_flat"])
def test_contagens_por_nivel(flat_fixture, request):
    flat = request.getfixturevalue(flat_fixture)
    counts = Counter(item["level"] for item in flat)
    assert dict(counts) == EXPECTED_COUNTS


@pytest.mark.parametrize("flat_fixture", ["full_flat", "legacy_flat"])
def test_l1_esperados_em_ordem(flat_fixture, request):
    flat = request.getfixturevalue(flat_fixture)
    assert [i["code"] for i in flat if i["level"] == 1] == EXPECTED_L1


@pytest.mark.parametrize("flat_fixture", ["full_flat", "legacy_flat"])
def test_sem_codigos_duplicados(flat_fixture, request):
    flat = request.getfixturevalue(flat_fixture)
    dup = [code for code, n in Counter(i["code"] for i in flat).items() if n > 1]
    assert dup == []


@pytest.mark.parametrize("flat_fixture", ["full_flat", "legacy_flat"])
def test_formato_do_codigo_e_pais_coerentes(flat_fixture, request):
    flat = request.getfixturevalue(flat_fixture)
    for item in flat:
        code, level, parent = item["code"], item["level"], item["parent"]
        assert isinstance(code, str), f"código não é string: {code!r}"
        assert CODE_PATTERN[level].match(code), f"{code} não tem formato de L{level}"
        if level == 1:
            assert parent is None
        else:
            assert parent == code.rsplit(".", 1)[0], f"{code} com pai {parent}"


@pytest.mark.parametrize("flat_fixture", ["full_flat", "legacy_flat"])
def test_codigos_removidos_ausentes(flat_fixture, request):
    flat = request.getfixturevalue(flat_fixture)
    for item in flat:
        code = item["code"]
        assert not any(
            code == p or code.startswith(p + ".") for p in REMOVED_PREFIXES
        ), f"código removido ainda presente: {code}"


@pytest.mark.parametrize("flat_fixture", ["full_flat", "legacy_flat"])
def test_contrato_tema_26(flat_fixture, request):
    flat = request.getfixturevalue(flat_fixture)
    index = {i["code"]: i for i in flat}
    assert index["26"]["label"] == THEME_26_LABEL
    assert {c: index[c]["label"] for c in THEME_26_L2} == THEME_26_L2
    assert {c: index[c]["label"] for c in THEME_26_L3} == THEME_26_L3
    filhos_26 = sorted(i["code"] for i in flat if (i["code"] + ".").startswith("26."))
    assert filhos_26 == sorted(["26", *THEME_26_L2, *THEME_26_L3])


# --------------------------------------------------------------------------- #
# Alinhamento entre os arquivos
# --------------------------------------------------------------------------- #


def test_legado_identico_ao_full(full_flat, legacy_flat):
    """``themes_tree.yaml`` tem exatamente os códigos, labels e pais do full (= banco)."""
    as_tuples = lambda flat: [(i["code"], i["label"], i["level"], i["parent"]) for i in flat]
    assert as_tuples(legacy_flat) == as_tuples(full_flat)


def test_enriched_l1_alinhado_ao_full(enriched_l1, full_flat):
    l1_full = [(i["code"], i["label"]) for i in full_flat if i["level"] == 1]
    assert [(t["code"], t["label"]) for t in enriched_l1] == l1_full


def test_enriched_l1_tem_mesmo_conteudo_do_full(enriched_l1, full_index):
    """Todo L1 tem descrição/keywords/includes/excludes iguais nos dois arquivos."""
    for theme in enriched_l1:
        code = theme["code"]
        for field in ("description", "keywords", "includes", "excludes"):
            assert theme[field] == full_index[code]["node"][field], (code, field)


# --------------------------------------------------------------------------- #
# Códigos L1/L2 entre aspas (strings explícitas, à prova de parsers YAML 1.2)
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "path,quote", [(FULL, "'"), (ENRICHED, '"')], ids=["full", "enriched"]
)
def test_codigos_l1_l2_entre_aspas(path, quote):
    text = path.read_text(encoding="utf-8")
    codes = re.findall(r"^\s*-?\s*code:\s*(\S+)\s*$", text, flags=re.M)
    l1_l2 = [c for c in codes if c.strip("'\"").count(".") <= 1]
    assert l1_l2, "nenhum código L1/L2 encontrado"
    sem_aspas = [c for c in l1_l2 if not (c.startswith(quote) and c.endswith(quote))]
    assert sem_aspas == []


# --------------------------------------------------------------------------- #
# Versão
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("path", [FULL, ENRICHED, LEGACY], ids=lambda p: p.name)
def test_versao_no_cabecalho(path):
    head = path.read_text(encoding="utf-8").splitlines()[:10]
    assert f"# Versão: {VERSION}" in head


# --------------------------------------------------------------------------- #
# Conteúdo do tema 26 e limpeza de 05.02.01 / 15.02.03 / 19
# --------------------------------------------------------------------------- #


def test_tema_26_enriquecido(full_index):
    node = full_index["26"]["node"]
    for field in ("description", "keywords", "includes", "excludes"):
        assert node.get(field), f"26 sem {field}"
    excludes = " ".join(node["excludes"])
    # Distingue explicitamente de clima (05), benefícios (15) e segurança pública (04).
    for alvo in ("05.02.01", "15.02.03", "Segurança Pública", "bombeiros"):
        assert alvo in excludes, f"excludes do 26 não citam {alvo!r}"


def test_tema_26_preserva_conteudo_de_19_03_e_19_04(full_index):
    """L2/L3 do 26 mantêm descrição, keywords e exemplos herdados de 19.03/19.04."""
    for code in (*THEME_26_L2, *THEME_26_L3):
        node = full_index[code]["node"]
        assert node.get("description"), code
        assert node.get("keywords"), code
        if code in THEME_26_L3:
            assert node.get("examples"), code


def test_excludes_do_19_apontam_para_o_26(full_index):
    excludes = full_index["19"]["node"]["excludes"]
    assert any(THEME_26_LABEL in e for e in excludes)
    assert not any("ver tema relacionado" in e for e in excludes)


@pytest.mark.parametrize("code", ["04", "05", "15"])
def test_l1_vizinhos_excluem_defesa_civil(full_index, code):
    excludes = full_index[code]["node"]["excludes"]
    assert any(THEME_26_LABEL in e for e in excludes), code


@pytest.mark.parametrize("code", ["05.02.01", "15.02.03"])
def test_keywords_sem_termos_de_defesa_civil(full_index, code):
    node = full_index[code]["node"]
    blob = " | ".join(node["keywords"] + node.get("examples", [])).lower()
    achados = [t for t in CONTRADICTORY_TERMS if t in blob]
    assert achados == [], f"{code} ainda tem termos de Defesa Civil: {achados}"


# --------------------------------------------------------------------------- #
# Contrato com consumidores
# --------------------------------------------------------------------------- #


def test_activitypub_seed_le_os_24_l1():
    """activitypub-server/scripts/seed-actors.ts lê os L1 linha a linha com regex."""
    found = {}
    for line in LEGACY.read_text(encoding="utf-8").splitlines():
        match = ACTIVITYPUB_L1.match(line)
        if match:
            found[match.group(1)] = match.group(2)
    assert list(found) == EXPECTED_L1
    assert found["26"] == THEME_26_LABEL


def test_populate_themes_compativel(full_flat):
    """data-platform/scripts/populate_themes.py: code/label/level/parent_code planos."""
    rows = [(i["code"], i["label"], i["level"], i["parent"]) for i in full_flat]
    assert len(rows) == sum(EXPECTED_COUNTS.values())
    assert all(isinstance(c, str) and isinstance(lbl, str) for c, lbl, *_ in rows)


def test_readme_registra_o_sha256_do_full_copiado_no_data_platform():
    """data-platform/test-data é cópia byte a byte do full, com o sha256 fixado lá.

    Mudar o full sem trocar o hash no README (e a cópia no data-platform) reabre o drift:
    duas versões da mesma taxonomia, uma aqui e outra nos testes do data-platform.
    """
    digest = hashlib.sha256(FULL.read_bytes()).hexdigest()
    assert digest in README.read_text(encoding="utf-8"), (
        f"README não registra o sha256 atual do full ({digest}); copie o full para "
        "data-platform/test-data/ e atualize o hash no README e em "
        "data-platform/tests/unit/test_themes_test_data.py (SHA256_THEMES_FULL)"
    )
