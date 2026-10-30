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

const SCENARIOS = [
  { name: 'noground', flags: ['noground'], expected: { noGround: true, noShadows: false } },
  { name: 'noshadows', flags: ['noshadows'], expected: { noGround: false, noShadows: true } },
  { name: 'noground-noshadows', flags: ['noground', 'noshadows'], expected: { noGround: true, noShadows: true } },
];

for (const scenario of SCENARIOS) {
  test(`Caral flag ${scenario.name}`, async ({ page, browserName }, testInfo) => {
    test.skip(browserName !== 'chromium', 'Flags de QA solo en Chromium');
    test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
    const errors = trackConsole(page);
    await openCity(page, 'caral', { lod: 0, flags: scenario.flags });
    await waitForViewer(page);

    const report = await getQaReport(page);
    expect(report?.metrics?.flags).toEqual(scenario.expected);
    await saveQaReport(testInfo, `caral-flags-${scenario.name}`, report);
    expectNoConsoleErrors(errors);
  });
}
