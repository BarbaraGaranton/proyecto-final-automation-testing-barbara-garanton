"""Casos de prueba automatizados para https://www.saucedemo.com/"""

import logging

from selenium.webdriver.common.by import By

from utils.selenium_helpers import (
    agregar_primer_producto_al_carrito,
    escribir,
    esperar_url,
    esperar_visible,
    hacer_clic,
    iniciar_sesion,
    ir_al_carrito,
    obtener_nombre_y_precio,
    obtener_productos,
    obtener_titulo_seccion,
)

logger = logging.getLogger(__name__)


# TEST DE LOGIN
def test_login(driver):
    # Ingresa usuario y contraseña válidos y hace clic en Login
    iniciar_sesion(driver)

    # Verifica que se llegue al inventario
    esperar_url(driver, "/inventory.html")
    assert "/inventory.html" in driver.current_url

    # Valida el título de la pestaña y el de la sección
    assert driver.title == "Swag Labs"
    assert obtener_titulo_seccion(driver) == "Products"


# TEST DE NAVEGACION AL CATALOGO DE PRODUCTOS
def test_catalogo(driver):
    iniciar_sesion(driver)
    esperar_url(driver, "/inventory.html")

    # Valida que el título sea "Products"
    assert obtener_titulo_seccion(driver) == "Products"

    # Valida que haya productos visibles
    productos = obtener_productos(driver)
    assert len(productos) > 0, "No se encontraron productos en el inventario"

    # Lista el nombre y el precio del primer producto
    nombre, precio = obtener_nombre_y_precio(productos[0])
    logger.info("Primer producto: %s - Precio: %s", nombre, precio)
    assert nombre != ""
    assert precio.startswith("$")

    # Valida elementos importantes de la interfaz: menú, filtro y carrito
    assert esperar_visible(driver, (By.ID, "react-burger-menu-btn")).is_displayed()
    assert esperar_visible(driver, (By.CLASS_NAME, "product_sort_container")).is_displayed()
    assert esperar_visible(driver, (By.CLASS_NAME, "shopping_cart_link")).is_displayed()


# TEST DE AGREGAR PRODUCTO AL CARRITO
def test_agregar_producto_carrito(driver):
    iniciar_sesion(driver)
    esperar_url(driver, "/inventory.html")

    # Agrega el primer producto al carrito
    nombre_agregado = agregar_primer_producto_al_carrito(driver)

    # Verifica que el contador del carrito pase a 1
    contador = esperar_visible(driver, (By.CLASS_NAME, "shopping_cart_badge"))
    assert contador.text == "1"

    # Entra al carrito
    ir_al_carrito(driver)

    # Verifica que el producto agregado esté en el carrito
    producto_en_carrito = esperar_visible(driver, (By.CLASS_NAME, "inventory_item_name"))
    assert producto_en_carrito.text == nombre_agregado


# TEST DE CHECKOUT (adicional a lo obligatorio)
def test_checkout(driver):
    iniciar_sesion(driver)
    esperar_url(driver, "/inventory.html")

    nombre_agregado = agregar_primer_producto_al_carrito(driver)
    ir_al_carrito(driver)

    # Abre el formulario de checkout
    hacer_clic(driver, (By.ID, "checkout"))
    esperar_url(driver, "/checkout-step-one.html")

    # Completa los datos del comprador
    escribir(driver, (By.ID, "first-name"), "John")
    escribir(driver, (By.ID, "last-name"), "Doe")
    escribir(driver, (By.ID, "postal-code"), "12345")

    # Continúa y verifica que se llegue al resumen de compra
    hacer_clic(driver, (By.ID, "continue"))
    esperar_url(driver, "/checkout-step-two.html")
    assert obtener_titulo_seccion(driver) == "Checkout: Overview"

    # Verifica que el resumen muestre el producto agregado
    producto_en_resumen = esperar_visible(driver, (By.CLASS_NAME, "inventory_item_name"))
    assert producto_en_resumen.text == nombre_agregado

    # Finaliza la compra y valida el mensaje de confirmación
    hacer_clic(driver, (By.ID, "finish"))
    esperar_url(driver, "/checkout-complete.html")
    mensaje = esperar_visible(driver, (By.CLASS_NAME, "complete-header"))
    assert mensaje.text == "Thank you for your order!"
