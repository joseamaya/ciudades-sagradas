import { test, expect } from '@playwright/test';
import { hasWebgl, waitForViewer } from './helpers.js';

test('visor: salir durante la carga no añade el modelo ni renderiza tras dispose', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const errors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', (error) => errors.push(error.message));

  let release;
  const gate = new Promise((resolve) => {
    release = resolve;
  });
  await page.route('**/*.glb', async (route) => {
    await gate;
    await route.continue();
  });

  const modelRequest = page.waitForRequest(/model_lod1\.glb/);
  await page.goto('/?nosw=1&lod=1&qa=1#/ciudad/caral');
  await modelRequest;
  await page.waitForFunction(() => Boolean(window.__ciudadesSagradas?.viewer));
  const viewer = await page.evaluateHandle(() => window.__ciudadesSagradas.viewer);

  await page.evaluate(() => {
    window.location.hash = '#/';
  });
  await expect(page.locator('.city-card')).toHaveCount(6);
  release();
  await page.waitForTimeout(1500);

  const state = await viewer.evaluate((instance) => ({
    destroyed: instance._destroyed,
    model: instance.model,
    meshes: instance.meshes.length,
  }));
  expect(state.destroyed).toBe(true);
  expect(state.model).toBeNull();
  expect(state.meshes).toBe(0);
  expect(await page.evaluate(() => window.__ciudadesSagradas.viewer)).toBeNull();
  expect(errors).toEqual([]);

  await page.evaluate(() => {
    window.location.hash = '#/ciudad/caral';
  });
  await waitForViewer(page);
  expect(errors).toEqual([]);
});
