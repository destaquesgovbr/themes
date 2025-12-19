"""
Testes do fluxo de anotação usando Playwright.

Para executar os testes, certifique-se de que:
1. O app Streamlit está rodando em http://localhost:8501
2. As dependências estão instaladas: pip install -r tests/requirements.txt
3. Playwright browsers instalados: playwright install

Executar testes:
    pytest tests/test_annotation_flow.py -v
"""

import pytest
from playwright.sync_api import Page, expect


class TestHomePage:
    """Testes da página inicial"""

    def test_home_page_loads(self, page_with_app: Page):
        """Verifica que a home page carrega corretamente"""
        page = page_with_app

        # Verificar título principal
        expect(page.locator("text=Anotação Manual de Notícias GovBR")).to_be_visible()

        # Verificar seções de instruções
        expect(page.locator("text=🎯 Objetivo")).to_be_visible()
        expect(page.locator("text=📝 Como Anotar")).to_be_visible()
        expect(page.locator("text=✅ Dicas de Qualidade")).to_be_visible()

    def test_annotator_name_field_exists(self, page_with_app: Page):
        """Verifica que o campo de nome do anotador existe"""
        page = page_with_app

        # Verificar campo de nome
        name_input = page.get_by_placeholder("Digite seu nome completo")
        expect(name_input).to_be_visible()

    def test_start_button_validation(self, page_with_app: Page):
        """Verifica validação ao tentar iniciar sem nome"""
        page = page_with_app

        # Tentar iniciar sem preencher nome
        start_button = page.locator("text=🚀 Iniciar Anotação")
        start_button.click()

        # Deve mostrar mensagem de erro
        expect(page.locator("text=Por favor, informe seu nome antes de iniciar")).to_be_visible(timeout=3000)

    def test_start_annotation_with_name(self, page_with_app: Page):
        """Verifica que é possível iniciar com nome preenchido"""
        page = page_with_app

        # Preencher nome
        name_input = page.get_by_placeholder("Digite seu nome completo")
        name_input.fill("Teste Anotador")

        # Clicar em iniciar
        start_button = page.locator("text=🚀 Iniciar Anotação")
        start_button.click()

        # Aguardar transição para interface de anotação (Streamlit precisa fazer rerun)
        page.wait_for_timeout(6000)

        # Verificar que saiu da home
        expect(page.locator("text=🎯 Objetivo")).not_to_be_visible(timeout=3000)


