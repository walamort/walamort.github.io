#!/usr/bin/env python3
"""Genera el sitio de Walamort.

Uso:  python3 _fuente/build.py

Para un instrumento nuevo: agrega un objeto al final de _fuente/instrumentos.json
(el último de la lista es el instrumento de la semana) y, si quieres, su ilustración
en el objeto ARTE de _fuente/plantilla-inicio.html. Luego ejecuta este script.
Cuando tengas dominio propio, cambia BASE_URL en _fuente/sitio.json.
"""
import html, json, os, re, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, "_fuente")

def leer(p):
    with open(os.path.join(FUENTE, p), encoding="utf8") as f:
        return f.read()

def escribir(rel, texto):
    p = os.path.join(RAIZ, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf8") as f:
        f.write(texto)

SITIO = json.loads(leer("sitio.json"))
BASE = SITIO["base_url"].rstrip("/")
INST = json.loads(leer("instrumentos.json"))
PLANTILLA = leer("plantilla-inicio.html")
ARTE = dict(re.findall(r"^  (\w+): '(<svg.*?</svg>)',?$", PLANTILLA, re.M))
HOY = datetime.date.today().isoformat()
e = html.escape

REDES = [("Instagram", "https://www.instagram.com/walamort/"),
         ("TikTok", "https://www.tiktok.com/@walamort"),
         ("YouTube", "https://www.youtube.com/@walamort"),
         ("Facebook", "https://www.facebook.com/walamort")]

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

PERSONA = {"@type": "Person", "name": "Walter Agudelo Múnera", "alternateName": "Walamort",
           "jobTitle": "Músico, productor musical y docente", "url": BASE + "/",
           "sameAs": [u for _, u in REDES]}

def head(titulo, desc, ruta, raiz, extra="", imagen=None, tipo="website"):
    url = BASE + "/" + ruta
    img = imagen or (BASE + "/og.png")
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta name="theme-color" content="#2B0D14">
<link rel="icon" href="{raiz}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{tipo}">
<meta property="og:site_name" content="Walamort">
<meta property="og:locale" content="es_CO">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(img)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&family=Lora:ital,wght@1,500&display=swap">
<link rel="stylesheet" href="{raiz}estilos.css">
{extra}"""

def nav(raiz):
    return f"""<a class="skip" href="#contenido">Saltar al contenido</a>
<nav aria-label="Principal">
  <div class="wrap">
    <a class="logo" href="{raiz}">Wala<span>mort</span></a>
    <ul>
      <li><a href="{raiz}#semana">Esta semana</a></li>
      <li><a href="{raiz}instrumentos/">Instrumentos</a></li>
      <li><a href="{raiz}#tienda">Tienda</a></li>
      <li><a href="{raiz}#clases">Clases</a></li>
      <li><a href="{raiz}#contacto">Contacto</a></li>
    </ul>
  </div>
  <div class="stripes" aria-hidden="true"><i></i><i></i><i></i></div>
</nav>"""

def pie(raiz):
    redes = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in REDES)
    return f"""<div class="stripes" aria-hidden="true"><i></i><i></i><i></i></div>
<footer>
  <div class="wrap">
    <span>© {datetime.date.today().year} Walamort · Walter Agudelo Múnera</span>
    <span class="foot-links">{redes}</span>
  </div>
</footer>"""

YT_JS = """<script>
document.querySelectorAll('.yt').forEach(function (b) {
  b.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.id + '?autoplay=1&rel=0';
    f.title = b.dataset.title; f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
    b.replaceWith(f);
  });
});
</script>"""

def video_card(v):
    t = e(v["titulo"])
    return f"""<figure class="ytbox">
  <button type="button" class="yt" data-id="{e(v['id'])}" data-title="{t}" aria-label="Reproducir: {t}">
    <img src="https://i.ytimg.com/vi/{e(v['id'])}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">
    <span class="ytplay" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
  </button>
  <figcaption>{t} · <a href="https://www.youtube.com/shorts/{e(v['id'])}" target="_blank" rel="noopener">Ver en YouTube</a></figcaption>
