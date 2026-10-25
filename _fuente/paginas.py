# Páginas adicionales de walamort.com. build.py ejecuta este archivo con exec(),
# así que aquí están disponibles head(), nav(), pie(), jsonld(), BASE, e, HOY.

METODOS = {
    "kalimba": {"nombre": "Kalimba", "guia": "Kalimba-Primeros-Pasos-Walamort.pdf", "guia_pt": "Kalimba-Primeiros-Passos-Walamort.pdf",
                "basico": "https://pay.hotmart.com/M108153727I", "pack": "https://pay.hotmart.com/P108171383P"},
    "handpan": {"nombre": "Handpan", "guia": "Handpan-Primeros-Pasos-Walamort.pdf", "guia_pt": "Handpan-Primeiros-Passos-Walamort.pdf",
                "basico": "https://pay.hotmart.com/U108171401P", "pack": "https://pay.hotmart.com/C108171442W"},
    "tongue-drum": {"nombre": "Tongue drum", "guia": "Tongue-Drum-Primeros-Pasos-Walamort.pdf", "guia_pt": "Tongue-Drum-Primeiros-Passos-Walamort.pdf",
                    "basico": "https://pay.hotmart.com/M108171463V", "pack": "https://pay.hotmart.com/U108171515J"},
}

def doc(titulo, desc, ruta, cuerpo, imagen=None, extra="", lang="es"):
    h = head(titulo, desc, ruta, "/", extra, imagen=imagen)
    if lang != "es":
        h = h.replace('content="es_CO"', 'content="pt_BR"')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{h}
</head>
<body>
{nav('/')}
<main id="contenido">
{cuerpo}
</main>
{pie('/')}
</body>
</html>
"""

def cta_instrumento(slug, guia_compra=True):
    m = METODOS[slug]
    gc = f'<a class="btn ghost" href="/guias/{slug}/">Guía de compra</a>' if guia_compra else ""
    return f"""<div class="btns">
  <a class="btn solid" href="/descargas/{m['guia']}" target="_blank" rel="noopener">Descargar la guía gratis</a>
  <a class="btn ghost" href="{m['basico']}" target="_blank" rel="noopener">Método básico · $24.900</a>
  {gc}
</div>"""

# ------------------------------------------------------------------ test
TEST_PREGUNTAS = [
    ("¿Qué sonido te atrae más?", [
        ("Delicado y brillante, como una caja de música", "kalimba"),
        ("Profundo y envolvente, como campanas que flotan", "handpan"),
        ("Cálido y redondo, como gotas de lluvia sobre metal", "tongue-drum")]),
    ("¿Qué te gustaría tocar primero?", [
        ("Canciones que todo el mundo conoce", "kalimba"),
        ("Improvisar y dejarme llevar", "handpan"),
        ("Un poco de las dos cosas", "tongue-drum")]),
    ("¿Cómo te imaginas tocando?", [
        ("Con los pulgares, sentado en cualquier parte", "kalimba"),
        ("Con las yemas de los dedos, como un tambor que canta", "handpan"),
        ("Con baquetas o con los dedos, como más me guste", "tongue-drum")]),
    ("¿Dónde vas a tocar más?", [
        ("En todas partes: lo llevo en la maleta", "kalimba"),
        ("En casa, en un rato de calma solo para mí", "handpan"),
        ("En casa, con mi familia, con niños o en grupo", "tongue-drum")]),
    ("¿Cuánto quieres invertir en tu primer instrumento?", [
        ("Lo menos posible: quiero probar si me gusta", "kalimba"),
        ("Es un sueño y quiero un instrumento para toda la vida", "handpan"),
        ("Algo intermedio, que suene bonito y dure", "tongue-drum")]),
    ("¿Qué quieres sentir cuando toques?", [
        ("Alegría: tocar y cantar canciones", "kalimba"),
        ("Calma profunda, casi como meditar", "handpan"),
        ("Relajación sin complicarme", "tongue-drum")]),
]
TEST_RES = {
    "kalimba": ("Tu instrumento es la kalimba", "El «piano de pulgares» africano. Es pequeña, económica y viene afinada en una escala en la que casi todo suena bien: en una tarde puedes tocar tus primeras canciones. Ideal si quieres melodías conocidas y un instrumento que te acompañe a todas partes."),
    "handpan": ("Tu instrumento es el handpan", "Un instrumento de acero nacido en Suiza en el año 2000, con un sonido hondo y envolvente que invita a improvisar. Es una inversión mayor, pero es de esos instrumentos que se tienen para toda la vida. Ideal si buscas calma, ritmo y expresión libre."),
    "tongue-drum": ("Tu instrumento es el tongue drum", "Un tambor de acero con lengüetas que suena como gotas de lluvia. Se toca con baquetas o con los dedos, es resistente y está a medio camino entre la kalimba y el handpan: fácil para empezar y perfecto para tocar en familia."),
}

def pagina_test():
    data = {"q": [{"t": t, "o": [{"t": o, "v": v} for o, v in ops]} for t, ops in TEST_PREGUNTAS],
            "r": {k: {"t": t, "d": d, "g": "/descargas/" + METODOS[k]["guia"], "m": METODOS[k]["basico"], "c": f"/guias/{k}/",
                      "i": f"/instrumentos/{k}/"} for k, (t, d) in TEST_RES.items()}}
    cuerpo = f"""<section style="border-top:0"><div class="wrap quiz-wrap">
