import { test, expect } from '@playwright/test';
import { RESEARCH_CITIES, expectNoConsoleErrors, saveScreenshot, trackConsole } from './helpers.js';

test('atlas: seis ciudades, aviso de preview y badges', async ({ page }, testInfo) => {
  const errors = trackConsole(page);
  await page.goto('/');

  await expect(page.locator('.city-card')).toHaveCount(6);
  await expect(page.locator('.catalog__notice')).toContainText('Preview público');
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
    expectNoConsoleErrors(errors);
  });
}

test('navegación: atlas a Caral y regreso', async ({ page }) => {
  const errors = trackConsole(page);
  await page.goto('/');
  await page.locator('a[href="#/ciudad/caral"]').click();
  await expect(page).toHaveURL(/#\/ciudad\/caral$/);
  await expect(page.locator('.city-heading h1')).toHaveText('Caral');
  await page.locator('.back-link').click();
  await expect(page).toHaveURL(/#\/?$/);
  await expect(page.locator('.city-card')).toHaveCount(6);
  expectNoConsoleErrors(errors);
});
