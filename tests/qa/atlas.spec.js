import { readFile } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
import { RESEARCH_CITIES, expectNoConsoleErrors, saveScreenshot, trackConsole } from './helpers.js';

test('atlas: seis ciudades, aviso de preview y badges', async ({ page }, testInfo) => {
  const errors = trackConsole(page);
  await page.goto('/');

  await expect(page.locator('.city-card')).toHaveCount(6);
  await expect(page.locator('.catalog__notice')).toContainText('Preview público');
  await expect(page.locator('.catalog__notice')).toContainText('Caral v2 es la referencia');
  await expect(page.locator('.catalog__notice')).toContainText('La QA de hardware está en curso');
  await expect(page.locator('.catalog__stats')).toContainText('6');
  await expect(page.locator('.catalog__stats')).toContainText('5000');
  await expect(page.locator('.city-card__status')).toHaveCount(6);
  await expect(page.locator('.city-card .badge')).toHaveCount(6);
  await saveScreenshot(page, testInfo, 'atlas');
  expectNoConsoleErrors(errors);
});

for (const city of RESEARCH_CITIES) {
  test(`${city.name}: ficha documental sin canvas`, async ({ page }) => {
    const errors = trackConsole(page);
    await page.goto(`/#/ciudad/${city.id}`);

    await expect(page.locator('.city-view--research h1')).toHaveText(city.name);
    await expect(page.locator('#city-canvas')).toHaveCount(0);
    await expect(page.locator('.research-status .status-badge')).toHaveCount(2);
    await expect(page.locator('.research-note h2')).toContainText('reconstrucción 3D');
    await expect(page.locator('.research-sources a').first()).toBeVisible();
    await expect(page.locator('.disclaimer')).not.toBeEmpty();
    await expect(page.locator('.credits')).not.toBeEmpty();
    expectNoConsoleErrors(errors);
  });
}

test('catálogo: escapa datos de index.json', async ({ page }) => {
  const index = JSON.parse(await readFile('public/cities/index.json', 'utf8'));
  const payload = {
    ...index[0],
    name: 'Caral <b>demo</b>',
    summary: 'Resumen <script>window.__xss = true</script>',
    accent: 'red; background: url(javascript:window.__xss = true)',
    thumb: "x') ; background: url(javascript:window.__xss = true) ; ('",
  };
  await page.route('**/cities/index.json', (route) =>
    route.fulfill({ json: [payload, ...index.slice(1)] }),
  );
  await page.goto('/');

  await expect(page.locator('.city-card h2').first()).toHaveText('Caral <b>demo</b>');
  await expect(page.locator('.city-card b')).toHaveCount(0);
  await expect(page.locator('.city-card script')).toHaveCount(0);
  const mediaStyle = await page.locator('.city-card__media').first().getAttribute('style');
  expect(mediaStyle).not.toContain('javascript');
  expect(await page.evaluate(() => window.__xss)).toBeUndefined();
});

test('ficha documental: escapa datos de city.json', async ({ page }) => {
  const index = JSON.parse(await readFile('public/cities/index.json', 'utf8'));
  const city = JSON.parse(await readFile('public/cities/wari/city.json', 'utf8'));
  Object.assign(city, {
    availability: 'research',
    maturity: 'research',
    evidence: 'not-applicable',
    qa: 'not-applicable',
    model: null,
    lod: undefined,
    fallbackModel: undefined,
    tour: undefined,
    layers: undefined,
    camera: undefined,
  });
  city.name = 'Wari <b>demo</b>';
  city.summary = 'Resumen <script>window.__xss = true</script>';
  city.accent = 'red; background: url(javascript:window.__xss = true)';
  city.sources = [{ label: '<em>Fuente</em>', url: 'javascript:window.__xss = true' }];
  const entry = index.find((item) => item.id === 'wari');
  const researchEntry = {
    ...entry,
    availability: 'research',
    maturity: 'research',
    evidence: 'not-applicable',
    qa: 'not-applicable',
    version: undefined,
    thumb: null,
  };
  await page.route('**/cities/index.json', (route) =>
    route.fulfill({ json: index.map((item) => (item.id === 'wari' ? researchEntry : item)) }),
  );
  await page.route('**/cities/wari/city.json', (route) =>
    route.fulfill({ json: city }),
  );
  await page.goto('/#/ciudad/wari');

  await expect(page.locator('.research-hero h1')).toHaveText('Wari <b>demo</b>');
  await expect(page.locator('.research-main b')).toHaveCount(0);
  await expect(page.locator('.research-main script')).toHaveCount(0);
  await expect(page.locator('.source-list em')).toHaveCount(0);
  await expect(page.locator('.source-list a').first()).toContainText('<em>Fuente</em>');
  await expect(page.locator('.source-list a').first()).toHaveAttribute('href', '#');
  const cityStyle = await page.locator('.city-view').first().getAttribute('style');
  expect(cityStyle).not.toContain('javascript');
  expect(await page.evaluate(() => window.__xss)).toBeUndefined();
});

test('navegación: atlas a ciudad y regreso', async ({ page }) => {
  const errors = trackConsole(page);
  await page.goto('/');
  await page.locator('a[href="#/ciudad/wari"]').click();
  await expect(page).toHaveURL(/#\/ciudad\/wari$/);
  await expect(page.locator('.city-heading h1')).toHaveText('Wari');
  await page.locator('.back-link').click();
  await expect(page).toHaveURL(/#\/?$/);
  await expect(page.locator('.city-card')).toHaveCount(6);
  expectNoConsoleErrors(errors);
});
