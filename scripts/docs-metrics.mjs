import { execFileSync } from 'node:child_process';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { inspectGlb } from './model-metrics.mjs';

const root = process.cwd();
const METRICS_FILE = 'docs/metricas.json';
const OVERRIDES_FILE = 'docs/metricas-overrides.json';
const DOCS = {
  readme: 'README.md',
  estado: 'docs/estado.md',
  auditoria: 'docs/estandares/auditoria-ciudades.md',
  remaster: 'docs/remaster/README.md',
};
const EVIDENCE_LABELS = {
  documented: 'Documentada',
  mixed: 'Mixta',
  interpretive: 'Interpretativa',
  'not-applicable': 'No aplica',
};
const QA_README = {
  passed: 'Aprobada',
  partial: 'Parcial',
  pending: 'Pendiente',
  waived: 'Excepción P2 aceptada',
  'not-applicable': 'No aplica',
};
const QA_ESTADO = {
  passed: '`passed`',
  partial: '`partial`',
  pending: '`pending`',
  waived: '`waived` (P2 Android)',
  'not-applicable': 'No aplica',
};
const number = new Intl.NumberFormat('es-ES');
const decimal = new Intl.NumberFormat('es-ES', { maximumFractionDigits: 1 });

async function readJson(file) {
  return JSON.parse(await readFile(path.join(root, file), 'utf8'));
}

async function readOptionalJson(file) {
  try {
    return JSON.parse(await readFile(path.join(root, file), 'utf8'));
  } catch {
    return {};
  }
}

async function walkJsonFiles(dir) {
  const files = [];
  const entries = await readdir(path.join(root, dir), { withFileTypes: true });
  for (const entry of entries) {
    const relative = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...(await walkJsonFiles(relative)));
    else if (entry.isFile() && entry.name.endsWith('.json')) files.push(relative);
  }
  return files;
}

function lastCommitDate(file) {
  try {
    const output = execFileSync('git', ['log', '-1', '--format=%cI', '--', file], {
      cwd: root,
      encoding: 'utf8',
    }).trim();
    return output ? Date.parse(output) : null;
  } catch {
    return null;
  }
}

async function collectQaReports() {
  const reports = new Map();
  for (const file of await walkJsonFiles('docs/qa/resultados')) {
    let json;
    try {
      json = JSON.parse(await readFile(path.join(root, file), 'utf8'));
    } catch {
      continue;
    }
    const candidates = [];
    if (json.metrics) candidates.push(json);
    if (json.lod0?.report) candidates.push(json.lod0.report);
    if (json.lod1?.report) candidates.push(json.lod1.report);
    for (const report of candidates) {
      const city = report.city;
      const lod = report.metrics?.lod;
      const calls = report.metrics?.calls;
      if (!city || lod == null || !Number.isFinite(calls)) continue;
      const generatedAt = report.generatedAt ?? json.generatedAt ?? null;
      const candidate = {
        calls,
        textureMB: Number.isFinite(report.metrics?.textureMB) ? report.metrics.textureMB : null,
        generatedAt,
        source: file,
        stamp: generatedAt ? Date.parse(generatedAt) : 0,
      };
      const key = `${city}:${String(lod)}`;
      const current = reports.get(key);
      if (!current || candidate.stamp >= current.stamp) reports.set(key, candidate);
    }
  }
  return reports;
}

function pickModelInfo(info) {
  return {
    triangles: info.triangles,
    bytes: info.bytes,
    images: info.images,
    materials: info.materials,
    primitives: info.primitives,
    sha256: info.sha256,
  };
}

