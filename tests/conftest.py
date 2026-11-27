"""Chromium compartido (una instancia por sesion) para generar PDFs y capturas de prueba."""
import os

import pytest


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as e:  # Chromium sin instalar: en local se saltan; en CI es un fallo
            if os.environ.get("CI"):
                raise
            pytest.skip(f"Chromium no disponible: {str(e).splitlines()[0][:120]}")
        yield b
        b.close()
