"""Fixtures exclusivas de las pruebas de API."""

import pytest

from utils.api_client import ApiClient


@pytest.fixture
def api():
    """Devuelve un cliente de API nuevo para cada test y lo cierra al terminar."""
    cliente = ApiClient()
    yield cliente
    cliente.cerrar()
