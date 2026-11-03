const DOUBLE_SIDED_MATERIAL = /(?:^|_)(Leaf|Leaves|LeafDark|Vegetation|Grass|Thatch|Cotton|Cloth|Fabric|Fire)$/i;
const SINGLE_SIDED_MATERIAL = /(?:^|_)(Water)$/i;
const LOD1_MATERIAL = /(?:^|_)LOD1(?:_|$)/i;
const TERRAIN_TOKEN = /(?:^|_)(Terrain|Field|Hill|Tree|Reed|Rock|Path|SiteApron)(?:_|$)/i;
const PROPS_TOKEN = /(?:^|_)(Props|Shicra|StoneBlock|CottonPlant|Textile|Offering|Pebble)(?:_|$)/i;
const REFERENCE_TOKEN = /(?:^|_)(Reference|HumanScale)(?:_|$)/i;

export function materialKey(material) {
  return (material?.name || '').split('.')[0];
}

export function isDoubleSided(material) {
  const key = materialKey(material);
  if (SINGLE_SIDED_MATERIAL.test(key)) return false;
  if (LOD1_MATERIAL.test(key)) return false;
  return DOUBLE_SIDED_MATERIAL.test(key);
}

export function isSingleSided(material) {
  return SINGLE_SIDED_MATERIAL.test(materialKey(material));
}

export function deviceProfile(env = globalThis) {
  const navigator = env.navigator ?? {};
  const browser = env.window ?? env;
  const userAgent = navigator.userAgent || '';
  const uaMobile = navigator.userAgentData?.mobile === true;
  const mobileUA = /Android|iPhone|iPad|iPod|Mobile|Tablet/i.test(userAgent);
  const iPadDesktop = /Macintosh/i.test(userAgent) && (navigator.maxTouchPoints ?? 0) > 1;
  const memory = navigator.deviceMemory ?? 8;
  const cores = navigator.hardwareConcurrency ?? 8;
  const screen = browser.screen ?? {};
  const small = Math.min(screen.width ?? Infinity, screen.height ?? Infinity) <= 600;
  const coarse = browser.matchMedia?.('(pointer: coarse)').matches === true;
  const lowPower = Boolean(
    uaMobile ||
    mobileUA ||
    iPadDesktop ||
    memory <= 4 ||
    cores <= 4 ||
    (small && coarse),
  );
  return { lowPower, uaMobile, mobileUA, iPadDesktop, memory, cores, small, coarse };
}

export function selectLodLevel(city, lowPower, search = globalThis.location?.search ?? '') {
  const levels = city.lod?.levels ?? {};
  const override = new URLSearchParams(search).get('lod');
  if (override && levels[override]) return override;
  const preferred = city.lod?.default;
  if (preferred && preferred !== 'auto' && levels[preferred]) return preferred;
  if (lowPower && levels['1']) return '1';
  if (levels['0']) return '0';
  return Object.keys(levels)[0] ?? null;
}

export function buildModelCandidates(city, lowPower, search) {
  const levels = city.lod?.levels ?? {};
  const selected = selectLodLevel(city, lowPower, search);
  const candidates = [];
  const add = (level, url) => {
    if (!url || candidates.some((candidate) => candidate.url === url)) return;
    candidates.push({ level, url });
  };
  if (selected && levels[selected]) add(selected, levels[selected]);

  if (lowPower && selected === '1') {
    add('v1', city.fallbackModel);
    for (const [level, url] of Object.entries(levels)) add(level, url);
    add(null, city.model);
    return candidates;
  }

  for (const [level, url] of Object.entries(levels)) add(level, url);
  add(null, city.model);
  add('v1', city.fallbackModel);
  return candidates;
}

export function classify(name = '') {
  const rest = name.replace(/^(?:GEO|MESH)-[^_]+_/, '');
  if (TERRAIN_TOKEN.test(rest)) return 'terrain';
  if (PROPS_TOKEN.test(rest)) return 'props';
  if (REFERENCE_TOKEN.test(rest)) return 'reference';
  return 'city';
}

export function layerFor(object) {
  let current = object;
  while (current) {
    if (typeof current.userData?.layer === 'string' && current.userData.layer) {
      return current.userData.layer;
    }
    current = current.parent;
  }
  return null;
}
