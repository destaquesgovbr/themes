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


# Configuração da página
st.set_page_config(
    page_title="Anotação de Notícias GovBR - Fase 4",
    page_icon="📋",
    layout="wide"
)


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

    def render_sidebar(self, df):
        """Renderiza sidebar com estatísticas e filtros"""
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
            st.markdown(f"**Órgão:** {row['orgao']}")
            st.markdown(f"**Data:** {row['data_publicacao']}")
            st.markdown(f"**Complexidade:** `{row['complexidade_estimada']}`")

        with col_info2:
            st.markdown(f"**ID:** `{row['unique_id']}`")
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

    def render_annotation_form(self, row, themes):
        """Renderiza formulário de anotação"""
        st.subheader("🏷️ Classificação Temática")

        with st.form(key="annotation_form"):
            # L1 - Tema
            l1_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L1'].items())]
            l1_current = ""
            if pd.notna(row['L1_anotado']) and str(row['L1_anotado']):
                matches = [x for x in l1_options if x.startswith(str(row['L1_anotado']))]
                if matches:
                    l1_current = matches[0]

            l1_selected = st.selectbox(
                "**Tema (L1)**",
                l1_options,
                index=l1_options.index(l1_current) if l1_current in l1_options else 0
            )

            l2_selected = None
            l3_selected = None

            # L2 - Subtema
            if l1_selected:
                l1_code = l1_selected.split(' - ')[0]
                l2_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L2'].get(l1_code, {}).items())]

                l2_current = ""
                if pd.notna(row['L2_anotado']) and str(row['L2_anotado']):
                    matches = [x for x in l2_options if x.startswith(str(row['L2_anotado']))]
                    if matches:
                        l2_current = matches[0]

                l2_selected = st.selectbox(
                    "**Subtema (L2)**",
                    l2_options,
                    index=l2_options.index(l2_current) if l2_current in l2_options else 0
                )

                # L3 - Categoria
                if l2_selected:
                    l2_code = l2_selected.split(' - ')[0]
                    l3_options = [""] + [f"{code} - {label}" for code, label in sorted(themes['L3'].get(l2_code, {}).items())]

                    l3_current = ""
                    if pd.notna(row['L3_anotado']) and str(row['L3_anotado']):
                        matches = [x for x in l3_options if x.startswith(str(row['L3_anotado']))]
                        if matches:
                            l3_current = matches[0]

                    l3_selected = st.selectbox(
                        "**Categoria (L3)**",
                        l3_options,
                        index=l3_options.index(l3_current) if l3_current in l3_options else 0
                    )

            # Confiança
            conf_value = "media"
            if pd.notna(row['confianca']) and row['confianca'] in ["baixa", "media", "alta"]:
                conf_value = row['confianca']

            confianca = st.select_slider(
                "**Confiança na Classificação**",
                options=["baixa", "media", "alta"],
                value=conf_value
            )

            # Observações
            obs_value = ""
            if pd.notna(row['observacoes']):
                obs_value = str(row['observacoes'])

            observacoes = st.text_area(
                "**Observações** (opcional)",
                value=obs_value,
                placeholder="Casos ambíguos, dúvidas, comentários..."
            )

            # Anotador
            anotador_value = ""
            if pd.notna(row['anotador']):
                anotador_value = str(row['anotador'])

            anotador = st.text_input(
                "**Nome do Anotador**",
                value=anotador_value,
                placeholder="Seu nome"
            )

            # Botões
            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                submit = st.form_submit_button("💾 Salvar Anotação", type="primary", use_container_width=True)

            with col_btn2:
                skip = st.form_submit_button("⏭️ Pular", use_container_width=True)

            return submit, skip, l1_selected, l2_selected, l3_selected, confianca, observacoes, anotador

    def render_ground_truth(self, row):
        """Renderiza classificação original (ground truth)"""
        if pd.notna(row['L1_original']) and row['L1_original']:
            with st.expander("🔍 Ver Classificação Original (Ground Truth)"):
                st.markdown(f"**L1:** `{row['L1_original']}`")
                if pd.notna(row['L2_original']):
                    st.markdown(f"**L2:** `{row['L2_original']}`")
                if pd.notna(row['L3_original']):
                    st.markdown(f"**L3:** `{row['L3_original']}`")

    def run(self):
        """Executa aplicação principal"""
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

        # Navegação
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button("⬅️ Anterior"):
                current_pos = indices.index(st.session_state.current_index)
                if current_pos > 0:
                    st.session_state.current_index = indices[current_pos - 1]
                    st.rerun()

        with col2:
            current_pos = indices.index(st.session_state.current_index)
            st.markdown(f"**Notícia {current_pos + 1} de {len(indices)}**")

        with col3:
            if st.button("Próxima ➡️"):
                current_pos = indices.index(st.session_state.current_index)
                if current_pos < len(indices) - 1:
                    st.session_state.current_index = indices[current_pos + 1]
                    st.rerun()

        st.markdown("---")

        # Exibir notícia atual
        row = df.loc[st.session_state.current_index]

        # Renderizar conteúdo da notícia
        self.render_news_content(row)

        # Renderizar formulário de anotação
        submit, skip, l1_selected, l2_selected, l3_selected, confianca, observacoes, anotador = self.render_annotation_form(row, themes)

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

        # Mostrar ground truth
        self.render_ground_truth(row)


def main():
    """Função principal"""
    app = AnnotationApp()
    app.run()


if __name__ == "__main__":
    main()
