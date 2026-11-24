"""Creación del navegador que usan las pruebas de UI."""

import logging

from selenium import webdriver

from utils.config import HEADLESS

logger = logging.getLogger(__name__)


def crear_driver():
    """Inicia Chrome con las opciones necesarias para que las pruebas sean estables."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--incognito")
    opciones.add_argument("--window-size=1920,1080")

    if HEADLESS:
        # Modo sin ventana para servidores de integración continua
        opciones.add_argument("--headless=new")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
    else:
        opciones.add_argument("--start-maximized")

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
    logger.info("Iniciando el navegador Chrome (headless=%s)", HEADLESS)
    try:
        return webdriver.Chrome(options=opciones)
    except Exception as error:
        # Si la PC está muy cargada Chrome puede tardar demasiado en abrir:
        # se reintenta una vez antes de dar el test por fallido
        logger.warning("Chrome no pudo iniciar (%s). Reintentando una vez...", type(error).__name__)
        return webdriver.Chrome(options=opciones)
