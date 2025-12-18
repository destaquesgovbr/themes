"""
Interface de Anotação Manual de Notícias - Fase 4.3

Aplicação Streamlit para anotação manual de notícias com classificação temática.
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from utils.data_loader import DataLoader
from utils.theme_hierarchy import get_theme_hierarchy, get_level
from utils.agencies import AgencyLoader


# Configuração da página
st.set_page_config(
    page_title="Anotação de Notícias GovBR - Fase 4",
    page_icon="📋",
    layout="wide"
)

# Emojis para complexidade
COMPLEXITY_EMOJI = {
    "clara": "🟢",
    "moderada": "🟡",
    "dificil": "🔴"
}


class AnnotationApp:
    """App de anotação manual de notícias"""

    def __init__(self):
        # Detectar ambiente (local ou GCP)
        self.use_gcs = os.getenv('USE_GCS', 'false').lower() == 'true'
        self.bucket_name = os.getenv('GCS_BUCKET', 'dgb-streamlit-data')

        # Inicializar data loader
        self.data_loader = DataLoader(use_gcs=self.use_gcs, bucket_name=self.bucket_name)

        # Nomes dos arquivos
        self.dataset_filename = os.getenv('DATASET_FILE', 'test_dataset.csv')
        self.themes_filename = os.getenv('THEMES_FILE', 'themes_tree_enriched_full.yaml')
        self.agencies_filename = 'agencies.yaml'

        # Inicializar agency loader
        data_dir = Path(__file__).parent.parent / 'data'
        agencies_file = data_dir / self.agencies_filename
        self.agency_loader = AgencyLoader(agencies_file) if agencies_file.exists() else None

    @st.cache_data
    def load_data(_self):
        """Carrega dataset e árvore temática"""
        try:
            df = _self.data_loader.load_csv(_self.dataset_filename)
            themes_tree = _self.data_loader.load_yaml(_self.themes_filename)
            return df, themes_tree
        except FileNotFoundError as e:
            st.error(f"❌ Erro ao carregar dados: {e}")
            st.info("💡 Certifique-se de que os arquivos estão no local correto:")
            st.code(f"- {_self.dataset_filename}\n- {_self.themes_filename}")
            st.stop()

    def save_data(self, df):
        """Salva dataset anotado"""
        self.data_loader.save_csv(df, self.dataset_filename)

    def get_agency_name(self, sigla: str) -> str:
        """Obtém nome completo da agência"""
        if self.agency_loader:
            return self.agency_loader.get_agency_name(sigla)
        return sigla

    def get_theme_label(self, code: str, themes: dict) -> str:
        """
        Obtém o label de um tema a partir do código.

        Args:
            code: Código do tema (ex: "01", "01.01", "01.01.01")
            themes: Dicionário com hierarquia de temas

        Returns:
            Label do tema ou código se não encontrado
        """
        if not code or not themes:
            return code

        # Determinar nível
        parts = str(code).split('.')
        level = len(parts)

        if level == 1:
            # L1
            return themes['L1'].get(code, code)
        elif level == 2:
            # L2
            parent = parts[0]
            return themes['L2'].get(parent, {}).get(code, code)
        elif level == 3:
            # L3
            parent = '.'.join(parts[:2])
            return themes['L3'].get(parent, {}).get(code, code)

        return code

    def render_home_page(self):
        """Renderiza página inicial com instruções"""
        st.title("📋 Anotação Manual de Notícias GovBR")
        st.markdown("### Fase 4.3 - Validação da Taxonomia Temática")

        st.markdown("---")

        # Instruções
        st.markdown("""
        ## 🎯 Objetivo

        Esta ferramenta permite a **anotação manual de notícias governamentais brasileiras**
        com classificação temática hierárquica em 3 níveis:

        - **L1 (Tema)**: Área temática principal (ex: "Economia e Finanças")
        - **L2 (Subtema)**: Subcategoria do tema (ex: "Política Econômica")
        - **L3 (Categoria)**: Classificação específica (ex: "Política Fiscal")

        ## 📝 Como Anotar

        1. **Leia** o título, resumo e conteúdo da notícia
        2. **Identifique** o tema principal (L1)
        3. **Selecione** o subtema (L2) e categoria (L3) mais específicos
        4. **Avalie** seu nível de confiança na classificação
        5. **Documente** observações para casos ambíguos ou dúvidas
        6. **Salve** a anotação e passe para a próxima notícia

        ## ✅ Dicas de Qualidade

        - Sempre escolha a **categoria mais específica** possível
        - Para notícias **multi-temáticas**, priorize o tema **dominante**
        - Use **"Confiança Baixa"** quando houver **ambiguidade**
        - Documente **dúvidas** no campo de observações
        - Consulte a **classificação original** (ground truth) se disponível

        ## 🚀 Filtros Disponíveis

        - **Status**: Todas / Pendentes / Anotadas
        - **Complexidade**:
          - 🟢 Clara: Tema óbvio
          - 🟡 Moderada: Requer análise
          - 🔴 Difícil: Ambígua ou multi-temática

        ---
        """)

        # Nome do anotador
        st.markdown("## 👤 Identificação")

        # Carregar nome do cookie (session_state)
        if 'annotator_name' not in st.session_state:
            st.session_state.annotator_name = ""

        annotator_name = st.text_input(
            "**Seu Nome**",
            value=st.session_state.annotator_name,
            placeholder="Digite seu nome completo",
            help="Seu nome será salvo junto com cada anotação que você fizer"
        )

        # Atualizar session state
        if annotator_name:
            st.session_state.annotator_name = annotator_name

        # Botão para iniciar
        if st.button("🚀 Iniciar Anotação", type="primary", use_container_width=True):
            if not annotator_name:
                st.error("⚠️ Por favor, informe seu nome antes de iniciar")
            else:
                st.session_state.show_home = False
                st.rerun()

    def render_sidebar(self, df):
        """Renderiza sidebar com estatísticas e filtros"""
        with st.sidebar:
            # Nome do anotador (topo)
            st.markdown(f"### 👤 {st.session_state.annotator_name}")

            if st.button("🏠 Voltar para Home"):
                st.session_state.show_home = True
                st.rerun()

            st.markdown("---")

            st.header("📊 Progresso")

            total = len(df)
            anotadas = df['L1_anotado'].notna().sum()
            pendentes = total - anotadas
            progresso = (anotadas / total) * 100 if total > 0 else 0

            st.metric("Total", total)
            st.metric("Anotadas", f"{anotadas} ({progresso:.1f}%)")
            st.metric("Pendentes", pendentes)

            st.progress(progresso / 100)

            st.markdown("---")

            # Filtros
            st.subheader("🔍 Filtros")

            filtro_status = st.selectbox(
                "Status",
                ["Todas", "Pendentes", "Anotadas"],
                help="Filtrar notícias por status de anotação"
            )

            filtro_complexidade = st.selectbox(
                "Complexidade",
                ["Todas", "clara", "moderada", "dificil"],
                format_func=lambda x: f"{COMPLEXITY_EMOJI.get(x, '')} {x}".strip() if x != "Todas" else x,
                help="Filtrar por complexidade estimada da classificação"
            )

            return filtro_status, filtro_complexidade

    def apply_filters(self, df, filtro_status, filtro_complexidade):
        """Aplica filtros ao dataframe"""
        df_filtrado = df.copy()

        if filtro_status == "Pendentes":
            df_filtrado = df_filtrado[df_filtrado['L1_anotado'].isna()]
        elif filtro_status == "Anotadas":
            df_filtrado = df_filtrado[df_filtrado['L1_anotado'].notna()]

        if filtro_complexidade != "Todas":
            df_filtrado = df_filtrado[df_filtrado['complexidade_estimada'] == filtro_complexidade]

        return df_filtrado

    def render_news_content(self, row):
        """Renderiza conteúdo da notícia"""
        # Informações da notícia
        col_info1, col_info2 = st.columns(2)

        with col_info1:
            agency_name = self.get_agency_name(row['orgao'])
            st.markdown(f"**Órgão:** {agency_name}")
            st.markdown(f"**Data:** {row['data_publicacao']}")

            complexity = row['complexidade_estimada']
            emoji = COMPLEXITY_EMOJI.get(complexity, "")
            st.markdown(f"**Complexidade:** {emoji} {complexity}")

        with col_info2:
            if row['url']:
                st.markdown(f"[🔗 Link original]({row['url']})")

        st.markdown("---")

        # Conteúdo
        st.subheader("📰 Título")
        st.markdown(f"### {row['titulo']}")

        if pd.notna(row['resumo']) and row['resumo']:
            st.subheader("📝 Resumo")
            st.info(row['resumo'])

        if pd.notna(row['conteudo_inicio']) and row['conteudo_inicio']:
            with st.expander("📄 Início do Conteúdo (500 caracteres)"):
                st.text(row['conteudo_inicio'])

        st.markdown("---")

    def render_hierarchical_selection(self, row, themes):
        """
        Renderiza seleção hierárquica L1 → L2 → L3 FORA do form.

        IMPORTANTE: Não pode estar dentro de st.form() para permitir reatividade.
        """
        st.subheader("🏷️ Classificação Temática")

        # Inicializar session state para as seleções
        if 'selected_l1' not in st.session_state:
            st.session_state.selected_l1 = ""
        if 'selected_l2' not in st.session_state:
            st.session_state.selected_l2 = ""
        if 'selected_l3' not in st.session_state:
            st.session_state.selected_l3 = ""

        # Verificar se temos valores anotados para esta notícia
        if pd.notna(row['L1_anotado']) and str(row['L1_anotado']):
            current_l1 = str(row['L1_anotado'])
        else:
            current_l1 = st.session_state.selected_l1

        if pd.notna(row['L2_anotado']) and str(row['L2_anotado']):
            current_l2 = str(row['L2_anotado'])
        else:
            current_l2 = st.session_state.selected_l2

        if pd.notna(row['L3_anotado']) and str(row['L3_anotado']):
            current_l3 = str(row['L3_anotado'])
        else:
            current_l3 = st.session_state.selected_l3

        # L1 - Tema
        l1_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L1'].items())]

        l1_current_formatted = ""
        if current_l1:
            matches = [x for x in l1_options if x.startswith(current_l1)]
            if matches:
                l1_current_formatted = matches[0]

        l1_index = l1_options.index(l1_current_formatted) if l1_current_formatted in l1_options else 0

        l1_selected = st.selectbox(
            "**Tema (L1)**",
            l1_options,
            index=l1_index,
            key="l1_selector",
            help="Selecione o tema principal da notícia"
        )

        # Atualizar session state
        st.session_state.selected_l1 = l1_selected.split(' - ')[0] if l1_selected else ""

        # Inicializar variáveis de retorno
        l2_selected = None
        l3_selected = None

        # L2 - Subtema (só aparece se L1 selecionado)
        if l1_selected:
            l1_code = l1_selected.split(' - ')[0]
            l2_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L2'].get(l1_code, {}).items())]

            l2_current_formatted = ""
            if current_l2 and current_l2.startswith(l1_code):
                matches = [x for x in l2_options if x.startswith(current_l2)]
                if matches:
                    l2_current_formatted = matches[0]

            l2_index = l2_options.index(l2_current_formatted) if l2_current_formatted in l2_options else 0

            l2_selected = st.selectbox(
                "**Subtema (L2)**",
                l2_options,
                index=l2_index,
                key="l2_selector",
                help="Selecione o subtema mais específico"
            )

            # Atualizar session state
            st.session_state.selected_l2 = l2_selected.split(' - ')[0] if l2_selected else ""

            # L3 - Categoria (só aparece se L2 selecionado)
            if l2_selected:
                l2_code = l2_selected.split(' - ')[0]
                l3_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L3'].get(l2_code, {}).items())]

                l3_current_formatted = ""
                if current_l3 and current_l3.startswith(l2_code):
                    matches = [x for x in l3_options if x.startswith(current_l3)]
                    if matches:
                        l3_current_formatted = matches[0]

                l3_index = l3_options.index(l3_current_formatted) if l3_current_formatted in l3_options else 0

                l3_selected = st.selectbox(
                    "**Categoria (L3)**",
                    l3_options,
                    index=l3_index,
                    key="l3_selector",
                    help="Selecione a categoria mais específica"
                )

                # Atualizar session state
                st.session_state.selected_l3 = l3_selected.split(' - ')[0] if l3_selected else ""

        return l1_selected, l2_selected, l3_selected

    def render_annotation_form(self, row):
        """
        Renderiza apenas os campos finais do formulário (confiança, observações, botões).

        IMPORTANTE: A seleção L1/L2/L3 deve estar FORA do form.
        """
        st.markdown("---")
        st.subheader("📊 Avaliação da Classificação")

        with st.form(key="annotation_form"):
            # Confiança
            conf_value = "media"
            if pd.notna(row['confianca']) and row['confianca'] in ["baixa", "media", "alta"]:
                conf_value = row['confianca']

            confianca = st.select_slider(
                "**Confiança na Classificação**",
                options=["baixa", "media", "alta"],
                value=conf_value,
                help="Quão confiante você está nesta classificação?"
            )

            # Observações
            obs_value = ""
            if pd.notna(row['observacoes']):
                obs_value = str(row['observacoes'])

            observacoes = st.text_area(
                "**Observações** (opcional)",
                value=obs_value,
                placeholder="Casos ambíguos, dúvidas, comentários...",
                help="Documente qualquer observação relevante sobre a classificação"
            )

            # Botões
            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                submit = st.form_submit_button("💾 Salvar Anotação", type="primary", use_container_width=True)

            with col_btn2:
                skip = st.form_submit_button("⏭️ Pular", use_container_width=True)

            return submit, skip, confianca, observacoes

    def render_ground_truth(self, row, themes):
        """Renderiza classificação original (ground truth) com código E label"""
        if pd.notna(row['L1_original']) and row['L1_original']:
            with st.expander("🔍 Ver Classificação Original (Ground Truth)"):
                l1_code = str(row['L1_original'])
                l1_label = self.get_theme_label(l1_code, themes)
                st.markdown(f"**L1:** `{l1_code}` - {l1_label}")

                if pd.notna(row['L2_original']):
                    l2_code = str(row['L2_original'])
                    l2_label = self.get_theme_label(l2_code, themes)
                    st.markdown(f"**L2:** `{l2_code}` - {l2_label}")

                if pd.notna(row['L3_original']):
                    l3_code = str(row['L3_original'])
                    l3_label = self.get_theme_label(l3_code, themes)
                    st.markdown(f"**L3:** `{l3_code}` - {l3_label}")

    def run(self):
        """Executa aplicação principal"""
        # Inicializar session state
        if 'show_home' not in st.session_state:
            st.session_state.show_home = True

        # Mostrar home se necessário
        if st.session_state.show_home:
            self.render_home_page()
            return

        # Aplicação principal
        st.title("📋 Anotação Manual de Notícias - Fase 4.3")
        st.markdown("---")

        # Carregar dados
        df, themes_tree = self.load_data()
        themes = get_theme_hierarchy(themes_tree)

        # Sidebar com filtros
        filtro_status, filtro_complexidade = self.render_sidebar(df)

        # Aplicar filtros
        df_filtrado = self.apply_filters(df, filtro_status, filtro_complexidade)

        # Verificar se há notícias para anotar
        if len(df_filtrado) == 0:
            st.info("✅ Todas as notícias foram anotadas!")
            return

        # Seletor de notícia
        indices = df_filtrado.index.tolist()
        if 'current_index' not in st.session_state:
            st.session_state.current_index = indices[0]

        # Garantir que o índice atual está na lista filtrada
        if st.session_state.current_index not in indices:
            st.session_state.current_index = indices[0]

        # Navegação
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button("⬅️ Anterior"):
                current_pos = indices.index(st.session_state.current_index)
                if current_pos > 0:
                    st.session_state.current_index = indices[current_pos - 1]
                    # Limpar seleções ao mudar de notícia
                    st.session_state.selected_l1 = ""
                    st.session_state.selected_l2 = ""
                    st.session_state.selected_l3 = ""
                    st.rerun()

        with col2:
            current_pos = indices.index(st.session_state.current_index)
            st.markdown(f"**Notícia {current_pos + 1} de {len(indices)}**")

        with col3:
            if st.button("Próxima ➡️"):
                current_pos = indices.index(st.session_state.current_index)
                if current_pos < len(indices) - 1:
                    st.session_state.current_index = indices[current_pos + 1]
                    # Limpar seleções ao mudar de notícia
                    st.session_state.selected_l1 = ""
                    st.session_state.selected_l2 = ""
                    st.session_state.selected_l3 = ""
                    st.rerun()

        st.markdown("---")

        # Exibir notícia atual
        row = df.loc[st.session_state.current_index]

        # Renderizar conteúdo da notícia
        self.render_news_content(row)

        # Renderizar seleção hierárquica FORA do form
        l1_selected, l2_selected, l3_selected = self.render_hierarchical_selection(row, themes)

        # Renderizar formulário (apenas campos finais)
        submit, skip, confianca, observacoes = self.render_annotation_form(row)

        if submit:
            if not l1_selected:
                st.error("⚠️ Selecione pelo menos o Tema (L1)")
            else:
                # Salvar anotação
                df.at[st.session_state.current_index, 'L1_anotado'] = l1_selected.split(' - ')[0]
                if l2_selected:
                    df.at[st.session_state.current_index, 'L2_anotado'] = l2_selected.split(' - ')[0]
                else:
                    df.at[st.session_state.current_index, 'L2_anotado'] = None

                if l3_selected:
                    df.at[st.session_state.current_index, 'L3_anotado'] = l3_selected.split(' - ')[0]
                else:
                    df.at[st.session_state.current_index, 'L3_anotado'] = None

                df.at[st.session_state.current_index, 'confianca'] = confianca
                df.at[st.session_state.current_index, 'observacoes'] = observacoes
                df.at[st.session_state.current_index, 'anotador'] = st.session_state.annotator_name
                df.at[st.session_state.current_index, 'data_anotacao'] = datetime.now().isoformat()

                self.save_data(df)
                st.success("✅ Anotação salva!")

                # Ir para próxima
                current_pos = indices.index(st.session_state.current_index)
                if current_pos < len(indices) - 1:
                    st.session_state.current_index = indices[current_pos + 1]

                # Limpar seleções
                st.session_state.selected_l1 = ""
                st.session_state.selected_l2 = ""
                st.session_state.selected_l3 = ""

                st.rerun()

        if skip:
            # Ir para próxima sem salvar
            current_pos = indices.index(st.session_state.current_index)
            if current_pos < len(indices) - 1:
                st.session_state.current_index = indices[current_pos + 1]

                # Limpar seleções
                st.session_state.selected_l1 = ""
                st.session_state.selected_l2 = ""
                st.session_state.selected_l3 = ""

                st.rerun()

        # Mostrar ground truth
        self.render_ground_truth(row, themes)


def main():
    """Função principal"""
    app = AnnotationApp()
    app.run()


if __name__ == "__main__":
    main()
