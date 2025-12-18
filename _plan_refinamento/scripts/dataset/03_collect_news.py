"""
Subfase 4.3: Coleta de Notícias para Dataset de Teste

Baixa amostra do dataset GovBRNews do HuggingFace e prepara para anotação manual.
"""

import sys
from pathlib import Path
from typing import List, Dict
import pandas as pd
from collections import Counter

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import TEST_DATASET_SIZE, DATA_DIR
from colorama import Fore, Style, init

init(autoreset=True)


class NewsCollector:
    """Coleta e prepara notícias para anotação"""

    def __init__(self, dataset_name: str = "nitaibezerra/govbrnews", sample_size: int = TEST_DATASET_SIZE):
        self.dataset_name = dataset_name
        self.sample_size = sample_size
        self.output_file = DATA_DIR / "test_dataset.csv"

    def load_dataset(self):
        """Carrega dataset do HuggingFace"""
        from datasets import load_dataset

        print(f"\n{Fore.CYAN}Carregando dataset: {self.dataset_name}{Style.RESET_ALL}")

        # Carregar dataset
        dataset = load_dataset(self.dataset_name, split="train")
        print(f"✓ Dataset carregado: {len(dataset)} documentos")

        return dataset

    def stratified_sample(self, dataset, by_field: str = "theme_1_level_1_code"):
        """
        Cria amostra estratificada por tema L1

        Args:
            dataset: Dataset do HuggingFace
            by_field: Campo para estratificação

        Returns:
            Amostra estratificada
        """
        print(f"\n{Fore.CYAN}Criando amostra estratificada de {self.sample_size} documentos{Style.RESET_ALL}")

        # Converter para pandas para facilitar
        df = pd.DataFrame(dataset)

        # Verificar distribuição original
        theme_counts = df[by_field].value_counts()
        print(f"\nDistribuição original de temas (top 10):")
        for theme, count in theme_counts.head(10).items():
            pct = (count / len(df)) * 100
            print(f"  {theme}: {count} ({pct:.1f}%)")

        # Estratificar proporcionalmente
        sampled = df.groupby(by_field, group_keys=False).apply(
            lambda x: x.sample(
                n=max(1, int((len(x) / len(df)) * self.sample_size)),
                random_state=42
            )
        ).reset_index(drop=True)

        # Ajustar tamanho se necessário (pode haver arredondamentos)
        if len(sampled) > self.sample_size:
            sampled = sampled.sample(n=self.sample_size, random_state=42)
        elif len(sampled) < self.sample_size:
            # Adicionar mais amostras aleatórias
            remaining = self.sample_size - len(sampled)
            extra = df[~df.index.isin(sampled.index)].sample(n=remaining, random_state=42)
            sampled = pd.concat([sampled, extra]).reset_index(drop=True)

        print(f"\n✓ Amostra criada: {len(sampled)} documentos")

        # Mostrar distribuição da amostra
        sample_counts = sampled[by_field].value_counts()
        print(f"\nDistribuição da amostra (top 10):")
        for theme, count in sample_counts.head(10).items():
            pct = (count / len(sampled)) * 100
            print(f"  {theme}: {count} ({pct:.1f}%)")

        return sampled

    def prepare_for_annotation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara dataframe para anotação manual

        Args:
            df: DataFrame com notícias

        Returns:
            DataFrame preparado para anotação
        """
        print(f"\n{Fore.CYAN}Preparando para anotação{Style.RESET_ALL}")

        # Selecionar e renomear colunas relevantes
        annotation_df = pd.DataFrame({
            'unique_id': df['unique_id'],
            'titulo': df['title'],
            'resumo': df.get('summary', ''),
            'conteudo_inicio': df['content'].str[:500] if 'content' in df.columns else '',  # Primeiros 500 chars
            'orgao': df.get('agency', ''),
            'data_publicacao': df.get('published_at', ''),
            'url': df.get('url', ''),

            # Campos para anotação (vazios inicialmente)
            'L1_anotado': '',
            'L2_anotado': '',
            'L3_anotado': '',
            'confianca': '',  # alta/media/baixa
            'observacoes': '',
            'anotador': '',
            'data_anotacao': '',

            # Ground truth original (para comparação posterior)
            'L1_original': df.get('theme_1_level_1_code', ''),
            'L2_original': df.get('theme_1_level_2_code', ''),
            'L3_original': df.get('theme_1_level_3_code', ''),
        })

        # Adicionar coluna de complexidade (estimativa baseada no título)
        annotation_df['complexidade_estimada'] = annotation_df['titulo'].apply(self._estimate_complexity)

        print(f"✓ {len(annotation_df)} documentos preparados")
        print(f"\nDistribuição de complexidade estimada:")
        complexity_dist = annotation_df['complexidade_estimada'].value_counts()
        for level, count in complexity_dist.items():
            pct = (count / len(annotation_df)) * 100
            print(f"  {level}: {count} ({pct:.1f}%)")

        return annotation_df

    def _estimate_complexity(self, title: str) -> str:
        """
        Estima complexidade de classificação baseado no título

        Args:
            title: Título da notícia

        Returns:
            'clara', 'moderada', ou 'dificil'
        """
        # Heurística simples:
        # - Clara: título tem palavras-chave específicas de um tema
        # - Difícil: título genérico ou pode se encaixar em múltiplos temas
        # - Moderada: entre os dois

        title_lower = title.lower()

        # Palavras-chave muito específicas (clara)
        specific_keywords = [
            'educação', 'escola', 'universidade', 'ensino',
            'saúde', 'sus', 'hospital', 'vacina',
            'segurança pública', 'polícia', 'prisão',
            'meio ambiente', 'ambiental', 'floresta', 'desmatamento',
            'agricultura', 'safra', 'agropecuária',
            'economia', 'pib', 'inflação', 'dólar',
        ]

        # Palavras genéricas (difícil)
        generic_keywords = [
            'governo', 'ministro', 'presidente', 'brasil',
            'federal', 'nacional', 'programa', 'projeto',
            'anuncia', 'divulga', 'informa', 'comunica',
        ]

        has_specific = any(kw in title_lower for kw in specific_keywords)
        has_generic = any(kw in title_lower for kw in generic_keywords)

        if has_specific and not has_generic:
            return 'clara'
        elif has_generic and not has_specific:
            return 'dificil'
        else:
            return 'moderada'

    def save_dataset(self, df: pd.DataFrame):
        """Salva dataset preparado"""
        print(f"\n{Fore.CYAN}Salvando dataset{Style.RESET_ALL}")

        # Salvar CSV
        df.to_csv(self.output_file, index=False, encoding='utf-8')
        print(f"✓ Dataset salvo em: {self.output_file}")

        # Gerar estatísticas
        stats = {
            'total_documentos': len(df),
            'temas_L1_unicos': df['L1_original'].nunique(),
            'orgaos_unicos': df['orgao'].nunique(),
            'distribuicao_complexidade': df['complexidade_estimada'].value_counts().to_dict(),
            'top_10_temas': df['L1_original'].value_counts().head(10).to_dict(),
        }

        stats_file = DATA_DIR / "test_dataset_stats.json"
        import json
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        print(f"✓ Estatísticas salvas em: {stats_file}")

        return stats

    def generate_report(self, stats: Dict):
        """Gera relatório sobre o dataset coletado"""
        from config import REPORTS_DIR

        report_file = REPORTS_DIR / "03_dataset_report.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Coleta do Dataset de Teste - Subfase 4.3\n\n")
            f.write(f"**Dataset fonte:** `{self.dataset_name}`\n\n")
            f.write(f"**Tamanho da amostra:** {stats['total_documentos']} documentos\n\n")

            f.write("## Estatísticas Gerais\n\n")
            f.write(f"- **Temas L1 únicos:** {stats['temas_L1_unicos']}\n")
            f.write(f"- **Órgãos únicos:** {stats['orgaos_unicos']}\n\n")

            f.write("## Distribuição de Complexidade Estimada\n\n")
            f.write("| Complexidade | Quantidade | Percentual |\n")
            f.write("|--------------|------------|------------|\n")
            total = stats['total_documentos']
            for level in ['clara', 'moderada', 'dificil']:
                count = stats['distribuicao_complexidade'].get(level, 0)
                pct = (count / total) * 100
                f.write(f"| {level.capitalize()} | {count} | {pct:.1f}% |\n")

            f.write("\n## Top 10 Temas L1 na Amostra\n\n")
            f.write("| Código | Quantidade | Percentual |\n")
            f.write("|--------|------------|------------|\n")
            for theme, count in stats['top_10_temas'].items():
                pct = (count / total) * 100
                f.write(f"| {theme} | {count} | {pct:.1f}% |\n")

            f.write("\n## Próximos Passos\n\n")
            f.write("1. Usar interface de anotação (`03_annotation_app.py`) para classificar manualmente\n")
            f.write("2. Preencher colunas: `L1_anotado`, `L2_anotado`, `L3_anotado`, `confianca`\n")
            f.write("3. Executar validação de anotações (`03_validate_annotations.py`)\n")
            f.write("4. Usar dataset anotado para testes de classificação (Subfase 4.4)\n")

        print(f"✓ Relatório salvo em: {report_file}")


def main():
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Subfase 4.3: Coleta de Notícias para Dataset de Teste{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    collector = NewsCollector()

    # 1. Carregar dataset
    dataset = collector.load_dataset()

    # 2. Criar amostra estratificada
    sample = collector.stratified_sample(dataset)

    # 3. Preparar para anotação
    annotation_df = collector.prepare_for_annotation(sample)

    # 4. Salvar
    stats = collector.save_dataset(annotation_df)

    # 5. Gerar relatório
    collector.generate_report(stats)

    # Sumário final
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Coleta de notícias concluída{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Próximo passo:{Style.RESET_ALL}")
    print(f"  streamlit run scripts/dataset/03_annotation_app.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
