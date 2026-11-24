"""Page Objects de los tres pasos del checkout."""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutInfoPage(BasePage):
    """Paso 1: formulario con los datos del comprador."""

    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def completar_datos(self, nombre, apellido, codigo_postal):
        """Completa el formulario con los datos del comprador."""
        logger.info("Completando datos: '%s' '%s' '%s'", nombre, apellido, codigo_postal)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)

    def continuar(self):
        """Hace clic en Continue (no espera cambio de página, por si hay un error)."""
        self.hacer_clic(self.BOTON_CONTINUAR)

    def continuar_al_resumen(self):
        """Hace clic en Continue y devuelve la página de resumen de compra."""
        self.continuar()
        self.esperar_url("/checkout-step-two.html")
        return CheckoutOverviewPage(self.driver)

    def obtener_mensaje_error(self):
        """Devuelve el mensaje de error del formulario."""
        mensaje = self.esperar_visible(self.MENSAJE_ERROR).text
        logger.info("Mensaje de error mostrado: %s", mensaje)
        return mensaje


class CheckoutOverviewPage(BasePage):
    """Paso 2: resumen de la compra antes de confirmarla."""

    NOMBRE_ITEM = (By.CLASS_NAME, "inventory_item_name")
    BOTON_FINALIZAR = (By.ID, "finish")

    def obtener_nombres_productos(self):
        """Devuelve los nombres de los productos del resumen."""
        self.esperar_visible(self.NOMBRE_ITEM)
        return [elemento.text for elemento in self.driver.find_elements(*self.NOMBRE_ITEM)]

    def finalizar_compra(self):
        """Hace clic en Finish y devuelve la página de confirmación."""
        self.hacer_clic(self.BOTON_FINALIZAR)
        self.esperar_url("/checkout-complete.html")
        return CheckoutCompletePage(self.driver)


class CheckoutCompletePage(BasePage):
    """Paso 3: confirmación de la compra."""

    MENSAJE_CONFIRMACION = (By.CLASS_NAME, "complete-header")

    def obtener_mensaje_confirmacion(self):
        """Devuelve el texto de confirmación de la compra."""
        return self.esperar_visible(self.MENSAJE_CONFIRMACION).text
