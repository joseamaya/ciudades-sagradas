import { test, expect } from '@playwright/test';
import {
  expectNoConsoleErrors,
  getQaReport,
  hasWebgl,
  openCity,
  saveQaReport,
  trackConsole,
  waitForViewer,
} from './helpers.js';

test('Caral offline tras cachear el modelo', async ({ page, context, browserName }, testInfo) => {
  test.skip(browserName !== 'chromium', 'Offline solo en Chromium');
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const errors = trackConsole(page);
  await openCity(page, 'caral', { lod: 0 });
  await waitForViewer(page);

  await page.evaluate(() => navigator.serviceWorker.ready);
  await expect
    .poll(
      async () =>
        page.evaluate(async () => {
          const names = await caches.keys();
          const name = names.find((item) => item.startsWith('ciudades-sagradas-'));
          if (!name) return false;
          const cache = await caches.open(name);
          const requests = await cache.keys();
          return requests.some((request) => request.url.includes('model_lod0.glb'));
        }),
      { timeout: 45_000, intervals: [500, 1000, 2000] },
    )
    .toBe(true);

  try {
    await context.setOffline(true);
    await page.reload();
    await waitForViewer(page);
    const report = await getQaReport(page);
    expect(report?.metrics?.ready).toBe(true);
    await saveQaReport(testInfo, 'caral-offline-lod0', report);
    expectNoConsoleErrors(errors);
  } finally {
    await context.setOffline(false);
  }
});
