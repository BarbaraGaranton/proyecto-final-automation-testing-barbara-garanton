"""Page Object del carrito de compras."""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Página que lista los productos agregados al carrito."""

    ITEMS_CARRITO = (By.CLASS_NAME, "cart_item")
    NOMBRE_ITEM = (By.CLASS_NAME, "inventory_item_name")
    BOTON_QUITAR = (By.CSS_SELECTOR, "button.cart_button")
    BOTON_CHECKOUT = (By.ID, "checkout")

    def obtener_nombres_productos(self):
        """Devuelve los nombres de los productos que hay en el carrito."""
        return [elemento.text for elemento in self.driver.find_elements(*self.NOMBRE_ITEM)]

    def cantidad_productos(self):
        """Devuelve cuántos productos hay en el carrito."""
        return self.cantidad_elementos(self.ITEMS_CARRITO)

    def quitar_primer_producto(self):
        """Quita del carrito el primer producto de la lista."""
        logger.info("Quitando el primer producto del carrito")
        self.hacer_clic(self.BOTON_QUITAR)

    def ir_al_checkout(self):
        """Hace clic en Checkout y devuelve la página del formulario de compra."""
        from pages.checkout_page import CheckoutInfoPage  # import local para evitar ciclos

        self.hacer_clic(self.BOTON_CHECKOUT)
        self.esperar_url("/checkout-step-one.html")
        return CheckoutInfoPage(self.driver)
