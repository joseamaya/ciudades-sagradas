import assert from 'node:assert/strict';
import { test } from 'node:test';
import { inspectGlb, trianglesOf } from '../../scripts/model-metrics.mjs';

test('trianglesOf cuenta triángulos y abanicos sin índices', () => {
  const triangles = {
    accessors: [{ count: 9 }],
    meshes: [{ primitives: [{ indices: 0 }] }],
  };
  assert.equal(trianglesOf(triangles), 3);

  const fan = {
    accessors: [{ count: 5 }],
    meshes: [{ primitives: [{ indices: 0, mode: 5 }] }],
  };
  assert.equal(trianglesOf(fan), 3);

  assert.equal(
    trianglesOf({
      accessors: [{ count: 6 }],
      meshes: [{ primitives: [{ attributes: { POSITION: 0 } }] }],
    }),
    2,
  );
});

test('trianglesOf ignora primitivas sin accessor válido', () => {
  assert.equal(trianglesOf({}), 0);
  assert.equal(trianglesOf({ meshes: [{ primitives: [{}] }] }), 0);
});

test('inspectGlb expone capas y detecta nodos sin extras.layer', async () => {
  const caral = await inspectGlb('public/cities/caral/model_lod1.glb');
  assert.deepEqual(caral.layers.sort(), ['city', 'props', 'reference', 'terrain']);
  assert.equal(caral.missingLayers.length, 0);

  const narihuala = await inspectGlb('public/cities/narihuala/model_lod0.glb');
  assert.ok(narihuala.layers.includes('later'));

  const fallback = await inspectGlb('public/cities/caral/model.glb');
  assert.equal(fallback.layers.length, 0);
  assert.ok(fallback.missingLayers.length > 0);
});
