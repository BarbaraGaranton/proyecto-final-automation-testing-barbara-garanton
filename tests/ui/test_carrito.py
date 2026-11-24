"""Casos de prueba del carrito de compras.

Los productos a agregar se leen de data/productos.json.
"""

import pytest

from utils.data_loader import generar_ids, leer_json

pytestmark = pytest.mark.ui

CASOS_PRODUCTOS = leer_json("productos.json")


# CP-14 a CP-16: agregar uno o varios productos al carrito
@pytest.mark.parametrize("caso", CASOS_PRODUCTOS, ids=generar_ids(CASOS_PRODUCTOS))
def test_agregar_productos_carrito(inventario, caso):
    for nombre in caso["productos"]:
        inventario.agregar_producto_por_nombre(nombre)

    assert inventario.obtener_contador_carrito() == len(caso["productos"])

    carrito = inventario.ir_al_carrito()
    assert sorted(carrito.obtener_nombres_productos()) == sorted(caso["productos"])


# CP-17: quitar un producto del carrito
@pytest.mark.smoke
def test_quitar_producto_carrito(inventario):
    inventario.agregar_primer_producto()
    carrito = inventario.ir_al_carrito()

    carrito.quitar_primer_producto()

    assert carrito.cantidad_productos() == 0
    assert carrito.obtener_contador_carrito() == 0
