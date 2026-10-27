import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
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

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"') {
        if (text[index + 1] === '"') {
          field += '"';
          index += 1;
        } else {
          quoted = false;
        }
      } else {
        field += char;
      }
      continue;
    }
    if (char === '"') quoted = true;
    else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (char !== '\r') {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

async function checkGlb(file) {
  const buffer = await readFile(file);
  check(buffer.length >= 12, `${file}: archivo GLB demasiado pequeño`);
  if (buffer.length < 12) return;
  check(buffer.toString('ascii', 0, 4) === 'glTF', `${file}: cabecera GLB inválida`);
  check(buffer.readUInt32LE(4) === 2, `${file}: versión GLB distinta de 2`);
  check(buffer.readUInt32LE(8) === buffer.length, `${file}: longitud GLB declarada no coincide`);
}

function isNumberTriplet(value) {
  return Array.isArray(value) && value.length === 3 && value.every((item) => Number.isFinite(item));
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

  if (city.coordinates) {
    check(Number.isFinite(city.coordinates.lat), `${entry.id}: coordinates.lat inválido`);
    check(Number.isFinite(city.coordinates.lon), `${entry.id}: coordinates.lon inválido`);
  }
  if (city.stage) {
    check(['piloto', 'preview', 'v1', 'v2'].includes(city.stage), `${entry.id}: stage inválido "${city.stage}"`);
  }
  if (city.verticalScale != null) {
    check(Number.isFinite(city.verticalScale) && city.verticalScale > 0, `${entry.id}: verticalScale inválido`);
  }

  if (city.status === 'available') {
    check(Boolean(city.model), `${entry.id}: una ciudad disponible necesita modelo`);
    check(Array.isArray(city.tour) && city.tour.length > 0, `${entry.id}: falta el recorrido`);
    check(Array.isArray(city.layers) && city.layers.length > 0, `${entry.id}: faltan capas`);
    check(Boolean(city.camera), `${entry.id}: falta la cámara inicial`);
    check(isNumberTriplet(city.camera?.position), `${entry.id}: camera.position inválido`);
    check(isNumberTriplet(city.camera?.target), `${entry.id}: camera.target inválido`);
    check(Number.isFinite(city.camera?.fov) && city.camera.fov > 0, `${entry.id}: camera.fov inválido`);

    const levels = city.lod?.levels ?? {};
    if (city.lod?.default && city.lod.default !== 'auto') {
      check(Boolean(levels[city.lod.default]), `${entry.id}: lod.default "${city.lod.default}" no existe en levels`);
    }
    for (const stop of city.tour || []) {
      check(Boolean(stop.title), `${entry.id}: parada sin título`);
      check(Boolean(stop.text), `${entry.id}: parada "${stop.title}" sin texto`);
      check(isNumberTriplet(stop.camera?.position), `${entry.id}: parada "${stop.title}" con cámara inválida`);
      check(isNumberTriplet(stop.camera?.target), `${entry.id}: parada "${stop.title}" con objetivo inválido`);
    }
    const layerIds = new Set();
    for (const layer of city.layers || []) {
      check(Boolean(layer.id) && Boolean(layer.label), `${entry.id}: capa sin id o etiqueta`);
      check(!layerIds.has(layer.id), `${entry.id}: capa duplicada "${layer.id}"`);
      layerIds.add(layer.id);
    }

    const modelPaths = [city.model, ...Object.values(levels), city.fallbackModel].filter(Boolean);
    for (const model of new Set(modelPaths)) {
      const modelPath = path.join(root, 'public', model);
      check(existsSync(modelPath), `${entry.id}: falta el modelo ${model}`);
      if (existsSync(modelPath)) {
        const size = (await stat(modelPath)).size;
        const mb = size / (1024 * 1024);
        if (mb > 25) warnings.push(`${entry.id}: modelo ${model} de ${mb.toFixed(1)} MB (objetivo < 25 MB)`);
        await checkGlb(modelPath);
      }
    }
  } else {
    check(!city.model, `${entry.id}: una ficha en investigación no debe declarar modelo`);
  }
}

check(existsSync(path.join(root, 'docs/fuentes/registro-assets.csv')), 'Falta docs/fuentes/registro-assets.csv');

const swPath = path.join(root, 'public/sw.js');
check(existsSync(swPath), 'Falta public/sw.js');
if (existsSync(swPath)) {
  const sw = await readFile(swPath, 'utf8');
  check(/const CACHE = 'ciudades-sagradas-v\d+';/.test(sw), 'public/sw.js: falta una versión de caché válida');
}

const registryPath = path.join(root, 'docs/fuentes/registro-assets.csv');
if (existsSync(registryPath)) {
  const registry = parseCsv(await readFile(registryPath, 'utf8'));
  const header = registry.shift() || [];
  const urlIndex = header.indexOf('url');
  const notesIndex = header.indexOf('notas');
  for (const row of registry) {
    const url = row[urlIndex];
    if (!url || !url.startsWith('public/')) continue;
    const file = path.join(root, url);
    check(existsSync(file), `registro-assets: falta ${url}`);
    if (!existsSync(file)) continue;
    const notes = row[notesIndex] || '';
    const hash = notes.match(/SHA256\s+([a-f0-9]{64})/i)?.[1];
    if (hash) {
      const actual = createHash('sha256').update(await readFile(file)).digest('hex');
      check(actual === hash, `registro-assets: SHA256 desactualizado para ${url}`);
    }
    const size = Number(notes.match(/(\d+)\s+bytes/)?.[1]);
    if (Number.isFinite(size) && size > 0) {
      const actualSize = (await stat(file)).size;
      check(actualSize === size, `registro-assets: tamaño desactualizado para ${url}`);
    }
  }
}

for (const warning of warnings) console.warn(`AVISO  ${warning}`);
for (const error of errors) console.error(`ERROR  ${error}`);
console.log(`Ciudades: ${index.length} · disponibles: ${index.filter((c) => c.status === 'available').length}`);
console.log(`Validación: ${errors.length ? 'FALLÓ' : 'OK'}`);
if (errors.length) process.exit(1);
