import { existsSync } from 'node:fs';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { computeAssetHash } from './asset-hash.mjs';

const root = process.cwd();
const dist = path.join(root, 'dist');
const errors = [];
const swPath = path.join(dist, 'sw.js');

if (!existsSync(swPath)) {
  errors.push('Falta dist/sw.js; ejecuta npm run build');
} else {
  const sw = await readFile(swPath, 'utf8');
  const match = sw.match(/const CACHE = 'ciudades-sagradas-([a-f0-9]{12})';/);
  if (!match) errors.push('dist/sw.js no contiene una versión de caché generada');

  const expected = await computeAssetHash(dist);
  if (match && match[1] !== expected) {
    errors.push(`dist/sw.js usa ${match[1]} pero el build produce ${expected}`);
  }
}

for (const file of [
  'draco/draco_decoder.js',
  'draco/draco_decoder.wasm',
  'draco/draco_wasm_wrapper.js',
]) {
  if (!existsSync(path.join(dist, file))) errors.push(`Falta dist/${file}`);
}

const assetsDir = path.join(dist, 'assets');
if (existsSync(assetsDir)) {
  const dracoAssets = (await readdir(assetsDir)).filter((file) =>
    /^draco_(?:decoder|wasm_wrapper)-.*\.(?:js|wasm)$/.test(file),
  );
  if (dracoAssets.length) {
    errors.push(`dist/assets conserva decoder Draco duplicado: ${dracoAssets.join(', ')}`);
  }
}

for (const error of errors) console.error(`ERROR  ${error}`);
console.log(errors.length ? 'Check dist: FALLÓ' : 'Check dist: OK');
if (errors.length) process.exit(1);