<div class="head">
  <span class="eyebrow">Test de 1 minuto</span>
  <h1 class="h1s">¿Qué instrumento <em class="script">va contigo?</em></h1>
  <p class="lead">Seis preguntas rápidas para descubrir si lo tuyo es la kalimba, el handpan o el tongue drum. Al final te llevas la guía gratis de tu instrumento.</p>
</div>
<div class="quiz" id="quiz" aria-live="polite">
  <div class="qbar"><i id="qprog"></i></div>
  <p class="qstep" id="qstep"></p>
  <h2 class="qtitle" id="qtitle"></h2>
  <div class="qopts" id="qopts"></div>
  <noscript><p>Activa JavaScript para hacer el test, o <a href="/#tienda">mira las guías gratis aquí</a>.</p></noscript>
</div>
<div class="qres" id="qres" hidden>
  <span class="eyebrow">Tu resultado</span>
  <h2 id="rtitle"></h2>
  <p class="lead" id="rdesc"></p>
  <div class="btns">
    <a class="btn solid" id="rguia" target="_blank" rel="noopener">Descargar mi guía gratis</a>
    <a class="btn ghost" id="rmet" target="_blank" rel="noopener">Método básico · $24.900</a>
    <a class="btn ghost" id="rcompra">Qué comprar</a>
  </div>
  <p class="qmore"><a id="rinst">Escucha cómo suena</a> · <button type="button" class="copy" id="again">Repetir el test</button> · <a id="rshare" target="_blank" rel="noopener">Compartir por WhatsApp</a></p>
