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
  for (const lod of [0, 1]) {
    test(`${city.name} LOD${lod}: informe QA de referencia`, async ({ page }, testInfo) => {
      test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
      const errors = trackConsole(page);
      await openCity(page, city.id, { lod });
      await waitForViewer(page);

      const report = await getQaReport(page);
      expect(report?.schemaVersion).toBe(1);
      expect(report?.metrics?.lod).toBe(String(lod));
      expect(report?.metrics?.modelTriangles).toBeGreaterThan(0);
      expect(report?.environment?.webgl?.renderer).toBeTruthy();

      await saveQaReport(testInfo, `${city.id}-lod${lod}`, report);
      expectNoConsoleErrors(errors);
    });
  }
}
