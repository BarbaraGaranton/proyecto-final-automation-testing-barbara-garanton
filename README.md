# Pre-Entrega - Automation Testing (SauceDemo)

Proyecto de pre-entrega del curso de QA Automation de Talento Tech.

## Propósito

Automatizar los flujos básicos de navegación del sitio de práctica
[saucedemo.com](https://www.saucedemo.com) y validar que funcionen correctamente:
login, catálogo de productos y carrito de compras.

## Tecnologías utilizadas

- **Python** como lenguaje principal
- **Pytest** para la estructura y ejecución de los tests
- **Selenium WebDriver** para automatizar el navegador (Google Chrome)
- **pytest-html** para generar el reporte HTML
- **Git y GitHub** para el control de versiones

## Estructura del proyecto

```
pre-entrega-final/
├── tests/
│   └── test_saucedemo.py      # Casos de prueba
├── utils/
│   └── selenium_helpers.py    # Funciones auxiliares (login, esperas, carrito)
├── reports/
│   ├── reporte.html           # Reporte HTML de la última ejecución
│   ├── ejecucion.log          # Log de la última ejecución
│   └── capturas/              # Capturas automáticas de los tests que fallan
├── conftest.py                # Fixture del navegador y captura en fallos
├── pytest.ini                 # Configuración de Pytest y de los logs
├── requirements.txt           # Dependencias
└── README.md
```

## Casos de prueba

| Test | Qué valida |
|------|------------|
| `test_login` | Login con `standard_user` / `secret_sauce`, redirección a `/inventory.html`, título "Swag Labs" y sección "Products" |
| `test_catalogo` | Título del inventario, presencia de productos, nombre y precio del primer producto, y elementos de la interfaz (menú, filtro, carrito) |
| `test_agregar_producto_carrito` | Agrega el primer producto, verifica el contador del carrito y que el producto aparezca dentro del carrito |
| `test_checkout` (adicional) | Completa el formulario de compra, verifica el resumen y el mensaje de compra finalizada |

Cada test abre y cierra su propio navegador, por lo que son independientes entre sí.

## Instalación de dependencias

Requisitos previos: Python 3 y Google Chrome instalados.

```bash
git clone https://github.com/BarbaraGaranton/pre-entrega-automation-testing-barbara-garanton.git
cd pre-entrega-automation-testing-barbara-garanton
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En Linux o Mac el entorno virtual se activa con `source .venv/bin/activate`.

## Cómo ejecutar las pruebas

Ejecutar todos los tests:

```bash
pytest -v
```

Ejecutar los tests y generar el reporte HTML:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Ejecutar un solo test:

```bash
pytest -v tests/test_saucedemo.py::test_login
```

## Reportes y evidencias

- **Reporte HTML:** `reports/reporte.html`
- **Logs de ejecución:** se muestran en la consola y se guardan en `reports/ejecucion.log`
- **Capturas de pantalla:** si un test falla, se guarda automáticamente una captura
  en `reports/capturas/` y se adjunta al reporte HTML

## Autora

Barbara Garanton