async function collectCities() {
  const index = await readJson('public/cities/index.json');
  const reports = await collectQaReports();
  const overrides = await readOptionalJson(OVERRIDES_FILE);
  const warnings = [];
  const cities = [];

  for (const entry of index) {
    const city = await readJson(`public/cities/${entry.id}/city.json`);
    const levels = city.lod?.levels ?? {};
    const models = {};
    for (const [level, modelPath] of Object.entries(levels).sort(([a], [b]) => a.localeCompare(b))) {
      const info = await inspectGlb(path.join(root, 'public', modelPath));
      const qa = reports.get(`${entry.id}:${level}`) ?? null;
      const override = overrides[entry.id]?.[level] ?? null;
      models[level] = {
        path: modelPath,
        ...pickModelInfo(info),
        calls: qa?.calls ?? null,
        textureMB: override?.textureMB ?? qa?.textureMB ?? null,
        textureSource: override?.textureMB != null ? OVERRIDES_FILE : qa?.source ?? null,
        qaSource: qa?.source ?? null,
        qaGeneratedAt: qa?.generatedAt ?? null,
      };
      if (qa) {
        const glbDate = lastCommitDate(path.join('public', modelPath));
        const qaDate = lastCommitDate(qa.source);
        if (glbDate && qaDate && qaDate < glbDate) {
          warnings.push(`${entry.id} LOD${level}: informe QA anterior al GLB; reejecuta la QA.`);
        }
      }
    }

    let fallback = null;
    if (city.fallbackModel && !Object.values(levels).includes(city.fallbackModel)) {
      const info = await inspectGlb(path.join(root, 'public', city.fallbackModel));
      fallback = { path: city.fallbackModel, ...pickModelInfo(info) };
    }

    cities.push({
      id: entry.id,
      name: entry.name,
      culture: entry.culture,
      period: entry.period,
      availability: entry.availability,
      maturity: entry.maturity,
      version: entry.version ?? null,
      evidence: entry.evidence,
      qa: entry.qa,
      stops: city.tour?.length ?? 0,
      layers: city.layers?.length ?? 0,
      models,
      fallback,
    });
  }

  const order = new Map(index.map((entry, position) => [entry.id, position]));
  cities.sort((a, b) => {
    const group = (city) => (city.availability === 'available' ? 0 : 1);
    return group(a) - group(b) || order.get(a.id) - order.get(b.id);
  });

  return { cities, warnings };
}

function formatMaturity(city) {
  return city.version ? `\`${city.maturity}\` · ${city.version}` : `\`${city.maturity}\``;
}

function formatEvidence(city, fallback = EVIDENCE_LABELS) {
  return fallback[city.evidence] ?? city.evidence;
}

function formatQa(city, labels) {
  if (city.availability === 'research') return 'No aplica';
  return labels[city.qa] ?? city.qa;
}

function formatTrisBytes(model) {
  if (!model) return '—';
  return `${number.format(model.triangles)} / ${number.format(model.bytes)} B`;
}

function formatCalls(city) {
  const lod0 = city.models['0']?.calls;
  const lod1 = city.models['1']?.calls;
  if (!Number.isFinite(lod0) && !Number.isFinite(lod1)) return '—';
  return `${Number.isFinite(lod0) ? lod0 : '—'} / ${Number.isFinite(lod1) ? lod1 : '—'}`;
}

function formatTextures(city) {
  const lod0 = city.models['0']?.textureMB;
  const lod1 = city.models['1']?.textureMB;
  if (!Number.isFinite(lod0) && !Number.isFinite(lod1)) return '—';
  const left = Number.isFinite(lod0) ? decimal.format(lod0) : '—';
  const right = Number.isFinite(lod1) ? decimal.format(lod1) : '—';
  return `${left} / ${right} MB VRAM estimada`;
}

function buildReadmeStatus(cities) {
  const rows = cities.map((city) => {
    const evidence = city.availability === 'research'
      ? 'Ficha documental'
      : formatEvidence(city);
    return `| ${city.name} | ${city.culture} · ${city.period} | \`${city.availability}\` | ${formatMaturity(city)} | ${evidence} | ${formatQa(city, QA_README)} |`;
  });
  return [
    '| Ciudad | Cultura / período | Disponibilidad | Madurez | Evidencia | QA |',
    '|---|---|---|---|---|---|',
    ...rows,
  ].join('\n');
}

function buildEstadoStatus(cities) {
  const rows = cities.map(
    (city) => `| ${city.name} | \`${city.availability}\` | ${formatMaturity(city)} | ${formatEvidence(city)} | ${formatQa(city, QA_ESTADO)} |`,
  );
  return [
    '| Ciudad | Disponibilidad | Madurez | Evidencia | QA |',
    '|---|---|---|---|---|',
    ...rows,
  ].join('\n');
}

function buildEstadoMetrics(cities) {
  const rows = cities
    .filter((city) => city.availability === 'available')
    .map(
      (city) => `| ${city.name} | ${formatTrisBytes(city.models['0'])} | ${formatTrisBytes(city.models['1'])} | ${formatCalls(city)} | ${city.stops || '—'} | hash |`,
    );
  return [
    '| Ciudad | LOD0 tris / bytes | LOD1 tris / bytes | Draw calls LOD0/LOD1 | Paradas | Caché |',
    '|---|---|---|---:|---:|---|',
    ...rows,
  ].join('\n');
}

function formatModelRow(label, model) {
  if (!model) return null;
  const calls = Number.isFinite(model.calls) ? model.calls : '—';
  return `| ${label} | ${number.format(model.triangles)} | ${number.format(model.bytes)} | ${model.images ?? '—'} | ${calls} |`;
}

