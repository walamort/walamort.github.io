const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http'), assert = require('assert/strict');
(async () => {
  const root = process.cwd(), out = path.resolve(root, '..', '..', 'outputs');
  fs.mkdirSync(out, { recursive: true });
  const server = http.createServer((req, res) => {
    let file = path.join(root, decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
    try {
      if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
      res.setHeader('Content-Type', ({ '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' })[path.extname(file)] || 'application/octet-stream');
      res.end(fs.readFileSync(file));
    } catch { res.writeHead(404).end(); }
  }).listen(0, '127.0.0.1');
  await new Promise(resolve => server.on('listening', resolve));
  const origin = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const page = await browser.newPage(), errors = [], missing = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => { if (r.url().startsWith(origin) && r.status() >= 400) missing.push(r.url()); });
    await page.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
    for (const width of [320, 390, 768, 1440]) {
      await page.setViewportSize({ width, height: 1000 });
      await page.goto(origin);
      await page.locator('#f-name').filter({ hasText: 'Tongue' }).waitFor();
      const overflow = await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1).map(e => e.tagName + '.' + e.className));
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, width + ': ' + overflow);
      assert.equal(await page.locator('h1').count(), 1);
      await page.screenshot({ path: path.join(out, 'walamort-' + width + '.png'), fullPage: true });
      if (width < 861) {
        await page.locator('.wm-menu-toggle').click();
        assert.equal(await page.locator('.wm-menu-toggle').getAttribute('aria-expanded'), 'true');
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.wm-menu-toggle').getAttribute('aria-expanded'), 'false');
        assert.equal(await page.locator('.wm-menu-toggle').evaluate(e => e === document.activeElement), true);
        await page.locator('.wm-menu-toggle').click();
        await page.locator('#wm-nav-links a[href="#virtuales"]').click();
        assert.equal(await page.locator('.wm-menu-toggle').getAttribute('aria-expanded'), 'false');
      }
      await page.locator('#instrument-search').fill('KALÍMBA');
      assert.equal(await page.locator('.instrument-card:visible').count(), 1);
      await page.locator('#instrument-family').selectOption('percusion');
      assert.equal(await page.locator('.instrument-card:visible').count(), 0);
      assert.equal(await page.locator('#instrument-empty').isVisible(), true);
      await page.getByRole('button', { name: 'Restablecer', exact: true }).click();
      assert.equal(await page.locator('.instrument-card:visible').count(), 3);
      await page.locator('#instrument-family').selectOption('percusion');
      assert.equal(await page.locator('.instrument-card:visible').count(), 2);
      await page.locator('#tab-handpan').click();
      assert.equal(await page.locator('#panel-handpan').isVisible(), true);
      assert.equal(await page.locator('#panel-kalimba').isVisible(), false);
      await page.locator('#tab-handpan').focus();
      await page.keyboard.press('ArrowRight');
      assert.equal(await page.locator('#panel-kalimba').isVisible(), true);
      await page.locator('#nextw').click();
      const slot = page.locator('.slot.free').first();
      await slot.click();
      assert.equal(await slot.getAttribute('aria-pressed'), 'true');
      assert.match(await page.locator('#slotpick').innerText(), /Horario elegido/);
      console.log(width + 'px: no overflow, menu/focus, accent search, combined filters, empty/reset, keyboard store tabs, calendar selection OK');
    }
    await page.goto(origin);
    const links = await page.locator('a[href],img[src],link[href],script[src]').evaluateAll(nodes => nodes.map(n => n.getAttribute('href') || n.getAttribute('src')).filter(u => !/^(https?:|mailto:|tel:)/.test(u)));
    for (const href of links) {
      const u = new URL(href, origin), dest = path.join(root, decodeURIComponent(u.pathname));
      assert.ok(fs.existsSync(dest), 'Missing ' + href);
      if (u.hash) {
        const file = fs.statSync(dest).isDirectory() ? path.join(dest, 'index.html') : dest;
        assert.ok(fs.readFileSync(file, 'utf8').includes('id="' + u.hash.slice(1) + '"'), href);
      }
    }
    for (const slug of ['kalimba', 'handpan', 'tongue-drum']) {
      await page.goto(origin + '/instrumentos/' + slug + '/studio/');
      assert.ok(await page.locator('body').innerText());
    }
    const nojs = await browser.newPage({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } });
    await nojs.goto(origin);
    assert.equal(await nojs.locator('.instrument-card a').count(), 9);
    assert.equal(await nojs.locator('#wm-nav-links').isVisible(), true);
    assert.deepEqual(errors, []);
    assert.deepEqual(missing, []);
    console.log('Local links/assets/fragments, studio pages, no-JS navigation, console errors OK');
  } finally { await browser.close(); server.close(); }
})().catch(e => { console.error(e); process.exit(1); });
