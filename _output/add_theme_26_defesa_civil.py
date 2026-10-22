#!/usr/bin/env python3
"""
Versão 3.2 da árvore (DEC-006): cria o L1 26 - Defesa Civil e Gestão de Desastres
em themes_tree_enriched_full.yaml.

- 19.03 (Defesa Civil) → 26.01, com 19.03.01–05 → 26.01.01–05 (mesmos labels e conteúdo);
- 19.04 (Situações de Emergência) → 26.02, com 19.04.01–05 → 26.02.01–05;
- excludes do 19 passam a apontar para o 26; 04, 05 e 15 ganham um exclude para o 26;
- 05.02.01 e 15.02.03 perdem keywords/exemplos de Defesa Civil;
- códigos L1 '08' e '09' passam a sair entre aspas (como os demais L1/L2).

Os textos de L1 (04, 05, 15, 19 e 26) são os mesmos do themes_tree_enriched.yaml
(editado à mão); tests/test_themes_tree.py confere a igualdade.

Uso: python _output/add_theme_26_defesa_civil.py  (aborta se o 26 já existir)
"""

import copy
import re
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent
FULL_FILE = BASE_DIR / "themes_tree_enriched_full.yaml"

HEADER = (
    "# Árvore Temática Enriquecida Completa - DestaquesGovBr\n"
    "# Versão: 3.2\n"
    "# Data: 2026-10-21\n"
    "# Inclui: Descrições L1 + L2 + L3 completas\n"
    "# Total: 24 temas L1 (01–21, 24, 25 e 26); temas 22 e 23 originais removidos (DEC-001/DEC-002)\n"
    "# 3.2: novo L1 26 - Defesa Civil e Gestão de Desastres (19.03 → 26.01, 19.04 → 26.02; DEC-006)\n\n"
)

REF_26 = "(ver Defesa Civil e Gestão de Desastres)"

THEME_26 = {
    "code": "26",
    "label": "Defesa Civil e Gestão de Desastres",
    "description": (
        "Proteção e defesa civil e gestão de riscos e desastres naturais ou\n"
        "tecnológicos em todas as fases: prevenção, preparação, resposta e\n"
        "recuperação. Inclui a atuação do SINPDEC e das defesas civis, alertas à\n"
        "população, reconhecimento de situação de emergência e calamidade pública,\n"
        "socorro às vítimas, abrigos e reconstrução de áreas atingidas.\n"
    ),
    "keywords": [
        "defesa civil",
        "Defesa Civil Nacional",
        "proteção e defesa civil",
        "SINPDEC",
        "SEDEC",
        "Secretaria Nacional de Defesa Civil",
        "CENAD",
        "Cemaden",
        "gestão de riscos",
        "gestão de desastres",
        "prevenção de desastres",
        "área de risco",
        "alerta de desastres",
        "Defesa Civil Alerta",
        "situação de emergência",
        "estado de calamidade",
        "calamidade pública",
        "reconhecimento federal",
        "resposta a desastres",
        "socorro às vítimas",
        "busca e salvamento",
        "desabrigados",
        "desalojados",
        "abrigo temporário",
        "assistência humanitária",
        "reconstrução",
        "recuperação pós-desastre",
    ],
    "includes": [
        "Atuação da Defesa Civil nos níveis federal, estadual e municipal (SINPDEC)",
        "Prevenção, preparação e gestão de riscos de desastres",
        "Monitoramento de riscos e alertas à população (Cemaden, Defesa Civil Alerta)",
        "Reconhecimento federal de situação de emergência e estado de calamidade pública",
        "Resposta a desastres: busca e salvamento, socorro, assistência humanitária e abrigos",
        "Repasses federais para resposta, restabelecimento e reconstrução de áreas atingidas",
    ],
    "excludes": [
        "Eventos climáticos extremos tratados como pauta de clima, adaptação e mitigação, "
        "sem ação de defesa civil (ver Meio Ambiente, 05.02.01 Catástrofes Climáticas)",
        "Auxílios e benefícios de renda a famílias atingidas "
        "(ver Desenvolvimento Social, 15.02.03 Apoio Emergencial)",
        "Policiamento e atuação rotineira de bombeiros e forças de segurança fora de "
        "desastres (ver Segurança Pública)",
        "Operações militares e defesa nacional sem relação com desastres "
        "(ver Defesa e Forças Armadas)",
        "Ajuda humanitária a outros países "
        "(ver Relações Internacionais, 12.02.01 Assistência Humanitária)",
        "Obras permanentes de drenagem e saneamento urbano (ver Habitação e Urbanismo)",
    ],
}

EXCLUDES_19_OLD = "Defesa civil e desastres (se foco civil, ver tema relacionado)"
EXCLUDES_19_NEW = (
    "Defesa civil, desastres e situações de emergência, inclusive com apoio das "
    f"Forças Armadas {REF_26}"
)