function buildCityMetrics(city) {
  const evidence = formatEvidence(city).toLowerCase();
  const lines = [
    `**Estado canónico:** \`${city.availability}\` · \`${city.maturity}\`${city.version ? ` · ${city.version}` : ''} · evidencia ${evidence} · QA ${formatQa(city, QA_ESTADO)}.`,
    '',
    '| Modelo | Triángulos | Bytes | Imágenes | Draw calls |',
    '|---|---:|---:|---:|---:|',
  ];
  const rows = [
    formatModelRow('LOD0', city.models['0']),
    formatModelRow('LOD1', city.models['1']),
    city.fallback ? formatModelRow('Fallback', city.fallback) : null,
  ].filter(Boolean);
  if (!rows.length) lines.push('| — | — | — | — | — |');
  else lines.push(...rows);
  return lines.join('\n');
}

function buildRemasterStatus(cities) {
  const rows = cities.map(
    (city) => `| ${city.name} | \`${city.availability}\` | ${formatMaturity(city)} | ${formatEvidence(city)} | ${formatQa(city, QA_ESTADO)} | ${formatTrisBytes(city.models['0'])} | ${formatTrisBytes(city.models['1'])} | ${formatCalls(city)} |`,
  );
  return [
    '| Ciudad | Disponibilidad | Madurez | Evidencia | QA | LOD0 tris / bytes | LOD1 tris / bytes | Draw calls LOD0/LOD1 |',
    '|---|---|---|---|---|---|---|---|',
    ...rows,
  ].join('\n');
}

function buildAuditoriaMetrics(cities) {
  const rows = cities
    .filter((city) => city.availability === 'available')
    .map(
      (city) => `| ${city.name} | ${formatTrisBytes(city.models['0'])} | ${formatTrisBytes(city.models['1'])} | ${formatTextures(city)} | hash | \`npm run validate\` + QA |`,
    );
  return [
    '| Ciudad | LOD0 tris / bytes | LOD1 tris / bytes | Texturas | Caché | Fuente |',
    '|---|---|---|---|---|---|',
    ...rows,
  ].join('\n');
}

function replaceBlock(content, key, body) {
  const start = `<!-- metrics:${key}:start -->`;
  const end = `<!-- metrics:${key}:end -->`;
  const startIndex = content.indexOf(start);
  const endIndex = content.indexOf(end);
  if (startIndex < 0 || endIndex < startIndex) {
    throw new Error(`Falta el bloque de métricas "${key}"`);
  }
  return `${content.slice(0, startIndex + start.length)}\n${body}\n${content.slice(endIndex)}`;
}

async function buildOutputs() {
  const { cities, warnings } = await collectCities();
  const files = {};

  files[DOCS.readme] = replaceBlock(
    await readFile(path.join(root, DOCS.readme), 'utf8'),
    'readme-status',
    buildReadmeStatus(cities),
  );
  let estado = replaceBlock(
    await readFile(path.join(root, DOCS.estado), 'utf8'),
    'estado-status',
    buildEstadoStatus(cities),
  );
  estado = replaceBlock(estado, 'estado-metricas', buildEstadoMetrics(cities));
  files[DOCS.estado] = estado;
  files[DOCS.auditoria] = replaceBlock(
    await readFile(path.join(root, DOCS.auditoria), 'utf8'),
    'auditoria-metricas',
    buildAuditoriaMetrics(cities),
  );
  files[DOCS.remaster] = replaceBlock(
    await readFile(path.join(root, DOCS.remaster), 'utf8'),
    'remaster-status',
    buildRemasterStatus(cities),
  );
  for (const city of cities) {
    const file = `public/cities/${city.id}/README.md`;
    files[file] = replaceBlock(
      await readFile(path.join(root, file), 'utf8'),
      `city:${city.id}`,
      buildCityMetrics(city),
    );
  }
  files[METRICS_FILE] = `${JSON.stringify({ schemaVersion: 1, cities }, null, 2)}\n`;

  return { files, warnings };
}

async function main() {
  const check = process.argv.includes('--check');
  const { files, warnings } = await buildOutputs();
  for (const warning of warnings) console.warn(`AVISO  ${warning}`);

  if (check) {
    const stale = [];
    for (const [file, expected] of Object.entries(files)) {
      let actual = null;
      try {
        actual = await readFile(path.join(root, file), 'utf8');
      } catch {
        actual = null;
      }
      if (actual !== expected) stale.push(file);
    }
    if (stale.length) {
      for (const file of stale) console.error(`ERROR  ${file} desactualizado`);
      console.error('Ejecuta npm run docs:metrics');
      process.exit(1);
    }
    console.log('Métricas: OK');
    return;
  }

  for (const [file, content] of Object.entries(files)) {
    await writeFile(path.join(root, file), content);
  }
  console.log(`Métricas: ${files[METRICS_FILE] ? 'docs/metricas.json' : ''} y tablas actualizadas`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
