#!/usr/bin/env python3
"""
Script para consolidar todas as descrições L3 no arquivo themes_tree_enriched.yaml
Versão 2: Usa a estrutura original de 25 temas
"""

import yaml
import glob
import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path(__file__).parent
ENRICHED_FILE = BASE_DIR / "themes_tree_enriched.yaml"
TREE_FILE = BASE_DIR / "themes_tree.yaml"
OUTPUT_FILE = BASE_DIR / "themes_tree_enriched_full.yaml"

# Descrições L1 para temas que estão faltando no enriched original
MISSING_L1_DESCRIPTIONS = {
    "22": {
        "label": "Eventos Oficiais e Cerimônias",
        "description": """Eventos oficiais do governo, cerimônias públicas, visitas de Estado,
inaugurações e atos protocolares. Inclui discursos oficiais, comemorações
de datas cívicas e luto nacional.""",
        "keywords": [
            "evento oficial", "cerimônia", "solenidade", "inauguração",
            "discurso", "pronunciamento", "visita oficial", "visita de Estado",
            "comemoração", "data cívica", "luto nacional", "homenagem",
            "protocolo", "coletiva de imprensa", "descerramento de placa",
            "posse", "condolência", "aniversário institucional"
        ],
        "includes": [
            "Discursos e pronunciamentos oficiais",
            "Inaugurações de obras e equipamentos públicos",
            "Visitas oficiais nacionais e internacionais",
            "Cerimônias de posse e homenagens",
            "Comemorações de datas cívicas e efemérides"
        ],
        "excludes": [
            "Eventos culturais e festivais (ver Cultura)",
            "Eventos esportivos (ver Esportes)",
            "Eventos turísticos (ver Turismo)"
        ]
    },
    "23": {
        "label": "Estatísticas e Dados Públicos",
        "description": """Produção e divulgação de estatísticas oficiais, censos, pesquisas,
indicadores econômicos e sociais. Inclui transparência, dados abertos
e infraestrutura de dados públicos.""",
        "keywords": [
            "estatística", "IBGE", "censo", "pesquisa", "indicador",
            "dados públicos", "dados abertos", "transparência",
            "Portal da Transparência", "LAI", "IPCA", "PIB", "IDH",
            "taxa de desemprego", "PNAD", "prestação de contas",
            "auditoria", "licitação", "contrato público"
        ],
        "includes": [
            "Censos demográfico e agropecuário",
            "Pesquisas socioeconômicas do IBGE",
            "Indicadores econômicos e sociais",
            "Transparência e acesso à informação",
            "Dados abertos e interoperabilidade"
        ],
        "excludes": [
            "Governança e gestão pública (ver Políticas Públicas)",
            "Fiscalização e auditorias de programas (ver tema específico)"
        ]
    },
    "24": {
        "label": "Minorias e Grupos Especiais",
        "description": """Políticas para grupos específicos como mulheres, população negra,
indígenas, LGBTQIA+, pessoas com deficiência e comunidades tradicionais.""",
        "keywords": [
            "mulher", "feminino", "igualdade de gênero", "violência contra mulher",
            "Maria da Penha", "negro", "negra", "racial", "racismo",
            "igualdade racial", "quilombola", "indígena", "índio", "terra indígena",
            "Funai", "LGBTQIA+", "LGBT", "homofobia", "pessoa com deficiência",
            "PCD", "acessibilidade", "inclusão", "comunidade tradicional",
            "ribeirinho", "cigano"
        ],
        "includes": [
            "Políticas de igualdade de gênero",
            "Combate ao racismo",
            "Direitos indígenas e demarcação de terras",
            "Direitos LGBTQIA+",
            "Acessibilidade e inclusão de PCD",
            "Comunidades quilombolas e tradicionais"
        ],
        "excludes": [
            "Direitos humanos gerais (ver Justiça)",
            "Assistência social (ver Desenvolvimento Social)",
            "Educação inclusiva (ver Educação)"
        ]
    },
    "25": {
        "label": "Habitação e Urbanismo",
        "description": """Políticas habitacionais, programas de moradia, planejamento urbano
e saneamento básico. Inclui Minha Casa Minha Vida e regularização fundiária.""",
        "keywords": [
            "habitação", "moradia", "casa", "apartamento", "Minha Casa Minha Vida",
            "MCMV", "Caixa", "financiamento habitacional", "regularização fundiária",
            "favela", "comunidade", "urbanização", "planejamento urbano",
            "plano diretor", "saneamento", "água", "esgoto", "tratamento de esgoto",
            "abastecimento de água", "drenagem", "enchente", "alagamento",
            "cidade", "município", "periferia"
        ],
        "includes": [
            "Programas habitacionais federais",
            "Financiamento de moradia",
            "Saneamento básico",
            "Urbanização de áreas precárias",
            "Regularização fundiária"
        ],
        "excludes": [
            "Infraestrutura de transporte urbano (ver Infraestrutura)",
            "Meio ambiente urbano (ver Meio Ambiente)",
            "Assistência a pessoas em situação de rua (ver Desenvolvimento Social)"
        ]
    }
}


