import { test, expect } from '@playwright/test';
import { hasWebgl, waitForViewer } from './helpers.js';

const CYCLES = 22;

test('visor: abrir y cerrar la ciudad 22 veces no agota los contextos WebGL', async ({ page }) => {
  test.slow();
  test.setTimeout(480_000);
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const messages = [];
  page.on('console', (message) => {
    if (message.type() === 'warning' || message.type() === 'error') messages.push(message.text());
  });
  page.on('pageerror', (error) => messages.push(error.message));

  await page.goto('/?nosw=1&lod=1&noshadows=1&qa=1');
  await expect(page.locator('.city-card')).toHaveCount(6);

  for (let index = 0; index < CYCLES; index += 1) {
    await page.evaluate(() => {
      window.location.hash = '#/ciudad/narihuala';
    });
    await waitForViewer(page);
    await page.evaluate(() => {
      window.location.hash = '#/';
    });
    await expect(page.locator('.city-card')).toHaveCount(6);
    await page.waitForTimeout(50);
  }

  await page.evaluate(() => {
    window.location.hash = '#/ciudad/narihuala';
  });
  await waitForViewer(page);

  expect(messages.filter((message) => /too many active webgl contexts/i.test(message))).toEqual([]);
});
