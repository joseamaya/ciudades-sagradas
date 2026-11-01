import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';

const root = process.cwd();
const errors = [];
const warnings = [];
const modelMetrics = [];

const AVAILABILITY = ['available', 'research'];
const MATURITY = ['research', 'blockout', 'preview', 'released'];
const EVIDENCE = ['documented', 'mixed', 'interpretive', 'not-applicable'];
const QA = ['passed', 'partial', 'pending', 'waived', 'not-applicable'];
const STOP_EVIDENCE = ['documented', 'inferred', 'interpretive'];
const REQUIRED_LAYERS = ['city', 'terrain', 'props', 'reference'];
const CITY_ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const HEX_COLOR = /^#[0-9a-f]{6}$/i;
const HERO_PATH = /^cities\/[a-z0-9-]+\/hero\.(?:jpe?g|png|webp)$/;

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

function isNumberTriplet(value) {
  return Array.isArray(value) && value.length === 3 && value.every((item) => Number.isFinite(item));
}

function trianglesOf(json) {
  let triangles = 0;
  for (const mesh of json.meshes ?? []) {
    for (const primitive of mesh.primitives ?? []) {
      const mode = primitive.mode ?? 4;
      const count = primitive.indices != null
        ? json.accessors?.[primitive.indices]?.count
        : json.accessors?.[primitive.attributes?.POSITION]?.count;
      if (!Number.isFinite(count)) continue;
      if (mode === 4) triangles += count / 3;
      else if (mode === 5) triangles += Math.max(0, count - 2);
    }
  }
  return Math.round(triangles);
}

async function inspectGlb(file) {
  const buffer = await readFile(file);
  check(buffer.length >= 20, `${file}: archivo GLB demasiado pequeño`);
  if (buffer.length < 20) return null;
  check(buffer.toString('ascii', 0, 4) === 'glTF', `${file}: cabecera GLB inválida`);
  check(buffer.readUInt32LE(4) === 2, `${file}: versión GLB distinta de 2`);
  check(buffer.readUInt32LE(8) === buffer.length, `${file}: longitud GLB declarada no coincide`);
  const jsonLength = buffer.readUInt32LE(12);
  const jsonType = buffer.toString('ascii', 16, 20);
  check(jsonType === 'JSON', `${file}: primer chunk GLB no es JSON`);
  if (jsonType !== 'JSON' || 20 + jsonLength > buffer.length) return null;
  const json = JSON.parse(buffer.toString('utf8', 20, 20 + jsonLength));
  const meshNodes = (json.nodes ?? []).filter((node) => node.mesh !== undefined);
  const missingLayers = meshNodes
    .filter((node) => typeof node.extras?.layer !== 'string' || !node.extras.layer)
    .map((node) => node.name || '(sin nombre)');
  return {
    triangles: trianglesOf(json),
    images: json.images?.length ?? 0,
    meshNodes,
    missingLayers,
  };
}

const index = await readJson('public/cities/index.json');
check(Array.isArray(index) && index.length > 0, 'public/cities/index.json debe ser un array con ciudades');

