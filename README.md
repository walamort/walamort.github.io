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
