import { createHash } from 'node:crypto';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

async function listFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...(await listFiles(fullPath)));
    else if (entry.isFile()) files.push(fullPath);
  }
  return files;
}

export async function computeAssetHash(directory) {
  const files = (await listFiles(directory)).sort();
  const hash = createHash('sha256');

  for (const file of files) {
    const relative = path.relative(directory, file).split(path.sep).join('/');
    if (relative === 'sw.js' || relative.endsWith('.md') || relative.endsWith('.txt')) continue;
    hash.update(relative);
    hash.update('\0');
    hash.update(await readFile(file));
  }

  return hash.digest('hex').slice(0, 12);
}
