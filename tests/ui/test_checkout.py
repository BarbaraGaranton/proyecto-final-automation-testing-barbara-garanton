"""Casos de prueba del flujo completo de compra (checkout)."""

import pytest

pytestmark = pytest.mark.ui


# CP-10: compra completa de punta a punta
@pytest.mark.smoke
def test_checkout_completo(inventario):
    nombre_agregado = inventario.agregar_primer_producto()
    carrito = inventario.ir_al_carrito()

    formulario = carrito.ir_al_checkout()
    formulario.completar_datos("John", "Doe", "12345")

    resumen = formulario.continuar_al_resumen()
    assert resumen.obtener_titulo_seccion() == "Checkout: Overview"
    assert resumen.obtener_nombres_productos() == [nombre_agregado]

    confirmacion = resumen.finalizar_compra()
    assert confirmacion.obtener_mensaje_confirmacion() == "Thank you for your order!"
