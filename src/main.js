import { AmbientAudio } from './core/audio.js';
import { renderCatalog } from './ui/catalog.js';
import { renderCity } from './ui/city.js';
import { evidenceBadge } from './ui/status.js';

const app = document.getElementById('app');
const loading = document.getElementById('loading');
const loadingBar = document.getElementById('loading-bar');
const loadingText = document.getElementById('loading-text');
const toastEl = document.getElementById('toast');

const PARAMS = new URLSearchParams(window.location.search);
const DEBUG = PARAMS.has('debug');
const NO_SW = PARAMS.has('nosw');
const audio = new AmbientAudio();
let cities = [];
let viewer = null;
let currentCity = null;
let routeToken = 0;
let tourIndex = 0;
let toastTimer = null;
let debugEl = null;
let debugTimer = null;
const qaIssues = [];

const asset = (path) => new URL(path, document.baseURI).href;

let cityViewerPromise = null;
function loadCityViewer() {
  if (!cityViewerPromise) {
    cityViewerPromise = import('./core/viewer.js')
      .then(({ CityViewer }) => CityViewer)
      .catch((error) => {
        cityViewerPromise = null;
        throw error;
      });
  }
  return cityViewerPromise;
}

function recordQaIssue(type, details = {}) {
  qaIssues.push({ type, time: new Date().toISOString(), ...details });
  if (qaIssues.length > 20) qaIssues.shift();
}

window.addEventListener('error', (event) => {
  recordQaIssue('error', {
    message: event.message || 'Error de ventana',
    source: event.filename || null,
    line: event.lineno || null,
    column: event.colno || null,
    city: currentCity?.id ?? null,
    route: window.location.hash || '#/',
  });
});

window.addEventListener('unhandledrejection', (event) => {
  recordQaIssue('unhandledrejection', {
    message: String(event.reason?.message ?? event.reason ?? 'Promesa rechazada'),
    city: currentCity?.id ?? null,
    route: window.location.hash || '#/',
  });
});

function buildQaReport() {
  return {
    schemaVersion: 1,
    generatedAt: new Date().toISOString(),
    route: window.location.hash || '#/',
    city: currentCity?.id ?? null,
    cityName: currentCity?.name ?? null,
    metrics: viewer?.getMetrics?.() ?? null,
    environment: viewer?.getEnvironment?.() ?? null,
    issues: [...qaIssues],
  };
}

function setupDebug() {
  if (!DEBUG) return;
  debugEl = document.createElement('div');
  debugEl.className = 'debug-panel';
  debugEl.innerHTML = '<button type="button" class="debug-copy" title="Incluye GPU, WebGL, PWA, flags y métricas">Copiar informe QA</button><pre class="debug-text" aria-live="polite"></pre>';
  document.body.appendChild(debugEl);
  const textEl = debugEl.querySelector('.debug-text');
  const copyButton = debugEl.querySelector('.debug-copy');

  const render = () => {
    const metrics = viewer?.getMetrics?.();
    if (!metrics) {
      textEl.textContent = 'debug · esperando visor 3D';
      return;
    }
    const environment = viewer?.getEnvironment?.();
    const mb = metrics.modelBytes ? `${(metrics.modelBytes / 1024 / 1024).toFixed(1)} MB` : '—';
    const gpu = environment?.webgl?.renderer || environment?.webgl?.vendor || '—';
    textEl.textContent = [
      `LOD ${metrics.lod ?? '—'} · ${metrics.lowPower ? 'móvil' : 'escritorio'} · ${metrics.timeOfDay}`,
      `${metrics.modelTriangles.toLocaleString('es')} tris · ${metrics.calls} calls · ${metrics.fps || 0} fps · ${metrics.frameMs || 0} ms`,
      `${metrics.viewport.width}×${metrics.viewport.height} @${metrics.pixelRatio} · sombras ${metrics.shadowMapSize[0]} · texturas ${metrics.textures} (${metrics.textureMB} MB)`,
      `GPU ${gpu} · WebGL ${environment?.webgl?.version ?? '—'} · máx. textura ${environment?.webgl?.maxTextureSize ?? '—'}`,
      `PWA ${environment?.standalone ? 'instalada' : 'navegador'} · SW ${environment?.serviceWorker ? 'sí' : 'no'} · ${environment?.online ? 'online' : 'offline'}`,
      `carga ${metrics.loadMs ?? '—'} ms · ${mb} · ${metrics.modelUrl ?? ''}`,
    ].join('\n');
  };

  copyButton.addEventListener('click', async () => {
    const report = buildQaReport();
    if (!report.metrics) {
      toast('El visor aún no está listo');
      return;
    }
    const text = JSON.stringify(report, null, 2);
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const area = document.createElement('textarea');
      area.value = text;
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }
    toast('Informe QA copiado');
  });

  render();
  debugTimer = setInterval(render, 500);
  window.addEventListener('beforeunload', () => clearInterval(debugTimer), { once: true });
}

