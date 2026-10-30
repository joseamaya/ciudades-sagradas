import { test, expect } from '@playwright/test';
import {
  CITIES,
  expectNoConsoleErrors,
  getQaReport,
  hasWebgl,
  openCity,
  saveQaReport,
  trackConsole,
  waitForViewer,
} from './helpers.js';

for (const city of CITIES) {
  test(`${city.name} LOD1: carga forzada e informe QA`, async ({ page }, testInfo) => {
    test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
    const errors = trackConsole(page);
    await openCity(page, city.id, { lod: 1 });
    await waitForViewer(page);

    const report = await getQaReport(page);
    expect(report?.metrics?.lod).toBe('1');
    expect(report?.metrics?.modelTriangles).toBeGreaterThan(0);
    expect(report?.environment?.webgl?.renderer).toBeTruthy();

    await saveQaReport(testInfo, `${city.id}-lod1`, report);
    expectNoConsoleErrors(errors);
  });
}
