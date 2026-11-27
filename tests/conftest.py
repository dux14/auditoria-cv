"""Chromium compartido (una instancia por sesion) para generar PDFs y capturas de prueba."""
import pytest


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as e:  # Chromium sin instalar: los casos que lo necesitan se saltan
            pytest.skip(f"Chromium no disponible: {str(e).splitlines()[0][:120]}")
        yield b
        b.close()
