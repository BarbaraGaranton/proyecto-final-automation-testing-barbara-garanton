"""Pruebas de API con peticiones encadenadas: cada paso usa datos de la respuesta anterior."""

import logging

import pytest

from utils.api_client import validar_estructura

pytestmark = pytest.mark.api

logger = logging.getLogger(__name__)

ESQUEMA_USUARIO = {"id": int, "name": str, "username": str, "email": str, "address": dict}
ESQUEMA_COMENTARIO = {"postId": int, "id": int, "name": str, "email": str, "body": str}


# API-10: post -> autor del post -> comentarios del post
def test_flujo_post_autor_y_comentarios(api):
    # Paso 1: obtiene un post y guarda el id de su autor
    post = api.get("/posts/5").json()
    id_autor = post["userId"]
    logger.info("El post %s pertenece al usuario %s", post["id"], id_autor)

    # Paso 2: con ese id obtiene los datos del autor
    respuesta_autor = api.get(f"/users/{id_autor}")
    assert respuesta_autor.status_code == 200
    autor = respuesta_autor.json()
    assert validar_estructura(autor, ESQUEMA_USUARIO) == []
    assert autor["id"] == id_autor
    assert "@" in autor["email"]

    # Paso 3: obtiene los comentarios del post y verifica que todos le pertenezcan
    respuesta_comentarios = api.get(f"/posts/{post['id']}/comments")
    assert respuesta_comentarios.status_code == 200
    comentarios = respuesta_comentarios.json()
    assert len(comentarios) > 0
    for comentario in comentarios:
        assert validar_estructura(comentario, ESQUEMA_COMENTARIO) == []
        assert comentario["postId"] == post["id"]


# API-11: busca un usuario -> crea un post a su nombre -> elimina uno de sus posts
def test_flujo_usuario_crear_y_eliminar_post(api):
    # Paso 1: busca al usuario por su username y guarda su id
    respuesta_usuario = api.get("/users", params={"username": "Bret"})
    assert respuesta_usuario.status_code == 200
    usuarios = respuesta_usuario.json()
    assert len(usuarios) == 1
    id_usuario = usuarios[0]["id"]
    logger.info("El usuario 'Bret' tiene id %s", id_usuario)

    # Paso 2: crea un post a nombre de ese usuario
    nuevo = {"title": "Post del flujo encadenado", "body": "Creado para Bret", "userId": id_usuario}
    respuesta_creacion = api.post("/posts", nuevo)
    assert respuesta_creacion.status_code == 201
    assert respuesta_creacion.json()["userId"] == id_usuario

    # Paso 3: lista los posts del usuario y elimina el primero
    # (JSONPlaceholder no guarda los posts nuevos, por eso se elimina uno existente)
    posts_usuario = api.get(f"/users/{id_usuario}/posts").json()
    assert len(posts_usuario) > 0
    assert all(post["userId"] == id_usuario for post in posts_usuario)

    respuesta_borrado = api.delete(f"/posts/{posts_usuario[0]['id']}")
    assert respuesta_borrado.status_code == 200