</figure>"""

def pagina_instrumento(i, inst):
    raiz = "../../"
    actual = i == len(INST) - 1
    nm = inst["nombre"].lower()
    ruta = f"instrumentos/{inst['slug']}/"
    titulo = f"¿Qué es {inst['un']} {nm}? Historia, sonido y cómo se toca | Walamort"
    datos = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in inst["datos"])
    secciones = "".join(
        f'<h2 class="ph">{e(s["titulo"])}</h2>' + "".join(f"<p>{e(p)}</p>" for p in s["parrafos"])
        for s in inst["secciones"])
    curios = "".join(f"<li>{e(c)}</li>" for c in inst["curiosidades"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in inst["faq"])
    videos = "".join(video_card(v) for v in inst["videos"])
    lista = (f'<p class="lead"><a href="{e(inst["lista"])}" target="_blank" rel="noopener">Ver todos los videos {inst["de"]} {nm} en YouTube</a></p>'
             if inst.get("lista") else
             '<p class="lead">Más videos en <a href="https://www.youtube.com/@walamort" target="_blank" rel="noopener">YouTube</a>, <a href="https://www.tiktok.com/@walamort" target="_blank" rel="noopener">TikTok</a> e <a href="https://www.instagram.com/walamort/" target="_blank" rel="noopener">Instagram</a>.</p>')
    if inst.get("tienda"):
        cta = f"""<div class="pack">
      <div>
        <span class="eyebrow" style="color:#2B0D14">Empieza gratis</span>
        <h3>Aprende a tocar {inst['el']} {nm}</h3>
        <p>Guía gratuita para tus primeros pasos y métodos Walamort en tres niveles, de principiante a creador.</p>
      </div>
      <div class="packbuy">
        <a class="btn" href="{raiz}#tienda">Ver guía gratis y métodos</a>
      </div>
    </div>"""
    else:
        cta = f"""<div class="pack">
      <div>
        <span class="eyebrow" style="color:#2B0D14">Aprende conmigo</span>
        <h3>¿Quieres tocar {inst['el']} {nm}?</h3>
        <p>Clases personalizadas por videollamada, a tu ritmo y desde cualquier lugar.</p>
      </div>
      <div class="packbuy">
        <a class="btn" href="{raiz}#clases">Ver clases</a>
      </div>
    </div>"""
    prev_ = INST[i - 1] if i > 0 else None
    next_ = INST[i + 1] if i < len(INST) - 1 else None
    pn = ""
    if prev_: pn += f'<a class="pn" href="../{prev_["slug"]}/"><span>← Anterior</span><b>{e(prev_["nombre"])}</b></a>'
    if next_: pn += f'<a class="pn next" href="../{next_["slug"]}/"><span>Siguiente →</span><b>{e(next_["nombre"])}</b></a>'
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Instrumentos", "item": BASE + "/instrumentos/"},
            {"@type": "ListItem", "position": 3, "name": inst["nombre"], "item": BASE + "/" + ruta}]},
        {"@context": "https://schema.org", "@type": "Article", "headline": f"¿Qué es {inst['un']} {nm}?",
         "description": inst["descripcion"], "datePublished": inst["fecha"], "dateModified": HOY,
         "inLanguage": "es", "author": PERSONA, "publisher": PERSONA, "mainEntityOfPage": BASE + "/" + ruta},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in inst["faq"]]},
    ]
    extra = "\n".join(jsonld(x) for x in ld)
    eyebrow = "Instrumento de la semana" if actual else "Archivo de la serie"
    return f"""<!doctype html>
<html lang="es">
<head>
{head(titulo, inst['descripcion'], ruta, raiz, extra, tipo='article')}
</head>
<body>
{nav(raiz)}
<main id="contenido">
<div class="wrap">
  <ol class="crumbs" aria-label="Ruta"><li><a href="{raiz}">Inicio</a></li><li><a href="../">Instrumentos</a></li><li aria-current="page">{e(inst['nombre'])}</li></ol>
  <header class="hero ihero">
    <div>
      <span class="eyebrow">{eyebrow} · {e(inst['semana'])}</span>
      <h1>{e(inst['nombre'])} <em class="script">qué es y cómo suena</em></h1>
      <p>{e(inst['texto'])}</p>
      <p class="aka">También conocido como: {e(inst['otros_nombres'])}.</p>
      <div class="btns">
        <a class="btn solid" href="#videos">Escúchalo</a>
        <a class="btn ghost" href="{raiz}{'#tienda' if inst.get('tienda') else '#clases'}">{'Guía gratis' if inst.get('tienda') else 'Clases'}</a>
      </div>
    </div>
    <div class="art" aria-hidden="true">
      <div class="disc"></div><div class="disc2"></div>
      {ARTE.get(inst['arte'], '')}
    </div>
  </header>
</div>

<section>
  <div class="wrap iwrap">
    <article class="prose">
      <div class="facts">{datos}</div>
      {secciones}
      <h2 class="ph">Datos curiosos</h2>
      <ul class="curios">{curios}</ul>
    </article>
  </div>
</section>

<section id="videos">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Escúchalo</span>
      <h2>{e(inst['nombre'])} <em class="script">en video</em></h2>
    </div>
    <div class="ytgrid">{videos}</div>
    {lista}
  </div>
</section>

<section>
  <div class="wrap">
    {cta}
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Preguntas frecuentes</span>
      <h2>Sobre {inst['el']} {e(nm)}</h2>
    </div>
    <div class="faq">{faq}</div>
    <nav class="pnav" aria-label="Otros instrumentos">{pn}</nav>
  </div>
