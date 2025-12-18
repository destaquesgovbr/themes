"""
Subfase 4.2: Validação de Qualidade das Descrições

Analisa:
- Tamanho e complexidade das descrições
- Problemas de comprimento (muito curtas/longas)
- Distribuição de tamanhos por nível
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import THEMES_FILE, REPORTS_DIR
from utils.yaml_utils import load_yaml, iter_all_nodes, count_words, get_level
from colorama import Fore, Style, init

init(autoreset=True)

MIN_WORDS = 30
MAX_WORDS = 200
RECOMMENDED_MIN = {"L1": 80, "L2": 50, "L3": 30}
RECOMMENDED_MAX = {"L1": 200, "L2": 150, "L3": 100}


class QualityValidator:
    """Valida qualidade das descrições"""

    def __init__(self, themes_file: Path):
        self.themes_file = themes_file
        self.tree = load_yaml(themes_file)
        self.problems = []
        self.stats = defaultdict(list)

    def analyze_size_and_complexity(self):
        """Analisa tamanho e complexidade das descrições"""
        print(f"\n{Fore.CYAN}=== Análise de Tamanho e Complexidade ==={Style.RESET_ALL}\n")

        issues_by_type = defaultdict(list)

        for node in iter_all_nodes(self.tree):
            code = node.get("code", "?")
            label = node.get("label", "?")
            description = node.get("description", "")
            level = get_level(code)

            word_count = count_words(description)
            self.stats[f"{level}_word_counts"].append(word_count)

            # Verificar se descrição existe
            if not description or not description.strip():
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "missing_description",
                    "severity": "CRÍTICO",
                    "message": "Descrição ausente ou vazia"
                })
                issues_by_type["missing_description"].append(code)
                continue

            # Verificar tamanho absoluto (muito curta ou longa)
            if word_count < MIN_WORDS:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "too_short",
                    "severity": "ALTO",
                    "message": f"Descrição muito curta: {word_count} palavras (mínimo: {MIN_WORDS})"
                })
                issues_by_type["too_short"].append(code)

            elif word_count > MAX_WORDS:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "too_long",
                    "severity": "MÉDIO",
                    "message": f"Descrição muito longa: {word_count} palavras (máximo: {MAX_WORDS})"
                })
                issues_by_type["too_long"].append(code)

            # Verificar tamanho recomendado por nível
            rec_min = RECOMMENDED_MIN.get(level, MIN_WORDS)
            rec_max = RECOMMENDED_MAX.get(level, MAX_WORDS)

            if word_count < rec_min:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "below_recommended",
                    "severity": "BAIXO",
                    "message": f"Abaixo do recomendado para {level}: {word_count} palavras (recomendado: {rec_min}-{rec_max})"
                })
                issues_by_type["below_recommended"].append(code)

            elif word_count > rec_max:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "above_recommended",
                    "severity": "BAIXO",
                    "message": f"Acima do recomendado para {level}: {word_count} palavras (recomendado: {rec_min}-{rec_max})"
                })
                issues_by_type["above_recommended"].append(code)

        # Imprimir resumo
        self._print_size_summary(issues_by_type)

    def _print_size_summary(self, issues_by_type: Dict[str, List[str]]):
        """Imprime resumo da análise de tamanho"""
        import numpy as np

        print(f"{Fore.YELLOW}Estatísticas de Tamanho por Nível:{Style.RESET_ALL}")
        for level in ["L1", "L2", "L3"]:
            counts = self.stats.get(f"{level}_word_counts", [])
            if counts:
                print(f"  {level}: média={np.mean(counts):.1f}, "
                      f"mediana={np.median(counts):.1f}, "
                      f"min={min(counts)}, max={max(counts)}")

        print(f"\n{Fore.YELLOW}Problemas Identificados:{Style.RESET_ALL}")
        severity_order = ["missing_description", "too_short", "too_long",
                         "below_recommended", "above_recommended"]

        total_issues = 0
        for issue_type in severity_order:
            codes = issues_by_type.get(issue_type, [])
            if codes:
                count = len(codes)
                total_issues += count
                severity = self._get_severity(issue_type)
                color = self._get_color(severity)
                print(f"  {color}[{severity}] {issue_type}: {count} nós{Style.RESET_ALL}")
                if count <= 10:
                    print(f"    Códigos: {', '.join(codes)}")
                else:
                    print(f"    Códigos: {', '.join(codes[:10])} ... (+{count-10})")

        if total_issues == 0:
            print(f"  {Fore.GREEN}✓ Nenhum problema de tamanho encontrado{Style.RESET_ALL}")

    def _get_severity(self, issue_type: str) -> str:
        """Retorna severidade do tipo de problema"""
        severity_map = {
            "missing_description": "CRÍTICO",
            "too_short": "ALTO",
            "too_long": "MÉDIO",
            "below_recommended": "BAIXO",
            "above_recommended": "BAIXO"
        }
        return severity_map.get(issue_type, "BAIXO")

    def _get_color(self, severity: str) -> str:
        """Retorna cor para severidade"""
        color_map = {
            "CRÍTICO": Fore.RED,
            "ALTO": Fore.YELLOW,
            "MÉDIO": Fore.CYAN,
            "BAIXO": Fore.WHITE
        }
        return color_map.get(severity, Fore.WHITE)

    def generate_report(self):
        """Gera relatório de qualidade em Markdown"""
        report_file = REPORTS_DIR / "02_qualidade_report.md"
        problems_file = REPORTS_DIR / "02_problemas_qualidade.csv"

        # Gerar markdown
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Relatório de Validação de Qualidade - Subfase 4.2\n\n")
            f.write(f"**Arquivo analisado:** `{self.themes_file.name}`\n\n")
            f.write(f"**Total de problemas:** {len(self.problems)}\n\n")

            # Estatísticas de tamanho
            f.write("## 1. Análise de Tamanho e Complexidade\n\n")
            f.write("### Estatísticas por Nível\n\n")
            f.write("| Nível | Média (palavras) | Mediana | Mínimo | Máximo |\n")
            f.write("|-------|------------------|---------|--------|--------|\n")

            import numpy as np
            for level in ["L1", "L2", "L3"]:
                counts = self.stats.get(f"{level}_word_counts", [])
                if counts:
                    f.write(f"| {level} | {np.mean(counts):.1f} | "
                           f"{np.median(counts):.1f} | {min(counts)} | {max(counts)} |\n")

            # Problemas por severidade
            f.write("\n### Problemas Identificados\n\n")
            problems_by_severity = defaultdict(list)
            for p in self.problems:
                problems_by_severity[p["severity"]].append(p)

            for severity in ["CRÍTICO", "ALTO", "MÉDIO", "BAIXO"]:
                probs = problems_by_severity.get(severity, [])
                if probs:
                    f.write(f"\n#### Severidade: {severity} ({len(probs)} problemas)\n\n")

                    # Agrupar por tipo
                    by_type = defaultdict(list)
                    for p in probs:
                        by_type[p["type"]].append(p)

                    for ptype, items in by_type.items():
                        f.write(f"\n**{ptype}** ({len(items)} nós):\n\n")
                        for item in items[:20]:  # Limitar a 20 por tipo
                            f.write(f"- `{item['code']}` - {item['label']}: {item['message']}\n")
                        if len(items) > 20:
                            f.write(f"- ... e mais {len(items)-20} nós\n")

            # Recomendações
            f.write("\n## 2. Recomendações\n\n")
            if len(self.problems) == 0:
                f.write("✅ Nenhum problema crítico identificado. Árvore temática possui boa qualidade de descrições.\n")
            else:
                f.write("### Ações Sugeridas:\n\n")

                critical = [p for p in self.problems if p["severity"] == "CRÍTICO"]
                if critical:
                    f.write(f"1. **URGENTE:** Adicionar descrições ausentes ({len(critical)} nós)\n")

                high = [p for p in self.problems if p["severity"] == "ALTO"]
                if high:
                    f.write(f"2. **Prioridade Alta:** Expandir descrições muito curtas ({len(high)} nós)\n")

                medium = [p for p in self.problems if p["severity"] == "MÉDIO"]
                if medium:
                    f.write(f"3. **Prioridade Média:** Revisar descrições muito longas ({len(medium)} nós)\n")

                low = [p for p in self.problems if p["severity"] == "BAIXO"]
                if low:
                    f.write(f"4. **Prioridade Baixa:** Ajustar para faixas recomendadas ({len(low)} nós)\n")

        # Gerar CSV com problemas
        import csv
        with open(problems_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["code", "label", "level", "type", "severity", "message"])
            writer.writeheader()
            writer.writerows(self.problems)

        print(f"\n{Fore.GREEN}✓ Relatório salvo em: {report_file}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Problemas salvos em: {problems_file}{Style.RESET_ALL}")


def main():
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Subfase 4.2: Validação de Qualidade das Descrições{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    validator = QualityValidator(THEMES_FILE)

    # Análise 1: Tamanho e complexidade
    validator.analyze_size_and_complexity()

    # Gerar relatórios
    print(f"\n{Fore.CYAN}=== Gerando Relatórios ==={Style.RESET_ALL}")
    validator.generate_report()

    # Sumário final
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Análise de qualidade (tamanho) concluída{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    critical_count = len([p for p in validator.problems if p["severity"] == "CRÍTICO"])
    high_count = len([p for p in validator.problems if p["severity"] == "ALTO"])

    if critical_count > 0:
        print(f"{Fore.RED}⚠ {critical_count} problemas CRÍTICOS encontrados!{Style.RESET_ALL}")
        return 1
    elif high_count > 0:
        print(f"{Fore.YELLOW}⚠ {high_count} problemas de ALTA prioridade encontrados{Style.RESET_ALL}")
        return 0
    else:
        print(f"{Fore.GREEN}✓ Qualidade das descrições está adequada{Style.RESET_ALL}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
