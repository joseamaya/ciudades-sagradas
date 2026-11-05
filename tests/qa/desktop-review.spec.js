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

const TIMES = ['morning', 'noon', 'dusk', 'night'];

async function captureTour(page, testInfo, city, lod, prefix) {
  await saveScreenshot(page, testInfo, `${prefix}-${city.id}-lod${lod}-hero`);
  for (let index = 1; index < 6; index += 1) {
    await page.locator('#tour-next').click();
    await page.waitForTimeout(150);
    const title = await page.locator('#tour-title').textContent();
    expect(title?.trim().length).toBeGreaterThan(0);
    await saveScreenshot(page, testInfo, `${prefix}-${city.id}-lod${lod}-stop${index + 1}`);
  }
}

for (const city of CITIES) {
  test(`${city.name}: revisión desktop 1600×900`, async ({ page }, testInfo) => {
    test.slow();
    test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
    await page.emulateMedia({ reducedMotion: 'reduce' });
    const errors = trackConsole(page);
    await openCity(page, city.id, { lod: 0 });
    await waitForViewer(page);

    await expect(page.locator('#city-canvas')).toBeVisible();
    expect(await page.locator('[data-layer]').count()).toBeGreaterThanOrEqual(4);
    await expect(page.locator('[data-time]')).toHaveCount(4);
    await expect(page.locator('[data-tour]')).toHaveCount(6);

    await captureTour(page, testInfo, city, 0, '1600');

    const report = await getQaReport(page);
    expect(report?.metrics?.ready).toBe(true);
    expect(report?.metrics?.lod).toBe('0');
    expect(report?.metrics?.calls).toBeGreaterThan(0);
    expect(report?.metrics?.modelTriangles).toBeGreaterThan(0);
    await saveQaReport(testInfo, `${city.id}-desktop-1600`, report);

    const layers = page.locator('[data-layer]');
    const layerCount = await layers.count();
    for (let index = 0; index < layerCount; index += 1) {
      const layer = layers.nth(index);
      const before = await layer.isChecked();
      await layer.click();
      await expect(layer).toBeChecked({ checked: !before });
      await layer.click();
      await expect(layer).toBeChecked({ checked: before });
    }

    for (const time of TIMES) {
      const button = page.locator(`[data-time="${time}"]`);
      await button.click();
      await expect(button).toHaveAttribute('aria-pressed', 'true');
    }
    await page.locator('[data-time="morning"]').click();

    expectNoConsoleErrors(errors);
  });
}

for (const city of CITIES.filter((item) => ['chan-chan', 'wari'].includes(item.id))) {
  for (const lod of ['0', '1']) {
    test(`${city.name} LOD${lod}: revisión desktop 1920×1080`, async ({ page }, testInfo) => {
      test.slow();
      test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
      await page.emulateMedia({ reducedMotion: 'reduce' });
      const errors = trackConsole(page);
      await openCity(page, city.id, { lod });
      await waitForViewer(page);

      await expect(page.locator('#city-canvas')).toBeVisible();
      await expect(page.locator('[data-tour]')).toHaveCount(6);
      await captureTour(page, testInfo, city, lod, '1080');

      const report = await getQaReport(page);
      expect(report?.metrics?.ready).toBe(true);
      expect(report?.metrics?.lod).toBe(lod);
      expect(report?.metrics?.calls).toBeGreaterThan(0);
      await saveQaReport(testInfo, `${city.id}-desktop-1080-lod${lod}`, report);
      expectNoConsoleErrors(errors);
    });
  }
}
