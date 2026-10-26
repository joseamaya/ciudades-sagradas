import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const errors = [];
const warnings = [];

async function readJson(file) {
  const full = path.join(root, file);
  if (!existsSync(full)) throw new Error(`Falta ${file}`);
  return JSON.parse(await readFile(full, 'utf8'));
}

function check(condition, message) {
  if (!condition) errors.push(message);
}

const index = await readJson('public/cities/index.json');
check(Array.isArray(index) && index.length > 0, 'public/cities/index.json debe ser un array con ciudades');

const ids = new Set();
for (const entry of index) {
  for (const field of ['id', 'name', 'subtitle', 'culture', 'period', 'region', 'status', 'summary']) {
    check(Boolean(entry[field]), `${entry.id || 'ciudad'}: falta el campo "${field}"`);
  }
  check(!ids.has(entry.id), `id duplicado: ${entry.id}`);
  ids.add(entry.id);

  const cityPath = `public/cities/${entry.id}/city.json`;
  const city = await readJson(cityPath);
  check(city.id === entry.id, `${entry.id}: city.json tiene id "${city.id}"`);
  check(Array.isArray(city.sources) && city.sources.length > 0, `${entry.id}: faltan fuentes públicas`);

  const dossier = `docs/fuentes/${entry.id}.md`;
  check(existsSync(path.join(root, dossier)), `${entry.id}: falta el dossier ${dossier}`);

  if (entry.thumb) {
    check(existsSync(path.join(root, 'public', entry.thumb)), `${entry.id}: falta la portada ${entry.thumb}`);
  }

  if (city.status === 'available') {
    check(Boolean(city.model), `${entry.id}: una ciudad disponible necesita modelo`);
    check(Array.isArray(city.tour) && city.tour.length > 0, `${entry.id}: falta el recorrido`);
    check(Array.isArray(city.layers) && city.layers.length > 0, `${entry.id}: faltan capas`);
    check(Boolean(city.camera), `${entry.id}: falta la cámara inicial`);
    const modelPaths = [city.model, ...Object.values(city.lod?.levels ?? {}), city.fallbackModel].filter(Boolean);
    for (const model of new Set(modelPaths)) {
      const modelPath = path.join(root, 'public', model);
      check(existsSync(modelPath), `${entry.id}: falta el modelo ${model}`);
      if (existsSync(modelPath)) {
        const size = (await stat(modelPath)).size;
        const mb = size / (1024 * 1024);
        if (mb > 25) warnings.push(`${entry.id}: modelo ${model} de ${mb.toFixed(1)} MB (objetivo < 25 MB)`);
      }
    }
  } else {
    check(!city.model, `${entry.id}: una ficha en investigación no debe declarar modelo`);
  }
}

check(existsSync(path.join(root, 'docs/fuentes/registro-assets.csv')), 'Falta docs/fuentes/registro-assets.csv');

for (const warning of warnings) console.warn(`AVISO  ${warning}`);
for (const error of errors) console.error(`ERROR  ${error}`);
console.log(`Ciudades: ${index.length} · disponibles: ${index.filter((c) => c.status === 'available').length}`);
console.log(`Validación: ${errors.length ? 'FALLÓ' : 'OK'}`);
if (errors.length) process.exit(1);
