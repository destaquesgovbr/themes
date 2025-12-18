"""
Configuração do Pytest para testes do app de anotação.
"""

import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configuração do contexto do browser.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture
def app_url():
    """URL base da aplicação (deve estar rodando)"""
    return "http://localhost:8501"


@pytest.fixture
def page_with_app(page: Page, app_url: str):
    """
    Fixture que navega para o app e espera carregar.

    Args:
        page: Página do Playwright
        app_url: URL base da aplicação

    Returns:
        Page object pronto para testes
    """
    page.goto(app_url)
    # Esperar app Streamlit carregar completamente
    page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=10000)
    return page
