"""
Utilitários para manipulação de arquivos YAML da árvore temática
"""
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Generator


def load_yaml(themes_file: Path) -> Dict:
    """Carrega árvore temática de arquivo YAML"""
    with open(themes_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_themes_tree(themes_file: Path) -> Dict:
    """Alias para load_yaml (compatibilidade)"""
    return load_yaml(themes_file)


def save_themes_tree(themes_file: Path, tree: Dict) -> None:
    """Salva árvore temática em arquivo YAML"""
    with open(themes_file, 'w', encoding='utf-8') as f:
        yaml.dump(tree, f, allow_unicode=True, sort_keys=False,
                  default_flow_style=False, width=120)


def iter_all_nodes(tree: Dict) -> Generator[Dict, None, None]:
    """
    Itera sobre todos os nós da árvore

    Yields:
        Dict: Cada nó da árvore
    """
    def _iter_nodes(nodes):
        for node in nodes:
            yield node

            # Recursivamente processar filhos
            if 'children' in node:
                yield from _iter_nodes(node['children'])

    yield from _iter_nodes(tree.get('themes', []))


def get_siblings(tree: Dict, code: str) -> List[Dict]:
    """
    Retorna lista de irmãos de um nó (nós no mesmo nível com mesmo pai)

    Args:
        tree: Árvore temática completa
        code: Código do nó

    Returns:
        Lista de nós irmãos (incluindo o próprio nó)
    """
    # Determinar nível e pai
    parts = code.split('.')
    level = len(parts)

    siblings = []

    if level == 1:  # L1 - irmãos são todos os L1
        siblings = tree.get('themes', [])

    elif level >= 2:  # L2 ou L3 - buscar pai e retornar seus filhos
        # Buscar pai
        parent_code = '.'.join(parts[:-1])
        parent_level, parent_node = get_node_by_code(tree, parent_code)

        if parent_node:
            siblings = parent_node.get('children', [])

    return siblings


def get_level(code: str) -> str:
    """
    Determina o nível de um nó baseado no código

    Args:
        code: Código do nó (ex: "01", "01.02", "01.02.03")

    Returns:
        "L1", "L2", ou "L3"
    """
    if not code:
        return "?"

    parts = code.split(".")
    level_map = {1: "L1", 2: "L2", 3: "L3"}
    return level_map.get(len(parts), "?")


def count_words(text: str) -> int:
    """Conta palavras em um texto"""
    return len(text.split())


def get_node_by_code(tree: Dict, code: str) -> Tuple[str, Dict]:
    """
    Busca nó por código

    Returns:
        Tuple[level, node]: Nível e nó encontrado, ou (None, None) se não encontrado
    """
    for node in iter_all_nodes(tree):
        if node.get('code') == code:
            level = get_level(code)
            return level, node

    return None, None
