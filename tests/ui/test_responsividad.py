"""Pruebas de responsividad: recorre las páginas principales en Desktop, Tablet y Móvil.

En cada tamaño de pantalla guarda una captura por página en reports/responsividad/
(por ejemplo Mobile_Inventario.png) y verifica que no aparezca scroll horizontal
y que los elementos clave sigan visibles.
"""

from pathlib import Path

import pytest

from pages import InventoryPage, LoginPage

pytestmark = pytest.mark.ui

CARPETA_RESPONSIVIDAD = Path(__file__).resolve().parents[2] / "reports" / "responsividad"

# Breakpoints del plan de pruebas: (nombre, ancho, alto, ¿es móvil?)
BREAKPOINTS = [
    pytest.param("Desktop", 1920, 1080, False, id="desktop_1920x1080"),
    pytest.param("Tablet", 768, 1024, True, id="tablet_768x1024"),
    pytest.param("Mobile", 390, 844, True, id="mobile_390x844"),
]


def emular_pantalla(driver, ancho, alto, movil):
    """Simula el tamaño de pantalla exacto usando las DevTools de Chrome."""
    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {"width": ancho, "height": alto, "deviceScaleFactor": 1, "mobile": movil},
    )


def hay_scroll_horizontal(driver):
    """Devuelve True si el contenido es más ancho que la pantalla."""
    return driver.execute_script(
        "return document.documentElement.scrollWidth > window.innerWidth;"
    )


def capturar(driver, dispositivo, pagina):
    """Guarda la captura de la página actual con un nombre descriptivo."""
    CARPETA_RESPONSIVIDAD.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(CARPETA_RESPONSIVIDAD / f"{dispositivo}_{pagina}.png"))


# CP-23 a CP-25: responsividad en Desktop, Tablet y Móvil
@pytest.mark.parametrize("dispositivo, ancho, alto, movil", BREAKPOINTS)
def test_responsividad(driver, dispositivo, ancho, alto, movil):
    emular_pantalla(driver, ancho, alto, movil)
    problemas = []

    # Login
    login = LoginPage(driver).abrir()
    capturar(driver, dispositivo, "Login")
    if not login.esta_visible(login.BOTON_LOGIN):
        problemas.append("Login: el botón no se ve")
    if hay_scroll_horizontal(driver):
        problemas.append("Login: hay scroll horizontal")

    # Inventario
    login.iniciar_sesion()
    inventario = InventoryPage(driver)
    inventario.esperar_url("/inventory.html")
    capturar(driver, dispositivo, "Inventario")
    if not inventario.elementos_principales_visibles():
        problemas.append("Inventario: no se ven el menú, el filtro o el carrito")
    if hay_scroll_horizontal(driver):
        problemas.append("Inventario: hay scroll horizontal")

    # Carrito
    inventario.agregar_primer_producto()
    carrito = inventario.ir_al_carrito()
    capturar(driver, dispositivo, "Carrito")
    if carrito.cantidad_productos() != 1:
        problemas.append("Carrito: no muestra el producto agregado")
    if hay_scroll_horizontal(driver):
        problemas.append("Carrito: hay scroll horizontal")

    # Checkout
    formulario = carrito.ir_al_checkout()
    capturar(driver, dispositivo, "Checkout")
    if not formulario.esta_visible(formulario.BOTON_CONTINUAR):
        problemas.append("Checkout: el botón Continue no se ve")
    if hay_scroll_horizontal(driver):
        problemas.append("Checkout: hay scroll horizontal")

    assert problemas == [], f"Problemas en {dispositivo}: {problemas}"
