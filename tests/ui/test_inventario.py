"""Casos de prueba del catálogo de productos."""

import logging

import pytest

pytestmark = pytest.mark.ui

logger = logging.getLogger(__name__)


# CP-06: navegación al catálogo
@pytest.mark.smoke
def test_catalogo(inventario):
    assert inventario.obtener_titulo_seccion() == "Products"

    productos = inventario.obtener_productos()
    assert len(productos) > 0, "No se encontraron productos en el inventario"

    nombre, precio = inventario.obtener_nombre_y_precio(productos[0])
    logger.info("Primer producto: %s - Precio: %s", nombre, precio)
    assert nombre != ""
    assert precio.startswith("$")

    assert inventario.elementos_principales_visibles()


# CP-07: ordenar por precio de menor a mayor
def test_ordenar_por_precio(inventario):
    inventario.ordenar_por("lohi")

    precios = inventario.obtener_precios()
    logger.info("Precios ordenados: %s", precios)
    assert precios == sorted(precios)
