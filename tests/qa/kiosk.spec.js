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

test('kiosco: Caral con clase kiosk y seis paradas', async ({ page, browserName }, testInfo) => {
  test.skip(browserName !== 'chromium', 'Kiosco solo en Chromium');
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const errors = trackConsole(page);
  await openCity(page, 'caral', { lod: 0, flags: ['kiosk'] });
  await waitForViewer(page);

  await expect(page.locator('body')).toHaveClass(/kiosk/);
  await expect(page.locator('.tour-list button')).toHaveCount(6);
  await saveQaReport(testInfo, 'caral-kiosk-lod0', await getQaReport(page));
  expectNoConsoleErrors(errors);
});
