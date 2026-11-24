"""Casos de prueba del login y logout de SauceDemo."""

import pytest

from pages import InventoryPage

pytestmark = pytest.mark.ui


# CP-01: login exitoso
@pytest.mark.smoke
def test_login_exitoso(login_page):
    login_page.iniciar_sesion()

    inventario = InventoryPage(login_page.driver)
    inventario.esperar_url("/inventory.html")
    assert "/inventory.html" in inventario.driver.current_url
    assert inventario.driver.title == "Swag Labs"
    assert inventario.obtener_titulo_seccion() == "Products"


# CP-02: login con contraseña incorrecta (negativo)
def test_login_password_incorrecta(login_page):
    login_page.iniciar_sesion(password="clave_incorrecta")

    assert "Username and password do not match" in login_page.obtener_mensaje_error()
    assert "/inventory.html" not in login_page.driver.current_url


# CP-03: login con usuario bloqueado (negativo)
def test_login_usuario_bloqueado(login_page):
    login_page.iniciar_sesion(usuario="locked_out_user")

    assert "this user has been locked out" in login_page.obtener_mensaje_error()
    assert "/inventory.html" not in login_page.driver.current_url


# CP-04: login con campos vacíos (negativo)
def test_login_campos_vacios(login_page):
    login_page.iniciar_sesion(usuario="", password="")

    assert "Username is required" in login_page.obtener_mensaje_error()


# CP-05: cierre de sesión
def test_logout(inventario):
    login_page = inventario.cerrar_sesion()

    assert login_page.esta_en_login()