</div>
</div></section>
<script>
(function () {{
  var D = {json.dumps(data, ensure_ascii=False)};
  var i = 0, score = {{}};
  var $ = function (id) {{ return document.getElementById(id); }};
  function show() {{
    var q = D.q[i];
    $("qprog").style.width = (i / D.q.length * 100) + "%";
    $("qstep").textContent = "Pregunta " + (i + 1) + " de " + D.q.length;
    $("qtitle").textContent = q.t;
    var box = $("qopts"); box.innerHTML = "";
    q.o.slice().sort(function () {{ return Math.random() - .5; }}).forEach(function (o) {{
      var b = document.createElement("button"); b.type = "button"; b.className = "qopt"; b.textContent = o.t;
      b.onclick = function () {{ score[o.v] = (score[o.v] || 0) + 1; i++; i < D.q.length ? show() : result(); }};
      box.appendChild(b);
    }});
  }}
  function result() {{
    var best = ["tongue-drum", "kalimba", "handpan"].sort(function (a, b) {{ return (score[b] || 0) - (score[a] || 0); }})[0];
    var r = D.r[best];
    $("quiz").hidden = true; $("qres").hidden = false;
    $("rtitle").textContent = r.t; $("rdesc").textContent = r.d;
    $("rguia").href = r.g; $("rmet").href = r.m; $("rcompra").href = r.c; $("rinst").href = r.i;
    $("rshare").href = "https://wa.me/?text=" + encodeURIComponent(r.t.replace("Tu", "Mi") + " según el test de Walamort. ¿Y el tuyo? https://walamort.com/test/");
    $("qres").scrollIntoView({{behavior: "smooth", block: "start"}});
  }}
  $("again").onclick = function () {{ i = 0; score = {{}}; $("quiz").hidden = false; $("qres").hidden = true; show(); }};
  show();
}})();
</script>"""
    return doc("¿Qué instrumento va contigo? Test | Walamort",
               "Descubre en un minuto si tu instrumento es la kalimba, el handpan o el tongue drum, y descarga gratis tu guía para empezar.",
               "test/", cuerpo)

# ------------------------------------------------------------------ guías de compra
GUIAS_COMPRA = {
 "kalimba": {
  "titulo": "Qué kalimba comprar", "t2": "si vas a empezar",
  "desc": "Guía para elegir tu primera kalimba: número de lengüetas, afinación, caja o tabla, materiales y qué revisar antes de pagar.",
  "intro": "La kalimba es el instrumento más económico de los tres y uno de los más fáciles para empezar. Aun así, entre una buena y una mala hay mucha diferencia: una lengüeta que zumba o una afinación que no se sostiene pueden quitarte las ganas en una semana. Esto es lo que yo miraría.",
  "puntos": [
   ("17 lengüetas en do mayor", "Es el modelo estándar y el que usan casi todos los métodos y tutoriales, incluidos los míos. Las de 8 o 10 lengüetas se quedan cortas muy rápido, y las de 21 o más son mejores cuando ya sabes tocar."),
   ("Caja o tabla", "La de caja es hueca: suena más fuerte y permite el efecto «wah» tapando el agujero. La de tabla suena más limpia y sostenida. Para empezar recomiendo la de caja, por versátil."),
   ("Madera sólida, mejor que acrílico", "Las kalimbas transparentes se ven muy bonitas, pero suelen sonar más apagadas. Las de madera (caoba, acacia, koa, nogal) tienen un sonido más cálido."),
   ("Que traiga lo básico", "Martillo de afinación, estuche y, si es posible, los números grabados en las lengüetas. Los números te ahorran mucho tiempo al leer las canciones."),
   ("Lengüetas parejas y lisas", "Revisa que ninguna esté torcida, que no rocen entre sí y que la punta sea redondeada. Si la compras en persona, toca todas las notas: ninguna debe zumbar."),
  ],
  "errores": ["Comprar la más barata del mercado: muchas llegan con lengüetas que zumban y se desafinan en días.",
              "Elegir una kalimba cromática o de muchas lengüetas para empezar: es más difícil y casi ningún material para principiantes la usa.",
              "Olvidar el afinador: cualquier aplicación gratuita de afinador cromático sirve, y la vas a necesitar desde el primer día."],
  "reco": "Una kalimba de 17 lengüetas en do mayor, de caja, en madera, con martillo y números grabados. Con eso puedes seguir mi guía gratis y los tres niveles del método sin cambiar de instrumento."},
 "handpan": {
  "titulo": "Qué handpan comprar", "t2": "sin equivocarte",
  "desc": "Guía para elegir tu primer handpan: escala, número de notas, tipo de acero, afinación y cómo evitar instrumentos de mala calidad.",
  "intro": "El handpan es una inversión grande, así que vale la pena tomarse el tiempo. Un buen handpan dura toda la vida; uno mal hecho se desafina, zumba y no tiene arreglo fácil. Estos son los puntos que revisaría antes de pagar.",
  "puntos": [
   ("Una escala menor de 9 notas", "Para empezar, lo más versátil es un ding y ocho notas alrededor en una escala menor como Kurd (por ejemplo, en Re o en Sol menor, la que uso en mis métodos). Suena bien en casi cualquier combinación y tiene mucho repertorio."),
   ("Inoxidable o nitrurado", "El acero inoxidable suele tener un sonido más largo y etéreo y resiste mejor la humedad. El nitrurado suele sonar más definido y con más ataque, pero necesita aceite con regularidad. Los dos son buenos; elige según el sonido que te guste y el clima donde vives."),
   ("Pide un video de cada nota", "Antes de comprar, pide al vendedor un video tocando cada nota por separado y con un afinador al lado. Ninguna debe zumbar ni sonar «doble», y todas deben durar parecido."),
   ("Afinación en 440 Hz", "Si vas a tocar con otros instrumentos o con pistas, elige 440 Hz, la afinación estándar. Los de 432 Hz suenan muy bien solos, pero no encajan con la mayoría de la música grabada."),
   ("Estuche rígido o acolchado", "El handpan se desafina con golpes. Un buen estuche no es un lujo: es parte del instrumento."),
  ],
  "errores": ["Comprar un «handpan» muy barato en una tienda en línea sin fabricante conocido: muchas veces llega desafinado y sin posibilidad de reparación.",
              "Confundirlo con un tongue drum: el tongue drum tiene lengüetas recortadas; el handpan, campos tonales abombados. Son instrumentos distintos.",
              "Elegir una escala exótica para empezar: primero una escala menor clásica; las escalas especiales son para un segundo instrumento."],
  "reco": "Un handpan de 9 notas en escala menor (Kurd), en 440 Hz, de un fabricante que muestre videos de sus instrumentos y responda tus preguntas, con estuche incluido. Si todavía no estás seguro, empieza por un tongue drum y da el salto después."},
 "tongue-drum": {
  "titulo": "Qué tongue drum comprar", "t2": "para empezar bien",
  "desc": "Guía para elegir tu primer tongue drum: tamaño, número de lengüetas, escala, materiales y accesorios.",
  "intro": "El tongue drum es la puerta de entrada perfecta a los instrumentos de acero: suena hermoso desde el primer golpe, es resistente y cuesta mucho menos que un handpan. Hay cientos de modelos, así que aquí va lo que de verdad importa.",
  "puntos": [
   ("11 lengüetas o más, en do mayor", "Con 11 lengüetas tienes la escala completa con graves y agudos, que es lo que uso en mis métodos. Los de 8 notas sirven para relajarse, pero se quedan cortos para tocar canciones."),
   ("Escala completa, no pentatónica", "Muchos tongue drums vienen en escala pentatónica (sin el 4 y el 7). Suenan muy bien para improvisar, pero no te dejan tocar la mayoría de las canciones. Si quieres canciones, busca uno con todas las notas, del 1 al 7."),
   ("Tamaño de 12 a 14 pulgadas", "Los de 6 u 8 pulgadas son lindos pero suenan agudos y cortos. Entre 12 y 14 pulgadas el sonido es más profundo y largo."),
   ("Números grabados", "Que cada lengüeta tenga su número grabado o que traiga stickers. Así puedes leer las canciones en números desde el primer día."),
   ("Lo que trae la caja", "Baquetas con punta de goma, funda acolchada y, si es posible, un soporte. La funda es importante: un golpe puede desafinar una lengüeta."),
  ],
  "errores": ["Elegir solo por el color o el diseño: primero el sonido, la escala y el número de lengüetas.",
              "Comprar uno pentatónico pensando en tocar canciones conocidas: vas a encontrar que faltan notas.",
              "Tocar con objetos metálicos: usa solo las baquetas que trae o tus dedos."],
  "reco": "Un tongue drum de 11 lengüetas en do mayor, de 12 a 14 pulgadas, con números grabados, baquetas y funda. Es el mismo tipo de instrumento que uso en mi guía gratis y en los tres niveles del método."},
}

def pagina_guia_compra(slug):
    g = GUIAS_COMPRA[slug]; m = METODOS[slug]
    pts = "".join(f'<div class="gpt"><b>{e(t)}</b><p>{e(d)}</p></div>' for t, d in g["puntos"])
    err = "".join(f"<li>{e(x)}</li>" for x in g["errores"])
    otros = " · ".join(f'<a href="/guias/{k}/">{METODOS[k]["nombre"]}</a>' for k in GUIAS_COMPRA if k != slug)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["titulo"] + " " + g["t2"], "description": g["desc"],
           "inLanguage": "es", "author": {"@type": "Person", "name": "Walter Agudelo Múnera", "url": BASE + "/"},
           "publisher": {"@type": "Organization", "name": "Walamort"}, "dateModified": HOY, "mainEntityOfPage": f"{BASE}/guias/{slug}/"}
    cuerpo = f"""<section style="border-top:0"><div class="wrap article">
