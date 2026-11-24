# Proyecto Final - Framework de Automatización de Pruebas

![Pruebas automatizadas](https://github.com/BarbaraGaranton/proyecto-final-automation-testing-barbara-garanton/actions/workflows/pruebas.yml/badge.svg)

¡Hola! Soy Barbara Garanton y este es mi Trabajo Final Integrador del curso de
QA Automation de Talento Tech.

## Propósito

Desarrollé un framework de automatización de pruebas en Python que combina todo
lo que aprendí en el curso:

- **Pruebas de UI** sobre [saucedemo.com](https://www.saucedemo.com) con Selenium
  WebDriver y el patrón **Page Object Model**.
- **Pruebas de API** sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com)
  con la biblioteca **Requests**.
- **Datos de prueba externos** (JSON y CSV) para ejecutar el mismo test con
  distintos conjuntos de datos.
- **Reportes HTML**, **logs** y **capturas de pantalla automáticas** cuando una
  prueba falla.
- **Integración continua** con GitHub Actions: las pruebas se ejecutan solas en
  cada push y los reportes quedan guardados como artefactos.

Este proyecto parte de mi pre-entrega (los 10 casos de SauceDemo) y la amplía:
reorganicé el código con Page Object Model, parametricé los tests con datos
externos, sumé las pruebas de API y configuré la ejecución en GitHub Actions.

## Tecnologías utilizadas

| Tecnología | Para qué la usé |
|------------|-----------------|
| **Python 3** | Lenguaje principal |
| **Pytest** | Framework de testing: fixtures, parametrización, marcadores |
| **Selenium WebDriver** | Automatizar el navegador (Google Chrome) |
| **Requests** | Enviar las peticiones HTTP de las pruebas de API |
| **pytest-html** | Generar el reporte HTML con las capturas incluidas |
| **logging** (módulo de Python) | Registrar los pasos clave de cada ejecución |
| **Git y GitHub** | Control de versiones, ramas por funcionalidad |
| **GitHub Actions** | Ejecutar las pruebas automáticamente en cada push |

## Estructura del proyecto

```
proyecto-final-automation-testing-barbara-garanton/
├── .github/workflows/
│   └── pruebas.yml            # Pipeline de GitHub Actions
├── data/                      # Datos de prueba externos
│   ├── login.json             # Usuarios válidos e inválidos para el login
│   ├── checkout.csv           # Datos del comprador (válidos y con campos vacíos)
│   ├── productos.json         # Productos a agregar al carrito
│   └── api_posts.json         # Cuerpos para crear posts en la API
├── pages/                     # Page Object Model (una clase por página)
│   ├── base_page.py           # Clase base: esperas, clics, escritura, encabezado
│   ├── login_page.py          # Página de login
│   ├── inventory_page.py      # Catálogo de productos
│   ├── cart_page.py           # Carrito de compras
│   └── checkout_page.py       # Los 3 pasos del checkout
├── tests/
│   ├── ui/                    # Pruebas de interfaz (Selenium)
│   │   ├── test_login.py
│   │   ├── test_inventario.py
│   │   ├── test_carrito.py
│   │   ├── test_checkout.py
│   │   ├── test_responsividad.py      # Desktop / Tablet / Móvil
│   │   └── test_defectos_conocidos.py # Bugs encontrados (xfail)
│   └── api/                   # Pruebas de API (Requests)
│       ├── conftest.py        # Fixture del cliente de API
│       ├── test_posts_api.py
│       └── test_encadenamiento_api.py
├── utils/
│   ├── config.py              # URLs, credenciales de prueba y tiempos de espera
│   ├── driver_factory.py      # Crea Chrome (normal o headless)
│   ├── api_client.py          # Cliente HTTP con logging y validación de estructura
│   └── data_loader.py         # Lee los archivos JSON y CSV de data/
├── reports/
│   ├── reporte.html           # Reporte HTML de la última ejecución
│   ├── ejecucion.log          # Log de la última ejecución
│   ├── capturas/              # Capturas automáticas de los tests que fallan
│   ├── evidencias/            # Capturas de cada test (con --evidencias)
│   └── responsividad/         # Capturas Desktop / Tablet / Móvil
├── docs/                      # Documento de entrega final (Word y PDF)
├── conftest.py                # Fixtures del navegador, capturas y hooks del reporte
├── pytest.ini                 # Configuración de Pytest, reporte, marcadores y logs
├── requirements.txt           # Dependencias con versiones fijas
└── README.md
```

### Cómo funciona el Page Object Model

Cada página del sitio tiene su propia clase en `pages/`, con sus **localizadores**
y **métodos que representan acciones** (`iniciar_sesion()`, `agregar_producto_por_nombre()`,
`ir_al_checkout()`, etc.). Los tests no tocan Selenium directamente: solo llaman
a esos métodos y hacen las validaciones.

Las acciones que se repiten en todas las páginas (esperas explícitas, clics,
escribir, ir al carrito, cerrar sesión) están en `BasePage`, de la que heredan las
demás. Además, los métodos que cambian de página devuelven el Page Object de la
página siguiente, así un flujo se lee casi como una frase:

```python
carrito = inventario.ir_al_carrito()
formulario = carrito.ir_al_checkout()
resumen = formulario.continuar_al_resumen()
confirmacion = resumen.finalizar_compra()
```

Si mañana cambia un botón del sitio, solo hay que corregir el localizador en su
Page Object y todos los tests siguen funcionando.

### Cómo agregar una prueba nueva

- **Nuevos datos para un test existente:** agregar una entrada en el JSON o una
  fila en el CSV de `data/`. No hace falta tocar código.
- **Nueva página:** crear una clase en `pages/` que herede de `BasePage`.
- **Nuevo test:** crear un archivo `test_*.py` en `tests/ui/` o `tests/api/` y usar
  las fixtures `login_page`, `inventario` o `api`.

## Casos de prueba

Total: **46 tests** (35 de UI y 11 de API). Cada caso parametrizado aparece en el
reporte con su propio nombre, por ejemplo `test_login[usuario_bloqueado]`.

El documento completo de la entrega (requerimientos, plan de pruebas, casos,
ejecución con evidencias, bugs y métricas) está en [`docs/`](docs/).

### Pruebas de UI - SauceDemo

| ID | Test | Datos | Tipo | Resultado esperado |
|----|------|-------|------|--------------------|
| CP-01 | `test_login[usuario_estandar]` | `login.json` | Positivo | Entra al inventario, título "Products" |
| CP-02 | `test_login[usuario_con_problemas]` | `login.json` | Positivo | Entra al inventario |
| CP-03 | `test_login[password_incorrecta]` | `login.json` | Negativo | Error "Username and password do not match..." |
| CP-04 | `test_login[usuario_inexistente]` | `login.json` | Negativo | Error "Username and password do not match..." |
| CP-05 | `test_login[usuario_bloqueado]` | `login.json` | Negativo | Error "this user has been locked out" |
| CP-06 | `test_login[campos_vacios]` | `login.json` | Negativo | Error "Username is required" |
| CP-07 | `test_login[password_vacia]` | `login.json` | Negativo | Error "Password is required" |
| CP-08 | `test_logout` | - | Positivo | Vuelve a la página de login |
| CP-09 | `test_catalogo` | - | Positivo | Hay productos con nombre y precio; se ven menú, filtro y carrito |
| CP-10 a CP-13 | `test_ordenar_catalogo[...]` | 4 opciones del filtro | Positivo | Nombres A-Z / Z-A y precios menor-mayor / mayor-menor quedan ordenados |
| CP-14 a CP-16 | `test_agregar_productos_carrito[...]` | `productos.json` | Positivo | El contador muestra la cantidad agregada y el carrito tiene esos productos |
| CP-17 | `test_quitar_producto_carrito` | - | Positivo | El carrito queda vacío y sin contador |
| CP-18 | `test_checkout[datos_completos]` | `checkout.csv` | Positivo (flujo completo) | Resumen con el producto y "Thank you for your order!" |
| CP-19 | `test_checkout[datos_completos_con_acentos]` | `checkout.csv` | Positivo (flujo completo) | Igual al anterior, con acentos en los datos |
| CP-20 | `test_checkout[falta_nombre]` | `checkout.csv` | Negativo | Error "First Name is required" y no avanza |
| CP-21 | `test_checkout[falta_apellido]` | `checkout.csv` | Negativo | Error "Last Name is required" y no avanza |
| CP-22 | `test_checkout[falta_codigo_postal]` | `checkout.csv` | Negativo | Error "Postal Code is required" y no avanza |
| CP-23 a CP-25 | `test_responsividad[...]` | Desktop 1920×1080, Tablet 768×1024, Móvil 390×844 | No funcional | Sin scroll horizontal y elementos clave visibles; guarda capturas en `reports/responsividad/` |
| CP-26 a CP-33 | `test_defectos_conocidos.py` | Usuarios especiales del sitio | Exploratorio | Imágenes, orden, carrito y checkout correctos → **XFail** por los bugs BUG-001 a BUG-006 y BUG-008 |
| CP-34 | `test_tiempo_de_login[standard_user]` | `standard_user` | No funcional | Login en 3 s o menos |
| CP-35 | `test_tiempo_de_login[performance_glitch_user]` | `performance_glitch_user` | No funcional | Login en 3 s o menos → **XFail** por BUG-007 |

### Defectos encontrados

Explorando el sitio con sus usuarios especiales (`problem_user`, `error_user`,
`visual_user` y `performance_glitch_user`) encontré 8 defectos reales: imágenes
incorrectas, filtro de orden roto, productos que no se agregan al carrito, un
campo del checkout que escribe en otro y un login lento.

Cada defecto quedó automatizado en `tests/ui/test_defectos_conocidos.py`. El test
verifica el comportamiento **correcto** y está marcado con `xfail` y el ID del bug.
Así el reporte lo muestra como *XFailed* (falla esperada y conocida) sin romper
el pipeline. Si un día el sitio corrige el defecto, el test aparece como
*XPassed* y se sabe que el bug se puede cerrar. El detalle de cada bug está en
el documento de `docs/`.

### Pruebas de API - JSONPlaceholder

| ID | Test | Método | Validaciones |
|----|------|--------|--------------|
| API-01 | `test_obtener_post_existente` | GET | Código 200, `Content-Type` JSON, estructura y tipos de los campos |
| API-02 | `test_listar_posts_de_un_usuario` | GET con parámetros | Código 200, 10 posts, todos del usuario pedido |
| API-03 | `test_obtener_post_inexistente` | GET | Código 404 y cuerpo vacío (negativo) |
| API-04 a API-06 | `test_crear_post[...]` | POST (`api_posts.json`) | Código 201, devuelve lo enviado y el `id` nuevo |
| API-07 | `test_actualizar_post` | PUT | Código 200 y cuerpo actualizado |
| API-08 | `test_eliminar_post` | DELETE | Código 200 y cuerpo vacío |
| API-09 | `test_endpoint_inexistente` | GET | Código 404 (negativo) |
| API-10 | `test_flujo_post_autor_y_comentarios` | GET encadenados | Post → su autor (con el `userId` recibido) → sus comentarios |
| API-11 | `test_flujo_usuario_crear_y_eliminar_post` | GET → POST → GET → DELETE | Busca un usuario, crea un post con su `id`, lista sus posts y borra uno |

> JSONPlaceholder es una API de práctica: responde a POST, PUT y DELETE como si
> guardara los cambios, pero no los persiste. Por eso en los flujos encadenados
> uso los datos devueltos en cada paso (como el `id` del usuario) para armar la
> petición siguiente, en lugar de volver a consultar el post recién creado.

### Criterios que seguí

- **Casos positivos y negativos:** no alcanza con probar que todo anda cuando se
  hace bien; también verifico que el sistema responda correctamente ante errores.
- **Tests independientes:** cada test de UI abre y cierra su propio navegador, y
  cada test de API usa su propio cliente. Si uno falla, los demás se ejecutan igual.
- **Validaciones claras:** ningún test se da por bueno solo porque "no dio error";
  todos tienen `assert` concretos.

## Instalación de dependencias

Requisitos previos: tener instalados **Python 3.10 o superior**, **Google Chrome**
y **Git**. No hace falta descargar el ChromeDriver: Selenium lo gestiona solo.

```bash
git clone https://github.com/BarbaraGaranton/proyecto-final-automation-testing-barbara-garanton.git
cd proyecto-final-automation-testing-barbara-garanton
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En Linux o Mac el entorno virtual se activa con `source .venv/bin/activate`.

## Cómo ejecutar las pruebas

Todas las pruebas (el reporte HTML y el log se generan solos):

```bash
pytest
```

Solo las pruebas de API o solo las de UI:

```bash
pytest -m api
pytest -m ui
```

Solo las pruebas rápidas de los flujos principales:

```bash
pytest -m smoke
```

Un archivo o un caso puntual:

```bash
pytest tests/ui/test_login.py
pytest "tests/ui/test_login.py::test_login[usuario_bloqueado]"
```

Sin los defectos conocidos (solo los flujos que deben pasar):

```bash
pytest -m "not defectos"
```

Guardando una captura de **cada** test de UI (no solo de los fallidos) en
`reports/evidencias/`, útil para documentar la ejecución:

```bash
pytest --evidencias
```

Sin abrir la ventana del navegador (modo headless, como en GitHub Actions):

```bash
# Windows (PowerShell)
$env:HEADLESS="1"; pytest
# Linux / Mac
HEADLESS=1 pytest
```

## Cómo interpretar los reportes

### Reporte HTML (`reports/reporte.html`)

Se genera en cada ejecución y se abre con cualquier navegador.

- **Resumen arriba:** cantidad de tests ejecutados, aprobados (*Passed*),
  fallados (*Failed*), fallas esperadas por defectos conocidos (*Expected
  failures* / XFailed), omitidos y la duración total. Se puede hacer clic en cada
  estado para filtrar la tabla.
- **Tabla de resultados:** una fila por test con su estado, nombre y duración.
  Los tests parametrizados muestran entre corchetes el caso de datos usado.
- **Detalle de cada test:** al hacer clic en una fila se despliega el log de ese
  test y, si falló, el error del `assert` (qué se esperaba y qué se obtuvo).
- **Capturas:** en los tests de UI que fallan, la captura de pantalla del momento
  del error aparece dentro del detalle del test.

### Log (`reports/ejecucion.log`)

Registra paso a paso cada ejecución con fecha, hora y nivel:

```
2026-11-24 16:51:39 [INFO] conftest: ========== INICIO: tests/ui/test_login.py::test_login[usuario_bloqueado] ==========
2026-11-24 16:51:44 [INFO] pages.login_page: Iniciando sesión con el usuario 'locked_out_user'
2026-11-24 16:51:45 [INFO] pages.login_page: Mensaje de error mostrado: Epic sadface: Sorry, this user has been locked out.
2026-11-24 16:51:45 [INFO] conftest: Resultado de test_login[usuario_bloqueado]: PASÓ (1.27 s)
2026-11-24 16:46:09 [INFO] utils.api_client: POST https://jsonplaceholder.typicode.com/posts | cuerpo: {"title": "Post del flujo encadenado", ...}
2026-11-24 16:46:09 [INFO] utils.api_client: Respuesta: 201 en 270 ms | {"title": "Post del flujo encadenado", ..., "id": 101}
```

Resultado de la última ejecución local: **33 de 33 tests aprobados**.

En las pruebas de API queda registrado el método, la URL, el cuerpo enviado, el
código de respuesta, el tiempo en milisegundos y el comienzo de la respuesta. Las
líneas `[ERROR]` marcan los tests fallidos y dónde se guardó su captura.

### Capturas de pantalla (`reports/capturas/`)

Cuando un test de UI falla se guarda automáticamente una captura con el nombre del
test y la fecha/hora, por ejemplo `test_checkout_falta_nombre_20261124_165012.png`.

### Reportes en GitHub Actions

En cada push el workflow `Pruebas automatizadas` ejecuta las pruebas de API y de UI
(Chrome en modo headless). Para ver los resultados: pestaña **Actions** del
repositorio → elegir la ejecución → sección **Artifacts** → descargar
`reportes-de-pruebas`, que contiene los reportes HTML, el log y las capturas.

## Control de versiones

Desarrollé cada funcionalidad en su propia rama y luego la fusioné con `main`:

| Rama | Contenido |
|------|-----------|
| `feature/page-object-model` | Clases de páginas y refactor de los tests de UI |
| `feature/datos-de-prueba` | Archivos JSON/CSV y parametrización |
| `feature/pruebas-api` | Cliente de API y pruebas con Requests |
| `feature/ci-reportes` | GitHub Actions, reportes y documentación |
| `feature/evidencias-y-defectos` | Defectos encontrados, responsividad, evidencias y documento de entrega |

## Lo que más me costó

**El checkout (de la pre-entrega).** El test llegaba al formulario pero al hacer
clic en `Continue` no avanzaba. El problema no estaba en el sitio sino en Chrome:
su aviso de "contraseña filtrada" (porque `secret_sauce` es una clave pública)
tapaba la página. Lo resolví desactivando el gestor de contraseñas en las opciones
del navegador (`utils/driver_factory.py`). Aprendí que un `PASSED` sin validaciones
no dice nada, y que cuando algo falla también hay que mirar el entorno.

**Las pruebas de API encadenadas.** Al principio quise crear un post y después
consultarlo, pero JSONPlaceholder no guarda los recursos nuevos y el GET devolvía
404. Leyendo la documentación entendí que es una API simulada, así que armé los
flujos encadenados con datos que sí existen y uso el resultado de cada petición
para construir la siguiente.

## Autora

Barbara Garanton
