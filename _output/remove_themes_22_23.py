#!/usr/bin/env python3
"""
Script para remover os temas 22 e 23 do arquivo themes_tree_enriched_full.yaml
Esses temas foram marcados para remoção conforme decisões estruturais:
- Tema 22: Eventos Oficiais e Cerimônias (removido - DEC-002)
- Tema 23: Estatísticas e Dados Públicos (fundido com tema 20 - DEC-001)
"""

import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
INPUT_FILE = BASE_DIR / "themes_tree_enriched_full.yaml"
OUTPUT_FILE = INPUT_FILE  # Sobrescrever o mesmo arquivo

def load_yaml_safe(filepath):
    """Carrega arquivo YAML de forma segura"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml_safe(filepath, data):
    """Salva arquivo YAML de forma segura"""
    with open(filepath, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Árvore Temática Enriquecida Completa - DestaquesGovBr\n")
        f.write("# Versão: 3.1\n")
        f.write("# Data: 2025-12-18\n")
        f.write("# Inclui: Descrições L1 + L2 + L3 completas\n")
        f.write("# Total: 23 temas L1 (temas 22 e 23 originais removidos)\n")
        f.write("# Estrutura final após decisões DEC-001 e DEC-002\n\n")

        yaml.dump(data, f, allow_unicode=True, sort_keys=False,
                  default_flow_style=False, width=120)

def main():
    print("Carregando themes_tree_enriched_full.yaml...")
    tree = load_yaml_safe(INPUT_FILE)

    original_count = len(tree['themes'])
    print(f"  Total de temas L1: {original_count}")

    # Filtrar temas, removendo 22 e 23
    filtered_themes = []
    removed_themes = []

    for theme in tree['themes']:
        code = theme.get('code')
        if code in ['22', '23']:
            removed_themes.append(f"{code} - {theme.get('label')}")
        else:
            filtered_themes.append(theme)

    tree['themes'] = filtered_themes

    print(f"\nTemas removidos ({len(removed_themes)}):")
    for theme in removed_themes:
        print(f"  - {theme}")

    print(f"\nTotal de temas após remoção: {len(filtered_themes)}")

    # Calcular estatísticas
    l2_count = sum(len(t.get('children', [])) for t in filtered_themes)
    l3_count = sum(len(l2.get('children', []))
                   for t in filtered_themes
                   for l2 in t.get('children', []))

    l2_with_desc = sum(1 for t in filtered_themes
                       for l2 in t.get('children', [])
                       if 'description' in l2)

    l3_with_desc = sum(1 for t in filtered_themes
                       for l2 in t.get('children', [])
                       for l3 in l2.get('children', [])
                       if 'description' in l3)

    print(f"\nEstatísticas finais:")
    print(f"  L1: {len(filtered_themes)} temas")
    print(f"  L2: {l2_count} subtemas ({l2_with_desc} com descrição)")
    print(f"  L3: {l3_count} categorias ({l3_with_desc} com descrição)")
    print(f"  Total de descrições: {len(filtered_themes) + l2_with_desc + l3_with_desc}")

    # Salvar arquivo atualizado
    print(f"\nSalvando arquivo atualizado...")
    save_yaml_safe(OUTPUT_FILE, tree)

    print(f"\n✅ Arquivo atualizado com sucesso!")
    print(f"   Temas removidos: {len(removed_themes)}")
    print(f"   Arquivo: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
