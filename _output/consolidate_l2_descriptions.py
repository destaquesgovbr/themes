#!/usr/bin/env python3
"""
Script para consolidar descrições L2 no arquivo themes_tree_enriched_full.yaml
Lê todos os arquivos L2_*.yaml e insere as descrições no lugar correto da hierarquia
"""

import yaml
import glob
import re
from pathlib import Path

def load_yaml_safe(filepath):
    """Carrega arquivo YAML de forma segura"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml_safe(filepath, data):
    """Salva arquivo YAML de forma segura"""
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

def main():
    base_path = Path(__file__).parent

    # Carrega o arquivo principal
    print("Carregando themes_tree_enriched_full.yaml...")
    main_file = base_path.parent / 'themes_tree_enriched_full.yaml'
    tree = load_yaml_safe(main_file)

    # Carrega todos os arquivos L2
    l2_files = sorted(glob.glob(str(base_path / 'L2_*.yaml')))
    print(f"Encontrados {len(l2_files)} arquivos L2")

    # Cria um dicionário de descrições L2 por código
    l2_descriptions = {}

    for l2_file in l2_files:
        print(f"Processando {Path(l2_file).name}...")
        l2_data = load_yaml_safe(l2_file)

        for item in l2_data:
            code = item['code']
            l2_descriptions[code] = {
                'description': item['description'],
                'keywords': item['keywords']
            }

    print(f"Total de descrições L2 carregadas: {len(l2_descriptions)}")

    # Função recursiva para inserir descrições L2
    def insert_l2_descriptions(nodes):
        for node in nodes:
            code = node.get('code', '')

            # Se tem filhos (children), processar recursivamente
            if 'children' in node:
                # Verificar se algum filho é L2 (formato XX.XX)
                for child in node['children']:
                    child_code = child.get('code', '')

                    # Se é L2 e temos descrição para ele
                    if child_code in l2_descriptions:
                        child['description'] = l2_descriptions[child_code]['description']
                        child['keywords'] = l2_descriptions[child_code]['keywords']
                        print(f"  ✓ Inserida descrição L2 para {child_code}")

                # Continuar recursivamente
                insert_l2_descriptions(node['children'])

    # Processar a árvore
    print("\nInserindo descrições L2 na árvore...")
    insert_l2_descriptions(tree['themes'])

    # Salvar arquivo atualizado
    output_file = main_file
    print(f"\nSalvando arquivo atualizado em {output_file}...")
    save_yaml_safe(output_file, tree)

    print("\n✅ Consolidação concluída com sucesso!")
    print(f"   Total de descrições L2 inseridas: {len(l2_descriptions)}")
    print(f"   Arquivo salvo: {output_file}")

if __name__ == '__main__':
    main()
