"""Configuración compartida de Pytest: navegador, capturas de pantalla y logs."""

import logging
from datetime import datetime
from pathlib import Path

import pytest
import pytest_html

from utils.selenium_helpers import crear_driver

CARPETA_CAPTURAS = Path(__file__).parent / "reports" / "capturas"

logger = logging.getLogger(__name__)


@pytest.fixture
def driver():
    """Abre un navegador nuevo para cada test y lo cierra al terminar.

    Así los tests son independientes: la falla de uno no afecta a los demás.
    """
    navegador = crear_driver()
    yield navegador
    logger.info("Cerrando el navegador")
    navegador.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura de pantalla y la adjunta al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when == "call" and reporte.failed:
        navegador = item.funcargs.get("driver")
        if navegador is None:
            return

        CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = CARPETA_CAPTURAS / f"{item.name}_{fecha}.png"
        navegador.save_screenshot(str(archivo))
        logger.error("El test falló. Captura guardada en %s", archivo)

        extras = getattr(reporte, "extras", [])
        extras.append(pytest_html.extras.png(navegador.get_screenshot_as_base64()))
        reporte.extras = extras