function setLoading(progress, message) {
  if (loadingBar) loadingBar.style.width = `${Math.max(0, Math.min(100, progress))}%`;
  if (message && loadingText) loadingText.textContent = message;
}

function showLoading(message) {
  if (loadingText) loadingText.textContent = message;
  setLoading(4);
  loading.hidden = false;
}

function hideLoading() {
  loading.hidden = true;
}

function toast(message) {
  toastEl.textContent = message;
  toastEl.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastEl.hidden = true;
  }, 2600);
}

async function fetchJson(path) {
  const response = await fetch(asset(path), { cache: 'no-store' });
  if (!response.ok) throw new Error(`No se pudo cargar ${path} (${response.status})`);
  return response.json();
}

function parseRoute() {
  const hash = window.location.hash.replace(/^#\/?/, '');
  const [section, id] = hash.split('/');
  return { section: section || 'catalog', id: id || null };
}

function disposeViewer() {
  if (!viewer) return;
  viewer.dispose();
  viewer = null;
}

function goCatalog() {
  routeToken += 1;
  disposeViewer();
  audio.disable();
  currentCity = null;
  if (window.__cityKeyHandler) {
    window.removeEventListener('keydown', window.__cityKeyHandler);
    window.__cityKeyHandler = null;
  }
  window.__cityPanelCleanup?.();
  window.__cityPanelCleanup = null;
  document.title = 'Ciudades Sagradas';
  renderCatalog(app, cities);
  hideLoading();
  window.scrollTo({ top: 0, behavior: 'instant' });
}

function updateTour(refs, city, index, fly = false) {
  const tour = city.tour || [];
  if (!tour.length) return;
  tourIndex = (index + tour.length) % tour.length;
  const stop = tour[tourIndex];
  refs.tourCount.textContent = `${String(tourIndex + 1).padStart(2, '0')} / ${String(tour.length).padStart(2, '0')}`;
  refs.tourTitle.textContent = stop.title;
  refs.tourText.textContent = stop.text;
  if (refs.tourEvidence) refs.tourEvidence.innerHTML = evidenceBadge(stop.evidence, true);
  refs.tourList.querySelectorAll('button').forEach((button, i) => {
    const active = i === tourIndex;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-current', String(active));
  });
  if (fly && stop.camera) viewer?.setCamera(stop.camera, false);
}

function handlesKeyboardShortcuts(target) {
  if (!(target instanceof Element)) return true;
  return !target.closest(
    'input, textarea, select, button, a[href], [contenteditable], [role="textbox"]',
  );
}

function bindCity(refs, city) {
  const panel = refs.panel;
  const infoToggle = refs.infoToggle;
  const mobileQuery = window.matchMedia('(max-width: 980px)');
  const isMobile = () => mobileQuery.matches;
  const isPanelOpen = () =>
    isMobile() ? panel.classList.contains('is-open') : !panel.classList.contains('is-collapsed');

  const syncPanel = () => {
    const open = isPanelOpen();
    infoToggle?.setAttribute('aria-expanded', String(open));
    panel.setAttribute('aria-hidden', String(!open));
    panel.inert = !open;
  };

  const openPanel = ({ focus = false } = {}) => {
    if (isMobile()) panel.classList.add('is-open');
    else panel.classList.remove('is-collapsed');
    syncPanel();
    if (focus && isMobile()) refs.panelClose?.focus();
  };

  const closePanel = ({ focus = false } = {}) => {
    if (isMobile()) panel.classList.remove('is-open');
    else panel.classList.add('is-collapsed');
    syncPanel();
    if (focus) infoToggle?.focus();
  };

  infoToggle?.addEventListener('click', () => {
    if (isPanelOpen()) closePanel();
    else openPanel({ focus: true });
  });
  refs.panelClose?.addEventListener('click', () => closePanel({ focus: true }));
  refs.canvas?.addEventListener('pointerdown', () => {
    if (isMobile() && isPanelOpen()) closePanel();
  });

  mobileQuery.addEventListener('change', syncPanel);
  window.__cityPanelCleanup = () => mobileQuery.removeEventListener('change', syncPanel);
  syncPanel();

  refs.sound?.addEventListener('click', async () => {
    try {
      const enabled = await audio.toggle();
      refs.sound.setAttribute('aria-pressed', String(enabled));
      toast(enabled ? 'Audio ambiental activado' : 'Audio ambiental desactivado');
    } catch (error) {
      console.warn('Audio no disponible', error);
      toast('El audio no está disponible en este navegador');
    }
  });

  refs.timeButtons?.forEach((button) => {
    button.addEventListener('click', () => {
      viewer?.setTimeOfDay(button.dataset.time);
      refs.timeButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });
    });
  });

  refs.layerInputs?.forEach((input) => {
    input.addEventListener('change', () => viewer?.setLayer(input.dataset.layer, input.checked));
  });

  refs.tourList?.addEventListener('click', (event) => {
    const button = event.target.closest('[data-tour]');
    if (!button) return;
    updateTour(refs, city, Number(button.dataset.tour), true);
  });

  refs.tourNext?.addEventListener('click', () => updateTour(refs, city, tourIndex + 1, true));
  refs.tourPrev?.addEventListener('click', () => updateTour(refs, city, tourIndex - 1, true));

  updateTour(refs, city, 0, false);

  if (window.__cityKeyHandler) {
    window.removeEventListener('keydown', window.__cityKeyHandler);
  }
  const keyHandler = (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === 'Escape') {
      if (isPanelOpen()) {
        closePanel({ focus: true });
        return;
      }
      window.location.hash = '#/';
      return;
    }
    if (!handlesKeyboardShortcuts(event.target)) return;
    if (event.key === 'ArrowRight') {
      event.preventDefault();
      updateTour(refs, city, tourIndex + 1, true);
      return;
    }
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      updateTour(refs, city, tourIndex - 1, true);
      return;
    }
    if (event.key.toLowerCase() === 'h') document.body.classList.toggle('ui-hidden');
  };
  window.__cityKeyHandler = keyHandler;
  window.addEventListener('keydown', keyHandler);

  if (document.body.classList.contains('kiosk')) {
    const startAudio = async () => {
      const enabled = await audio.enable();
      refs.sound?.setAttribute('aria-pressed', String(enabled));
    };
    window.addEventListener('pointerdown', startAudio, { once: true });
  }
}

