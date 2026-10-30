import { test, expect } from '@playwright/test';
import {
  CITIES,
  expectNoConsoleErrors,
  getQaReport,
  hasWebgl,
  openCity,
  saveQaReport,
  saveScreenshot,
  trackConsole,
  waitForViewer,
} from './helpers.js';

for (const city of CITIES) {
  test(`${city.name} LOD0: seis paradas, luces, capas e informe QA`, async ({ page }, testInfo) => {
    test.slow();
    test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
    const errors = trackConsole(page);
    await openCity(page, city.id, { lod: 0 });
    await waitForViewer(page);

    await expect(page.locator('.city-heading h1')).toHaveText(city.name);
    if (await page.evaluate(() => window.matchMedia('(max-width: 980px)').matches)) {
      await page.locator('#info-toggle').click();
    }
    await expect(page.locator('.tour-list button')).toHaveCount(6);
    await expect(page.locator('[data-time]')).toHaveCount(4);
    await expect(page.locator('[data-layer]').first()).toBeVisible();
    await saveScreenshot(page, testInfo, `${city.id}-lod0`);

    for (let index = 0; index < 6; index += 1) {
      await page.locator(`[data-tour="${index}"]`).click();
      const title = await page.locator('#tour-title').textContent();
      expect(title?.trim().length).toBeGreaterThan(0);
    }

    for (const time of ['noon', 'dusk', 'night', 'morning']) {
      await page.locator(`[data-time="${time}"]`).click();
      await expect(page.locator(`[data-time="${time}"]`)).toHaveClass(/is-active/);
    }

    const layerInputs = page.locator('[data-layer]');
    for (let index = 0; index < await layerInputs.count(); index += 1) {
      const input = layerInputs.nth(index);
      const checked = await input.isChecked();
      await input.setChecked(!checked);
      await input.setChecked(checked);
    }

    const report = await getQaReport(page);
    expect(report?.schemaVersion).toBe(1);
    expect(report?.metrics?.lod).toBe('0');
    expect(report?.metrics?.modelTriangles).toBeGreaterThan(0);
    expect(report?.environment?.webgl?.renderer).toBeTruthy();

    await saveQaReport(testInfo, `${city.id}-lod0`, report);
    expectNoConsoleErrors(errors);
  });
}
