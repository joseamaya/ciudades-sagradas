import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { isNumberTriplet, parseCsv } from './validate-lib.mjs';
import { inspectGlb } from './model-metrics.mjs';

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
const GROUND_TEXTURES = new Set(['sand']);
const LEGACY_FALLBACKS = new Set(['cities/caral/model.glb']);
const requiredAssets = [];

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
  for (const field of ['id', 'name', 'subtitle', 'culture', 'period', 'region', 'availability', 'maturity', 'evidence', 'qa', 'summary']) {
    check(Boolean(entry[field]), `${entry.id || 'ciudad'}: falta el campo "${field}"`);
  }
  check(CITY_ID.test(entry.id || ''), `${entry.id || 'ciudad'}: id inválido; usa minúsculas, números y guiones`);
  check(Number.isInteger(entry.yearsAgo) && entry.yearsAgo > 0, `${entry.id}: yearsAgo debe ser un entero positivo`);
  if (entry.accent != null) {
    check(HEX_COLOR.test(entry.accent), `${entry.id}: accent debe ser un color hexadecimal de seis dígitos`);
  }
  if (entry.thumb != null) {
    check(
      HERO_PATH.test(entry.thumb) && entry.thumb.startsWith(`cities/${entry.id}/hero.`),
      `${entry.id}: thumb debe apuntar a cities/${entry.id}/hero.(jpg|jpeg|png|webp)`,
    );
  }
  check(!ids.has(entry.id), `id duplicado: ${entry.id}`);
  ids.add(entry.id);
  check(!('status' in entry), `${entry.id}: index.json usa "status"; migra a "availability"`);
  check(!('stage' in entry), `${entry.id}: index.json usa "stage"; migra a "maturity" y "version"`);

  const cityPath = `public/cities/${entry.id}/city.json`;
  const city = await readJson(cityPath);
  check(city.id === entry.id, `${entry.id}: city.json tiene id "${city.id}"`);
  if (city.accent != null) {
    check(HEX_COLOR.test(city.accent), `${entry.id}: accent de city.json debe ser un color hexadecimal de seis dígitos`);
  }
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
  check(existsSync(path.join(root, 'public', 'cities', entry.id, 'README.md')), `${entry.id}: falta public/cities/${entry.id}/README.md`);

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
    if (city.ground?.texture != null) {
      check(
        typeof city.ground.texture === 'string' && GROUND_TEXTURES.has(city.ground.texture),
        `${entry.id}: ground.texture no soportada "${city.ground.texture}"`,
      );
    }
  }
  if (city.fog != null) {
    check(typeof city.fog === 'object', `${entry.id}: fog debe ser un objeto`);
    check(Number.isFinite(city.fog?.near) && Number.isFinite(city.fog?.far), `${entry.id}: fog.near/far inválidos`);
    check(!Number.isFinite(city.fog?.near) || !Number.isFinite(city.fog?.far) || city.fog.near < city.fog.far, `${entry.id}: fog.near debe ser menor que fog.far`);
  }
  if (city.lighting != null) {
    check(typeof city.lighting === 'object' && !Array.isArray(city.lighting), `${entry.id}: lighting debe ser un objeto`);
    const lightingKeys = ['fill', 'hemiIntensity', 'envIntensity'];
    const lightingPresets = ['morning', 'noon', 'dusk', 'night'];
    const checkLightingFields = (value, prefix) => {
      for (const field of lightingKeys) {
        if (value?.[field] != null) {
          check(Number.isFinite(value[field]) && value[field] >= 0, `${entry.id}: ${prefix}${field} inválido`);
        }
      }
    };
    checkLightingFields(city.lighting, 'lighting.');
    for (const [key, value] of Object.entries(city.lighting)) {
      if (lightingPresets.includes(key)) {
        check(Boolean(value) && typeof value === 'object' && !Array.isArray(value), `${entry.id}: lighting.${key} debe ser un objeto`);
        checkLightingFields(value, `lighting.${key}.`);
      } else if (!lightingKeys.includes(key)) {
        errors.push(`${entry.id}: lighting.${key} no reconocido`);
      }
    }
  }
  if (city.lights != null) {
    check(Array.isArray(city.lights), `${entry.id}: lights debe ser un array`);
    for (const [index, light] of (Array.isArray(city.lights) ? city.lights : []).entries()) {
      check(Boolean(light) && typeof light === 'object', `${entry.id}: light ${index} inválida`);
      check(light?.type === 'point', `${entry.id}: light ${index} debe ser de tipo "point"`);
      if (light?.color != null) {
        check(HEX_COLOR.test(light.color), `${entry.id}: light ${index} color inválido`);
      }
      for (const field of ['intensity', 'distance', 'decay']) {
        if (light?.[field] != null) {
          check(Number.isFinite(light[field]) && light[field] >= 0, `${entry.id}: light ${index} ${field} inválido`);
        }
      }
      check(isNumberTriplet(light?.position), `${entry.id}: light ${index} position inválida`);
    }
  }

  if (city.availability === 'available') {
    check(Boolean(city.model), `${entry.id}: una ciudad disponible necesita modelo`);
    check(Array.isArray(city.tour) && city.tour.length === 6, `${entry.id}: el estándar pide seis paradas; hay ${city.tour?.length ?? 0}`);
    check(Array.isArray(city.layers) && city.layers.length > 0, `${entry.id}: faltan capas`);
    check(Boolean(city.camera), `${entry.id}: falta la cámara inicial`);
    check(isNumberTriplet(city.camera?.position), `${entry.id}: camera.position inválido`);
    check(isNumberTriplet(city.camera?.target), `${entry.id}: camera.target inválido`);
    check(Number.isFinite(city.camera?.fov) && city.camera.fov > 0, `${entry.id}: camera.fov inválido`);
    if (city.camera?.near != null) {
      check(Number.isFinite(city.camera.near) && city.camera.near > 0, `${entry.id}: camera.near inválido`);
    }
    if (city.camera?.far != null) {
      check(Number.isFinite(city.camera.far) && city.camera.far > 0, `${entry.id}: camera.far inválido`);
    }
    check(
      !Number.isFinite(city.camera?.near) || !Number.isFinite(city.camera?.far) || city.camera.near < city.camera.far,
      `${entry.id}: camera.near debe ser menor que camera.far`,
    );
    check(
      !Number.isFinite(city.camera?.far) || !Number.isFinite(city.fog?.far) || city.camera.far >= city.fog.far,
      `${entry.id}: camera.far debe cubrir fog.far`,
    );
    check(Number.isFinite(city.scale) && city.scale > 0, `${entry.id}: scale inválido`);
    check(Boolean(city.disclaimer), `${entry.id}: falta el aviso de reconstrucción`);
    check(Boolean(city.credits), `${entry.id}: faltan créditos`);
    check(city.qa !== 'not-applicable', `${entry.id}: una ciudad disponible debe declarar un qa distinto de not-applicable`);

    const heroPath = path.join(root, 'public', 'cities', entry.id, 'hero.jpg');
    check(existsSync(heroPath), `${entry.id}: falta public/cities/${entry.id}/hero.jpg`);
    if (existsSync(heroPath)) {
      const heroBytes = (await stat(heroPath)).size;
      if (heroBytes > 400 * 1024) {
        warnings.push(`${entry.id}: hero.jpg de ${Math.round(heroBytes / 1024)} KB (objetivo < 400 KB)`);
      }
    }
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
    const actualLayers = new Set();
    for (const model of new Set(modelPaths)) {
      requiredAssets.push({ id: entry.id, asset: `public/${model}` });
      const modelPath = path.join(root, 'public', model);
      check(existsSync(modelPath), `${entry.id}: falta el modelo ${model}`);
      if (!existsSync(modelPath)) continue;
      const size = (await stat(modelPath)).size;
      const mb = size / (1024 * 1024);
      if (mb > 25) warnings.push(`${entry.id}: modelo ${model} de ${mb.toFixed(1)} MB (objetivo < 25 MB)`);
      let info;
      try {
        info = await inspectGlb(modelPath);
      } catch (error) {
        errors.push(`${entry.id}: ${model}: ${error.message}`);
        continue;
      }
      const level = Object.entries(levels).find(([, url]) => url === model)?.[0] ?? null;
      modelMetrics.push({ id: entry.id, model, level, triangles: info.triangles, bytes: size, images: info.images });
      if (strictModels.has(model)) {
        check(info.missingLayers.length === 0, `${entry.id}: ${model} tiene ${info.missingLayers.length} nodos con mesh sin extras.layer`);
        for (const layer of info.layers) {
          if (!layerIds.has(layer)) {
            errors.push(`${entry.id}: ${model} trae la capa "${layer}" no declarada en city.json`);
          }
          actualLayers.add(layer);
        }
        if (level === '0' && (info.triangles < 150000 || info.triangles > 250000)) {
          warnings.push(`${entry.id}: LOD0 ${info.triangles.toLocaleString('es')} tris fuera del rango 150.000–250.000`);
        }
        if (level === '1' && (info.triangles < 25000 || info.triangles > 80000)) {
          warnings.push(`${entry.id}: LOD1 ${info.triangles.toLocaleString('es')} tris fuera del rango 25.000–80.000`);
        }
        if (level === '0' && info.images > 40) {
          warnings.push(`${entry.id}: LOD0 tiene ${info.images} imágenes (objetivo ≤ 40)`);
        }
        if (level === '1' && info.images > 32) {
          warnings.push(`${entry.id}: LOD1 tiene ${info.images} imágenes (objetivo ≤ 32)`);
        }
      } else if (info.missingLayers.length) {
        if (LEGACY_FALLBACKS.has(model)) {
          warnings.push(`${entry.id}: fallback legado ${model} sin extras.layer; excepción documentada`);
        } else {
          errors.push(`${entry.id}: fallback ${model} tiene ${info.missingLayers.length} nodos con mesh sin extras.layer`);
        }
      }
    }
    requiredAssets.push({ id: entry.id, asset: `public/cities/${entry.id}/hero.jpg` });
    for (const layer of layerIds) {
      check(actualLayers.has(layer), `${entry.id}: la capa "${layer}" no aparece en ningún LOD`);
    }
    const levelImages = Object.fromEntries(
      modelMetrics
        .filter((metric) => metric.id === entry.id && metric.level != null)
        .map((metric) => [metric.level, metric.images]),
    );
    if (levelImages['0'] != null && levelImages['1'] != null) {
      check(
        levelImages['1'] <= levelImages['0'],
        `${entry.id}: LOD1 tiene ${levelImages['1']} imágenes y LOD0 ${levelImages['0']}; LOD1 no debe superar a LOD0`,
      );
    }
  } else {
    check(!city.model, `${entry.id}: una ficha en investigación no debe declarar modelo`);
    check(city.maturity === 'research', `${entry.id}: una ficha sin modelo debe tener maturity "research"`);
    check(city.evidence === 'not-applicable', `${entry.id}: una ficha sin modelo debe tener evidence "not-applicable"`);
    check(city.qa === 'not-applicable', `${entry.id}: una ficha sin modelo debe tener qa "not-applicable"`);
  }
}

