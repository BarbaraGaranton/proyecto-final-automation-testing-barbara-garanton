"""Page Object de la página de login de SauceDemo."""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import PASSWORD_VALIDO, URL_BASE, USUARIO_VALIDO

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Pantalla inicial donde el usuario ingresa sus credenciales."""

    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def abrir(self):
        """Abre la página de login."""
        logger.info("Abriendo %s", URL_BASE)
        self.driver.get(URL_BASE)
        return self

    def iniciar_sesion(self, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
        """Completa el formulario y hace clic en Login."""
        logger.info("Iniciando sesión con el usuario '%s'", usuario)
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_PASSWORD, password)
        self.hacer_clic(self.BOTON_LOGIN)

    def iniciar_sesion_valida(self):
        """Inicia sesión con el usuario estándar y devuelve la página de inventario."""
        from pages.inventory_page import InventoryPage  # import local para evitar ciclos

        self.abrir()
        self.iniciar_sesion()
        self.esperar_url("/inventory.html")
        return InventoryPage(self.driver)

    def obtener_mensaje_error(self):
        """Devuelve el mensaje de error que muestra el formulario."""
        mensaje = self.esperar_visible(self.MENSAJE_ERROR).text
        logger.info("Mensaje de error mostrado: %s", mensaje)
        return mensaje

    def esta_en_login(self):
        """Devuelve True si se está viendo la página de login."""
        return self.esta_visible(self.BOTON_LOGIN) and self.driver.current_url == URL_BASE
