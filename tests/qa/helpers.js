import { expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

export const CITIES = [
  { id: 'caral', name: 'Caral' },
  { id: 'chavin', name: 'Chavín de Huántar' },
  { id: 'aypate', name: 'Aypate' },
  { id: 'narihuala', name: 'Narihualá' },
];

export const RESEARCH_CITIES = [
  { id: 'chan-chan', name: 'Chan Chan' },
  { id: 'wari', name: 'Wari' },
];

const QA_DIR = 'qa-output/qa-reports';
const SHOT_DIR = 'qa-output/qa-shots';

export function trackConsole(page) {
  const errors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', (error) => errors.push(error.message));
  return errors;
}

export function expectNoConsoleErrors(errors) {
  expect(errors, 'Errores de consola o excepciones de página').toEqual([]);
}

export async function openCity(page, id, { lod, flags = [], debug = true } = {}) {
  const params = new URLSearchParams();
  if (debug) params.set('debug', '1');
  if (lod !== undefined) params.set('lod', String(lod));
  for (const flag of flags) params.set(flag, '1');
  const query = params.toString();
  await page.goto(`/${query ? `?${query}` : ''}#/ciudad/${id}`);
}

export async function waitForViewer(page) {
  await page.waitForFunction(
    () => Boolean(window.__ciudadesSagradas?.viewer?.model),
    null,
    { timeout: 90_000 },
  );
  await expect(page.locator('#loading')).toBeHidden({ timeout: 90_000 });
}

export async function getQaReport(page) {
  return page.evaluate(() => window.__ciudadesSagradas?.qaReport?.() ?? null);
}

export async function saveQaReport(testInfo, name, report) {
  const body = JSON.stringify(report, null, 2);
  await mkdir(QA_DIR, { recursive: true });
  const file = path.join(QA_DIR, `${testInfo.project.name}_${name}.json`);
  await writeFile(file, `${body}\n`);
  await testInfo.attach(`${name}.json`, { body, contentType: 'application/json' });
  return file;
}

export async function saveScreenshot(page, testInfo, name) {
  await mkdir(SHOT_DIR, { recursive: true });
  const file = path.join(SHOT_DIR, `${testInfo.project.name}_${name}.png`);
  await page.screenshot({ path: file, fullPage: false, timeout: 90_000 });
  await testInfo.attach(`${name}.png`, { path: file, contentType: 'image/png' });
  return file;
}

export async function hasWebgl(page) {
  return page.evaluate(() => {
    const canvas = document.createElement('canvas');
    return Boolean(canvas.getContext('webgl2') || canvas.getContext('webgl'));
  });
}
