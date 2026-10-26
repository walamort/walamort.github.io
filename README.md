# Walamort — sitio web

Sitio estático de la marca Walamort: «Un instrumento del mundo cada semana».
Se publica gratis con GitHub Pages.

## Estructura
- `index.html`: página de inicio (instrumento de la semana, tienda, clases, contacto).
- `instrumentos/`: archivo de la serie y una página por instrumento (pensadas para Google).
- `portadas/`, `descargas/`: portadas de los métodos y la guía gratis de kalimba.
- `horario.json`: horarios de clases que muestra el calendario de reservas.
- `_fuente/`: lo que se edita. Las páginas se generan desde aquí.

## Agregar el instrumento de la semana
1. Agrega un objeto al final de `_fuente/instrumentos.json` (el último es el de la semana).
2. Si tiene ilustración nueva, agrégala al objeto `ARTE` de `_fuente/plantilla-inicio.html`.
3. Ejecuta `python3 _fuente/build.py` y publica los cambios.

## Dominio propio
Cuando compres el dominio, escribe en `_fuente/sitio.json`:
`"base_url": "https://walamort.com"` y `"dominio": "walamort.com"`, ejecuta el build
y configura el dominio en GitHub (Settings → Pages → Custom domain).

## Academy, test y museo

- `python _fuente/build.py` regenera también `/academia/`, `/test-instrumento/` y `/museo/`.
- Editar Academy y test: `_fuente/explora/academia.html` y `test-instrumento.html`. Sus estilos y comportamiento están en `assets/`.
- Museo: editar `_fuente/museo.json`; `_fuente/museo.py` genera las fichas estáticas y las opciones de familia. No se necesita JavaScript para leerlas. Cada ficha exige slug único y fuente HTTPS. La plantilla está en `_fuente/explora/museo.html`.
- Las fichas actuales describen tipos instrumentales, no certifican los ejemplares del inventario. No agregar fabricante, afinación, origen de adquisición ni fotografía individual sin confirmar con Walter. Las fotos de los estudios virtuales no se reutilizan como fotos de ejemplares.
- El test procesa respuestas en memoria, sin almacenamiento ni envío. Presupuesto, portabilidad y volumen funcionan como condiciones; las preferencias ordenan las alternativas compatibles. Los empates se explican y las opciones incompatibles se muestran por separado. No hay precios ni diagnóstico de aptitud.
- Academy presenta un programa propuesto: sin pagos, inscripción, fechas, duración ni certificados anunciados. El contacto usa `mailto:`, no un formulario que simule una suscripción.
- Para verificar: `node _fuente/check-explora.cjs` con Playwright y Chrome instalados. En este entorno, configurar `NODE_PATH` al directorio de paquetes del runtime. Comprueba vistas de 320/390/1440 px, enlaces/fragmentos/recursos internos, SEO básico, filtros, casos sin resultados, navegación del test, 270 perfiles de restricciones y lectura sin JavaScript. Las capturas se guardan fuera del repositorio, en su directorio padre.

### Material pendiente para publicar más contenido

1. Inventario revisado: nombre por ejemplar, identificador, constructor si se conoce, procedencia documentada, medidas, material, afinación y estado. Marcar desconocidos.
2. Fotos identificadas por ejemplar y autorización de uso; audio/video propio y créditos, con permiso para publicarlo.
3. Curso: aprobación del programa, lecciones y materiales, modalidad, duración, fechas y acompañamiento. Definir precio, condiciones y autorización expresa antes de integrar venta o pagos.
