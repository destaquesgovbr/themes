"""
Subfase 4.3: Interface de Anotação Manual (Streamlit)

Interface web para anotação manual de notícias com classificação temática.
Executar com: streamlit run scripts/dataset/03_annotation_app.py
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import DATA_DIR, THEMES_FILE
from utils.yaml_utils import load_yaml, iter_all_nodes, get_level

import streamlit as st


class AnnotationApp:
    """App de anotação manual de notícias"""

    def __init__(self):
        self.dataset_file = DATA_DIR / "test_dataset.csv"
        self.themes_file = THEMES_FILE
        self.themes_tree = None

    def load_data(self):
        """Carrega dataset e árvore temática"""
        # Carregar dataset
        if not self.dataset_file.exists():
            st.error(f"Dataset não encontrado: {self.dataset_file}")
            st.info("Execute primeiro: python scripts/dataset/03_collect_news.py")
            st.stop()

        df = pd.read_csv(self.dataset_file)

        # Carregar árvore temática
        self.themes_tree = load_yaml(self.themes_file)

        return df

    def get_theme_hierarchy(self):
        """Extrai hierarquia de temas da árvore"""
        themes = {'L1': {}, 'L2': {}, 'L3': {}}

        for node in iter_all_nodes(self.themes_tree):
            code = node.get('code', '')
            label = node.get('label', '')
            level = get_level(code)

            if level == 'L1':
                themes['L1'][code] = label
            elif level == 'L2':
                parent_l1 = code.split('.')[0]
                if parent_l1 not in themes['L2']:
                    themes['L2'][parent_l1] = {}
                themes['L2'][parent_l1][code] = label
            elif level == 'L3':
                parent_l2 = '.'.join(code.split('.')[:2])
                if parent_l2 not in themes['L3']:
                    themes['L3'][parent_l2] = {}
                themes['L3'][parent_l2][code] = label

        return themes

    def save_data(self, df):
        """Salva dataset anotado"""
        df.to_csv(self.dataset_file, index=False, encoding='utf-8')

    def render_ui(self):
        """Renderiza interface principal"""
        st.set_page_config(
            page_title="Anotação de Notícias GovBR",
            page_icon="📋",
            layout="wide"
        )

        st.title("📋 Anotação Manual de Notícias - Fase 4.3")
        st.markdown("---")

        # Carregar dados
        df = self.load_data()
        themes = self.get_theme_hierarchy()

        # Sidebar: Estatísticas e navegação
        with st.sidebar:
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
                ["Todas", "Pendentes", "Anotadas"]
            )

            filtro_complexidade = st.selectbox(
                "Complexidade",
                ["Todas", "clara", "moderada", "dificil"]
            )

            # Aplicar filtros
            df_filtrado = df.copy()

            if filtro_status == "Pendentes":
                df_filtrado = df_filtrado[df_filtrado['L1_anotado'].isna()]
            elif filtro_status == "Anotadas":
                df_filtrado = df_filtrado[df_filtrado['L1_anotado'].notna()]

            if filtro_complexidade != "Todas":
                df_filtrado = df_filtrado[df_filtrado['complexidade_estimada'] == filtro_complexidade]

            st.markdown("---")
            st.caption(f"Exibindo: {len(df_filtrado)} notícias")

        # Área principal: Seleção e anotação
        if len(df_filtrado) == 0:
            st.info("✅ Todas as notícias foram anotadas!")
            return

        # Seletor de notícia
        indices = df_filtrado.index.tolist()
        if 'current_index' not in st.session_state:
            st.session_state.current_index = indices[0]

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button("⬅️ Anterior"):
                current_pos = indices.index(st.session_state.current_index)
                if current_pos > 0:
                    st.session_state.current_index = indices[current_pos - 1]
                    st.rerun()

        with col2:
            st.markdown(f"**Notícia {indices.index(st.session_state.current_index) + 1} de {len(indices)}**")

        with col3:
            if st.button("Próxima ➡️"):
                current_pos = indices.index(st.session_state.current_index)
                if current_pos < len(indices) - 1:
                    st.session_state.current_index = indices[current_pos + 1]
                    st.rerun()

        st.markdown("---")

        # Exibir notícia atual
        row = df.loc[st.session_state.current_index]

        # Informações da notícia
        col_info1, col_info2 = st.columns(2)

        with col_info1:
            st.markdown(f"**Órgão:** {row['orgao']}")
            st.markdown(f"**Data:** {row['data_publicacao']}")
            st.markdown(f"**Complexidade:** `{row['complexidade_estimada']}`")

        with col_info2:
            st.markdown(f"**ID:** `{row['unique_id']}`")
            if row['url']:
                st.markdown(f"[🔗 Link original]({row['url']})")

        st.markdown("---")

        # Conteúdo da notícia
        st.subheader("📰 Título")
        st.markdown(f"### {row['titulo']}")

        if pd.notna(row['resumo']) and row['resumo']:
            st.subheader("📝 Resumo")
            st.info(row['resumo'])

        if pd.notna(row['conteudo_inicio']) and row['conteudo_inicio']:
            with st.expander("📄 Início do Conteúdo (500 caracteres)"):
                st.text(row['conteudo_inicio'])

        st.markdown("---")

        # Formulário de anotação
        st.subheader("🏷️ Classificação Temática")

        with st.form(key="annotation_form"):
            # L1 - Tema
            l1_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L1'].items())]
            l1_selected = st.selectbox(
                "**Tema (L1)**",
                l1_options,
                index=0 if pd.isna(row['L1_anotado']) else l1_options.index([x for x in l1_options if x.startswith(row['L1_anotado'])][0]) if any(x.startswith(str(row['L1_anotado'])) for x in l1_options) else 0
            )

            # L2 - Subtema
            if l1_selected:
                l1_code = l1_selected.split(' - ')[0]
                l2_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L2'].get(l1_code, {}).items())]
                l2_selected = st.selectbox(
                    "**Subtema (L2)**",
                    l2_options,
                    index=0 if pd.isna(row['L2_anotado']) else l2_options.index([x for x in l2_options if x.startswith(row['L2_anotado'])][0]) if any(x.startswith(str(row['L2_anotado'])) for x in l2_options) else 0
                )

                # L3 - Categoria
                if l2_selected:
                    l2_code = l2_selected.split(' - ')[0]
                    l3_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L3'].get(l2_code, {}).items())]
                    l3_selected = st.selectbox(
                        "**Categoria (L3)**",
                        l3_options,
                        index=0 if pd.isna(row['L3_anotado']) else l3_options.index([x for x in l3_options if x.startswith(row['L3_anotado'])][0]) if any(x.startswith(str(row['L3_anotado'])) for x in l3_options) else 0
                    )
                else:
                    l3_selected = None
            else:
                l2_selected = None
                l3_selected = None

            # Confiança
            confianca = st.select_slider(
                "**Confiança na Classificação**",
                options=["baixa", "media", "alta"],
                value=row['confianca'] if pd.notna(row['confianca']) and row['confianca'] in ["baixa", "media", "alta"] else "media"
            )

            # Observações
            observacoes = st.text_area(
                "**Observações** (opcional)",
                value=row['observacoes'] if pd.notna(row['observacoes']) else "",
                placeholder="Casos ambíguos, dúvidas, comentários..."
            )

            # Anotador
            anotador = st.text_input(
                "**Nome do Anotador**",
                value=row['anotador'] if pd.notna(row['anotador']) else "",
                placeholder="Seu nome"
            )

            # Botões
            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                submit = st.form_submit_button("💾 Salvar Anotação", type="primary", use_container_width=True)

            with col_btn2:
                skip = st.form_submit_button("⏭️ Pular", use_container_width=True)

            if submit:
                if not l1_selected:
                    st.error("⚠️ Selecione pelo menos o Tema (L1)")
                elif not anotador:
                    st.error("⚠️ Informe o nome do anotador")
                else:
                    # Salvar anotação
                    df.at[st.session_state.current_index, 'L1_anotado'] = l1_selected.split(' - ')[0]
                    if l2_selected:
                        df.at[st.session_state.current_index, 'L2_anotado'] = l2_selected.split(' - ')[0]
                    if l3_selected:
                        df.at[st.session_state.current_index, 'L3_anotado'] = l3_selected.split(' - ')[0]

                    df.at[st.session_state.current_index, 'confianca'] = confianca
                    df.at[st.session_state.current_index, 'observacoes'] = observacoes
                    df.at[st.session_state.current_index, 'anotador'] = anotador
                    df.at[st.session_state.current_index, 'data_anotacao'] = datetime.now().isoformat()

                    self.save_data(df)
                    st.success("✅ Anotação salva!")

                    # Ir para próxima
                    current_pos = indices.index(st.session_state.current_index)
                    if current_pos < len(indices) - 1:
                        st.session_state.current_index = indices[current_pos + 1]
                    st.rerun()

            if skip:
                # Ir para próxima sem salvar
                current_pos = indices.index(st.session_state.current_index)
                if current_pos < len(indices) - 1:
                    st.session_state.current_index = indices[current_pos + 1]
                    st.rerun()

        # Mostrar classificação original (se houver)
        if pd.notna(row['L1_original']) and row['L1_original']:
            with st.expander("🔍 Ver Classificação Original (Ground Truth)"):
                st.markdown(f"**L1:** `{row['L1_original']}`")
                if pd.notna(row['L2_original']):
                    st.markdown(f"**L2:** `{row['L2_original']}`")
                if pd.notna(row['L3_original']):
                    st.markdown(f"**L3:** `{row['L3_original']}`")


def main():
    app = AnnotationApp()
    app.render_ui()


if __name__ == "__main__":
    main()
