import { test, expect } from '@playwright/test';
import {
  CITIES,
  hasWebgl,
  openCity,
  saveScreenshot,
  waitForViewer,
} from './helpers.js';

test('atlas: captura de referencia', async ({ page }, testInfo) => {
  await page.goto('/');
  await expect(page.locator('.city-card')).toHaveCount(6);
  await saveScreenshot(page, testInfo, 'atlas');
});

for (const city of CITIES) {
  test(`${city.name}: captura LOD0`, async ({ page }, testInfo) => {
    test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
    await openCity(page, city.id, { lod: 0, debug: false });
    await waitForViewer(page);
    if (await page.evaluate(() => window.matchMedia('(max-width: 980px)').matches)) {
      await page.locator('#info-toggle').click();
      await page.waitForTimeout(300);
    }
    await saveScreenshot(page, testInfo, `${city.id}-lod0`);
  });
}
