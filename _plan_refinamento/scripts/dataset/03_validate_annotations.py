"""
Subfase 4.3: Validação de Anotações

Valida qualidade e consistência das anotações manuais.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter, defaultdict

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import DATA_DIR, THEMES_FILE, REPORTS_DIR
from utils.yaml_utils import load_yaml, get_node_by_code
from colorama import Fore, Style, init

init(autoreset=True)


class AnnotationValidator:
    """Validador de anotações manuais"""

    def __init__(self):
        self.dataset_file = DATA_DIR / "test_dataset.csv"
        self.themes_tree = load_yaml(THEMES_FILE)
        self.issues = []

    def load_data(self):
        """Carrega dataset anotado"""
        if not self.dataset_file.exists():
            print(f"{Fore.RED}Erro: Dataset não encontrado{Style.RESET_ALL}")
            print(f"Arquivo esperado: {self.dataset_file}")
            sys.exit(1)

        df = pd.read_csv(self.dataset_file)
        return df

    def validate_completeness(self, df: pd.DataFrame):
        """Valida completude das anotações"""
        print(f"\n{Fore.CYAN}=== Validação de Completude ==={Style.RESET_ALL}\n")

        total = len(df)
        anotadas = df['L1_anotado'].notna().sum()
        pendentes = total - anotadas

        print(f"Total de documentos: {total}")
        print(f"Documentos anotados: {anotadas} ({(anotadas/total)*100:.1f}%)")
        print(f"Documentos pendentes: {pendentes}")

        if pendentes > 0:
            self.issues.append({
                'type': 'completeness',
                'severity': 'warning',
                'message': f"{pendentes} documentos ainda não foram anotados"
            })
            print(f"{Fore.YELLOW}⚠ {pendentes} documentos pendentes{Style.RESET_ALL}")

        # Verificar anotações incompletas (L1 sem L2/L3)
        incomplete = df[df['L1_anotado'].notna() & df['L2_anotado'].isna()]
        if len(incomplete) > 0:
            self.issues.append({
                'type': 'incomplete_hierarchy',
                'severity': 'warning',
                'message': f"{len(incomplete)} documentos com L1 mas sem L2"
            })
            print(f"{Fore.YELLOW}⚠ {len(incomplete)} documentos com hierarquia incompleta (só L1){Style.RESET_ALL}")

        return anotadas, pendentes

    def validate_hierarchy(self, df: pd.DataFrame):
        """Valida consistência hierárquica das anotações"""
        print(f"\n{Fore.CYAN}=== Validação de Hierarquia ==={Style.RESET_ALL}\n")

        anotadas = df[df['L1_anotado'].notna()].copy()
        erros_hierarquia = 0

        for idx, row in anotadas.iterrows():
            l1 = row['L1_anotado']
            l2 = row['L2_anotado']
            l3 = row['L3_anotado']

            # Verificar se L2 pertence ao L1
            if pd.notna(l2):
                if not str(l2).startswith(str(l1) + '.'):
                    self.issues.append({
                        'type': 'hierarchy_error',
                        'severity': 'error',
                        'row': idx,
                        'message': f"L2 '{l2}' não pertence ao L1 '{l1}'"
                    })
                    erros_hierarquia += 1

                # Verificar se L2 existe na árvore
                _, node = get_node_by_code(self.themes_tree, l2)
                if node is None:
                    self.issues.append({
                        'type': 'invalid_code',
                        'severity': 'error',
                        'row': idx,
                        'message': f"L2 '{l2}' não existe na árvore temática"
                    })
                    erros_hierarquia += 1

            # Verificar se L3 pertence ao L2
            if pd.notna(l3) and pd.notna(l2):
                if not str(l3).startswith(str(l2) + '.'):
                    self.issues.append({
                        'type': 'hierarchy_error',
                        'severity': 'error',
                        'row': idx,
                        'message': f"L3 '{l3}' não pertence ao L2 '{l2}'"
                    })
                    erros_hierarquia += 1

                # Verificar se L3 existe na árvore
                _, node = get_node_by_code(self.themes_tree, l3)
                if node is None:
                    self.issues.append({
                        'type': 'invalid_code',
                        'severity': 'error',
                        'row': idx,
                        'message': f"L3 '{l3}' não existe na árvore temática"
                    })
                    erros_hierarquia += 1

        if erros_hierarquia == 0:
            print(f"{Fore.GREEN}✓ Todas as anotações seguem a hierarquia correta{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {erros_hierarquia} erros de hierarquia encontrados{Style.RESET_ALL}")

        return erros_hierarquia

    def analyze_confidence(self, df: pd.DataFrame):
        """Analisa distribuição de confiança das anotações"""
        print(f"\n{Fore.CYAN}=== Análise de Confiança ==={Style.RESET_ALL}\n")

        anotadas = df[df['L1_anotado'].notna()].copy()

        if len(anotadas) == 0:
            print("Nenhuma anotação para analisar")
            return

        # Distribuição de confiança
        confidence_dist = anotadas['confianca'].value_counts()
        print("Distribuição de confiança:")
        for level in ['alta', 'media', 'baixa']:
            count = confidence_dist.get(level, 0)
            pct = (count / len(anotadas)) * 100
            print(f"  {level.capitalize()}: {count} ({pct:.1f}%)")

        # Alertar se muitas anotações de baixa confiança
        baixa_confianca = confidence_dist.get('baixa', 0)
        if baixa_confianca > len(anotadas) * 0.3:  # >30%
            self.issues.append({
                'type': 'low_confidence',
                'severity': 'warning',
                'message': f"{baixa_confianca} anotações de baixa confiança ({(baixa_confianca/len(anotadas))*100:.1f}%)"
            })
            print(f"\n{Fore.YELLOW}⚠ Muitas anotações de baixa confiança{Style.RESET_ALL}")
            print(f"  Considere revisar casos difíceis ou refinar a árvore temática")

    def analyze_agreement_with_original(self, df: pd.DataFrame):
        """Analisa concordância com classificação original"""
        print(f"\n{Fore.CYAN}=== Concordância com Classificação Original ==={Style.RESET_ALL}\n")

        # Filtrar apenas anotadas que têm classificação original
        anotadas = df[
            df['L1_anotado'].notna() &
            df['L1_original'].notna()
        ].copy()

        if len(anotadas) == 0:
            print("Nenhuma anotação com ground truth original para comparar")
            return

        # Concordância L1
        agreement_l1 = (anotadas['L1_anotado'] == anotadas['L1_original']).sum()
        acc_l1 = (agreement_l1 / len(anotadas)) * 100

        # Concordância L2
        anotadas_l2 = anotadas[anotadas['L2_anotado'].notna() & anotadas['L2_original'].notna()]
        if len(anotadas_l2) > 0:
            agreement_l2 = (anotadas_l2['L2_anotado'] == anotadas_l2['L2_original']).sum()
            acc_l2 = (agreement_l2 / len(anotadas_l2)) * 100
        else:
            acc_l2 = None

        # Concordância L3
        anotadas_l3 = anotadas[anotadas['L3_anotado'].notna() & anotadas['L3_original'].notna()]
        if len(anotadas_l3) > 0:
            agreement_l3 = (anotadas_l3['L3_anotado'] == anotadas_l3['L3_original']).sum()
            acc_l3 = (agreement_l3 / len(anotadas_l3)) * 100
        else:
            acc_l3 = None

        print(f"Concordância L1: {acc_l1:.1f}% ({agreement_l1}/{len(anotadas)})")
        if acc_l2 is not None:
            print(f"Concordância L2: {acc_l2:.1f}% ({agreement_l2}/{len(anotadas_l2)})")
        if acc_l3 is not None:
            print(f"Concordância L3: {acc_l3:.1f}% ({agreement_l3}/{len(anotadas_l3)})")

        # Analisar discordâncias
        discordancias_l1 = anotadas[anotadas['L1_anotado'] != anotadas['L1_original']]
        if len(discordancias_l1) > 0:
            print(f"\nTop 5 discordâncias L1:")
            for idx, row in discordancias_l1.head(5).iterrows():
                print(f"  {idx}: Original={row['L1_original']}, Anotado={row['L1_anotado']}")
                print(f"     Título: {row['titulo'][:70]}...")

        return acc_l1, acc_l2, acc_l3

    def analyze_annotator_consistency(self, df: pd.DataFrame):
        """Analisa consistência entre anotadores (se houver múltiplos)"""
        print(f"\n{Fore.CYAN}=== Análise de Anotadores ==={Style.RESET_ALL}\n")

        anotadas = df[df['L1_anotado'].notna()].copy()

        if len(anotadas) == 0:
            print("Nenhuma anotação para analisar")
            return

        # Contar anotações por anotador
        annotators = anotadas['anotador'].value_counts()
        print(f"Total de anotadores: {len(annotators)}")
        print("\nAnotações por anotador:")
        for annotator, count in annotators.items():
            print(f"  {annotator}: {count} documentos")

    def generate_report(self, stats: dict):
        """Gera relatório de validação"""
        report_file = REPORTS_DIR / "03_validation_report.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Validação de Anotações - Subfase 4.3\n\n")

            f.write("## Sumário Executivo\n\n")
            f.write(f"- **Total de documentos:** {stats['total']}\n")
            f.write(f"- **Documentos anotados:** {stats['anotadas']} ({(stats['anotadas']/stats['total'])*100:.1f}%)\n")
            f.write(f"- **Documentos pendentes:** {stats['pendentes']}\n")
            f.write(f"- **Erros de hierarquia:** {stats['erros_hierarquia']}\n\n")

            if stats.get('acc_l1'):
                f.write(f"- **Concordância com original (L1):** {stats['acc_l1']:.1f}%\n")
            if stats.get('acc_l2'):
                f.write(f"- **Concordância com original (L2):** {stats['acc_l2']:.1f}%\n")
            if stats.get('acc_l3'):
                f.write(f"- **Concordância com original (L3):** {stats['acc_l3']:.1f}%\n")

            # Problemas identificados
            f.write("\n## Problemas Identificados\n\n")

            if len(self.issues) == 0:
                f.write("✅ Nenhum problema crítico identificado.\n\n")
            else:
                f.write(f"Total de problemas: {len(self.issues)}\n\n")

                errors = [i for i in self.issues if i['severity'] == 'error']
                warnings = [i for i in self.issues if i['severity'] == 'warning']

                if errors:
                    f.write(f"### Erros ({len(errors)})\n\n")
                    for issue in errors[:20]:
                        f.write(f"- **Linha {issue.get('row', 'N/A')}:** {issue['message']}\n")
                    if len(errors) > 20:
                        f.write(f"\n*... e mais {len(errors)-20} erros*\n")

                if warnings:
                    f.write(f"\n### Avisos ({len(warnings)})\n\n")
                    for issue in warnings:
                        f.write(f"- {issue['message']}\n")

            # Recomendações
            f.write("\n## Recomendações\n\n")

            if stats['pendentes'] > 0:
                f.write(f"1. Completar anotação de {stats['pendentes']} documentos pendentes\n")

            if stats['erros_hierarquia'] > 0:
                f.write(f"2. Corrigir {stats['erros_hierarquia']} erros de hierarquia\n")

            baixa_conf = sum(1 for i in self.issues if i['type'] == 'low_confidence')
            if baixa_conf > 0:
                f.write(f"3. Revisar {baixa_conf} documentos de baixa confiança\n")

            if len(self.issues) == 0 and stats['pendentes'] == 0:
                f.write("✅ Dataset de teste pronto para uso na Subfase 4.4 (Testes de Classificação)\n")

        print(f"\n{Fore.GREEN}✓ Relatório salvo em: {report_file}{Style.RESET_ALL}")


def main():
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Subfase 4.3: Validação de Anotações{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    validator = AnnotationValidator()

    # Carregar dados
    df = validator.load_data()

    # Validações
    anotadas, pendentes = validator.validate_completeness(df)
    erros_hierarquia = validator.validate_hierarchy(df)
    validator.analyze_confidence(df)
    acc_l1, acc_l2, acc_l3 = validator.analyze_agreement_with_original(df)
    validator.analyze_annotator_consistency(df)

    # Gerar relatório
    stats = {
        'total': len(df),
        'anotadas': anotadas,
        'pendentes': pendentes,
        'erros_hierarquia': erros_hierarquia,
        'acc_l1': acc_l1,
        'acc_l2': acc_l2,
        'acc_l3': acc_l3,
    }

    validator.generate_report(stats)

    # Sumário final
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    if erros_hierarquia == 0 and pendentes == 0:
        print(f"{Fore.GREEN}✓ Validação concluída com sucesso{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Dataset pronto para testes de classificação{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ Validação concluída com problemas{Style.RESET_ALL}")
        if pendentes > 0:
            print(f"{Fore.YELLOW}  - {pendentes} documentos pendentes{Style.RESET_ALL}")
        if erros_hierarquia > 0:
            print(f"{Fore.RED}  - {erros_hierarquia} erros de hierarquia{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    return 1 if erros_hierarquia > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
