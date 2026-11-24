"""Cliente HTTP reutilizable para las pruebas de API, construido sobre Requests."""

import json
import logging

import requests

from utils.config import TIEMPO_ESPERA_API, URL_API

logger = logging.getLogger(__name__)


class ApiClient:
    """Envía peticiones a la API y registra en el log cada petición y su respuesta.

    Los tests usan este cliente en lugar de llamar a requests directamente,
    así la URL base, los encabezados y el logging quedan en un solo lugar.
    """

    def __init__(self, url_base=URL_API):
        self.url_base = url_base.rstrip("/")
        self.sesion = requests.Session()
        self.sesion.headers.update(
            {"Content-Type": "application/json; charset=UTF-8", "Accept": "application/json"}
        )

    def _enviar(self, metodo, endpoint, **kwargs):
        """Envía la petición, registra el resultado en el log y devuelve la respuesta."""
        url = f"{self.url_base}/{endpoint.lstrip('/')}"
        if "json" in kwargs:
            logger.info("%s %s | cuerpo: %s", metodo, url, json.dumps(kwargs["json"], ensure_ascii=False))
        else:
            logger.info("%s %s", metodo, url)

        respuesta = self.sesion.request(metodo, url, timeout=TIEMPO_ESPERA_API, **kwargs)

        logger.info(
            "Respuesta: %s en %.0f ms | %s",
            respuesta.status_code,
            respuesta.elapsed.total_seconds() * 1000,
            respuesta.text[:300].replace("\n", " "),
        )
        return respuesta

    def get(self, endpoint, params=None):
        return self._enviar("GET", endpoint, params=params)

    def post(self, endpoint, cuerpo):
        return self._enviar("POST", endpoint, json=cuerpo)

    def put(self, endpoint, cuerpo):
        return self._enviar("PUT", endpoint, json=cuerpo)

    def delete(self, endpoint):
        return self._enviar("DELETE", endpoint)

    def cerrar(self):
        """Cierra la sesión HTTP."""
        self.sesion.close()


def validar_estructura(objeto, esquema):
    """Verifica que el objeto JSON tenga todos los campos del esquema con el tipo esperado.

    esquema es un diccionario {campo: tipo}, por ejemplo {"id": int, "title": str}.
    Devuelve la lista de problemas encontrados (vacía si la estructura es correcta),
    para que el assert muestre exactamente qué campo falló.
    """
    problemas = []
    for campo, tipo in esquema.items():
        if campo not in objeto:
            problemas.append(f"falta el campo '{campo}'")
        elif not isinstance(objeto[campo], tipo):
            problemas.append(
                f"'{campo}' debería ser {tipo.__name__} y es {type(objeto[campo]).__name__}"
            )
    return problemas