</section>
</main>
{pie(raiz)}
{YT_JS}
</body>
</html>
"""

def pagina_archivo():
    raiz = "../"
    cards = ""
    for i, inst in enumerate(reversed(INST)):
        tag = "Esta semana" if i == 0 else inst["semana"]
        cards += f"""<a class="inst icard" href="{inst['slug']}/">
      <span class="tag">{e(tag)}</span>
      <h3>{e(inst['nombre'])}</h3>
      <p>{e(inst['texto'])}</p>
      <span class="more">Ver la página {inst['de']} {e(inst['nombre'].lower())} →</span>
    </a>"""
    desc = "Todos los instrumentos de la serie «Un instrumento del mundo cada semana» de Walamort: historia, sonido, cómo se tocan y videos."
    ld = jsonld({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "url": f"{BASE}/instrumentos/{x['slug']}/", "name": x["nombre"]} for n, x in enumerate(INST)]})
    return f"""<!doctype html>
<html lang="es">
<head>
{head('Instrumentos del mundo, uno por semana | Walamort', desc, 'instrumentos/', raiz, ld)}
</head>
<body>
{nav(raiz)}
<main id="contenido">
<section style="border-top:0">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Archivo de la serie</span>
      <h1 class="h1s">Instrumentos <em class="script">del mundo</em></h1>
      <p class="lead">Cada semana, un instrumento nuevo: de dónde viene, cómo suena y cómo se toca. Esta es la lista completa, del más reciente al primero.</p>
    </div>
    <div class="archive">{cards}</div>
  </div>
</section>
</main>
{pie(raiz)}
</body>
</html>
"""

def pagina_inicio():
    datos_js = []
    for x in INST:
        vids = [{"titulo": v["titulo"], "red": "YouTube", "url": "https://www.youtube.com/shorts/" + v["id"]} for v in x["videos"]]
        if x.get("lista"):
            vids.append({"titulo": "Todos los videos " + x["de"] + " " + x["nombre"].lower(), "red": "Lista de YouTube", "url": x["lista"]})
        datos_js.append({"slug": x["slug"], "nombre": x["nombre"], "de": x["de"], "el": x["el"], "semana": x["semana"],
                         "texto": x["texto"], "datos": x["datos"], "arte": x["arte"], "cancion": x["cancion"], "videos": vids})
    cur = INST[-1]
    desc = (f"Walamort: un instrumento del mundo cada semana. Esta semana, {cur['el']} {cur['nombre'].lower()}. "
            "Guías gratis y métodos de kalimba y handpan, y clases virtuales de música y de portugués con Walter Agudelo Múnera.")
    ld = "\n".join([
        jsonld({"@context": "https://schema.org", "@type": "WebSite", "name": "Walamort", "url": BASE + "/", "inLanguage": "es"}),
        jsonld(dict({"@context": "https://schema.org"}, **PERSONA)),
    ])
    h = head("Walamort · Un instrumento del mundo cada semana", desc, "", "", ld)
    out = PLANTILLA.replace("{{HEAD}}", h).replace("/*INSTRUMENTOS*/", json.dumps(datos_js, ensure_ascii=False, indent=1))
    out = out.replace('<main>', '<main id="contenido">', 1)
    out = out.replace('<nav aria-label="Principal">', '<a class="skip" href="#contenido">Saltar al contenido</a>\n<nav aria-label="Principal">', 1)
    return out

def pagina_404():
    return f"""<!doctype html>
<html lang="es">
<head>
{head('Página no encontrada | Walamort', 'Esta página no existe.', '404.html', '/')}
<meta name="robots" content="noindex">
</head>
<body>
{nav('/')}
<main id="contenido"><section style="border-top:0"><div class="wrap"><div class="head">
<span class="eyebrow">Error 404</span>
<h1 class="h1s">Esta nota <em class="script">no existe</em></h1>
<p class="lead">La página que buscas se movió o nunca existió.</p>
<div class="btns"><a class="btn solid" href="/">Ir al inicio</a><a class="btn ghost" href="/instrumentos/">Ver instrumentos</a></div>
</div></div></section></main>
{pie('/')}
</body>
</html>
"""

def sitemap():
    urls = [("", HOY, "1.0"), ("instrumentos/", HOY, "0.8")] + [(f"instrumentos/{x['slug']}/", HOY, "0.9") for x in INST]
    filas = "".join(f"<url><loc>{BASE}/{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n" for u, d, p in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{filas}</urlset>\n'

def main():
    escribir("estilos.css", leer("estilos-base.css") + "\n" + leer("estilos-extra.css"))
    escribir("index.html", pagina_inicio())
    escribir("instrumentos/index.html", pagina_archivo())
    for i, x in enumerate(INST):
        escribir(f"instrumentos/{x['slug']}/index.html", pagina_instrumento(i, x))
    escribir("404.html", pagina_404())
    escribir("sitemap.xml", sitemap())
    escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    if SITIO.get("dominio"):
        escribir("CNAME", SITIO["dominio"] + "\n")
    print(f"Listo: {len(INST)} instrumentos. Instrumento de la semana: {INST[-1]['nombre']}")

if __name__ == "__main__":
    main()