check(existsSync(path.join(root, 'docs/fuentes/registro-assets.csv')), 'Falta docs/fuentes/registro-assets.csv');

const swTemplatePath = path.join(root, 'scripts/sw.template.js');
check(existsSync(swTemplatePath), 'Falta scripts/sw.template.js');
if (existsSync(swTemplatePath)) {
  const sw = await readFile(swTemplatePath, 'utf8');
  check(sw.includes("const CACHE = '__CACHE_VERSION__';"), 'scripts/sw.template.js: falta el marcador __CACHE_VERSION__');
  check(sw.includes('self.addEventListener'), 'scripts/sw.template.js: no parece un service worker');
}
check(!existsSync(path.join(root, 'public/sw.js')), 'public/sw.js debe generarse en build; elimina la copia manual');

const registryPath = path.join(root, 'docs/fuentes/registro-assets.csv');
if (existsSync(registryPath)) {
  const registry = parseCsv(await readFile(registryPath, 'utf8'));
  const header = registry.shift() || [];
  const urlIndex = header.indexOf('url');
  const notesIndex = header.indexOf('notas');
  const registeredUrls = new Set();
  const registeredIntegrity = new Set();
  for (const row of registry) {
    const url = row[urlIndex];
    if (!url) continue;
    registeredUrls.add(url);
    if (!url.startsWith('public/')) continue;
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
    if (hash && Number.isFinite(size) && size > 0) registeredIntegrity.add(url);
  }
  for (const { id, asset } of requiredAssets) {
    check(registeredUrls.has(asset), `${id}: ${asset} no está en docs/fuentes/registro-assets.csv`);
    if (registeredUrls.has(asset)) {
      check(
        registeredIntegrity.has(asset),
        `${id}: ${asset} no declara SHA256 y bytes en docs/fuentes/registro-assets.csv`,
      );
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
