import { test, expect } from '@playwright/test';
import { getQaReport, hasWebgl, waitForViewer } from './helpers.js';

async function openCaralWithoutServiceWorker(page, lod = 0) {
  await page.goto(`/?nosw=1&lod=${lod}&qa=1#/ciudad/caral`);
}

test('visor: si falla LOD0 carga LOD1', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  await page.route('**/model_lod0.glb', (route) => route.abort());

  await openCaralWithoutServiceWorker(page, 0);
  await waitForViewer(page);

  const report = await getQaReport(page);
  expect(report?.metrics?.lod).toBe('1');
  expect(report?.metrics?.modelUrl).toContain('model_lod1.glb');
  expect(pageErrors).toEqual([]);
});

test('visor: si fallan LOD0 y LOD1 carga el fallback v1', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  await page.route('**/model_lod0.glb', (route) => route.abort());
  await page.route('**/model_lod1.glb', (route) => route.abort());

  await openCaralWithoutServiceWorker(page, 0);
  await waitForViewer(page);

  const report = await getQaReport(page);
  expect(report?.metrics?.lod).toBe('v1');
  expect(report?.metrics?.modelUrl).toContain('/model.glb');
  expect(pageErrors).toEqual([]);
});
