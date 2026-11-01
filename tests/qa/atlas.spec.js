import { readFile } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
import { RESEARCH_CITIES, expectNoConsoleErrors, saveScreenshot, trackConsole } from './helpers.js';

test('atlas: seis ciudades, aviso de preview y badges', async ({ page }, testInfo) => {
  const errors = trackConsole(page);
  await page.goto('/');

  await expect(page.locator('.city-card')).toHaveCount(6);
  await expect(page.locator('.catalog__notice')).toContainText('Preview público');
  await expect(page.locator('.catalog__notice')).toContainText('Caral v2 es la referencia');
  await expect(page.locator('.catalog__notice')).toContainText('Chan Chan y Wari son fichas documentales');
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
  };
  await page.route('**/cities/index.json', (route) =>
    route.fulfill({ json: [payload, ...index.slice(1)] }),
  );
  await page.goto('/');

  await expect(page.locator('.city-card h2').first()).toHaveText('Caral <b>demo</b>');
  await expect(page.locator('.city-card b')).toHaveCount(0);
  await expect(page.locator('.city-card script')).toHaveCount(0);
  expect(await page.evaluate(() => window.__xss)).toBeUndefined();
});

test('ficha documental: escapa datos de city.json', async ({ page }) => {
  const city = JSON.parse(await readFile('public/cities/chan-chan/city.json', 'utf8'));
  city.name = 'Chan <b>Chan</b>';
  city.summary = 'Resumen <script>window.__xss = true</script>';
  city.sources = [{ label: '<em>Fuente</em>', url: 'https://example.com/' }];
  await page.route('**/cities/chan-chan/city.json', (route) =>
    route.fulfill({ json: city }),
  );
  await page.goto('/#/ciudad/chan-chan');

  await expect(page.locator('.research-hero h1')).toHaveText('Chan <b>Chan</b>');
  await expect(page.locator('.research-main b')).toHaveCount(0);
  await expect(page.locator('.research-main script')).toHaveCount(0);
  await expect(page.locator('.source-list em')).toHaveCount(0);
  await expect(page.locator('.source-list a').first()).toContainText('<em>Fuente</em>');
  expect(await page.evaluate(() => window.__xss)).toBeUndefined();
});

test('navegación: atlas a ficha documental y regreso', async ({ page }) => {
  const errors = trackConsole(page);
  await page.goto('/');
  await page.locator('a[href="#/ciudad/chan-chan"]').click();
  await expect(page).toHaveURL(/#\/ciudad\/chan-chan$/);
  await expect(page.locator('.research-hero h1')).toHaveText('Chan Chan');
  await page.locator('.back-link').click();
  await expect(page).toHaveURL(/#\/?$/);
  await expect(page.locator('.city-card')).toHaveCount(6);
  expectNoConsoleErrors(errors);
});