<div class="head">
  <span class="eyebrow">Guía de compra · {e(m['nombre'])}</span>
  <h1 class="h1s">{e(g['titulo'])} <em class="script">{e(g['t2'])}</em></h1>
  <p class="lead">{e(g['intro'])}</p>
</div>
<h2 class="ph">Qué mirar antes de comprar</h2>
<div class="gpts">{pts}</div>
<h2 class="ph">Errores frecuentes</h2>
<ul class="list">{err}</ul>
<div class="reco">
  <span class="eyebrow">Mi recomendación</span>
  <p>{e(g['reco'])}</p>
</div>
<h2 class="ph">Cuando lo tengas en las manos</h2>
<p>Descarga la guía gratis para dar tus primeros pasos y, cuando quieras ir más lejos, sigue con el método por niveles.</p>
{cta_instrumento(slug, guia_compra=False)}
<p class="lead" style="margin-top:28px;font-size:15px">¿Aún no sabes qué instrumento elegir? <a href="/test/">Haz el test de un minuto</a>. Otras guías de compra: {otros}.</p>
</div></section>"""
    return doc(f"{g['titulo']} {g['t2']} | Walamort", g["desc"], f"guias/{slug}/", cuerpo, extra=jsonld(art))

def pagina_guias():
    cards = "".join(f"""<a class="gcard" href="/guias/{k}/"><span class="eyebrow">{e(METODOS[k]['nombre'])}</span><b>{e(g['titulo'])} {e(g['t2'])}</b><span>{e(g['desc'])}</span></a>"""
                    for k, g in GUIAS_COMPRA.items())
    cuerpo = f"""<section style="border-top:0"><div class="wrap">
