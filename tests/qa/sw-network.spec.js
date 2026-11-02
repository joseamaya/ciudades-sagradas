import { test, expect } from '@playwright/test';
import { hasWebgl, waitForViewer } from './helpers.js';

test('service worker: red lenta cae a caché y no guarda respuestas 206', async ({ page, context, browserName }) => {
  test.slow();
  test.skip(browserName !== 'chromium', 'Service worker y CDP solo en Chromium');
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const errors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', (error) => errors.push(error.message));

  await page.goto('/?qa=1&lod=1#/ciudad/caral');
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
          const urls = (await cache.keys()).map((request) => request.url);
          return (
            urls.some((url) => url.includes('model_lod1.glb')) &&
            urls.some((url) => url.includes('city.json')) &&
            urls.some((url) => url.includes('index.json'))
          );
        }),
      { timeout: 45_000, intervals: [500, 1000, 2000] },
    )
    .toBe(true);

  const cdp = await context.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions', {
    offline: false,
    latency: 12_000,
    downloadThroughput: 50 * 1024,
    uploadThroughput: 50 * 1024,
  });

  try {
    const atlasStarted = Date.now();
    await page.goto('/?qa=1#/');
    await expect(page.locator('.city-card')).toHaveCount(6, { timeout: 6000 });
    expect(Date.now() - atlasStarted).toBeLessThan(6000);

    const cityStarted = Date.now();
    await page.goto('/?qa=1&lod=1#/ciudad/caral');
    await waitForViewer(page);
    expect(Date.now() - cityStarted).toBeLessThan(12_000);
  } finally {
    await cdp.send('Network.emulateNetworkConditions', {
      offline: false,
      latency: 0,
      downloadThroughput: -1,
      uploadThroughput: -1,
    });
  }

  const rangeResult = await page.evaluate(async () => {
    const url = new URL('cities/caral/model_lod1.glb?range-test=1', location.href).href;
    const response = await fetch(url, { headers: { Range: 'bytes=0-1023' } });
    const names = await caches.keys();
    const name = names.find((item) => item.startsWith('ciudades-sagradas-'));
    if (!name) return { status: response.status, cached: false };
    const cache = await caches.open(name);
    return { status: response.status, cached: Boolean(await cache.match(url)) };
  });

  if (rangeResult.status === 206) {
    expect(rangeResult.cached).toBe(false);
  }
  expect(errors).toEqual([]);
});