function showViewerError(refs, city) {
  const host = refs.canvas?.closest('.city-view');
  if (!host) return;
  host.querySelector('.city-error')?.remove();

  const box = document.createElement('div');
  box.className = 'city-error';
  box.setAttribute('role', 'alert');

  const title = document.createElement('p');
  title.className = 'city-error__title';
  title.textContent = `No se pudo cargar ${city.name}`;

  const detail = document.createElement('p');
  detail.textContent = 'El modelo 3D no está disponible. Puedes reintentar o volver al atlas.';

  const actions = document.createElement('div');
  actions.className = 'city-error__actions';

  const retry = document.createElement('button');
  retry.type = 'button';
  retry.textContent = 'Reintentar';
  retry.addEventListener('click', () => window.location.reload());

  const back = document.createElement('a');
  back.href = '#/';
  back.textContent = 'Volver al atlas';

  actions.append(retry, back);
  box.append(title, detail, actions);
  host.appendChild(box);
}

async function openCity(id) {
  const token = ++routeToken;
  window.__cityPanelCleanup?.();
  window.__cityPanelCleanup = null;
  const meta = cities.find((city) => city.id === id);
  if (!meta) {
    goCatalog();
    return;
  }

  disposeViewer();
  audio.disable();
  showLoading(`Preparando ${meta.name}…`);

  let city;
  try {
    city = await fetchJson(`cities/${id}/city.json`);
  } catch (error) {
    console.error(error);
    hideLoading();
    toast('No se pudo cargar la ficha de la ciudad.');
    goCatalog();
    return;
  }

  if (token !== routeToken) return;
  currentCity = city;
  document.title = `${city.name} · Ciudades Sagradas`;
  const refs = renderCity(app, city);

  if (!refs.available) {
    hideLoading();
    return;
  }

  let instance = null;
  try {
    const CityViewer = await loadCityViewer();
    if (token !== routeToken) return;
    instance = new CityViewer(refs.canvas, {
      onProgress: (progress) => {
        if (token !== routeToken) return;
        setLoading(8 + progress * 90, `Cargando ${city.name}…`);
      },
      onReady: () => {
        if (token !== routeToken) return;
        setLoading(100, 'Listo');
        setTimeout(() => {
          if (token === routeToken) hideLoading();
        }, 260);
        warmOfflineCache();
      },
      onError: (error) => {
        if (token !== routeToken) return;
        console.error(error);
        hideLoading();
        toast('No se pudo cargar el modelo 3D.');
        showViewerError(refs, city);
      },
    });
    viewer = instance;
    bindCity(refs, city);
    await instance.load(city);
    if (token !== routeToken) {
      instance.dispose();
      if (viewer === instance) viewer = null;
    }
  } catch (error) {
    console.error(error);
    hideLoading();
    toast('No se pudo iniciar el visor 3D.');
    showViewerError(refs, city);
    if (instance) {
      instance.dispose();
      if (viewer === instance) viewer = null;
    }
  }
}