<div class="head">
  <span class="eyebrow">Guías de compra</span>
  <h1 class="h1s">Elige bien <em class="script">tu instrumento</em></h1>
  <p class="lead">Lo que miraría yo antes de comprar mi primer instrumento, sin marcas patrocinadas: solo criterios para que suene bien y te dure.</p>
</div>
<div class="gcards">{cards}</div>
<p class="lead" style="margin-top:24px;font-size:15px">¿No sabes por cuál empezar? <a href="/test/">Haz el test de un minuto</a>.</p>
</div></section>"""
    return doc("Guías de compra: kalimba, handpan y tongue drum | Walamort",
               "Qué kalimba, handpan o tongue drum comprar para empezar: criterios claros, errores frecuentes y recomendaciones de Walamort.",
               "guias/", cuerpo)

# ------------------------------------------------------------------ talleres
TALLERES = [
    ("La vuelta al mundo en instrumentos", "Charla-concierto · 45 a 60 min",
     "Llevo instrumentos de distintos continentes, cuento su historia y los hago sonar en vivo. El público adivina de dónde vienen, vota y participa tocando ritmos sencillos.",
     "Colegios, bibliotecas, cajas de compensación, eventos culturales y familiares."),
    ("Ritmo latino en equipo", "Taller vivencial · 60 a 90 min",
     "Con percusión corporal y pequeños instrumentos, el grupo construye junto un ritmo de salsa, cumbia o samba. Escuchar, coordinarse y sonar como uno solo.",
     "Empresas, integraciones, equipos de trabajo y grupos juveniles."),
    ("Haz un beat con el mundo", "Taller creativo · 90 a 120 min",
     "Grabamos sonidos de instrumentos del mundo y, con ellos, armamos en vivo un beat original, paso a paso, como en un estudio de producción.",
     "Jóvenes desde 12 años, semilleros de música, universidades y espacios de innovación."),
    ("Primeros pasos en kalimba, handpan o tongue drum", "Taller práctico · 60 a 90 min",
     "Un taller para tocar desde el primer minuto, con la misma notación por números de mis métodos. Cada participante se lleva la guía en PDF.",
     "Grupos pequeños que cuenten con instrumentos, o en modalidad virtual."),
]

def pagina_talleres():
    cards = "".join(f'<article class="tcard"><span class="tag">{e(f)}</span><h3>{e(t)}</h3><p>{e(d)}</p><p class="tfor"><b>Para:</b> {e(p)}</p></article>' for t, f, d, p in TALLERES)
    wa = "https://wa.me/573053650966?text=" + "Hola%20Walter%2C%20quiero%20una%20propuesta%20de%20taller%20Walamort.%20Instituci%C3%B3n%3A%20%20%7C%20Fecha%3A%20%20%7C%20N%C3%BAmero%20de%20personas%3A%20"
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "Talleres y charlas-concierto Walamort",
           "provider": {"@type": "Person", "name": "Walter Agudelo Múnera"}, "areaServed": ["Medellín", "Valle de Aburrá", "Colombia"],
           "serviceType": "Talleres de música e instrumentos del mundo", "url": BASE + "/talleres/"}
    cuerpo = f"""<section style="border-top:0"><div class="wrap">
