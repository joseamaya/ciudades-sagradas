import { test, expect } from '@playwright/test';
import { expectNoConsoleErrors, trackConsole } from './helpers.js';

test('API QA solo se expone con debug o qa', async ({ page }) => {
  const errors = trackConsole(page);

  await page.goto('/?nosw=1');
  expect(await page.evaluate(() => typeof window.__ciudadesSagradas)).toBe('undefined');

  await page.goto('/?nosw=1&qa=1');
  expect(await page.evaluate(() => typeof window.__ciudadesSagradas?.qaReport)).toBe('function');

  await page.goto('/?nosw=1&debug=1');
  expect(await page.evaluate(() => typeof window.__ciudadesSagradas?.qaReport)).toBe('function');

  expectNoConsoleErrors(errors);
});