async function route() {
  const { section, id } = parseRoute();
  if (section === 'ciudad' && id) {
    await openCity(id);
  } else {
    goCatalog();
  }
}

function setupKiosk() {
  const params = new URLSearchParams(window.location.search);
  const kiosk = params.get('kiosk') === '1' || params.get('modo') === 'kiosco';
  if (!kiosk) return;

  document.body.classList.add('kiosk');
  const enterFullscreen = () => {
    document.documentElement.requestFullscreen?.().catch(() => {});
    window.removeEventListener('pointerdown', enterFullscreen);
  };
  window.addEventListener('pointerdown', enterFullscreen, { once: true });

  let idleTimer;
  const resetIdle = () => {
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      if (window.location.hash && window.location.hash !== '#/') {
        window.location.hash = '#/';
      }
    }, 90000);
  };
  ['pointerdown', 'keydown', 'touchstart'].forEach((eventName) => {
    window.addEventListener(eventName, resetIdle, { passive: true });
  });
  resetIdle();
}

async function warmOfflineCache() {
  if (NO_SW || !import.meta.env.PROD || !('caches' in window) || !('serviceWorker' in navigator)) return;
  try {
    const ready = await Promise.race([
      navigator.serviceWorker.ready,
      new Promise((resolve) => setTimeout(() => resolve(null), 5000)),
    ]);
    if (!ready) return;
    const cacheName = (await caches.keys()).find((key) => key.startsWith('ciudades-sagradas-'));
    if (!cacheName) return;
    const cache = await caches.open(cacheName);
    const resources = performance
      .getEntriesByType('resource')
      .map((entry) => entry.name)
      .filter((url) => url.startsWith(window.location.origin));
    const urls = new Set([window.location.origin + window.location.pathname, ...resources]);
    await Promise.all(
      [...urls].map(async (url) => {
        if (await cache.match(url)) return;
        await cache.add(url).catch(() => {});
      }),
    );
  } catch (error) {
    console.warn('No se pudo preparar la caché offline', error);
  }
}

function registerServiceWorker() {
  if (NO_SW || !import.meta.env.PROD || !('serviceWorker' in navigator)) return;
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register(asset('sw.js'))
      .then(() => warmOfflineCache())
      .catch((error) => {
        console.warn('Service worker no registrado', error);
      });
  });
}

async function boot() {
  setupDebug();
  registerServiceWorker();
  setupKiosk();
  try {
    cities = await fetchJson('cities/index.json');
  } catch (error) {
    console.error(error);
    app.innerHTML = '<p style="padding:40px">No se pudo cargar el atlas. Revisa la conexión e inténtalo de nuevo.</p>';
    hideLoading();
    return;
  }
  window.addEventListener('hashchange', route);
  await route();
  window.__ciudadesSagradas = {
    get cities() {
      return cities;
    },
    get viewer() {
      return viewer;
    },
    get city() {
      return currentCity;
    },
    metrics: () => viewer?.getMetrics?.() ?? null,
    qaReport: buildQaReport,
    debug: DEBUG,
    openCity,
    goCatalog,
  };
}

boot();
