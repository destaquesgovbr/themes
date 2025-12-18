#!/usr/bin/env python3
"""
Script para consolidar todas as descrições L3 no arquivo themes_tree_enriched.yaml
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


def parse_tree_structure(tree_content):
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


def build_enriched_yaml(l1_data, tree_structure, l3_descriptions):
    """
    Constrói a estrutura YAML enriquecida final
    """
    output = {'themes': []}

    for l1_theme in l1_data.get('themes', []):
        l1_code = l1_theme.get('code')

        # Copia dados L1
        l1_entry = {
            'code': l1_code,
            'label': l1_theme.get('label'),
            'description': l1_theme.get('description'),
            'keywords': l1_theme.get('keywords', []),
        }

        # Adiciona includes/excludes se existirem
        if 'includes' in l1_theme:
            l1_entry['includes'] = l1_theme['includes']
        if 'excludes' in l1_theme:
            l1_entry['excludes'] = l1_theme['excludes']

        # Adiciona L2s
        l1_entry['children'] = []

        if l1_code in tree_structure:
            for l2_code, l2_data in tree_structure[l1_code]['children'].items():
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
    print("Carregando arquivo L1 enriquecido...")
    l1_data = load_yaml(ENRICHED_FILE)

    print("Parseando estrutura da árvore temática...")
    tree_structure = parse_tree_structure(TREE_FILE)

    print("Carregando descrições L3...")
    l3_descriptions = load_l3_descriptions()
    print(f"  -> {len(l3_descriptions)} descrições L3 carregadas")

    print("Construindo YAML consolidado...")
    output = build_enriched_yaml(l1_data, tree_structure, l3_descriptions)

    print(f"Salvando em {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Árvore Temática Enriquecida Completa - DestaquesGovBr\n")
        f.write("# Versão: 3.0\n")
        f.write("# Data: 2025-12-18\n")
        f.write("# Inclui: Descrições L1 + Estrutura L2 + Descrições L3\n")
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