<div class="idiomas-hero">
  <div class="head" style="margin:0">
    <span class="eyebrow">Talleres y charlas-concierto</span>
    <h1 class="h1s">El mundo suena <em class="script">en tu espacio</em></h1>
    <p class="lead">Llevo los instrumentos del mundo a colegios, empresas, bibliotecas y eventos: historias, sonidos en vivo y mucha participación. Presencial en Medellín y el Valle de Aburrá, y virtual desde cualquier lugar.</p>
    <div class="btns"><a class="btn solid" href="{wa}" target="_blank" rel="noopener">Pedir una propuesta</a><a class="btn ghost" href="/descargas/Propuesta-Talleres-Walamort.pdf" target="_blank" rel="noopener">Descargar la propuesta (PDF)</a></div>
  </div>
  <img src="/fotos/estudio.webp?v=3" alt="Walter tocando bongós en un salón de ensayo" width="600" height="750" style="aspect-ratio:4/5;max-width:420px;justify-self:end">
</div>
<h2 class="ph">Formatos</h2>
<div class="tcards">{cards}</div>
<h2 class="ph">Cómo trabajamos</h2>
<ol class="steps">
  <li><b>Me cuentas</b><span>Tipo de grupo, edades, número de personas, fecha y lugar.</span></li>
  <li><b>Te envío la propuesta</b><span>Formato, duración, lo que necesito del espacio y el valor, en menos de 48 horas.</span></li>
  <li><b>Lo vivimos</b><span>Llego con los instrumentos y el sonido. Ustedes solo ponen las ganas.</span></li>
</ol>
<p class="lead" style="margin-top:24px">Cada taller se cotiza según el formato, la duración y el número de participantes. Escríbeme por <a href="{wa}" target="_blank" rel="noopener">WhatsApp</a> o a <a href="mailto:hola@walamort.com">hola@walamort.com</a>.</p>
</div></section>"""
    return doc("Talleres de música para colegios y empresas en Medellín | Walamort",
               "Charlas-concierto y talleres con instrumentos del mundo para colegios, empresas y eventos, en Medellín y en modalidad virtual.",
               "talleres/", cuerpo, imagen=BASE + "/fotos/estudio.webp", extra=jsonld(svc))

# ------------------------------------------------------------------ portugués
def pagina_pt():
    guias = "".join(f"""<article class="ptg"><span class="eyebrow">Guia grátis</span><b>{e(n)}</b><p>{e(d)}</p>