def load_yaml(filepath):
    """Carrega arquivo YAML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_l3_descriptions():
    """Carrega todas as descrições L3 dos arquivos gerados"""
    l3_map = {}
    for filepath in sorted(glob.glob(str(OUTPUT_DIR / "L3_*.yaml"))):
        data = load_yaml(filepath)
        if data:
            for item in data:
                code = item.get('code')
                if code:
                    l3_map[code] = {
                        'description': item.get('description', '').strip(),
                        'keywords': item.get('keywords', []),
                        'examples': item.get('examples', [])
                    }
    return l3_map


def load_l1_descriptions():
    """Carrega descrições L1 do arquivo enriched, complementando com as faltantes"""
    l1_map = {}

    enriched = load_yaml(ENRICHED_FILE)
    for theme in enriched.get('themes', []):
        code = theme.get('code')
        # Mapeamento para corrigir numeração (no enriched, 22=Minorias, 23=Habitação)
        if code == "22" and theme.get('label') == "Minorias e Grupos Especiais":
            mapped_code = "24"
        elif code == "23" and theme.get('label') == "Habitação e Urbanismo":
            mapped_code = "25"
        else:
            mapped_code = code

        l1_map[mapped_code] = {
            'label': theme.get('label'),
            'description': theme.get('description'),
            'keywords': theme.get('keywords', []),
            'includes': theme.get('includes', []),
            'excludes': theme.get('excludes', [])
        }

    # Adiciona descrições que estão faltando (temas 22 e 23 originais)
    for code, data in MISSING_L1_DESCRIPTIONS.items():
        if code not in l1_map:
            l1_map[code] = data

    return l1_map


def parse_tree_structure():
    """
    Parse a estrutura hierárquica do themes_tree.yaml
    Retorna dict com estrutura L1 -> L2 -> L3
    """
    structure = {}

    with open(TREE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_l1 = None
    current_l2 = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # L1: "01 - Economia e Finanças:"
        if not line.startswith(' ') and stripped.endswith(':') and ' - ' in stripped:
            parts = stripped[:-1].split(' - ', 1)
            code = parts[0].strip()
            label = parts[1].strip()
            current_l1 = code
            structure[code] = {'label': label, 'children': {}}

        # L2: "  01.01 - Política Econômica:"
        elif line.startswith('  ') and not line.startswith('    ') and stripped.endswith(':') and '.' in stripped and ' - ' in stripped:
            parts = stripped[:-1].split(' - ', 1)
            code = parts[0].strip()
            label = parts[1].strip()
            current_l2 = code
            if current_l1:
                structure[current_l1]['children'][code] = {'label': label, 'children': []}

        # L3: "    - 01.01.01 - Política Fiscal"
        elif stripped.startswith('- ') and '.' in stripped and stripped.count('.') >= 2:
            parts = stripped[2:].split(' - ', 1)
            if len(parts) == 2:
                code = parts[0].strip()
                label = parts[1].strip()
                if current_l1 and current_l2 and current_l2 in structure[current_l1]['children']:
                    structure[current_l1]['children'][current_l2]['children'].append({
                        'code': code,
                        'label': label
                    })

    return structure


def build_enriched_yaml(l1_descriptions, tree_structure, l3_descriptions):
    """
    Constrói a estrutura YAML enriquecida final
    """
    output = {'themes': []}

    # Ordena os códigos L1 numericamente
    sorted_l1_codes = sorted(tree_structure.keys(), key=lambda x: int(x))

    for l1_code in sorted_l1_codes:
        l1_tree = tree_structure[l1_code]
        l1_desc = l1_descriptions.get(l1_code, {})

        # Copia dados L1
        l1_entry = {
            'code': l1_code,
            'label': l1_desc.get('label', l1_tree['label']),
            'description': l1_desc.get('description', ''),
            'keywords': l1_desc.get('keywords', []),
        }

        # Adiciona includes/excludes se existirem
        if l1_desc.get('includes'):
            l1_entry['includes'] = l1_desc['includes']
        if l1_desc.get('excludes'):
            l1_entry['excludes'] = l1_desc['excludes']

        # Adiciona L2s
        l1_entry['children'] = []

        for l2_code, l2_data in l1_tree['children'].items():
            l2_entry = {
                'code': l2_code,
                'label': l2_data['label'],
                # L2 descriptions serão adicionadas na Fase 3
                'children': []
            }

            # Adiciona L3s
            for l3_item in l2_data['children']:
                l3_code = l3_item['code']
                l3_entry = {
                    'code': l3_code,
                    'label': l3_item['label']
                }

                # Adiciona descrições L3 se existirem
                if l3_code in l3_descriptions:
                    l3_desc = l3_descriptions[l3_code]
                    l3_entry['description'] = l3_desc['description']
                    l3_entry['keywords'] = l3_desc['keywords']
                    if l3_desc['examples']:
                        l3_entry['examples'] = l3_desc['examples']

                l2_entry['children'].append(l3_entry)

            l1_entry['children'].append(l2_entry)

        output['themes'].append(l1_entry)

    return output


def main():
    print("Carregando descrições L1...")
    l1_descriptions = load_l1_descriptions()
    print(f"  -> {len(l1_descriptions)} descrições L1 carregadas")

    print("Parseando estrutura da árvore temática...")
    tree_structure = parse_tree_structure()
    print(f"  -> {len(tree_structure)} temas L1 na estrutura")

    print("Carregando descrições L3...")
    l3_descriptions = load_l3_descriptions()
    print(f"  -> {len(l3_descriptions)} descrições L3 carregadas")

    print("Construindo YAML consolidado...")
    output = build_enriched_yaml(l1_descriptions, tree_structure, l3_descriptions)

    print(f"Salvando em {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Árvore Temática Enriquecida Completa - DestaquesGovBr\n")
        f.write("# Versão: 3.0\n")
        f.write("# Data: 2025-12-18\n")
        f.write("# Inclui: Descrições L1 + Estrutura L2 + Descrições L3\n")
        f.write("# Total: 25 temas L1\n")
        f.write("# Próximo passo: Adicionar descrições L2 (Fase 3)\n\n")

        yaml.dump(output, f,
                  default_flow_style=False,
                  allow_unicode=True,
                  sort_keys=False,
                  width=120)

    # Estatísticas
    l1_count = len(output['themes'])
    l2_count = sum(len(t['children']) for t in output['themes'])
    l3_count = sum(len(l2['children']) for t in output['themes'] for l2 in t['children'])
    l3_with_desc = sum(1 for t in output['themes']
                       for l2 in t['children']
                       for l3 in l2['children']
                       if 'description' in l3)

    print(f"\nEstatísticas:")
    print(f"  L1: {l1_count} temas")
    print(f"  L2: {l2_count} subtemas")
    print(f"  L3: {l3_count} categorias")
    print(f"  L3 com descrição: {l3_with_desc} ({l3_with_desc/l3_count*100:.1f}%)")

    print(f"\nArquivo salvo: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
