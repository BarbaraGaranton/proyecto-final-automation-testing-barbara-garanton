# Pre-Entrega - Automation Testing (SauceDemo)

¡Hola! Soy Barbara Garanton y este es mi proyecto de pre-entrega del curso de
QA Automation de Talento Tech.

## Propósito

En este proyecto automaticé los flujos principales de
[saucedemo.com](https://www.saucedemo.com), un sitio de práctica para testing.
Mi objetivo fue poner en práctica lo que aprendí hasta la clase 8: ubicar
elementos en una página, interactuar con ellos y validar que el sitio responda
como se espera.

Probé el login, el catálogo de productos y el carrito de compras, que eran los
flujos obligatorios, y además sumé algunos casos por mi cuenta, como el checkout
y los logins que deberían fallar.

## Tecnologías que usé

- **Python** como lenguaje principal
- **Pytest** para organizar y ejecutar los tests
- **Selenium WebDriver** para manejar el navegador (Google Chrome)
- **pytest-html** para generar el reporte HTML
- **Git y GitHub** para el control de versiones

## Cómo organicé el proyecto

```
pre-entrega-final/
├── tests/
│   └── test_saucedemo.py      # Mis casos de prueba
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

Separé los tests de las funciones auxiliares para no repetir el mismo código de
login en cada prueba. Así los tests quedan cortos y se entiende rápido qué valida
cada uno.

## Casos de prueba

Diseñé 10 casos de prueba pensando como QA: no alcanza con probar que todo
funciona cuando el usuario hace las cosas bien (casos positivos), también hay
que comprobar que el sitio responda correctamente cuando algo sale mal (casos
negativos). Por eso, además del login exitoso, probé qué pasa con una contraseña
incorrecta, con un usuario bloqueado y con los campos vacíos.

Criterios que seguí:

- **Un resultado esperado claro por caso.** Cada test tiene validaciones
  (`assert`) específicas; ninguno se da por bueno solo porque "no dio error".
- **Tests independientes.** Cada uno abre y cierra su propio navegador, así que
  si uno falla los demás se ejecutan igual.
- **Evidencia.** Cada ejecución deja un reporte, un log y capturas de los fallos.

Precondición general: el sitio está disponible y, salvo en los casos de login,
la sesión se inicia con `standard_user` / `secret_sauce`.

| ID | Test | Tipo | Pasos principales | Resultado esperado |
|----|------|------|-------------------|--------------------|
| CP-01 | `test_login` | Positivo | Ingresar usuario y contraseña válidos y hacer clic en Login | Redirige a `/inventory.html`, con título "Swag Labs" y sección "Products" |
| CP-02 | `test_login_password_incorrecta` | Negativo | Ingresar usuario válido con contraseña incorrecta | Muestra el error "Username and password do not match..." y no entra al inventario |
| CP-03 | `test_login_usuario_bloqueado` | Negativo | Ingresar con `locked_out_user` | Muestra el error "this user has been locked out" y no entra al inventario |
| CP-04 | `test_login_campos_vacios` | Negativo | Hacer clic en Login sin completar los campos | Muestra el error "Username is required" |
| CP-05 | `test_logout` | Positivo | Abrir el menú y hacer clic en Logout | Vuelve a la página de login |
| CP-06 | `test_catalogo` | Positivo | Entrar al inventario y revisar la página | Título "Products", hay productos visibles, el primero tiene nombre y precio, y están el menú, el filtro y el carrito |
| CP-07 | `test_ordenar_por_precio` | Positivo | Elegir en el filtro "precio de menor a mayor" | Los precios quedan ordenados de menor a mayor |
| CP-08 | `test_agregar_producto_carrito` | Positivo | Agregar el primer producto y entrar al carrito | El contador pasa a 1 y el producto aparece en el carrito |
| CP-09 | `test_quitar_producto_carrito` | Positivo | Agregar un producto, entrar al carrito y quitarlo | El carrito queda vacío y desaparece el contador |
| CP-10 | `test_checkout` | Positivo | Agregar un producto, completar el formulario, continuar y finalizar | El resumen muestra el producto y aparece "Thank you for your order!" |

Resultado de la última ejecución: **10 de 10 casos aprobados** (ver
`reports/reporte.html`).

## Lo que más me costó: el checkout

El checkout fue la parte que más se me complicó. El test llegaba al formulario y
completaba los datos, pero al hacer clic en `Continue` la página no avanzaba al
resumen de compra: la URL seguía siendo `checkout-step-one.html`. Lo confuso es
que en un momento el test figuraba como `PASSED`, pero solo porque no tenía
ninguna validación que comprobara que realmente había avanzado.

El problema no estaba en el sitio sino en el navegador: Chrome mostraba su aviso
de "contraseña filtrada" (porque `secret_sauce` es una clave pública) y esa
ventana tapaba la página y bloqueaba los clics. Lo resolví desactivando el gestor
de contraseñas de Chrome en las opciones del navegador, dentro de
`utils/selenium_helpers.py`.

De esto me llevo dos aprendizajes:

- Que un test diga `PASSED` no significa que la funcionalidad ande bien. Si no
  hay una validación clara, el resultado no dice nada.
- Cuando algo falla, conviene mirar también el entorno (el navegador, en este
  caso) y no solo el código del test.

## Instalación de dependencias

Requisitos previos: tener instalados Python 3 y Google Chrome.

```bash
git clone https://github.com/BarbaraGaranton/pre-entrega-automation-testing-barbara-garanton.git
cd pre-entrega-automation-testing-barbara-garanton
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En Linux o Mac el entorno virtual se activa con `source .venv/bin/activate`.

## Cómo ejecutar las pruebas

Para ejecutar todos los tests:

```bash
pytest -v
```

Para ejecutarlos y generar el reporte HTML:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Para ejecutar un solo test:

```bash
pytest -v tests/test_saucedemo.py::test_login
```

## Reportes y evidencias

- **Reporte HTML:** queda en `reports/reporte.html`.
- **Logs de ejecución:** se ven en la consola y se guardan en `reports/ejecucion.log`.
- **Capturas de pantalla:** si un test falla, se guarda sola una captura en
  `reports/capturas/` y también se adjunta al reporte HTML.

## Autora

Barbara Garanton
