"""
Subfase 4.2: Análise de Similaridade Semântica

Usa embeddings para identificar:
- Irmãos L2 com descrições muito similares (>0.85)
- Irmãos L3 com descrições muito similares
- Redundâncias conceituais
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import (
    THEMES_FILE, REPORTS_DIR, DATA_DIR,
    EMBEDDING_MODEL, EMBEDDINGS_CACHE_DIR, EMBEDDING_DEVICE
)
from utils.yaml_utils import load_yaml, iter_all_nodes, get_level, get_siblings
from utils.embedding_utils import EmbeddingGenerator, similarity_matrix
from colorama import Fore, Style, init

init(autoreset=True)

SIMILARITY_THRESHOLD = 0.85  # Threshold para considerar muito similar


class SimilarityAnalyzer:
    """Analisa similaridade semântica entre descrições"""

    def __init__(self, themes_file: Path):
        self.themes_file = themes_file
        self.tree = load_yaml(themes_file)
        self.problems = []

        # Inicializar gerador de embeddings
        print(f"{Fore.CYAN}Inicializando modelo de embeddings...{Style.RESET_ALL}")
        self.embedding_gen = EmbeddingGenerator(
            model_name=EMBEDDING_MODEL,
            cache_dir=EMBEDDINGS_CACHE_DIR,
            device=EMBEDDING_DEVICE
        )

    def analyze_l2_similarity(self):
        """Analisa similaridade entre irmãos L2"""
        print(f"\n{Fore.CYAN}=== Análise de Similaridade L2 ==={Style.RESET_ALL}\n")

        # Agrupar L2 por pai L1
        l2_by_l1 = defaultdict(list)
        for node in iter_all_nodes(self.tree):
            if get_level(node.get("code", "")) == "L2":
                l1_code = node["code"].split(".")[0]
                l2_by_l1[l1_code].append(node)

        high_similarity_pairs = []

        for l1_code, l2_nodes in l2_by_l1.items():
            if len(l2_nodes) <= 1:
                continue  # Precisa de pelo menos 2 irmãos

            # Gerar embeddings
            descriptions = [n.get("description", "") for n in l2_nodes]
            codes = [n.get("code") for n in l2_nodes]
            labels = [n.get("label") for n in l2_nodes]

            embeddings = self.embedding_gen.encode(descriptions, show_progress=False)

            # Calcular matriz de similaridade
            sim_matrix = similarity_matrix(embeddings)

            # Identificar pares com alta similaridade
            n = len(l2_nodes)
            for i in range(n):
                for j in range(i + 1, n):
                    similarity = sim_matrix[i, j]
                    if similarity > SIMILARITY_THRESHOLD:
                        high_similarity_pairs.append({
                            "code1": codes[i],
                            "label1": labels[i],
                            "code2": codes[j],
                            "label2": labels[j],
                            "similarity": similarity,
                            "level": "L2",
                            "parent": l1_code
                        })

                        self.problems.append({
                            "type": "high_similarity_l2",
                            "severity": "MÉDIO",
                            "code1": codes[i],
                            "code2": codes[j],
                            "similarity": f"{similarity:.3f}",
                            "message": f"L2 irmãos muito similares: {labels[i]} ↔ {labels[j]} (similaridade: {similarity:.3f})"
                        })

        print(f"Pares L2 com similaridade > {SIMILARITY_THRESHOLD}: {len(high_similarity_pairs)}")
        if high_similarity_pairs:
            print(f"{Fore.YELLOW}Top 10 pares mais similares:{Style.RESET_ALL}")
            sorted_pairs = sorted(high_similarity_pairs, key=lambda x: x["similarity"], reverse=True)
            for pair in sorted_pairs[:10]:
                print(f"  {pair['code1']} ↔ {pair['code2']}: {pair['similarity']:.3f}")
                print(f"    {pair['label1']} ↔ {pair['label2']}")

        return high_similarity_pairs

    def analyze_l3_similarity(self):
        """Analisa similaridade entre irmãos L3"""
        print(f"\n{Fore.CYAN}=== Análise de Similaridade L3 ==={Style.RESET_ALL}\n")

        # Agrupar L3 por pai L2
        l3_by_l2 = defaultdict(list)
        for node in iter_all_nodes(self.tree):
            if get_level(node.get("code", "")) == "L3":
                l2_code = ".".join(node["code"].split(".")[:2])
                l3_by_l2[l2_code].append(node)

        high_similarity_pairs = []
        l2_with_issues = set()

        for l2_code, l3_nodes in l3_by_l2.items():
            if len(l3_nodes) <= 1:
                continue

            # Gerar embeddings
            descriptions = [n.get("description", "") for n in l3_nodes]
            codes = [n.get("code") for n in l3_nodes]
            labels = [n.get("label") for n in l3_nodes]

            embeddings = self.embedding_gen.encode(descriptions, show_progress=False)

            # Calcular matriz de similaridade
            sim_matrix = similarity_matrix(embeddings)

            # Identificar pares com alta similaridade
            n = len(l3_nodes)
            has_issue = False
            for i in range(n):
                for j in range(i + 1, n):
                    similarity = sim_matrix[i, j]
                    if similarity > SIMILARITY_THRESHOLD:
                        high_similarity_pairs.append({
                            "code1": codes[i],
                            "label1": labels[i],
                            "code2": codes[j],
                            "label2": labels[j],
                            "similarity": similarity,
                            "level": "L3",
                            "parent": l2_code
                        })

                        self.problems.append({
                            "type": "high_similarity_l3",
                            "severity": "BAIXO",
                            "code1": codes[i],
                            "code2": codes[j],
                            "similarity": f"{similarity:.3f}",
                            "message": f"L3 irmãos muito similares: {labels[i]} ↔ {labels[j]} (similaridade: {similarity:.3f})"
                        })

                        has_issue = True

            if has_issue:
                l2_with_issues.add(l2_code)

        print(f"Pares L3 com similaridade > {SIMILARITY_THRESHOLD}: {len(high_similarity_pairs)}")
        print(f"Subtemas L2 com problemas de similaridade L3: {len(l2_with_issues)}")

        if high_similarity_pairs:
            print(f"{Fore.YELLOW}Top 10 pares L3 mais similares:{Style.RESET_ALL}")
            sorted_pairs = sorted(high_similarity_pairs, key=lambda x: x["similarity"], reverse=True)
            for pair in sorted_pairs[:10]:
                print(f"  {pair['code1']} ↔ {pair['code2']}: {pair['similarity']:.3f}")
                print(f"    {pair['label1']} ↔ {pair['label2']}")

        return high_similarity_pairs

    def generate_similarity_heatmaps(self):
        """Gera heatmaps de similaridade para visualização"""
        print(f"\n{Fore.CYAN}=== Gerando Heatmaps de Similaridade ==={Style.RESET_ALL}\n")

        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
        except ImportError:
            print(f"{Fore.YELLOW}⚠ matplotlib/seaborn não disponíveis, pulando heatmaps{Style.RESET_ALL}")
            return

        # Heatmap L2 por tema L1 (apenas alguns exemplos)
        l1_themes = list(self.tree.get("themes", []))[:5]  # Primeiros 5 temas

        for l1_theme in l1_themes:
            l1_code = l1_theme["code"]
            l1_label = l1_theme["label"]
            l2_nodes = l1_theme.get("subtemas", [])

            if len(l2_nodes) <= 1:
                continue

            descriptions = [n.get("description", "") for n in l2_nodes]
            labels = [f"{n['code']}\n{n['label'][:20]}..." for n in l2_nodes]

            embeddings = self.embedding_gen.encode(descriptions, show_progress=False)
            sim_matrix = similarity_matrix(embeddings)

            # Criar heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(
                sim_matrix,
                xticklabels=labels,
                yticklabels=labels,
                annot=True,
                fmt=".2f",
                cmap="YlOrRd",
                vmin=0,
                vmax=1,
                square=True
            )
            plt.title(f"Similaridade L2 - Tema {l1_code}: {l1_label}")
            plt.tight_layout()

            output_file = REPORTS_DIR / f"02_similarity_heatmap_L2_{l1_code}.png"
            plt.savefig(output_file, dpi=150, bbox_inches="tight")
            plt.close()

            print(f"  Heatmap salvo: {output_file.name}")

    def generate_report(self, l2_pairs: List[Dict], l3_pairs: List[Dict]):
        """Gera relatório de similaridade"""
        report_file = REPORTS_DIR / "02_similarity_report.md"

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Relatório de Análise de Similaridade Semântica - Subfase 4.2\n\n")
            f.write(f"**Modelo de embeddings:** `{EMBEDDING_MODEL}`\n\n")
            f.write(f"**Threshold de similaridade:** {SIMILARITY_THRESHOLD}\n\n")

            # Sumário
            f.write("## Sumário Executivo\n\n")
            f.write(f"- **Pares L2 com alta similaridade:** {len(l2_pairs)}\n")
            f.write(f"- **Pares L3 com alta similaridade:** {len(l3_pairs)}\n")
            f.write(f"- **Total de problemas identificados:** {len(self.problems)}\n\n")

            # Detalhes L2
            if l2_pairs:
                f.write("## Pares L2 Similares\n\n")
                f.write("| Código 1 | Label 1 | Código 2 | Label 2 | Similaridade |\n")
                f.write("|----------|---------|----------|---------|-------------|\n")
                sorted_l2 = sorted(l2_pairs, key=lambda x: x["similarity"], reverse=True)
                for pair in sorted_l2:
                    f.write(f"| {pair['code1']} | {pair['label1']} | "
                           f"{pair['code2']} | {pair['label2']} | {pair['similarity']:.3f} |\n")
            else:
                f.write("## Pares L2 Similares\n\n")
                f.write("✅ Nenhum par de irmãos L2 com similaridade excessiva.\n\n")

            # Detalhes L3 (top 50)
            if l3_pairs:
                f.write("## Pares L3 Similares (Top 50)\n\n")
                f.write("| Código 1 | Label 1 | Código 2 | Label 2 | Similaridade |\n")
                f.write("|----------|---------|----------|---------|-------------|\n")
                sorted_l3 = sorted(l3_pairs, key=lambda x: x["similarity"], reverse=True)
                for pair in sorted_l3[:50]:
                    f.write(f"| {pair['code1']} | {pair['label1']} | "
                           f"{pair['code2']} | {pair['label2']} | {pair['similarity']:.3f} |\n")

                if len(l3_pairs) > 50:
                    f.write(f"\n*... e mais {len(l3_pairs)-50} pares*\n")
            else:
                f.write("## Pares L3 Similares\n\n")
                f.write("✅ Nenhum par de irmãos L3 com similaridade excessiva.\n\n")

            # Recomendações
            f.write("\n## Recomendações\n\n")
            if len(l2_pairs) > 0:
                f.write("### Prioridade Média: Revisar L2 similares\n\n")
                f.write("Os seguintes pares de subtemas L2 possuem descrições muito similares "
                       "e podem causar confusão na classificação:\n\n")
                for pair in sorted(l2_pairs, key=lambda x: x["similarity"], reverse=True)[:10]:
                    f.write(f"- **{pair['code1']}** ({pair['label1']}) ↔ "
                           f"**{pair['code2']}** ({pair['label2']}): {pair['similarity']:.3f}\n")
                    f.write(f"  → Adicionar termos distintivos às descrições\n\n")

            if len(l3_pairs) > 20:
                f.write("### Prioridade Baixa: Revisar L3 similares\n\n")
                f.write(f"Foram identificados {len(l3_pairs)} pares de categorias L3 com alta similaridade. "
                       "Considerar adicionar keywords mais específicas para diferenciação.\n\n")

            if len(self.problems) == 0:
                f.write("✅ **Conclusão:** Qualidade semântica das descrições está adequada.\n")

        print(f"\n{Fore.GREEN}✓ Relatório salvo em: {report_file}{Style.RESET_ALL}")


def main():
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Subfase 4.2: Análise de Similaridade Semântica{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    analyzer = SimilarityAnalyzer(THEMES_FILE)

    # Análise L2
    l2_pairs = analyzer.analyze_l2_similarity()

    # Análise L3
    l3_pairs = analyzer.analyze_l3_similarity()

    # Gerar heatmaps (opcional)
    analyzer.generate_similarity_heatmaps()

    # Gerar relatório
    print(f"\n{Fore.CYAN}=== Gerando Relatório ==={Style.RESET_ALL}")
    analyzer.generate_report(l2_pairs, l3_pairs)

    # Sumário final
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Análise de similaridade concluída{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if len(l2_pairs) > 0:
        print(f"{Fore.YELLOW}⚠ {len(l2_pairs)} pares L2 com alta similaridade{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✓ Qualidade semântica adequada{Style.RESET_ALL}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
