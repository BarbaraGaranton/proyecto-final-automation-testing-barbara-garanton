"""Defectos reales encontrados en SauceDemo con sus usuarios especiales.

Cada test verifica el comportamiento CORRECTO esperado. Como el sitio tiene
el defecto, el test está marcado con xfail ("se espera que falle") y el ID del
bug documentado en docs/. En el reporte aparecen como "XFailed".
Si algún día el defecto se corrige, el test aparecerá como "XPassed" y el
bug se puede cerrar.
"""

import time

import pytest

from pages import InventoryPage, LoginPage
from utils.config import PASSWORD_VALIDO

pytestmark = [pytest.mark.ui, pytest.mark.defectos]

# Tiempo máximo aceptable para el login (criterio no funcional)
TIEMPO_MAXIMO_LOGIN = 3.0


def bug(id_bug, descripcion):
    """Marca un caso como defecto conocido, con su ID para el reporte."""
    return pytest.mark.xfail(reason=f"{id_bug}: {descripcion}", strict=False)


def entrar_como(driver, usuario):
    """Inicia sesión con el usuario indicado y devuelve la página de inventario."""
    login = LoginPage(driver).abrir()
    login.iniciar_sesion(usuario, PASSWORD_VALIDO)
    inventario = InventoryPage(driver)
    inventario.esperar_url("/inventory.html")
    return inventario


# CP-26 y CP-27: cada producto debe mostrar su propia imagen
@pytest.mark.parametrize(
    "usuario",
    [
        pytest.param("problem_user", marks=bug("BUG-001", "todas las imágenes son la misma"), id="problem_user"),
        pytest.param("visual_user", marks=bug("BUG-008", "la mochila muestra una imagen incorrecta"), id="visual_user"),
    ],
)
def test_imagenes_de_productos(driver, usuario):
    inventario = entrar_como(driver, usuario)

    imagenes = inventario.obtener_imagenes()
    assert len(set(imagenes)) == len(imagenes), f"Imágenes repetidas: {imagenes}"
    assert not any("sl-404" in imagen for imagen in imagenes), "Hay imágenes de error 404"


# CP-28 y CP-29: el filtro Z-A debe ordenar los productos sin errores
@pytest.mark.parametrize(
    "usuario",
    [
        pytest.param("problem_user", marks=bug("BUG-002", "el filtro no ordena"), id="problem_user"),
        pytest.param("error_user", marks=bug("BUG-005", "alerta 'Sorting is broken!'"), id="error_user"),
    ],
)
def test_ordenar_z_a(driver, usuario):
    inventario = entrar_como(driver, usuario)

    inventario.ordenar_por("za")
    alerta = inventario.aceptar_alerta_si_existe()

    assert alerta is None, f"El sitio mostró la alerta: {alerta}"
    nombres = inventario.obtener_nombres()
    assert nombres == sorted(nombres, reverse=True)


# CP-30 y CP-31: se deben poder agregar los 6 productos al carrito
@pytest.mark.parametrize(
    "usuario",
    [
        pytest.param("problem_user", marks=bug("BUG-003", "solo se agregan 3 de 6 productos"), id="problem_user"),
        pytest.param("error_user", marks=bug("BUG-003", "solo se agregan 3 de 6 productos"), id="error_user"),
    ],
)
def test_agregar_todos_los_productos(driver, usuario):
    inventario = entrar_como(driver, usuario)

    nombres = inventario.obtener_nombres()
    assert len(nombres) == 6, f"El catálogo debería tener 6 productos y tiene {len(nombres)}"
    for nombre in nombres:
        inventario.agregar_producto_por_nombre(nombre)

    assert inventario.obtener_contador_carrito() == len(nombres)


# CP-32 y CP-33: el checkout debe guardar lo que escribe el usuario y completar la compra
@pytest.mark.parametrize(
    "usuario",
    [
        pytest.param("problem_user", marks=bug("BUG-004", "el apellido se escribe en el campo nombre"), id="problem_user"),
        pytest.param("error_user", marks=bug("BUG-006", "el apellido no se guarda y Finish no finaliza"), id="error_user"),
    ],
)
def test_checkout_con_usuario_especial(driver, usuario):
    inventario = entrar_como(driver, usuario)
    inventario.agregar_primer_producto()
    formulario = inventario.ir_al_carrito().ir_al_checkout()

    formulario.completar_datos("John", "Doe", "12345")
    assert formulario.leer_valor(formulario.CAMPO_NOMBRE) == "John"
    assert formulario.leer_valor(formulario.CAMPO_APELLIDO) == "Doe"

    confirmacion = formulario.continuar_al_resumen().finalizar_compra()
    assert confirmacion.obtener_mensaje_confirmacion() == "Thank you for your order!"


# CP-34 y CP-35: criterio no funcional, el login no debe tardar más de 3 segundos
@pytest.mark.parametrize(
    "usuario",
    [
        pytest.param("standard_user", id="standard_user"),
        pytest.param("performance_glitch_user", marks=bug("BUG-007", "el login tarda más de 3 s"), id="performance_glitch_user"),
    ],
)
def test_tiempo_de_login(driver, usuario):
    login = LoginPage(driver).abrir()

    inicio = time.perf_counter()
    login.iniciar_sesion(usuario, PASSWORD_VALIDO)
    InventoryPage(driver).esperar_url("/inventory.html")
    duracion = time.perf_counter() - inicio

    assert duracion <= TIEMPO_MAXIMO_LOGIN, f"El login tardó {duracion:.2f} s"
