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

test('Caral: selección automática de LOD por perfil', async ({ page }, testInfo) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const mobile = ['chromium-mobile', 'webkit-mobile'].includes(testInfo.project.name);
  const errors = trackConsole(page);
  await openCity(page, 'caral');
  await waitForViewer(page);

  const report = await getQaReport(page);
  expect(report?.metrics?.lowPower).toBe(mobile);
  expect(report?.metrics?.lod).toBe(mobile ? '1' : '0');
  await saveQaReport(testInfo, `caral-auto-${mobile ? 'mobile' : 'desktop'}`, report);
  expectNoConsoleErrors(errors);
});
