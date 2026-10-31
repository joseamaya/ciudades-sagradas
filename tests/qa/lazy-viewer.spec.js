import { readdir } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
import { hasWebgl, waitForViewer } from './helpers.js';

async function viewerChunkName() {
  const files = await readdir('dist/assets');
  const name = files.find((file) => /^viewer-.*\.js$/.test(file));
  if (!name) throw new Error('El build no generó el chunk diferido viewer-*.js');
  return name;
}

test('catálogo no descarga el visor; la ciudad sí', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const chunk = await viewerChunkName();

  const requests = [];
  page.on('request', (request) => requests.push(request.url()));
  await page.goto('/?nosw=1');
  await expect(page.locator('.city-card')).toHaveCount(6);
  expect(requests.some((url) => url.includes(chunk))).toBe(false);

  await page.locator('a[href="#/ciudad/caral"]').click();
  await waitForViewer(page);
  expect(requests.some((url) => url.includes(chunk))).toBe(true);
});

test('fallo del chunk del visor: estado recuperable', async ({ page }) => {
  const chunk = await viewerChunkName();

  await page.route(`**/assets/${chunk}`, (route) => route.abort());
  await page.goto('/?nosw=1#/ciudad/caral');
  await expect(page.locator('.city-error')).toBeVisible({ timeout: 60_000 });
  await expect(page.locator('.city-error__title')).toContainText('Caral');
});
