import { test, expect } from '@playwright/test';
import { hasWebgl, openCity, waitForViewer } from './helpers.js';

const frames = (page) =>
  page.evaluate(() => window.__ciudadesSagradas.viewer.getMetrics().framesRendered);

async function waitForIdle(page) {
  let previous = -1;
  await expect
    .poll(async () => {
      const current = await frames(page);
      const stable = current === previous;
      previous = current;
      return stable;
    }, { timeout: 10_000, intervals: [200] })
    .toBe(true);
}

test('visor: no dibuja con la escena quieta y sí al cambiar la hora', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  test.slow();
  await openCity(page, 'caral', { lod: 1, debug: false });
  await waitForViewer(page);
  await waitForIdle(page);

  const before = await frames(page);
  await page.waitForTimeout(700);
  expect(await frames(page)).toBe(before);

  await page.locator('[data-time="night"]').dispatchEvent('click');
  await expect.poll(() => frames(page), { timeout: 5_000 }).toBeGreaterThan(before);
});

test('visor: la rueda redibuja la escena', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await openCity(page, 'caral', { lod: 1, debug: false });
  await waitForViewer(page);
  await waitForIdle(page);

  const before = await frames(page);
  const box = await page.locator('#city-canvas').boundingBox();
  await page.mouse.move(box.x + box.width * 0.25, box.y + box.height * 0.5);
  await page.mouse.wheel(0, -500);
  await expect.poll(() => frames(page), { timeout: 5_000 }).toBeGreaterThan(before);
});

test('visor: arrastrar con movimiento reducido redibuja', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await openCity(page, 'caral', { lod: 1, debug: false });
  await waitForViewer(page);
  await waitForIdle(page);

  const before = await frames(page);
  const box = await page.locator('#city-canvas').boundingBox();
  const x = box.x + box.width * 0.25;
  const y = box.y + box.height * 0.5;
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x + 120, y + 60, { steps: 8 });
  await page.mouse.up();
  await expect.poll(() => frames(page), { timeout: 5_000 }).toBeGreaterThan(before);
});

test('visor: ?noshadows=1 también queda quieto', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await openCity(page, 'caral', { lod: 1, flags: ['noshadows'], debug: false });
  await waitForViewer(page);
  await waitForIdle(page);

  const before = await frames(page);
  await page.waitForTimeout(700);
  expect(await frames(page)).toBe(before);
});
