"""Casos de prueba del carrito de compras."""

import pytest

pytestmark = pytest.mark.ui


# CP-08: agregar un producto al carrito
@pytest.mark.smoke
def test_agregar_producto_carrito(inventario):
    nombre_agregado = inventario.agregar_primer_producto()
    assert inventario.obtener_contador_carrito() == 1

    carrito = inventario.ir_al_carrito()
    assert carrito.obtener_nombres_productos() == [nombre_agregado]


# CP-09: quitar un producto del carrito
def test_quitar_producto_carrito(inventario):
    inventario.agregar_primer_producto()
    carrito = inventario.ir_al_carrito()

    carrito.quitar_primer_producto()

    assert carrito.cantidad_productos() == 0
    assert carrito.obtener_contador_carrito() == 0
