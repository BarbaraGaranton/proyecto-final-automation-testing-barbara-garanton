"""Pruebas de API sobre el recurso /posts de JSONPlaceholder.

JSONPlaceholder es una API pública de práctica: acepta POST, PUT y DELETE y
responde como si los guardara, pero no persiste los cambios.
"""

import pytest

from utils.api_client import validar_estructura
from utils.data_loader import generar_ids, leer_json

pytestmark = pytest.mark.api

# Estructura esperada de un post
ESQUEMA_POST = {"userId": int, "id": int, "title": str, "body": str}

CASOS_POST = leer_json("api_posts.json")


# API-01: GET de un post existente
@pytest.mark.smoke
def test_obtener_post_existente(api):
    respuesta = api.get("/posts/1")

    assert respuesta.status_code == 200
    assert "application/json" in respuesta.headers["Content-Type"]

    post = respuesta.json()
    assert validar_estructura(post, ESQUEMA_POST) == []
    assert post["id"] == 1
    assert post["title"].strip() != ""


# API-02: GET de una lista filtrada por parámetro
def test_listar_posts_de_un_usuario(api):
    respuesta = api.get("/posts", params={"userId": 1})

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert isinstance(posts, list)
    assert len(posts) == 10
    assert all(post["userId"] == 1 for post in posts)
    for post in posts:
        assert validar_estructura(post, ESQUEMA_POST) == []


# API-03: GET de un post que no existe (negativo)
def test_obtener_post_inexistente(api):
    respuesta = api.get("/posts/99999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {}


# API-04 a API-06: POST para crear posts con distintos datos (data/api_posts.json)
@pytest.mark.parametrize("caso", CASOS_POST, ids=generar_ids(CASOS_POST))
def test_crear_post(api, caso):
    respuesta = api.post("/posts", caso["cuerpo"])

    assert respuesta.status_code == 201
    creado = respuesta.json()
    assert validar_estructura(creado, ESQUEMA_POST) == []
    # La API devuelve lo enviado más el id asignado al nuevo recurso
    for campo, valor in caso["cuerpo"].items():
        assert creado[campo] == valor
    assert creado["id"] > 0


# API-07: PUT para actualizar un post
def test_actualizar_post(api):
    cambios = {"id": 1, "userId": 1, "title": "Título actualizado", "body": "Cuerpo actualizado"}

    respuesta = api.put("/posts/1", cambios)

    assert respuesta.status_code == 200
    assert respuesta.json() == cambios


# API-08: DELETE de un post
@pytest.mark.smoke
def test_eliminar_post(api):
    respuesta = api.delete("/posts/1")

    assert respuesta.status_code == 200
    assert respuesta.json() == {}


# API-09: ruta inexistente (negativo)
def test_endpoint_inexistente(api):
    respuesta = api.get("/ruta-que-no-existe")

    assert respuesta.status_code == 404