<a class="btn solid" href="/descargas/{METODOS[k]['guia_pt']}" target="_blank" rel="noopener">Baixar o PDF</a></article>"""
                    for k, n, d in [("kalimba", "Primeiros passos na kalimba", "Partes, postura, afinação, mapa de notas e suas duas primeiras músicas."),
                                    ("handpan", "Primeiros passos no handpan", "Partes, técnica, mapa de notas, grooves e duas melodias originais."),
                                    ("tongue-drum", "Primeiros passos no tongue drum", "Partes, técnica, mapa de notas, exercícios e suas duas primeiras músicas.")])
    alt = f'<link rel="alternate" hreflang="es" href="{BASE}/">\n<link rel="alternate" hreflang="pt-BR" href="{BASE}/pt/">'
    cuerpo = f"""<section style="border-top:0"><div class="wrap">
<div class="idiomas-hero">
  <div class="head" style="margin:0">
    <span class="eyebrow">Walamort em português</span>
    <h1 class="h1s">Um instrumento novo <em class="script">toda semana.</em></h1>
    <p class="lead">Olá! Eu sou o Walter Agudelo Múnera, músico, produtor e professor em Medellín, na Colômbia. Toda semana apresento um instrumento do mundo: sua história, um beat com seus sons e a música que a comunidade escolhe. Falo português e preparei guias grátis para você começar a tocar.</p>
    <div class="btns"><a class="btn solid" href="#guias">Guias grátis</a><a class="btn ghost" href="/idiomas/">Aulas de espanhol</a></div>
  </div>
  <img src="/fotos/walter-saxofon-medellin.webp" alt="Walter Agudelo Múnera tocando saxofone em Medellín" width="900" height="1125" style="aspect-ratio:4/5;max-width:420px;justify-self:end">
</div>
<h2 class="ph" id="guias">Guias grátis em português</h2>
<div class="ptgrid">{guias}</div>
<h2 class="ph">Métodos completos</h2>
<p>Os métodos por níveis (básico, intermediário e avançado) de kalimba, handpan e tongue drum estão em espanhol, com notação por números, muito fácil de acompanhar mesmo sem falar espanhol. O pagamento é seguro, pela Hotmart.</p>
<div class="btns" style="margin-top:14px"><a class="btn ghost" href="/#tienda">Ver os métodos</a></div>
<h2 class="ph">Aulas on-line</h2>
<p>Aulas de espanhol por videochamada para brasileiros, com um professor colombiano: conversação desde a primeira aula, pronúncia latino-americana e música latina para aprender ouvindo.</p>
<div class="btns" style="margin-top:14px"><a class="btn solid" href="/?tema=Espanhol%20para%20brasileiros#reservar">Agendar aula de espanhol</a><a class="btn ghost" href="https://wa.me/573053650966?text=Ol%C3%A1%20Walter!" target="_blank" rel="noopener">Falar pelo WhatsApp</a></div>
</div></section>"""
    return doc("Walamort em português: guias grátis de kalimba, handpan e tongue drum",
               "Guias grátis em português para começar a tocar kalimba, handpan e tongue drum, e aulas de espanhol por videochamada com Walter Agudelo Múnera.",
               "pt/", cuerpo, extra=alt, lang="pt-BR")

def escribir_paginas_nuevas():
    escribir("test/index.html", pagina_test())
    escribir("guias/index.html", pagina_guias())
    for k in GUIAS_COMPRA:
        escribir(f"guias/{k}/index.html", pagina_guia_compra(k))
    escribir("talleres/index.html", pagina_talleres())
    escribir("pt/index.html", pagina_pt())

PAGINAS_SITEMAP = [("test/", "0.8"), ("guias/", "0.7"), ("talleres/", "0.8"), ("pt/", "0.8")] + [(f"guias/{k}/", "0.7") for k in GUIAS_COMPRA]