NEW_EXCLUDES = {
    "04": f"Defesa civil e resposta a desastres, inclusive resgates feitos por bombeiros {REF_26}",
    "05": f"Ações de defesa civil: alertas, socorro, abrigos e reconstrução após desastres {REF_26}",
    "15": f"Socorro, abrigos e demais ações de defesa civil em desastres {REF_26}",
}

L3_UPDATES = {
    "05.02.01": {
        "description": (
            "Eventos climáticos extremos como enchentes, secas severas, deslizamentos e\n"
            "tempestades sob a ótica das mudanças climáticas: frequência, causas, impactos\n"
            "ambientais, adaptação e resiliência. Alertas, decretação de emergência, socorro,\n"
            "abrigos e reconstrução pertencem a 26 - Defesa Civil e Gestão de Desastres."
        ),
        "keywords": [
            "catástrofes climáticas",
            "eventos climáticos extremos",
            "desastres naturais",
            "eventos extremos",
            "enchentes",
            "inundações",
            "alagamentos",
            "enxurradas",
            "secas extremas",
            "estiagem severa",
            "seca histórica",
            "deslizamentos de terra",
            "desabamentos",
            "chuvas intensas",
            "onda de calor",
            "El Niño",
            "La Niña",
            "adaptação climática",
            "resiliência climática",
            "desastres ambientais",
        ],
        "examples": [
            "Estudo associa aumento de enchentes e secas extremas no país ao aquecimento global",
            "Governo apresenta plano de adaptação para cidades vulneráveis a eventos climáticos extremos",
            "El Niño deve intensificar a estiagem no Norte e as chuvas no Sul, aponta boletim climático",
        ],
    },
    "15.02.03": {
        "description": (
            "Auxílios e benefícios temporários de transferência de renda para famílias afetadas\n"
            "por emergências, calamidade pública, desastres naturais ou crises econômicas. Socorro,\n"
            "abrigos e demais ações de defesa civil pertencem a 26 - Defesa Civil e Gestão de Desastres."
        ),
        "keywords": [
            "auxílio emergencial, benefício emergencial",
            "auxílio extraordinário, benefício temporário",
            "antecipação de benefícios, parcela adicional",
            "renda emergencial, transferência de renda emergencial",
            "crise econômica, apoio financeiro a famílias atingidas",
        ],
        "examples": [
            "Governo libera auxílio emergencial para famílias atingidas por enchentes no Sul do país",
            "MDS antecipa o pagamento do Bolsa Família em municípios atingidos por enchentes",
            "Benefício emergencial temporário é prorrogado para trabalhadores informais afetados pela crise",
        ],
    },
}

MOVES = {"19.03": "26.01", "19.04": "26.02"}


def _index(nodes, acc=None):
    acc = {} if acc is None else acc
    for node in nodes:
        acc[node["code"]] = node
        _index(node.get("children") or [], acc)
    return acc


def _renumber(l2: dict, new_code: str) -> dict:
    """Copia um L2 trocando o prefixo do código dele e dos L3, sem mudar a ordem das chaves."""
    old_code = l2["code"]
    moved = copy.deepcopy(l2)
    moved["code"] = new_code
    for l3 in moved.get("children") or []:
        assert l3["code"].startswith(old_code + "."), l3["code"]
        l3["code"] = new_code + l3["code"][len(old_code):]
    return moved


def transform(tree: dict) -> dict:
    themes = tree["themes"]
    if any(t["code"] == "26" for t in themes):
        sys.exit("O tema 26 já existe; nada a fazer.")

    by_code = {t["code"]: t for t in themes}
    l19 = by_code["19"]

    moved = {}
    kept = []
    for l2 in l19["children"]:
        if l2["code"] in MOVES:
            moved[l2["code"]] = _renumber(l2, MOVES[l2["code"]])
        else:
            kept.append(l2)
    assert set(moved) == set(MOVES), moved.keys()
    l19["children"] = kept

    excludes_19 = l19["excludes"]
    excludes_19[excludes_19.index(EXCLUDES_19_OLD)] = EXCLUDES_19_NEW

    for code, line in NEW_EXCLUDES.items():
        by_code[code]["excludes"].append(line)

    index = _index(themes)
    for code, fields in L3_UPDATES.items():
        index[code].update(fields)

    theme_26 = copy.deepcopy(THEME_26)
    theme_26["children"] = [moved["19.03"], moved["19.04"]]
    themes.append(theme_26)
    return tree


def dump(tree: dict) -> str:
    body = yaml.dump(tree, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    # '08' e '09' são strings para o PyYAML (não casam com int YAML 1.1) e saem sem aspas;
    # um parser YAML 1.2 os leria como inteiros. Força aspas como nos demais L1/L2.
    body = re.sub(r"^- code: (0[89])$", r"- code: '\1'", body, flags=re.M)
    return HEADER + body


def main():
    with FULL_FILE.open(encoding="utf-8") as fh:
        tree = yaml.safe_load(fh)
    FULL_FILE.write_text(dump(transform(tree)), encoding="utf-8")
    print(f"Atualizado: {FULL_FILE}")


if __name__ == "__main__":
    main()
