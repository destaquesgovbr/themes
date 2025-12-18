"""
Subfase 4.2: Análise de Keywords

Verifica:
- Quantidade de keywords (mínimo 5, recomendado 8-15)
- Keywords genéricas demais
- Keywords duplicadas entre irmãos
- Cobertura de termos técnicos vs coloquiais
"""

import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import THEMES_FILE, REPORTS_DIR
from utils.yaml_utils import load_yaml, iter_all_nodes, get_level
from colorama import Fore, Style, init

init(autoreset=True)

MIN_KEYWORDS = 5
RECOMMENDED_MIN = 8
RECOMMENDED_MAX = 15

# Keywords consideradas genéricas demais
GENERIC_KEYWORDS = {
    "brasil", "governo", "federal", "nacional", "brasileiro", "brasileira",
    "país", "estado", "município", "público", "pública", "programa",
    "projeto", "ação", "política", "políticas", "sistema", "serviço"
}


class KeywordAnalyzer:
    """Analisa qualidade e consistência das keywords"""

    def __init__(self, themes_file: Path):
        self.themes_file = themes_file
        self.tree = load_yaml(themes_file)
        self.problems = []
        self.stats = defaultdict(int)

    def analyze_keyword_quantity(self):
        """Analisa quantidade de keywords por nó"""
        print(f"\n{Fore.CYAN}=== Análise de Quantidade de Keywords ==={Style.RESET_ALL}\n")

        issues_by_level = defaultdict(list)

        for node in iter_all_nodes(self.tree):
            code = node.get("code", "?")
            label = node.get("label", "?")
            keywords = node.get("keywords", [])
            level = get_level(code)

            kw_count = len(keywords)
            self.stats[f"{level}_keyword_counts"] += 1

            # Verificar mínimo absoluto
            if kw_count < MIN_KEYWORDS:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "insufficient_keywords",
                    "severity": "ALTO",
                    "count": kw_count,
                    "message": f"Keywords insuficientes: {kw_count} (mínimo: {MIN_KEYWORDS})"
                })
                issues_by_level[level].append(code)
                self.stats[f"{level}_insufficient"] += 1

            # Verificar faixa recomendada
            elif kw_count < RECOMMENDED_MIN:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "below_recommended_keywords",
                    "severity": "BAIXO",
                    "count": kw_count,
                    "message": f"Abaixo do recomendado: {kw_count} keywords (recomendado: {RECOMMENDED_MIN}-{RECOMMENDED_MAX})"
                })
                self.stats[f"{level}_below_recommended"] += 1

            elif kw_count > RECOMMENDED_MAX:
                self.problems.append({
                    "code": code,
                    "label": label,
                    "level": level,
                    "type": "too_many_keywords",
                    "severity": "BAIXO",
                    "count": kw_count,
                    "message": f"Keywords excessivas: {kw_count} (recomendado: {RECOMMENDED_MIN}-{RECOMMENDED_MAX})"
                })
                self.stats[f"{level}_too_many"] += 1

        # Imprimir resumo
        print(f"{Fore.YELLOW}Problemas por Nível:{Style.RESET_ALL}")
        for level in ["L1", "L2", "L3"]:
            insufficient = self.stats.get(f"{level}_insufficient", 0)
            below_rec = self.stats.get(f"{level}_below_recommended", 0)
            too_many = self.stats.get(f"{level}_too_many", 0)

            print(f"  {level}:")
            print(f"    Insuficientes (<{MIN_KEYWORDS}): {insufficient}")
            print(f"    Abaixo recomendado: {below_rec}")
            print(f"    Acima recomendado: {too_many}")

            if insufficient > 0 and len(issues_by_level[level]) <= 10:
                print(f"    Códigos: {', '.join(issues_by_level[level])}")

    def analyze_generic_keywords(self):
        """Identifica uso excessivo de keywords genéricas"""
        print(f"\n{Fore.CYAN}=== Análise de Keywords Genéricas ==={Style.RESET_ALL}\n")

        nodes_with_generic = []

        for node in iter_all_nodes(self.tree):
            code = node.get("code", "?")
            label = node.get("label", "?")
            keywords = node.get("keywords", [])
            level = get_level(code)

            # Normalizar keywords para lowercase
            kw_set = {kw.lower() for kw in keywords}

            # Contar genéricas
            generic_found = kw_set & GENERIC_KEYWORDS
            if generic_found:
                generic_ratio = len(generic_found) / len(keywords) if keywords else 0

                if generic_ratio > 0.3:  # Mais de 30% genéricas
                    self.problems.append({
                        "code": code,
                        "label": label,
                        "level": level,
                        "type": "too_many_generic_keywords",
                        "severity": "MÉDIO",
                        "generic_keywords": list(generic_found),
                        "ratio": generic_ratio,
                        "message": f"Keywords genéricas excessivas: {len(generic_found)}/{len(keywords)} ({generic_ratio:.1%})"
                    })
                    nodes_with_generic.append({
                        "code": code,
                        "label": label,
                        "generic": list(generic_found),
                        "ratio": generic_ratio
                    })

        print(f"Nós com keywords genéricas excessivas (>30%): {len(nodes_with_generic)}")
        if nodes_with_generic:
            sorted_nodes = sorted(nodes_with_generic, key=lambda x: x["ratio"], reverse=True)
            print(f"{Fore.YELLOW}Top 10 nós:{Style.RESET_ALL}")
            for n in sorted_nodes[:10]:
                print(f"  {n['code']} - {n['label']}: {n['ratio']:.1%}")
                print(f"    Genéricas: {', '.join(n['generic'])}")

    def analyze_keyword_overlap(self):
        """Analisa sobreposição de keywords entre irmãos"""
        print(f"\n{Fore.CYAN}=== Análise de Sobreposição de Keywords ==={Style.RESET_ALL}\n")

        # Analisar L2 por pai L1
        l2_by_l1 = defaultdict(list)
        for node in iter_all_nodes(self.tree):
            if get_level(node.get("code", "")) == "L2":
                l1_code = node["code"].split(".")[0]
                l2_by_l1[l1_code].append(node)

        high_overlap_l2 = []
        for l1_code, l2_nodes in l2_by_l1.items():
            if len(l2_nodes) <= 1:
                continue

            for i, node1 in enumerate(l2_nodes):
                kw1 = set(k.lower() for k in node1.get("keywords", []))
                for node2 in l2_nodes[i+1:]:
                    kw2 = set(k.lower() for k in node2.get("keywords", []))

                    if not kw1 or not kw2:
                        continue

                    overlap = kw1 & kw2
                    overlap_ratio = len(overlap) / min(len(kw1), len(kw2))

                    if overlap_ratio > 0.5:  # Mais de 50% de sobreposição
                        high_overlap_l2.append({
                            "code1": node1["code"],
                            "label1": node1["label"],
                            "code2": node2["code"],
                            "label2": node2["label"],
                            "overlap": list(overlap),
                            "ratio": overlap_ratio
                        })

                        self.problems.append({
                            "code": f"{node1['code']} ↔ {node2['code']}",
                            "label": f"{node1['label']} ↔ {node2['label']}",
                            "level": "L2",
                            "type": "high_keyword_overlap",
                            "severity": "MÉDIO",
                            "overlap_keywords": list(overlap),
                            "ratio": overlap_ratio,
                            "message": f"Sobreposição alta de keywords: {len(overlap)} termos em comum ({overlap_ratio:.1%})"
                        })

        print(f"Pares L2 com alta sobreposição (>50%): {len(high_overlap_l2)}")
        if high_overlap_l2:
            sorted_overlap = sorted(high_overlap_l2, key=lambda x: x["ratio"], reverse=True)
            print(f"{Fore.YELLOW}Top 10 pares:{Style.RESET_ALL}")
            for pair in sorted_overlap[:10]:
                print(f"  {pair['code1']} ↔ {pair['code2']}: {pair['ratio']:.1%}")
                print(f"    Comuns: {', '.join(list(pair['overlap'])[:5])}...")

        # Analisar L3 por pai L2 (apenas contagem)
        l3_by_l2 = defaultdict(list)
        for node in iter_all_nodes(self.tree):
            if get_level(node.get("code", "")) == "L3":
                l2_code = ".".join(node["code"].split(".")[:2])
                l3_by_l2[l2_code].append(node)

        high_overlap_l3_count = 0
        for l2_code, l3_nodes in l3_by_l2.items():
            if len(l3_nodes) <= 1:
                continue

            for i, node1 in enumerate(l3_nodes):
                kw1 = set(k.lower() for k in node1.get("keywords", []))
                for node2 in l3_nodes[i+1:]:
                    kw2 = set(k.lower() for k in node2.get("keywords", []))

                    if not kw1 or not kw2:
                        continue

                    overlap = kw1 & kw2
                    overlap_ratio = len(overlap) / min(len(kw1), len(kw2))

                    if overlap_ratio > 0.5:
                        high_overlap_l3_count += 1

        print(f"Pares L3 com alta sobreposição (>50%): {high_overlap_l3_count}")

    def generate_report(self):
        """Gera relatório de análise de keywords"""
        report_file = REPORTS_DIR / "02_keywords_report.md"

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Relatório de Análise de Keywords - Subfase 4.2\n\n")
            f.write(f"**Arquivo analisado:** `{self.themes_file.name}`\n\n")
            f.write(f"**Total de problemas:** {len(self.problems)}\n\n")

            # Estatísticas
            f.write("## 1. Estatísticas Gerais\n\n")
            f.write("| Nível | Insuficientes | Abaixo Rec. | Acima Rec. |\n")
            f.write("|-------|---------------|-------------|------------|\n")
            for level in ["L1", "L2", "L3"]:
                insufficient = self.stats.get(f"{level}_insufficient", 0)
                below = self.stats.get(f"{level}_below_recommended", 0)
                above = self.stats.get(f"{level}_too_many", 0)
                f.write(f"| {level} | {insufficient} | {below} | {above} |\n")

            # Problemas por tipo
            f.write("\n## 2. Problemas Identificados\n\n")

            problems_by_type = defaultdict(list)
            for p in self.problems:
                problems_by_type[p["type"]].append(p)

            for ptype in ["insufficient_keywords", "too_many_generic_keywords",
                         "high_keyword_overlap", "below_recommended_keywords",
                         "too_many_keywords"]:
                items = problems_by_type.get(ptype, [])
                if items:
                    f.write(f"### {ptype.replace('_', ' ').title()} ({len(items)} casos)\n\n")

                    for item in items[:20]:
                        f.write(f"- **{item['code']}** - {item['label']}: {item['message']}\n")

                        # Detalhes específicos
                        if "generic_keywords" in item:
                            f.write(f"  - Genéricas: {', '.join(item['generic_keywords'])}\n")
                        elif "overlap_keywords" in item:
                            f.write(f"  - Comuns: {', '.join(item['overlap_keywords'][:10])}\n")

                    if len(items) > 20:
                        f.write(f"\n*... e mais {len(items)-20} casos*\n")
                    f.write("\n")

            # Recomendações
            f.write("## 3. Recomendações\n\n")

            insufficient = [p for p in self.problems if p["type"] == "insufficient_keywords"]
            if insufficient:
                f.write(f"1. **Prioridade Alta:** Adicionar keywords aos {len(insufficient)} nós com <{MIN_KEYWORDS} keywords\n")

            generic = [p for p in self.problems if p["type"] == "too_many_generic_keywords"]
            if generic:
                f.write(f"2. **Prioridade Média:** Substituir keywords genéricas em {len(generic)} nós por termos mais específicos\n")

            overlap = [p for p in self.problems if p["type"] == "high_keyword_overlap"]
            if overlap:
                f.write(f"3. **Prioridade Média:** Diferenciar keywords em {len(overlap)} pares de irmãos com alta sobreposição\n")

            if len(self.problems) == 0:
                f.write("✅ Qualidade das keywords está adequada.\n")

        print(f"\n{Fore.GREEN}✓ Relatório salvo em: {report_file}{Style.RESET_ALL}")


def main():
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Subfase 4.2: Análise de Keywords{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    analyzer = KeywordAnalyzer(THEMES_FILE)

    # Análises
    analyzer.analyze_keyword_quantity()
    analyzer.analyze_generic_keywords()
    analyzer.analyze_keyword_overlap()

    # Gerar relatório
    print(f"\n{Fore.CYAN}=== Gerando Relatório ==={Style.RESET_ALL}")
    analyzer.generate_report()

    # Sumário final
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Análise de keywords concluída{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    high_priority = len([p for p in analyzer.problems if p["severity"] == "ALTO"])
    if high_priority > 0:
        print(f"{Fore.YELLOW}⚠ {high_priority} problemas de alta prioridade{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✓ Qualidade das keywords está adequada{Style.RESET_ALL}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