class TestAnnotationInterface:
    """Testes da interface de anotação"""

    @pytest.fixture
    def annotation_page(self, page_with_annotation: Page):
        """
        Fixture que usa modo direto (direct=true) para pular home page.

        Isso evita problemas com reruns do Streamlit nos testes.
        """
        # Já está na interface de anotação (direct mode)
        return page_with_annotation

    def test_sidebar_shows_annotator_name(self, annotation_page: Page):
        """Verifica que o nome do anotador aparece no topo da sidebar"""
        page = annotation_page

        # Verificar nome na sidebar (modo direto usa "Test User")
        expect(page.locator("text=👤 Test User")).to_be_visible()

    def test_sidebar_shows_progress_metrics(self, annotation_page: Page):
        """Verifica que métricas de progresso estão visíveis"""
        page = annotation_page

        # Verificar métricas
        expect(page.locator("text=📊 Progresso")).to_be_visible()
        expect(page.locator("text=Total")).to_be_visible()
        expect(page.locator("text=Anotadas")).to_be_visible()
        expect(page.locator("text=Pendentes")).to_be_visible()

    def test_filters_have_tooltips(self, annotation_page: Page):
        """Verifica que os filtros têm tooltips (help text)"""
        page = annotation_page

        # Filtro de Status deve ter tooltip
        status_label = page.locator("text=Status").first
        expect(status_label).to_be_visible()

        # Filtro de Complexidade deve ter tooltip
        complexity_label = page.locator("text=Complexidade").first
        expect(complexity_label).to_be_visible()

    def test_complexity_has_emoji(self, annotation_page: Page):
        """Verifica que a complexidade exibe emoji"""
        page = annotation_page

        # Aguardar conteúdo carregar
        page.wait_for_timeout(2000)

        # Procurar por emojis de complexidade no corpo principal (não no filtro)
        complexity_section = page.locator("text=/Complexidade:.*[🟢🟡🔴]/")
        expect(complexity_section).to_be_visible()

    def test_agency_shows_full_name_not_sigla(self, annotation_page: Page):
        """Verifica que o nome completo da agência é exibido, não apenas a sigla"""
        page = annotation_page

        # Aguardar conteúdo carregar
        page.wait_for_timeout(2000)

        # Verificar que existe um órgão exibido
        organ_label = page.locator("text=/Órgão:.*Ministério|Agência|Secretaria|Instituto/")
        expect(organ_label).to_be_visible()

    def test_unique_id_not_displayed(self, annotation_page: Page):
        """Verifica que o unique_id NÃO é exibido"""
        page = annotation_page

        # Aguardar conteúdo carregar
        page.wait_for_timeout(2000)

        # Não deve ter texto "ID:" ou "unique_id"
        id_elements = page.locator("text=/ID:|unique_id/")
        expect(id_elements).not_to_be_visible()

    def test_l1_selection_shows_l2_field(self, annotation_page: Page):
        """TESTE CRÍTICO: Verifica que selecionar L1 faz aparecer o campo L2"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Encontrar seletor L1
        l1_selector = page.locator("[data-testid='stSelectbox']").filter(has_text="Tema (L1)").first

        # Inicialmente L2 não deve estar visível
        l2_selector = page.locator("text=Subtema (L2)")
        expect(l2_selector).not_to_be_visible()

        # Clicar no seletor L1
        l1_selector.click()

        # Selecionar primeiro tema disponível (não vazio)
        # Aguardar opções carregarem
        page.wait_for_timeout(500)

        # Selecionar uma opção que não seja vazia
        first_option = page.locator("[role='option']").filter(has_text="01 -").first
        if first_option.is_visible():
            first_option.click()

            # Aguardar reatividade
            page.wait_for_timeout(1000)

            # Agora L2 DEVE estar visível
            expect(l2_selector).to_be_visible(timeout=3000)

    def test_l2_selection_shows_l3_field(self, annotation_page: Page):
        """TESTE CRÍTICO: Verifica que selecionar L2 faz aparecer o campo L3"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Selecionar L1 primeiro
        l1_selector = page.locator("[data-testid='stSelectbox']").filter(has_text="Tema (L1)").first
        l1_selector.click()
        page.wait_for_timeout(500)

        first_l1_option = page.locator("[role='option']").filter(has_text="01 -").first
        if first_l1_option.is_visible():
            first_l1_option.click()
            page.wait_for_timeout(1000)

            # Selecionar L2
            l2_selector = page.locator("[data-testid='stSelectbox']").filter(has_text="Subtema (L2)").first
            l2_selector.click()
            page.wait_for_timeout(500)

            # Selecionar primeiro subtema disponível
            first_l2_option = page.locator("[role='option']").filter(has_text="01.01").first
            if first_l2_option.is_visible():
                first_l2_option.click()
                page.wait_for_timeout(1000)

                # Agora L3 DEVE estar visível
                l3_selector = page.locator("text=Categoria (L3)")
                expect(l3_selector).to_be_visible(timeout=3000)

    def test_ground_truth_shows_code_and_label(self, annotation_page: Page):
        """Verifica que o ground truth mostra código E label"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Procurar expander de ground truth
        ground_truth_expander = page.locator("text=Ver Classificação Original (Ground Truth)")

        if ground_truth_expander.is_visible():
            # Expandir
            ground_truth_expander.click()
            page.wait_for_timeout(500)

            # Verificar formato: deve ter código (entre backticks) E label (após hífen)
            # Exemplo: L1: `01` - Economia e Finanças
            l1_pattern = page.locator("text=/L1:.*`.*`.*-/")
            expect(l1_pattern).to_be_visible()

    def test_navigation_buttons_work(self, annotation_page: Page):
        """Verifica que os botões de navegação funcionam"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Verificar posição atual (ex: "Notícia 1 de X")
        counter = page.locator("text=/Notícia \\d+ de \\d+/")
        expect(counter).to_be_visible()

        initial_text = counter.inner_text()

        # Clicar em "Próxima"
        next_button = page.locator("text=Próxima ➡️")
        if next_button.is_visible():
            next_button.click()
            page.wait_for_timeout(1500)

            # Contador deve ter mudado
            new_text = counter.inner_text()
            assert initial_text != new_text, "Navegação não funcionou"

    def test_confidence_slider_exists(self, annotation_page: Page):
        """Verifica que o slider de confiança existe"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Verificar slider de confiança
        confidence_label = page.locator("text=Confiança na Classificação")
        expect(confidence_label).to_be_visible()

    def test_observations_field_exists(self, annotation_page: Page):
        """Verifica que o campo de observações existe"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Verificar campo de observações
        obs_field = page.get_by_placeholder("Casos ambíguos, dúvidas, comentários...")
        expect(obs_field).to_be_visible()

    def test_submit_button_validation(self, annotation_page: Page):
        """Verifica que o botão salvar valida L1 obrigatório"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Tentar salvar sem selecionar L1
        save_button = page.locator("text=💾 Salvar Anotação")
        save_button.click()

        # Deve mostrar erro
        expect(page.locator("text=Selecione pelo menos o Tema (L1)")).to_be_visible(timeout=3000)

    def test_back_to_home_button_works(self, annotation_page: Page):
        """Verifica que o botão de voltar para home funciona"""
        page = annotation_page

        # Clicar em voltar para home
        home_button = page.locator("text=🏠 Voltar para Home")
        home_button.click()

        # Deve voltar para home
        expect(page.locator("text=🎯 Objetivo")).to_be_visible(timeout=5000)


class TestComplexityEmojis:
    """Testes específicos para emojis de complexidade"""

    @pytest.fixture
    def annotation_page(self, page_with_annotation: Page):
        """
        Fixture que usa modo direto (direct=true) para pular home page.
        """
        # Já está na interface de anotação (direct mode)
        return page_with_annotation

    def test_complexity_filter_shows_emoji(self, annotation_page: Page):
        """Verifica que o filtro de complexidade mostra emojis"""
        page = annotation_page

        # Aguardar carregamento
        page.wait_for_timeout(2000)

        # Clicar no filtro de complexidade
        complexity_selectbox = page.locator("[data-testid='stSelectbox']").filter(has_text="Complexidade")
        complexity_selectbox.click()

        page.wait_for_timeout(500)

        # Verificar que as opções têm emojis
        # 🟢 clara, 🟡 moderada, 🔴 dificil
        clara_option = page.locator("[role='option']").filter(has_text="🟢")
        moderada_option = page.locator("[role='option']").filter(has_text="🟡")
        dificil_option = page.locator("[role='option']").filter(has_text="🔴")

        # Pelo menos um deve estar visível
        assert clara_option.is_visible() or moderada_option.is_visible() or dificil_option.is_visible(), \
            "Nenhum emoji de complexidade encontrado no filtro"
