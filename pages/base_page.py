"""Clase base con las acciones comunes a todas las páginas."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import TIEMPO_ESPERA

logger = logging.getLogger(__name__)


class BasePage:
    """Agrupa las esperas y acciones que reutilizan todas las páginas.

    Las páginas concretas heredan de esta clase y solo definen sus
    localizadores y las acciones propias de cada pantalla.
    """

    # Elementos que se repiten en todas las páginas internas del sitio
    TITULO_SECCION = (By.CLASS_NAME, "title")
    ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    LINK_LOGOUT = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, TIEMPO_ESPERA)

    # ----- Esperas y acciones genéricas -----

    def esperar_visible(self, localizador):
        """Espera a que el elemento sea visible y lo devuelve."""
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def esta_visible(self, localizador):
        """Devuelve True si el elemento llega a ser visible dentro del tiempo de espera."""
        try:
            return self.esperar_visible(localizador).is_displayed()
        except Exception:
            return False

    def hacer_clic(self, localizador):
        """Espera a que el elemento se pueda clickear y hace clic."""
        logger.info("Clic en el elemento %s", localizador)
        self.espera.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        """Espera a que el campo sea visible, lo limpia y escribe el texto."""
        campo = self.esperar_visible(localizador)
        campo.clear()
        campo.send_keys(texto)

    def esperar_url(self, fragmento):
        """Espera a que la URL actual contenga el fragmento indicado."""
        self.espera.until(EC.url_contains(fragmento))
        logger.info("URL actual: %s", self.driver.current_url)

    def cantidad_elementos(self, localizador):
        """Cuenta cuántos elementos hay en la página con ese localizador (sin esperar)."""
        return len(self.driver.find_elements(*localizador))

    # ----- Acciones del encabezado, comunes a las páginas internas -----

    def obtener_titulo_seccion(self):
        """Devuelve el título de la sección actual (por ejemplo 'Products')."""
        return self.esperar_visible(self.TITULO_SECCION).text

    def obtener_contador_carrito(self):
        """Devuelve el número que muestra el ícono del carrito (0 si no hay contador)."""
        if self.cantidad_elementos(self.CONTADOR_CARRITO) == 0:
            return 0
        return int(self.esperar_visible(self.CONTADOR_CARRITO).text)

    def ir_al_carrito(self):
        """Entra al carrito desde el ícono del encabezado y devuelve su Page Object."""
        from pages.cart_page import CartPage  # import local para evitar ciclos

        self.hacer_clic(self.ICONO_CARRITO)
        self.esperar_url("/cart.html")
        return CartPage(self.driver)

    def cerrar_sesion(self):
        """Abre el menú lateral, hace clic en Logout y devuelve la página de login."""
        from pages.login_page import LoginPage  # import local para evitar ciclos

        logger.info("Cerrando la sesión desde el menú")
        self.hacer_clic(self.BOTON_MENU)
        self.hacer_clic(self.LINK_LOGOUT)
        return LoginPage(self.driver)
