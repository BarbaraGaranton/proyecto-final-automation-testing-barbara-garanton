"""Funciones auxiliares reutilizables para los tests de SauceDemo."""

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Datos del sitio bajo prueba
URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"

# Tiempo máximo (en segundos) de las esperas explícitas
TIEMPO_ESPERA = 10

logger = logging.getLogger(__name__)


def crear_driver():
    """Inicia Chrome con las opciones necesarias para que las pruebas sean estables."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--incognito")
    # Desactiva el gestor de contraseñas de Chrome: su aviso de
    # "contraseña filtrada" tapa la página y bloquea los clics
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    logger.info("Iniciando el navegador Chrome")
    return webdriver.Chrome(options=opciones)


def crear_espera(driver, segundos=TIEMPO_ESPERA):
    """Devuelve una espera explícita para el driver recibido."""
    return WebDriverWait(driver, segundos)


def esperar_visible(driver, localizador):
    """Espera a que el elemento sea visible y lo devuelve."""
    return crear_espera(driver).until(EC.visibility_of_element_located(localizador))


def hacer_clic(driver, localizador):
    """Espera a que el elemento se pueda clickear y hace clic."""
    logger.info("Clic en el elemento %s", localizador)
    crear_espera(driver).until(EC.element_to_be_clickable(localizador)).click()


def escribir(driver, localizador, texto):
    """Espera a que el campo sea visible y escribe el texto."""
    campo = esperar_visible(driver, localizador)
    campo.clear()
    campo.send_keys(texto)


def iniciar_sesion(driver, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
    """Abre SauceDemo y completa el formulario de login."""
    logger.info("Abriendo %s", URL_BASE)
    driver.get(URL_BASE)

    logger.info("Iniciando sesión con el usuario '%s'", usuario)
    escribir(driver, (By.ID, "user-name"), usuario)
    escribir(driver, (By.ID, "password"), password)
    hacer_clic(driver, (By.ID, "login-button"))


def esperar_url(driver, fragmento):
    """Espera a que la URL actual contenga el fragmento indicado."""
    crear_espera(driver).until(EC.url_contains(fragmento))
    logger.info("URL actual: %s", driver.current_url)


def obtener_titulo_seccion(driver):
    """Devuelve el título de la sección actual (por ejemplo 'Products')."""
    return esperar_visible(driver, (By.CLASS_NAME, "title")).text


def obtener_productos(driver):
    """Devuelve la lista de tarjetas de producto visibles en el inventario."""
    return crear_espera(driver).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )


def obtener_nombre_y_precio(producto):
    """Devuelve el nombre y el precio de una tarjeta de producto."""
    nombre = producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    return nombre, precio


def agregar_primer_producto_al_carrito(driver):
    """Agrega al carrito el primer producto del inventario y devuelve su nombre."""
    primer_producto = obtener_productos(driver)[0]
    nombre, _ = obtener_nombre_y_precio(primer_producto)

    logger.info("Agregando al carrito el producto '%s'", nombre)
    primer_producto.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
    return nombre


def ir_al_carrito(driver):
    """Entra al carrito de compras desde el ícono del encabezado."""
    hacer_clic(driver, (By.CLASS_NAME, "shopping_cart_link"))
    esperar_url(driver, "/cart.html")


def obtener_mensaje_error(driver):
    """Devuelve el mensaje de error que muestra el formulario de login."""
    mensaje = esperar_visible(driver, (By.CSS_SELECTOR, "[data-test='error']")).text
    logger.info("Mensaje de error mostrado: %s", mensaje)
    return mensaje


def ordenar_productos(driver, opcion):
    """Ordena el catálogo con el filtro. Opciones: 'az', 'za', 'lohi', 'hilo'."""
    logger.info("Ordenando los productos con la opción '%s'", opcion)
    filtro = esperar_visible(driver, (By.CLASS_NAME, "product_sort_container"))
    Select(filtro).select_by_value(opcion)


def obtener_precios(driver):
    """Devuelve los precios del catálogo como números, en el orden en que se ven."""
    precios = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    return [float(precio.text.replace("$", "")) for precio in precios]


def cerrar_sesion(driver):
    """Abre el menú lateral y hace clic en Logout."""
    logger.info("Cerrando la sesión desde el menú")
    hacer_clic(driver, (By.ID, "react-burger-menu-btn"))
    hacer_clic(driver, (By.ID, "logout_sidebar_link"))
