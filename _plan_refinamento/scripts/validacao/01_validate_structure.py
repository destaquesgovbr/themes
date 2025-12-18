#!/usr/bin/env python3
"""
Subfase 4.1: Validação de Consistência Estrutural

Este script valida:
1. Sintaxe YAML e encoding
2. Unicidade de códigos e labels
3. Hierarquia (órfãos, referências quebradas)
4. Campos obrigatórios
5. Estatísticas de completude
"""

import sys
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

import yaml

# Adicionar diretório pai ao path para imports
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    THEMES_FILE, REPORTS_DIR, MIN_KEYWORDS, COLORS,
    print_config
)


class StructureValidator:
    """Validador de estrutura da árvore temática"""

    def __init__(self, themes_file: Path):
        self.themes_file = themes_file
        self.tree = None
        self.errors = []
        self.warnings = []
        self.stats = {
            "l1_count": 0,
            "l2_count": 0,
            "l3_count": 0,
            "total_nodes": 0,
        }

    def load_yaml(self) -> bool:
        """Carrega e valida sintaxe YAML"""
        print(f"{COLORS['blue']}1. Validando sintaxe YAML...{COLORS['reset']}")

        try:
            with open(self.themes_file, 'r', encoding='utf-8') as f:
                self.tree = yaml.safe_load(f)

            print(f"  {COLORS['green']}✓{COLORS['reset']} Sintaxe YAML válida")
            print(f"  {COLORS['green']}✓{COLORS['reset']} Encoding UTF-8 correto")
            return True

        except yaml.YAMLError as e:
            self.errors.append(f"Erro de sintaxe YAML: {e}")
            print(f"  {COLORS['red']}✗{COLORS['reset']} Erro de sintaxe YAML: {e}")
            return False

        except UnicodeDecodeError as e:
            self.errors.append(f"Erro de encoding: {e}")
            print(f"  {COLORS['red']}✗{COLORS['reset']} Erro de encoding: {e}")
            return False

        except Exception as e:
            self.errors.append(f"Erro ao carregar arquivo: {e}")
            print(f"  {COLORS['red']}✗{COLORS['reset']} Erro: {e}")
            return False

    def validate_uniqueness(self) -> None:
        """Valida unicidade de códigos e labels"""
        print(f"\n{COLORS['blue']}2. Validando unicidade de códigos e labels...{COLORS['reset']}")

        all_codes = []
        all_labels = []
        code_locations = defaultdict(list)  # Para rastrear duplicações

        def collect_codes_labels(nodes, parent_code="ROOT"):
            for node in nodes:
                code = node.get('code', '')
                label = node.get('label', '')

                all_codes.append(code)
                all_labels.append(label)
                code_locations[code].append(f"{parent_code} -> {label}")

                if 'children' in node:
                    collect_codes_labels(node['children'], code)

        collect_codes_labels(self.tree.get('themes', []))

        # Verificar códigos duplicados
        code_counts = Counter(all_codes)
        duplicated_codes = [(code, count) for code, count in code_counts.items() if count > 1]

        if duplicated_codes:
            for code, count in duplicated_codes:
                locations = code_locations[code]
                self.errors.append(
                    f"Código duplicado '{code}' ({count}x): {', '.join(locations)}"
                )
                print(f"  {COLORS['red']}✗{COLORS['reset']} Código duplicado: {code} ({count}x)")
        else:
            print(f"  {COLORS['green']}✓{COLORS['reset']} Todos os códigos são únicos ({len(all_codes)} códigos)")

        # Verificar labels duplicados (apenas warning, não é erro crítico)
        label_counts = Counter(all_labels)
        duplicated_labels = [(label, count) for label, count in label_counts.items() if count > 1]

        if duplicated_labels:
            for label, count in duplicated_labels:
                self.warnings.append(f"Label duplicado: '{label}' ({count}x)")
            print(f"  {COLORS['yellow']}⚠{COLORS['reset']}  {len(duplicated_labels)} labels duplicados (não crítico)")
        else:
            print(f"  {COLORS['green']}✓{COLORS['reset']} Todos os labels são únicos")

    def validate_hierarchy(self) -> None:
        """Valida hierarquia: pais válidos, sem órfãos"""
        print(f"\n{COLORS['blue']}3. Validando hierarquia...{COLORS['reset']}")

        l1_codes = set()
        l2_codes = set()
        l3_codes = set()

        orphan_l2 = []
        orphan_l3 = []

        # Coletar todos os códigos por nível
        for l1 in self.tree.get('themes', []):
            l1_code = l1.get('code')
            l1_codes.add(l1_code)
            self.stats['l1_count'] += 1

            for l2 in l1.get('children', []):
                l2_code = l2.get('code')
                l2_codes.add(l2_code)
                self.stats['l2_count'] += 1

                # Verificar se L2 pertence ao pai correto
                if not l2_code.startswith(l1_code + "."):
                    orphan_l2.append(f"{l2_code} (pai: {l1_code})")

                for l3 in l2.get('children', []):
                    l3_code = l3.get('code')
                    l3_codes.add(l3_code)
                    self.stats['l3_count'] += 1

                    # Verificar se L3 pertence ao pai correto
                    if not l3_code.startswith(l2_code + "."):
                        orphan_l3.append(f"{l3_code} (pai: {l2_code})")

        self.stats['total_nodes'] = self.stats['l1_count'] + self.stats['l2_count'] + self.stats['l3_count']

        # Reportar órfãos
        if orphan_l2:
            for orphan in orphan_l2:
                self.errors.append(f"L2 órfão ou numeração incorreta: {orphan}")
            print(f"  {COLORS['red']}✗{COLORS['reset']} {len(orphan_l2)} nós L2 com numeração incorreta")
        else:
            print(f"  {COLORS['green']}✓{COLORS['reset']} Todos os L2 têm numeração correta")

        if orphan_l3:
            for orphan in orphan_l3:
                self.errors.append(f"L3 órfão ou numeração incorreta: {orphan}")
            print(f"  {COLORS['red']}✗{COLORS['reset']} {len(orphan_l3)} nós L3 com numeração incorreta")
        else:
            print(f"  {COLORS['green']}✓{COLORS['reset']} Todos os L3 têm numeração correta")

        print(f"\n  Estatísticas de hierarquia:")
        print(f"    L1: {self.stats['l1_count']} temas")
        print(f"    L2: {self.stats['l2_count']} subtemas")
        print(f"    L3: {self.stats['l3_count']} categorias")
        print(f"    Total: {self.stats['total_nodes']} nós")

    def validate_required_fields(self) -> None:
        """Valida presença de campos obrigatórios"""
        print(f"\n{COLORS['blue']}4. Validando campos obrigatórios...{COLORS['reset']}")

        missing_fields = []

        def check_node(node, level, path=""):
            code = node.get('code', '')
            label = node.get('label', '')
            node_path = f"{path}/{code}" if path else code

            # Campos obrigatórios para todos
            required = ['code', 'label', 'description', 'keywords']

            for field in required:
                if field not in node or not node[field]:
                    missing_fields.append({
                        'level': level,
                        'code': code,
                        'label': label,
                        'field': field,
                        'path': node_path
                    })

            # Validar keywords mínimo
            keywords = node.get('keywords', [])
            if len(keywords) < MIN_KEYWORDS:
                self.warnings.append(
                    f"{level} {code}: Apenas {len(keywords)} keywords (mínimo {MIN_KEYWORDS})"
                )

            # L1 deve ter includes e excludes
            if level == "L1":
                if 'includes' not in node or not node['includes']:
                    self.warnings.append(f"L1 {code}: Falta campo 'includes'")
                if 'excludes' not in node or not node['excludes']:
                    self.warnings.append(f"L1 {code}: Falta campo 'excludes'")

            # Recursão para filhos
            if 'children' in node:
                next_level = "L2" if level == "L1" else "L3"
                for child in node['children']:
                    check_node(child, next_level, node_path)

        # Verificar todos os nós
        for l1 in self.tree.get('themes', []):
            check_node(l1, "L1")

        # Reportar campos faltantes
        if missing_fields:
            by_field = defaultdict(list)
            for item in missing_fields:
                by_field[item['field']].append(f"{item['level']} {item['code']}")

            for field, nodes in by_field.items():
                self.errors.append(f"Campo '{field}' faltando em {len(nodes)} nós: {', '.join(nodes[:5])}...")
                print(f"  {COLORS['red']}✗{COLORS['reset']} Campo '{field}' faltando em {len(nodes)} nós")
        else:
            print(f"  {COLORS['green']}✓{COLORS['reset']} Todos os nós têm campos obrigatórios")

        # Reportar warnings de keywords
        low_keyword_count = sum(1 for w in self.warnings if "keywords" in w.lower())
        if low_keyword_count:
            print(f"  {COLORS['yellow']}⚠{COLORS['reset']}  {low_keyword_count} nós com menos de {MIN_KEYWORDS} keywords")

        # Reportar warnings de includes/excludes
        missing_includes_excludes = sum(1 for w in self.warnings if "includes" in w.lower() or "excludes" in w.lower())
        if missing_includes_excludes:
            print(f"  {COLORS['yellow']}⚠{COLORS['reset']}  {missing_includes_excludes} nós L1 sem includes/excludes")

    def calculate_distribution_stats(self) -> Dict:
        """Calcula estatísticas de distribuição"""
        print(f"\n{COLORS['blue']}5. Calculando estatísticas de distribuição...{COLORS['reset']}")

        distribution = {
            "l1": [],
            "l2_per_l1": {},
            "l3_per_l2": {},
        }

        for l1 in self.tree.get('themes', []):
            l1_code = l1.get('code')
            l1_label = l1.get('label')
            l2_children = l1.get('children', [])
            l2_count = len(l2_children)

            distribution["l1"].append({
                "code": l1_code,
                "label": l1_label,
                "l2_count": l2_count
            })

            distribution["l2_per_l1"][l1_code] = l2_count

            for l2 in l2_children:
                l2_code = l2.get('code')
                l3_count = len(l2.get('children', []))
                distribution["l3_per_l2"][l2_code] = l3_count

        # Estatísticas de distribuição
        l2_counts = list(distribution["l2_per_l1"].values())
        l3_counts = list(distribution["l3_per_l2"].values())

        distribution["stats"] = {
            "l2_per_l1": {
                "min": min(l2_counts) if l2_counts else 0,
                "max": max(l2_counts) if l2_counts else 0,
                "avg": sum(l2_counts) / len(l2_counts) if l2_counts else 0,
            },
            "l3_per_l2": {
                "min": min(l3_counts) if l3_counts else 0,
                "max": max(l3_counts) if l3_counts else 0,
                "avg": sum(l3_counts) / len(l3_counts) if l3_counts else 0,
            }
        }

        print(f"\n  Distribuição L2 por L1:")
        print(f"    Mín: {distribution['stats']['l2_per_l1']['min']}")
        print(f"    Máx: {distribution['stats']['l2_per_l1']['max']}")
        print(f"    Média: {distribution['stats']['l2_per_l1']['avg']:.1f}")

        print(f"\n  Distribuição L3 por L2:")
        print(f"    Mín: {distribution['stats']['l3_per_l2']['min']}")
        print(f"    Máx: {distribution['stats']['l3_per_l2']['max']}")
        print(f"    Média: {distribution['stats']['l3_per_l2']['avg']:.1f}")

        # Identificar desequilíbrios
        l2_imbalance = distribution["stats"]["l2_per_l1"]["max"] / distribution["stats"]["l2_per_l1"]["min"] if distribution["stats"]["l2_per_l1"]["min"] > 0 else 0
        l3_imbalance = distribution["stats"]["l3_per_l2"]["max"] / distribution["stats"]["l3_per_l2"]["min"] if distribution["stats"]["l3_per_l2"]["min"] > 0 else 0

        if l2_imbalance > 3:
            self.warnings.append(f"Desequilíbrio significativo em L2 (razão {l2_imbalance:.1f}:1)")
            print(f"  {COLORS['yellow']}⚠{COLORS['reset']}  Desequilíbrio L2: razão {l2_imbalance:.1f}:1")

        if l3_imbalance > 5:
            self.warnings.append(f"Desequilíbrio significativo em L3 (razão {l3_imbalance:.1f}:1)")
            print(f"  {COLORS['yellow']}⚠{COLORS['reset']}  Desequilíbrio L3: razão {l3_imbalance:.1f}:1")

        return distribution

    def generate_report(self, distribution: Dict) -> None:
        """Gera relatório final em Markdown"""
        print(f"\n{COLORS['blue']}6. Gerando relatórios...{COLORS['reset']}")

        # Relatório em Markdown
        report_file = REPORTS_DIR / "01_estrutura_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Validação Estrutural\n\n")
            f.write(f"**Data:** {Path(__file__).stat().st_mtime}\n")
            f.write(f"**Arquivo validado:** `{self.themes_file.name}`\n\n")

            f.write("---\n\n")

            f.write("## Resumo\n\n")
            f.write(f"- **L1:** {self.stats['l1_count']} temas principais\n")
            f.write(f"- **L2:** {self.stats['l2_count']} subtemas\n")
            f.write(f"- **L3:** {self.stats['l3_count']} categorias folha\n")
            f.write(f"- **Total:** {self.stats['total_nodes']} nós\n\n")

            f.write(f"- **Erros:** {len(self.errors)}\n")
            f.write(f"- **Warnings:** {len(self.warnings)}\n\n")

            # Status
            if self.errors:
                f.write(f"**Status:** ❌ FALHOU - {len(self.errors)} erro(s) crítico(s)\n\n")
            elif self.warnings:
                f.write(f"**Status:** ⚠️  PASSOU COM WARNINGS - {len(self.warnings)} aviso(s)\n\n")
            else:
                f.write("**Status:** ✅ PASSOU - Nenhum problema encontrado\n\n")

            f.write("---\n\n")

            # Erros
            if self.errors:
                f.write("## ❌ Erros Críticos\n\n")
                for i, error in enumerate(self.errors, 1):
                    f.write(f"{i}. {error}\n")
                f.write("\n")

            # Warnings
            if self.warnings:
                f.write("## ⚠️  Warnings\n\n")
                for i, warning in enumerate(self.warnings, 1):
                    f.write(f"{i}. {warning}\n")
                f.write("\n")

            # Distribuição
            f.write("## 📊 Distribuição\n\n")
            f.write("### L2 por L1\n\n")
            f.write(f"- Mínimo: {distribution['stats']['l2_per_l1']['min']}\n")
            f.write(f"- Máximo: {distribution['stats']['l2_per_l1']['max']}\n")
            f.write(f"- Média: {distribution['stats']['l2_per_l1']['avg']:.1f}\n\n")

            f.write("### L3 por L2\n\n")
            f.write(f"- Mínimo: {distribution['stats']['l3_per_l2']['min']}\n")
            f.write(f"- Máximo: {distribution['stats']['l3_per_l2']['max']}\n")
            f.write(f"- Média: {distribution['stats']['l3_per_l2']['avg']:.1f}\n\n")

            f.write("### Detalhamento por L1\n\n")
            f.write("| Código | Tema | L2 | L3 Total |\n")
            f.write("|--------|------|----:|----------:|\n")

            for l1_info in distribution['l1']:
                l1_code = l1_info['code']
                l3_total = sum(
                    distribution['l3_per_l2'].get(l2_code, 0)
                    for l2_code in distribution['l3_per_l2']
                    if l2_code.startswith(l1_code + ".")
                )
                f.write(f"| {l1_code} | {l1_info['label']} | {l1_info['l2_count']} | {l3_total} |\n")

        print(f"  {COLORS['green']}✓{COLORS['reset']} Relatório Markdown: {report_file}")

        # Estatísticas em JSON
        stats_file = REPORTS_DIR / "01_estrutura_stats.json"
        stats_data = {
            "summary": self.stats,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "distribution": distribution
        }

        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)

        print(f"  {COLORS['green']}✓{COLORS['reset']} Estatísticas JSON: {stats_file}")

    def run(self) -> bool:
        """Executa todas as validações"""
        print(f"{COLORS['bold']}{'='*70}{COLORS['reset']}")
        print(f"{COLORS['bold']}Subfase 4.1: Validação de Consistência Estrutural{COLORS['reset']}")
        print(f"{COLORS['bold']}{'='*70}{COLORS['reset']}\n")

        print_config()

        # 1. Carregar YAML
        if not self.load_yaml():
            return False

        # 2-5. Validações
        self.validate_uniqueness()
        self.validate_hierarchy()
        self.validate_required_fields()
        distribution = self.calculate_distribution_stats()

        # 6. Gerar relatórios
        self.generate_report(distribution)

        # Resumo final
        print(f"\n{COLORS['bold']}{'='*70}{COLORS['reset']}")
        print(f"{COLORS['bold']}RESULTADO{COLORS['reset']}\n")

        if self.errors:
            print(f"{COLORS['red']}❌ FALHOU{COLORS['reset']}: {len(self.errors)} erro(s) crítico(s)")
            print(f"\nPrimeiros erros:")
            for error in self.errors[:5]:
                print(f"  • {error}")
            if len(self.errors) > 5:
                print(f"  ... e mais {len(self.errors) - 5} erro(s)")
            return False

        elif self.warnings:
            print(f"{COLORS['yellow']}⚠️  PASSOU COM WARNINGS{COLORS['reset']}: {len(self.warnings)} aviso(s)")
            print(f"\nPrimeiros warnings:")
            for warning in self.warnings[:5]:
                print(f"  • {warning}")
            if len(self.warnings) > 5:
                print(f"  ... e mais {len(self.warnings) - 5} warning(s)")
            return True

        else:
            print(f"{COLORS['green']}✅ PASSOU{COLORS['reset']}: Nenhum problema encontrado!")
            print(f"\nEstatísticas:")
            print(f"  • {self.stats['l1_count']} temas L1")
            print(f"  • {self.stats['l2_count']} subtemas L2")
            print(f"  • {self.stats['l3_count']} categorias L3")
            print(f"  • {self.stats['total_nodes']} nós totais")
            return True


def main():
    """Função principal"""
    validator = StructureValidator(THEMES_FILE)
    success = validator.run()

    print(f"\n{COLORS['bold']}Relatórios gerados:{COLORS['reset']}")
    print(f"  • {REPORTS_DIR / '01_estrutura_report.md'}")
    print(f"  • {REPORTS_DIR / '01_estrutura_stats.json'}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
