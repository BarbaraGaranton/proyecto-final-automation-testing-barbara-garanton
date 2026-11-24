"""Configuración general del framework: URLs, credenciales de prueba y tiempos."""

import os

# Sitio bajo prueba (UI)
URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"

# API bajo prueba
URL_API = "https://jsonplaceholder.typicode.com"

# Tiempo máximo (en segundos) de las esperas explícitas y de las peticiones HTTP
TIEMPO_ESPERA = 10
TIEMPO_ESPERA_API = 15

# Si la variable de entorno HEADLESS vale "1", Chrome se abre sin ventana
# (así se ejecutan las pruebas en GitHub Actions)
HEADLESS = os.getenv("HEADLESS", "0") == "1"
