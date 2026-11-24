"""Casos de prueba del login y logout de SauceDemo.

Los datos de login se leen de data/login.json: cada caso se ejecuta como un
test independiente y aparece con su propio nombre en el reporte.
"""

import pytest

from pages import InventoryPage
from utils.data_loader import generar_ids, leer_json

pytestmark = pytest.mark.ui

CASOS_LOGIN = leer_json("login.json")


# CP-01 a CP-07: login con distintos usuarios (positivos y negativos)
@pytest.mark.parametrize("caso", CASOS_LOGIN, ids=generar_ids(CASOS_LOGIN))
def test_login(login_page, caso):
    login_page.iniciar_sesion(caso["usuario"], caso["password"])

    if caso["debe_ingresar"]:
        # Caso positivo: se llega al inventario
        inventario = InventoryPage(login_page.driver)
        inventario.esperar_url("/inventory.html")
        assert inventario.driver.title == "Swag Labs"
        assert inventario.obtener_titulo_seccion() == "Products"
    else:
        # Caso negativo: se muestra el error y no se entra al inventario
        assert caso["mensaje_esperado"] in login_page.obtener_mensaje_error()
        assert "/inventory.html" not in login_page.driver.current_url


# CP-08: cierre de sesión
@pytest.mark.smoke
def test_logout(inventario):
    login_page = inventario.cerrar_sesion()

    assert login_page.esta_en_login()
