import assert from 'node:assert/strict';
import { test } from 'node:test';
import { trianglesOf } from '../../scripts/model-metrics.mjs';

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
