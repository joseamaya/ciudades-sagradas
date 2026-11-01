import { test, expect } from '@playwright/test';
import { expectNoConsoleErrors, hasWebgl, openCity, trackConsole, waitForViewer } from './helpers.js';

test('ficha: semántica del panel y controles con estado', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  const errors = trackConsole(page);
  await openCity(page, 'caral', { lod: 1 });
  await waitForViewer(page);

  const canvas = page.locator('#city-canvas');
  await expect(canvas).toHaveAttribute('role', 'img');
  await expect(canvas).toHaveAttribute('aria-describedby', 'city-canvas-help');
  await expect(page.locator('#city-canvas-help')).toHaveClass(/sr-only/);

  const toggle = page.locator('#info-toggle');
  const panel = page.locator('#city-panel');
  const mobile = await page.evaluate(() => window.matchMedia('(max-width: 980px)').matches);
  await expect(toggle).toHaveAttribute('aria-controls', 'city-panel');
  await expect(toggle).toHaveAttribute('aria-expanded', String(!mobile));
  await expect(panel).toHaveAttribute('aria-hidden', String(mobile));
  if (mobile) await expect(panel).toHaveAttribute('inert', '');

  if (mobile) {
    await toggle.dispatchEvent('click');
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(panel).toHaveAttribute('aria-hidden', 'false');
  } else {
    await toggle.dispatchEvent('click');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(panel).toHaveAttribute('inert', '');
    await expect(panel).toHaveAttribute('aria-hidden', 'true');
    await toggle.dispatchEvent('click');
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(panel).not.toHaveAttribute('inert', '');
  }

  await expect(page.locator('[data-time="morning"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-tour="0"]')).toHaveAttribute('aria-current', 'true');
  await page.locator('[data-time="night"]').dispatchEvent('click');
  await expect(page.locator('[data-time="night"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-time="morning"]')).toHaveAttribute('aria-pressed', 'false');

  expectNoConsoleErrors(errors);
});

test('movimiento reducido: sin amortiguación ni vuelo animado', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await openCity(page, 'caral', { lod: 1 });
  await waitForViewer(page);
  const state = await page.evaluate(() => {
    const viewer = window.__ciudadesSagradas?.viewer;
    return {
      reducedMotion: viewer?.reducedMotion,
      damping: viewer?.controls?.enableDamping,
    };
  });
  expect(state.reducedMotion).toBe(true);
  expect(state.damping).toBe(false);
});

test('teclado: modificadores y controles no cambian de parada', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await openCity(page, 'caral', { lod: 1 });
  await waitForViewer(page);

  const mobile = await page.evaluate(() => window.matchMedia('(max-width: 980px)').matches);
  if (mobile) await page.locator('#info-toggle').click();

  const title = page.locator('#tour-title');
  const before = await title.textContent();

  await page.evaluate(() => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', altKey: true }));
  });
  await expect(title).toHaveText(before);

  await page.locator('[data-layer]').first().focus();
  await page.keyboard.press('ArrowRight');
  await page.keyboard.press('ArrowLeft');
  await expect(title).toHaveText(before);

  await page.keyboard.press('Control+h');
  await expect(page.locator('body')).not.toHaveClass(/ui-hidden/);

  await page.evaluate(() => document.activeElement?.blur());
  await page.keyboard.press('h');
  await expect(page.locator('body')).toHaveClass(/ui-hidden/);
});

test('teclado: Escape cierra la ficha antes de salir', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await openCity(page, 'caral', { lod: 1 });
  await waitForViewer(page);

  if (await page.evaluate(() => window.matchMedia('(max-width: 980px)').matches)) {
    await page.locator('#info-toggle').click();
  }
  await expect(page.locator('#info-toggle')).toHaveAttribute('aria-expanded', 'true');

  await page.keyboard.press('Escape');
  await expect(page.locator('#info-toggle')).toHaveAttribute('aria-expanded', 'false');
  await page.keyboard.press('Escape');
  await expect(page).toHaveURL(/#\/?$/);
});

test('recorrido: texto completo legible a 375 px', async ({ page }) => {
  test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
  await page.setViewportSize({ width: 375, height: 812 });
  await openCity(page, 'caral', { lod: 1 });
  await waitForViewer(page);

  const state = await page.locator('#tour-text').evaluate((element) => {
    const style = getComputedStyle(element);
    return {
      clamp: style.webkitLineClamp,
      scrollHeight: element.scrollHeight,
      clientHeight: element.clientHeight,
      text: element.textContent,
    };
  });
  const expected = await page.evaluate(
    () => window.__ciudadesSagradas?.city?.tour?.[0]?.text ?? '',
  );

  expect(state.clamp === 'none' || state.clamp === '').toBe(true);
  expect(state.text).toBe(expected);
  expect(state.text.length).toBeGreaterThan(140);
  expect(state.scrollHeight).toBeLessThanOrEqual(state.clientHeight + 1);
});

test('fallo de modelo: muestra estado recuperable', async ({ page }) => {
  await page.route('**/cities/caral/*.glb', (route) => route.abort());
  await openCity(page, 'caral', { lod: 0, flags: ['nosw'] });
  await expect(page.locator('.city-error')).toBeVisible({ timeout: 60_000 });
  await expect(page.locator('.city-error__title')).toContainText('Caral');
  await expect(page.locator('.city-error button')).toHaveText('Reintentar');
  await expect(page.locator('.city-error a')).toHaveAttribute('href', '#/');
});
