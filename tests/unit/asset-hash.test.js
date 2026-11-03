import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { computeAssetHash } from '../../scripts/asset-hash.mjs';

async function fixture() {
  const directory = await mkdtemp(path.join(tmpdir(), 'ciudades-hash-'));
  await writeFile(path.join(directory, 'index.html'), '<h1>atlas</h1>');
  await mkdir(path.join(directory, 'assets'));
  await writeFile(path.join(directory, 'assets', 'app.js'), 'console.log(1);');
  await writeFile(path.join(directory, 'notes.md'), 'ignorado');
  await writeFile(path.join(directory, 'sw.js'), 'ignorado');
  return directory;
}

test('computeAssetHash es determinista y devuelve 12 hex', async () => {
  const first = await fixture();
  const second = await fixture();
  try {
    const a = await computeAssetHash(first);
    const b = await computeAssetHash(second);
    assert.match(a, /^[a-f0-9]{12}$/);
    assert.equal(a, b);
  } finally {
    await rm(first, { recursive: true, force: true });
    await rm(second, { recursive: true, force: true });
  }
});

test('computeAssetHash cambia con un asset y ignora md/txt/sw.js', async () => {
  const directory = await fixture();
  try {
    const before = await computeAssetHash(directory);
    await writeFile(path.join(directory, 'notes.md'), 'otro texto');
    await writeFile(path.join(directory, 'sw.js'), 'otro worker');
    assert.equal(await computeAssetHash(directory), before);
    await writeFile(path.join(directory, 'assets', 'app.js'), 'console.log(2);');
    assert.notEqual(await computeAssetHash(directory), before);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});
