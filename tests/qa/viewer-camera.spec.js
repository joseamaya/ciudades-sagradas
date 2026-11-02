import { test, expect } from '@playwright/test';
import {
  CITIES,
  expectNoConsoleErrors,
  hasWebgl,
  openCity,
  saveScreenshot,
  trackConsole,
  waitForViewer,
} from './helpers.js';

const LODS = ['0', '1'];
const MAX_NEAR = 0.3;
const MIN_FAR = 200;
const MAX_DEPTH_RATIO = 5000;
const MAX_DEPTH_RATIO_DEFAULT_NEAR = 1200;

for (const city of CITIES) {
  for (const lod of LODS) {
    test(`${city.name} LOD${lod}: rango de cámara y seis paradas`, async ({ page }, testInfo) => {
      test.slow();
      test.skip(!(await hasWebgl(page)), 'WebGL no disponible en este navegador headless');
      await page.emulateMedia({ reducedMotion: 'reduce' });
      const errors = trackConsole(page);
      await openCity(page, city.id, { lod, debug: false });
      await waitForViewer(page);

      const info = await page.evaluate(() => {
        const viewer = window.__ciudadesSagradas.viewer;
        const city = window.__ciudadesSagradas.city;
        const stopDistances = city.tour.map((stop) => {
          const [px, py, pz] = stop.camera.position;
          const [tx, ty, tz] = stop.camera.target;
          return Math.hypot(px - tx, py - ty, pz - tz);
        });
        const minStopDistance = Math.min(...stopDistances);
        const expectedNear = city.camera?.near
          ?? Math.max(0.01, Math.min(0.3, minStopDistance / 3));
        return {
          near: viewer.camera.near,
          far: viewer.camera.far,
          fogFar: city.fog?.far ?? viewer.scene.fog.far,
          minDistance: viewer.controls.minDistance,
          maxDistance: viewer.controls.maxDistance,
          minStopDistance,
          expectedNear,
        };
      });

      const depthRatio = info.far / info.near;
      expect(info.near).toBeCloseTo(info.expectedNear, 5);
      expect(info.near).toBeLessThanOrEqual(MAX_NEAR);
      expect(info.far).toBeGreaterThanOrEqual(MIN_FAR);
      expect(info.far).toBeGreaterThanOrEqual(info.fogFar);
      expect(depthRatio).toBeLessThan(
        info.expectedNear >= MAX_NEAR ? MAX_DEPTH_RATIO_DEFAULT_NEAR : MAX_DEPTH_RATIO,
      );
      expect(info.minStopDistance).toBeGreaterThan(info.near * 2);

      await saveScreenshot(page, testInfo, `${city.id}-lod${lod}-stop1`);
      for (let index = 1; index < 6; index += 1) {
        await page.locator('#tour-next').click();
        await page.waitForTimeout(150);
        await saveScreenshot(page, testInfo, `${city.id}-lod${lod}-stop${index + 1}`);
      }

      expectNoConsoleErrors(errors);
    });
  }
}