const ids = new Set();
for (const entry of index) {
  for (const field of ['id', 'name', 'subtitle', 'culture', 'period', 'region', 'availability', 'maturity', 'evidence', 'qa', 'summary']) {
    check(Boolean(entry[field]), `${entry.id || 'ciudad'}: falta el campo "${field}"`);
  }
  check(CITY_ID.test(entry.id || ''), `${entry.id || 'ciudad'}: id inválido; usa minúsculas, números y guiones`);
  if (entry.yearsAgo != null) {
    check(Number.isInteger(entry.yearsAgo) && entry.yearsAgo > 0, `${entry.id}: yearsAgo debe ser un entero positivo`);
  }
  if (entry.accent != null) {
    check(HEX_COLOR.test(entry.accent), `${entry.id}: accent debe ser un color hexadecimal de seis dígitos`);
  }
  if (entry.thumb != null) {
    check(HERO_PATH.test(entry.thumb), `${entry.id}: thumb debe apuntar a cities/<id>/hero.(jpg|jpeg|png|webp)`);
  }
  check(!ids.has(entry.id), `id duplicado: ${entry.id}`);
  ids.add(entry.id);
  check(!('status' in entry), `${entry.id}: index.json usa "status"; migra a "availability"`);
  check(!('stage' in entry), `${entry.id}: index.json usa "stage"; migra a "maturity" y "version"`);

  const cityPath = `public/cities/${entry.id}/city.json`;
  const city = await readJson(cityPath);
  check(city.id === entry.id, `${entry.id}: city.json tiene id "${city.id}"`);
  check(Array.isArray(city.sources) && city.sources.length > 0, `${entry.id}: faltan fuentes públicas`);
  for (const source of city.sources || []) {
    check(Boolean(source?.label), `${entry.id}: fuente sin etiqueta`);
    check(
      typeof source?.url === 'string' && /^https:\/\//i.test(source.url),
      `${entry.id}: la fuente "${source?.label || 'sin etiqueta'}" debe usar una URL https`,
    );
  }
  check(!('status' in city), `${entry.id}: city.json usa "status"; migra a "availability"`);
  check(!('stage' in city), `${entry.id}: city.json usa "stage"; migra a "maturity" y "version"`);

  for (const field of ['name', 'subtitle', 'culture', 'period', 'region', 'availability', 'maturity', 'evidence', 'qa']) {
    check(entry[field] === city[field], `${entry.id}: index.json y city.json difieren en "${field}"`);
  }
  check((entry.version ?? null) === (city.version ?? null), `${entry.id}: index.json y city.json difieren en "version"`);

  check(AVAILABILITY.includes(city.availability), `${entry.id}: availability inválida "${city.availability}"`);
  check(MATURITY.includes(city.maturity), `${entry.id}: maturity inválida "${city.maturity}"`);
  check(EVIDENCE.includes(city.evidence), `${entry.id}: evidence inválido "${city.evidence}"`);
  check(QA.includes(city.qa), `${entry.id}: qa inválido "${city.qa}"`);
  if (city.maturity !== 'research') {
    check(typeof city.version === 'string' && city.version.length > 0, `${entry.id}: falta version para maturity "${city.maturity}"`);
  }

  const dossier = `docs/fuentes/${entry.id}.md`;
  check(existsSync(path.join(root, dossier)), `${entry.id}: falta el dossier ${dossier}`);

  if (entry.thumb) {
    check(existsSync(path.join(root, 'public', entry.thumb)), `${entry.id}: falta la portada ${entry.thumb}`);
  }

  if (city.coordinates) {
    check(Number.isFinite(city.coordinates.lat), `${entry.id}: coordinates.lat inválido`);
    check(Number.isFinite(city.coordinates.lon), `${entry.id}: coordinates.lon inválido`);
  }
  if (city.verticalScale != null) {
    check(Number.isFinite(city.verticalScale) && city.verticalScale > 0, `${entry.id}: verticalScale inválido`);
  }
  if (city.ground != null) {
    check(typeof city.ground === 'object', `${entry.id}: ground debe ser un objeto`);
    if (city.ground?.y != null) check(Number.isFinite(city.ground.y), `${entry.id}: ground.y inválido`);
  }
  if (city.fog != null) {
    check(typeof city.fog === 'object', `${entry.id}: fog debe ser un objeto`);
    check(Number.isFinite(city.fog?.near) && Number.isFinite(city.fog?.far), `${entry.id}: fog.near/far inválidos`);
    check(!Number.isFinite(city.fog?.near) || !Number.isFinite(city.fog?.far) || city.fog.near < city.fog.far, `${entry.id}: fog.near debe ser menor que fog.far`);
  }
  if (city.lights != null) {
    check(Array.isArray(city.lights), `${entry.id}: lights debe ser un array`);
  }

  if (city.availability === 'available') {
    check(Boolean(city.model), `${entry.id}: una ciudad disponible necesita modelo`);
    check(Array.isArray(city.tour) && city.tour.length === 6, `${entry.id}: el estándar pide seis paradas; hay ${city.tour?.length ?? 0}`);
    check(Array.isArray(city.layers) && city.layers.length > 0, `${entry.id}: faltan capas`);
    check(Boolean(city.camera), `${entry.id}: falta la cámara inicial`);
    check(isNumberTriplet(city.camera?.position), `${entry.id}: camera.position inválido`);
    check(isNumberTriplet(city.camera?.target), `${entry.id}: camera.target inválido`);
    check(Number.isFinite(city.camera?.fov) && city.camera.fov > 0, `${entry.id}: camera.fov inválido`);
    check(Number.isFinite(city.scale) && city.scale > 0, `${entry.id}: scale inválido`);
    check(Boolean(city.disclaimer), `${entry.id}: falta el aviso de reconstrucción`);
    check(Boolean(city.credits), `${entry.id}: faltan créditos`);
    check(city.qa !== 'not-applicable', `${entry.id}: una ciudad disponible debe declarar un qa distinto de not-applicable`);

    check(existsSync(path.join(root, 'public', 'cities', entry.id, 'hero.jpg')), `${entry.id}: falta public/cities/${entry.id}/hero.jpg`);
    check(existsSync(path.join(root, 'docs', 'remaster', entry.id, 'cobertura.md')), `${entry.id}: falta docs/remaster/${entry.id}/cobertura.md`);

    const levels = city.lod?.levels ?? {};
    check(Boolean(levels['0']), `${entry.id}: falta LOD0 en lod.levels`);
    check(Boolean(levels['1']), `${entry.id}: falta LOD1 en lod.levels`);
    if (city.model && levels['0']) {
      check(city.model === levels['0'], `${entry.id}: city.model debe coincidir con lod.levels["0"]`);
    }
    if (city.lod?.default && city.lod.default !== 'auto') {
      check(Boolean(levels[city.lod.default]), `${entry.id}: lod.default "${city.lod.default}" no existe en levels`);
    }
    for (const stop of city.tour || []) {
      check(Boolean(stop.title), `${entry.id}: parada sin título`);
      check(Boolean(stop.text), `${entry.id}: parada "${stop.title}" sin texto`);
      check(STOP_EVIDENCE.includes(stop.evidence), `${entry.id}: parada "${stop.title}" con evidence inválido`);
      check(isNumberTriplet(stop.camera?.position), `${entry.id}: parada "${stop.title}" con cámara inválida`);
      check(isNumberTriplet(stop.camera?.target), `${entry.id}: parada "${stop.title}" con objetivo inválido`);
    }
    const layerIds = new Set();
    for (const layer of city.layers || []) {
      check(Boolean(layer.id) && Boolean(layer.label), `${entry.id}: capa sin id o etiqueta`);
      check(!layerIds.has(layer.id), `${entry.id}: capa duplicada "${layer.id}"`);
      layerIds.add(layer.id);
    }
    for (const required of REQUIRED_LAYERS) {
      check(layerIds.has(required), `${entry.id}: falta la capa estándar "${required}"`);
    }

    const modelPaths = [city.model, ...Object.values(levels), city.fallbackModel].filter(Boolean);
    const levelPaths = new Set(Object.values(levels));
    const strictModels = new Set([city.model, ...levelPaths].filter(Boolean));
    for (const model of new Set(modelPaths)) {
      const modelPath = path.join(root, 'public', model);
      check(existsSync(modelPath), `${entry.id}: falta el modelo ${model}`);
      if (!existsSync(modelPath)) continue;
      const size = (await stat(modelPath)).size;
      const mb = size / (1024 * 1024);
      if (mb > 25) warnings.push(`${entry.id}: modelo ${model} de ${mb.toFixed(1)} MB (objetivo < 25 MB)`);
      const info = await inspectGlb(modelPath);
      if (!info) continue;
      const level = Object.entries(levels).find(([, url]) => url === model)?.[0] ?? null;
      modelMetrics.push({ id: entry.id, model, level, triangles: info.triangles, bytes: size, images: info.images });
      if (strictModels.has(model)) {
        check(info.missingLayers.length === 0, `${entry.id}: ${model} tiene ${info.missingLayers.length} nodos con mesh sin extras.layer`);
        if (level === '0' && (info.triangles < 150000 || info.triangles > 250000)) {
          warnings.push(`${entry.id}: LOD0 ${info.triangles.toLocaleString('es')} tris fuera del rango 150.000–250.000`);
        }
        if (level === '1' && (info.triangles < 25000 || info.triangles > 80000)) {
          warnings.push(`${entry.id}: LOD1 ${info.triangles.toLocaleString('es')} tris fuera del rango 25.000–80.000`);
        }
      } else if (info.missingLayers.length) {
        warnings.push(`${entry.id}: fallback legado ${model} sin extras.layer; usa la clasificación por nombre`);
      }
    }
  } else {
    check(!city.model, `${entry.id}: una ficha en investigación no debe declarar modelo`);
    check(city.maturity === 'research', `${entry.id}: una ficha sin modelo debe tener maturity "research"`);
    check(city.evidence === 'not-applicable', `${entry.id}: una ficha sin modelo debe tener evidence "not-applicable"`);
    check(city.qa === 'not-applicable', `${entry.id}: una ficha sin modelo debe tener qa "not-applicable"`);
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
console.log(`Ciudades: ${index.length} · con modelo: ${index.filter((c) => c.availability === 'available').length}`);
for (const metric of modelMetrics.sort((a, b) => a.id.localeCompare(b.id) || String(a.level).localeCompare(String(b.level)))) {
  const label = metric.level == null ? 'fallback' : `LOD${metric.level}`;
  console.log(`  ${metric.id.padEnd(10)} ${label.padEnd(8)} ${metric.triangles.toLocaleString('es').padStart(9)} tris · ${(metric.bytes / 1024 / 1024).toFixed(2)} MB · ${metric.images} imágenes`);
}
console.log(`Validación: ${errors.length ? 'FALLÓ' : 'OK'}`);
if (errors.length) process.exit(1);
