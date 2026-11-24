"""Configuración compartida de Pytest: navegador, capturas de pantalla y reporte."""

import logging
import re
from datetime import datetime
from pathlib import Path

import pytest
import pytest_html

from pages import LoginPage
from utils.driver_factory import crear_driver

CARPETA_CAPTURAS = Path(__file__).parent / "reports" / "capturas"
CARPETA_EVIDENCIAS = Path(__file__).parent / "reports" / "evidencias"

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Opción --evidencias: guarda una captura al final de CADA test de UI
    (no solo de los que fallan), para documentar la ejecución."""
    parser.addoption(
        "--evidencias",
        action="store_true",
        default=False,
        help="Guarda una captura de pantalla al final de cada test de UI en reports/evidencias/",
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def driver():
    """Abre un navegador nuevo para cada test y lo cierra al terminar.

    Así los tests son independientes: la falla de uno no afecta a los demás.
    """
    navegador = crear_driver()
    yield navegador
    logger.info("Cerrando el navegador")
    navegador.quit()


@pytest.fixture
def login_page(driver):
    """Devuelve la página de login ya abierta."""
    return LoginPage(driver).abrir()


@pytest.fixture
def inventario(driver):
    """Inicia sesión con el usuario estándar y devuelve la página de inventario."""
    return LoginPage(driver).iniciar_sesion_valida()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def pytest_runtest_setup(item):
    """Deja una marca en el log al comenzar cada test, para seguirlo fácilmente."""
    logger.info("========== INICIO: %s ==========", item.nodeid)


def _nombre_archivo_seguro(texto):
    """Reemplaza los caracteres que no conviene usar en nombres de archivo."""
    return re.sub(r"[^\w\-]+", "_", texto).strip("_")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Registra el resultado de cada test y, si un test de UI falla, guarda una
    captura de pantalla con fecha/hora y la adjunta al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when != "call":
        return

    if hasattr(reporte, "wasxfail"):
        estado = f"FALLO ESPERADO ({reporte.wasxfail})" if reporte.skipped else "PASÓ (defecto corregido)"
    else:
        estado = "PASÓ" if reporte.passed else "FALLÓ" if reporte.failed else "OMITIDO"
    logger.info("Resultado de %s: %s (%.2f s)", item.name, estado, reporte.duration)

    navegador = item.funcargs.get("driver")
    if navegador is None:
        return  # Los tests de API no tienen navegador, no hay captura que tomar

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{_nombre_archivo_seguro(item.name)}_{fecha}.png"

    if reporte.failed:
        CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
        archivo = CARPETA_CAPTURAS / nombre_archivo
        navegador.save_screenshot(str(archivo))
        logger.error("El test falló. Captura guardada en %s", archivo)

        extras = getattr(reporte, "extras", [])
        extras.append(pytest_html.extras.png(navegador.get_screenshot_as_base64(), name=archivo.name))
        reporte.extras = extras

    elif item.config.getoption("--evidencias"):
        CARPETA_EVIDENCIAS.mkdir(parents=True, exist_ok=True)
        _aceptar_alerta_pendiente(navegador)
        navegador.save_screenshot(str(CARPETA_EVIDENCIAS / nombre_archivo))
        logger.info("Evidencia guardada: %s", nombre_archivo)


def _aceptar_alerta_pendiente(navegador):
    """Cierra una alerta abierta (si la hay) para poder tomar la captura."""
    try:
        navegador.switch_to.alert.accept()
    except Exception:
        pass


def pytest_html_report_title(report):
    """Título del reporte HTML."""
    report.title = "Reporte de pruebas - Framework de Automatización (SauceDemo + JSONPlaceholder)"
