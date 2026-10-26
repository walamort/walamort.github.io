"""Render the museum from reviewed records; never infer collection specimen data."""
records = json.loads(leer("museo.json"))
items = []
slugs = set()
for number, record in enumerate(records, 1):
    slug = record['slug']
    if not re.fullmatch(r'[a-z0-9-]+', slug) or slug in slugs:
        raise ValueError('Invalid or duplicate museum slug')
    slugs.add(slug)
    if not record['source'].startswith('https://'):
        raise ValueError('Museum records need an HTTPS source')
    r = {key: e(str(value), quote=True) for key, value in record.items()}
    items.append(f'''<article class="record" id="{r['slug']}" data-family="{r['family']}">
<div class="record-head"><span class="kicker">Ficha {number:02d} / {r['family']}</span><a href="#{r['slug']}">Enlace a esta ficha</a></div>
<h2>{r['name']}</h2><div class="split"><div><p class="lead">{r['text']}</p>
<dl><dt>Qué vibra</dt><dd>{r['mechanism']}</dd><dt>Contexto</dt><dd>{r['context']}</dd><dt>Ejemplar</dt><dd>Fabricante, procedencia, medidas, afinación y fotografía individual pendientes de confirmar.</dd></dl></div>
<div><h3>Una primera escucha</h3><p>{r['try']}</p><div class="actions"><a class="button" href="https://www.youtube.com/watch?v={r['video']}">Ver demostración en YouTube</a><a class="button alt" href="/instrumentos/{r['slug']}/studio/">Probar versión virtual</a></div><p class="quiet">La versión virtual es una aproximación interactiva al instrumento.</p><p>Fuente: <a href="{r['source']}">{r['sourceName']}</a>.</p><a href="/instrumentos/{r['slug']}/">Consultar la página de la serie →</a></div></div></article>''')
page = leer('explora/museo.html').replace('{{RECORDS}}', '\n'.join(items))
families = sorted({record['family'] for record in records})
page = re.sub(r'(<select id="family">).*?(</select>)', lambda m: m[1] + '<option value="">Todas las familias</option>' + ''.join(f'<option>{e(f)}</option>' for f in families) + m[2], page)
page = page.replace('3 fichas', f'{len(records)} fichas').replace('tres instrumentos documentados', f'{len(records)} instrumentos documentados')
escribir('museo/index.html', page)
