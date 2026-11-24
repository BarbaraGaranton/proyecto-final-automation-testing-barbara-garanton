"""Casos de prueba del flujo de compra (checkout).

Los datos del comprador se leen de data/checkout.csv. Las filas sin
mensaje_error son compras válidas; las demás deben mostrar ese error.
"""

import pytest

from utils.data_loader import generar_ids, leer_csv

pytestmark = pytest.mark.ui

CASOS_CHECKOUT = leer_csv("checkout.csv")


# CP-18 a CP-22: checkout con distintos datos del comprador
@pytest.mark.parametrize("caso", CASOS_CHECKOUT, ids=generar_ids(CASOS_CHECKOUT))
def test_checkout(inventario, caso):
    nombre_agregado = inventario.agregar_primer_producto()
    carrito = inventario.ir_al_carrito()

    formulario = carrito.ir_al_checkout()
    formulario.completar_datos(caso["nombre"], caso["apellido"], caso["codigo_postal"])

    if caso["mensaje_error"]:
        # Caso negativo: el formulario no deja avanzar y muestra el error
        formulario.continuar()
        assert caso["mensaje_error"] in formulario.obtener_mensaje_error()
        assert "/checkout-step-one.html" in formulario.driver.current_url
        return

    # Caso positivo: compra completa de punta a punta
    resumen = formulario.continuar_al_resumen()
    assert resumen.obtener_titulo_seccion() == "Checkout: Overview"
    assert resumen.obtener_nombres_productos() == [nombre_agregado]

    confirmacion = resumen.finalizar_compra()
    assert confirmacion.obtener_mensaje_confirmacion() == "Thank you for your order!"
