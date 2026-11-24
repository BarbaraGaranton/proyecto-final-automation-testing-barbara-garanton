"""Page Object del catálogo de productos (inventario)."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Página principal luego del login, con la lista de productos."""

    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
    PRECIO_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
    BOTON_AGREGAR = (By.CSS_SELECTOR, "button.btn_inventory")
    FILTRO_ORDEN = (By.CLASS_NAME, "product_sort_container")

    def obtener_productos(self):
        """Devuelve la lista de tarjetas de producto visibles."""
        return self.espera.until(EC.visibility_of_all_elements_located(self.PRODUCTOS))

    @classmethod
    def obtener_nombre_y_precio(cls, producto):
        """Devuelve el nombre y el precio (como texto) de una tarjeta de producto."""
        nombre = producto.find_element(*cls.NOMBRE_PRODUCTO).text
        precio = producto.find_element(*cls.PRECIO_PRODUCTO).text
        return nombre, precio

    def obtener_nombres(self):
        """Devuelve los nombres de todos los productos, en el orden en que se ven.

        Primero espera a que los productos estén visibles: si se leyera la lista
        antes de que cargue, volvería vacía y el test podría pasar sin validar nada.
        """
        self.obtener_productos()
        return [elemento.text for elemento in self.driver.find_elements(*self.NOMBRE_PRODUCTO)]

    def obtener_precios(self):
        """Devuelve los precios del catálogo como números, en el orden en que se ven."""
        self.obtener_productos()
        precios = self.driver.find_elements(*self.PRECIO_PRODUCTO)
        return [float(precio.text.replace("$", "")) for precio in precios]

    def agregar_producto_por_nombre(self, nombre):
        """Agrega al carrito el producto con el nombre indicado."""
        for producto in self.obtener_productos():
            nombre_actual, _ = self.obtener_nombre_y_precio(producto)
            if nombre_actual == nombre:
                logger.info("Agregando al carrito el producto '%s'", nombre)
                producto.find_element(*self.BOTON_AGREGAR).click()
                return nombre
        raise ValueError(f"No se encontró el producto '{nombre}' en el catálogo")

    def agregar_primer_producto(self):
        """Agrega al carrito el primer producto del catálogo y devuelve su nombre."""
        primer_producto = self.obtener_productos()[0]
        nombre, _ = self.obtener_nombre_y_precio(primer_producto)
        logger.info("Agregando al carrito el producto '%s'", nombre)
        primer_producto.find_element(*self.BOTON_AGREGAR).click()
        return nombre

    def ordenar_por(self, opcion):
        """Ordena el catálogo con el filtro. Opciones: 'az', 'za', 'lohi', 'hilo'."""
        logger.info("Ordenando los productos con la opción '%s'", opcion)
        Select(self.esperar_visible(self.FILTRO_ORDEN)).select_by_value(opcion)

    def obtener_imagenes(self):
        """Devuelve el nombre de archivo de la imagen de cada producto."""
        imagenes = self.driver.find_elements(By.CSS_SELECTOR, "img.inventory_item_img")
        return [imagen.get_attribute("src").split("/")[-1] for imagen in imagenes]

    def elementos_principales_visibles(self):
        """Devuelve True si se ven el menú, el filtro de orden y el carrito."""
        return all(
            self.esta_visible(localizador)
            for localizador in (self.BOTON_MENU, self.FILTRO_ORDEN, self.ICONO_CARRITO)
        )
