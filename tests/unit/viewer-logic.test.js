import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  buildModelCandidates,
  classify,
  deviceProfile,
  isDoubleSided,
  isSingleSided,
  layerFor,
  materialKey,
  selectLodLevel,
} from '../../src/core/viewer-logic.js';

const CITY = {
  model: 'cities/demo/model_lod0.glb',
  fallbackModel: 'cities/demo/model.glb',
  lod: { default: 'auto', levels: { '0': 'cities/demo/model_lod0.glb', '1': 'cities/demo/model_lod1.glb' } },
};

test('selectLodLevel usa LOD0 en escritorio y LOD1 en móvil', () => {
  assert.equal(selectLodLevel(CITY, false), '0');
  assert.equal(selectLodLevel(CITY, true), '1');
});

test('selectLodLevel respeta ?lod, default fijo y ausencia de niveles', () => {
  assert.equal(selectLodLevel(CITY, true, '?lod=0'), '0');
  assert.equal(selectLodLevel(CITY, false, '?lod=1'), '1');
  assert.equal(selectLodLevel(CITY, false, '?lod=2'), '0');
  assert.equal(selectLodLevel({ ...CITY, lod: { default: '1', levels: CITY.lod.levels } }, false), '1');
  assert.equal(selectLodLevel({ ...CITY, lod: { default: 'missing', levels: CITY.lod.levels } }, false), '0');
  assert.equal(selectLodLevel({}, false), null);
});

test('buildModelCandidates mantiene orden y deduplica URLs', () => {
  assert.deepEqual(
    buildModelCandidates(CITY, false).map((item) => item.url),
    [
      'cities/demo/model_lod0.glb',
      'cities/demo/model_lod1.glb',
      'cities/demo/model.glb',
    ],
  );
  assert.deepEqual(
    buildModelCandidates(CITY, true).map((item) => item.url),
    [
      'cities/demo/model_lod1.glb',
      'cities/demo/model.glb',
      'cities/demo/model_lod0.glb',
    ],
  );
  assert.deepEqual(
    buildModelCandidates(
      { model: 'cities/demo/model_lod0.glb', fallbackModel: 'cities/demo/model_lod0.glb', lod: CITY.lod },
      false,
    ).map((item) => item.url),
    ['cities/demo/model_lod0.glb', 'cities/demo/model_lod1.glb'],
  );
});

test('buildModelCandidates no devuelve candidatos vacíos', () => {
  assert.deepEqual(buildModelCandidates({}, false), []);
});

test('classify reconoce terreno, props, referencia y ciudad', () => {
  assert.equal(classify('GEO-Caral_Terrain_01'), 'terrain');
  assert.equal(classify('MESH-Caral_Props_StoneBlock'), 'props');
  assert.equal(classify('GEO-Caral_Reference_HumanScale'), 'reference');
  assert.equal(classify('GEO-Caral_PlazaMayor'), 'city');
  assert.equal(classify(''), 'city');
});

test('layerFor busca en el objeto y en sus padres', () => {
  const parent = { userData: { layer: 'terrain' } };
  const child = { parent, userData: {} };
  assert.equal(layerFor(child), 'terrain');
  assert.equal(layerFor({ userData: { layer: 'city' } }), 'city');
  assert.equal(layerFor({ userData: { layer: '' }, parent: null }), null);
  assert.equal(layerFor(null), null);
});

test('materialKey e isDoubleSided aplican las reglas del visor', () => {
  assert.equal(materialKey({ name: 'MAT_Leaf.001' }), 'MAT_Leaf');
  assert.equal(materialKey(null), '');
  assert.equal(isDoubleSided({ name: 'MAT_Leaf' }), true);
  assert.equal(isDoubleSided({ name: 'MAT_Water' }), false);
  assert.equal(isDoubleSided({ name: 'MAT_LOD1_Stone' }), false);
  assert.equal(isDoubleSided({ name: 'MAT_Stone' }), false);
  assert.equal(isSingleSided({ name: 'MAT_Water' }), true);
  assert.equal(isSingleSided({ name: 'MAT_Stone' }), false);
});

test('deviceProfile detecta móvil, iPad, memoria, núcleos y pantalla pequeña', () => {
  const desktop = deviceProfile({
    navigator: { userAgent: 'Mozilla/5.0 (X11; Linux x86_64)', deviceMemory: 16, hardwareConcurrency: 8 },
    window: { screen: { width: 1920, height: 1080 }, matchMedia: () => ({ matches: false }) },
  });
  assert.equal(desktop.lowPower, false);

  const android = deviceProfile({
    navigator: { userAgent: 'Mozilla/5.0 (Linux; Android 13)', deviceMemory: 8, hardwareConcurrency: 8 },
    window: { screen: { width: 412, height: 915 }, matchMedia: () => ({ matches: true }) },
  });
  assert.equal(android.lowPower, true);

  const ipadDesktop = deviceProfile({
    navigator: { userAgent: 'Mozilla/5.0 (Macintosh)', maxTouchPoints: 5, deviceMemory: 8, hardwareConcurrency: 8 },
    window: { screen: { width: 1024, height: 1366 }, matchMedia: () => ({ matches: false }) },
  });
  assert.equal(ipadDesktop.lowPower, true);

  const lowMemory = deviceProfile({
    navigator: { userAgent: 'Mozilla/5.0 (X11; Linux x86_64)', deviceMemory: 4, hardwareConcurrency: 8 },
    window: { screen: { width: 1920, height: 1080 }, matchMedia: () => ({ matches: false }) },
  });
  assert.equal(lowMemory.lowPower, true);

  const fewCores = deviceProfile({
    navigator: { userAgent: 'Mozilla/5.0 (X11; Linux x86_64)', deviceMemory: 16, hardwareConcurrency: 4 },
    window: { screen: { width: 1920, height: 1080 }, matchMedia: () => ({ matches: false }) },
  });
  assert.equal(fewCores.lowPower, true);

  const smallCoarse = deviceProfile({
    navigator: { userAgent: 'Mozilla/5.0 (X11; Linux x86_64)', deviceMemory: 16, hardwareConcurrency: 8 },
    window: { screen: { width: 600, height: 900 }, matchMedia: () => ({ matches: true }) },
  });
  assert.equal(smallCoarse.lowPower, true);
});
