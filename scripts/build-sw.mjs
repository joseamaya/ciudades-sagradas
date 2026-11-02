import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { computeAssetHash } from './asset-hash.mjs';

const root = process.cwd();
const dist = path.join(root, 'dist');
const version = await computeAssetHash(dist);
const template = await readFile(path.join(root, 'scripts/sw.template.js'), 'utf8');
const source = template.replaceAll('__CACHE_VERSION__', `ciudades-sagradas-${version}`);

await writeFile(path.join(dist, 'sw.js'), source);
console.log(`Service worker: ciudades-sagradas-${version}`);
