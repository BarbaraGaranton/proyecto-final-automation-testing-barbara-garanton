"""Casos de prueba del catálogo de productos."""

import logging

import pytest

pytestmark = pytest.mark.ui

logger = logging.getLogger(__name__)

# Opciones del filtro de orden: (valor del <select>, clave para ordenar, ¿descendente?)
OPCIONES_ORDEN = [
    pytest.param("az", "nombres", False, id="nombre_A_a_Z"),
    pytest.param("za", "nombres", True, id="nombre_Z_a_A"),
    pytest.param("lohi", "precios", False, id="precio_menor_a_mayor"),
    pytest.param("hilo", "precios", True, id="precio_mayor_a_menor"),
]


# CP-09: navegación al catálogo
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


# CP-10 a CP-13: ordenar el catálogo con cada opción del filtro
@pytest.mark.parametrize("opcion, criterio, descendente", OPCIONES_ORDEN)
def test_ordenar_catalogo(inventario, opcion, criterio, descendente):
    inventario.ordenar_por(opcion)

    valores = inventario.obtener_precios() if criterio == "precios" else inventario.obtener_nombres()
    logger.info("Valores luego de ordenar por '%s': %s", opcion, valores)
    assert valores == sorted(valores, reverse=descendente)
