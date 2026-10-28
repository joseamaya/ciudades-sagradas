#!/usr/bin/env node
/**
 * Benchmark reproducible de una ciudad con Chrome DevTools Protocol.
 *
 * Uso:
 *   npm run build
 *   npm run bench -- --out /tmp/caral-bench
 *   npm run bench -- --city chavin --out /tmp/chavin-bench --qa
 *
 * El script levanta `npm run serve`, abre Chrome headless con SwiftShader y
 * mide LOD0, LOD1, móvil, fallback y offline. No requiere dependencias nuevas.
 *
 * En CI no se ejecuta: SwiftShader no representa una GPU real. Sirve para
 * comparar antes/después y detectar regresiones de draw calls, triángulos,
 * texturas, carga y consola.
 */

import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const ROOT = path.resolve(import.meta.dirname, '..');
const CHROME = process.env.CHROME_BIN || 'google-chrome';
const DEBUG_PORT = 9222;
const args = process.argv.slice(2);
const arg = (name, fallback) => {
  const index = args.indexOf(`--${name}`);
  return index >= 0 ? args[index + 1] : fallback;
};
const BASE = arg('base', 'http://127.0.0.1:4173/');
const OUT_DIR = path.resolve(arg('out', '/tmp/ciudades-sagradas-bench'));
const ONLY = arg('only', '');
const CITY = arg('city', 'caral');
const CITY_ROUTE = `#/ciudad/${CITY}`;
const NO_SERVER = args.includes('--no-server');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function waitForHttp(url, timeout = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    try {
      const response = await fetch(url);
      if (response.ok) return;
    } catch {
      // esperando
    }
    await sleep(250);
  }
  throw new Error(`Timeout esperando ${url}`);
}

class CDP {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.nextId = 1;
    this.pending = new Map();
    this.listeners = new Map();
  }

  async connect() {
    this.ws = new WebSocket(this.url);
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
    this.ws.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.id) {
        const pending = this.pending.get(message.id);
        if (!pending) return;
        this.pending.delete(message.id);
        if (message.error) pending.reject(new Error(message.error.message));
        else pending.resolve(message.result);
        return;
      }
      const handlers = this.listeners.get(message.method) || [];
      for (const handler of handlers) handler(message.params);
    });
  }

  send(method, params = {}) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  on(method, handler) {
    if (!this.listeners.has(method)) this.listeners.set(method, []);
    this.listeners.get(method).push(handler);
  }

  once(method) {
    return new Promise((resolve) => {
      const handler = (params) => {
        const handlers = this.listeners.get(method) || [];
        this.listeners.set(method, handlers.filter((item) => item !== handler));
        resolve(params);
      };
      this.on(method, handler);
    });
  }

  close() {
    this.ws?.close();
  }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
    userGesture: true,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.text || 'Error evaluando en la página');
  }
  return result.result?.value;
}

const READY_EXPRESSION = `(() => {
  const viewer = window.__ciudadesSagradas?.viewer;
  return Boolean(viewer && viewer.model && viewer.lodLevel !== null && viewer.lodLevel !== undefined);
})()`;

async function waitForViewer(cdp, timeout = 120000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    if (await evaluate(cdp, READY_EXPRESSION)) return;
    await sleep(250);
  }
  throw new Error('Timeout esperando el visor 3D');
}

const METRICS_EXPRESSION = `(() => {
  const viewer = window.__ciudadesSagradas?.viewer;
  if (!viewer) return { error: 'sin viewer' };
  const metrics = viewer.getMetrics?.() ?? {};
  const entries = performance.getEntriesByType('resource');
  const modelEntry = entries
    .filter((entry) => entry.name.includes('model'))
    .sort((a, b) => b.responseEnd - a.responseEnd)[0];
  return {
    ...metrics,
    camera: {
      position: viewer.camera.position.toArray().map((value) => +value.toFixed(3)),
      target: viewer.controls.target.toArray().map((value) => +value.toFixed(3)),
      fov: viewer.camera.fov,
      modelScale: viewer.model?.scale?.toArray?.().map((value) => +value.toFixed(4)),
    },
    modelResponseEnd: modelEntry ? Math.round(modelEntry.responseEnd) : null,
    transferBytes: modelEntry ? modelEntry.transferSize : null,
    encodedBytes: modelEntry ? modelEntry.encodedBodySize : null,
    device: {
      userAgent: navigator.userAgent,
      memory: navigator.deviceMemory ?? null,
      cores: navigator.hardwareConcurrency ?? null,
      screen: [window.screen.width, window.screen.height],
      touch: navigator.maxTouchPoints,
    },
  };
})()`;

const FPS_EXPRESSION = `new Promise((resolve) => {
  let frames = 0;
  let last = performance.now();
  const start = last;
  let maxDelta = 0;
  function tick(now) {
    const delta = now - last;
    last = now;
    if (delta > maxDelta) maxDelta = delta;
    frames += 1;
    if (now - start >= 2500) {
      const elapsed = now - start;
      resolve({
        fps: +(frames * 1000 / elapsed).toFixed(1),
        frameMs: +(elapsed / frames).toFixed(2),
        worstFrameMs: +maxDelta.toFixed(2),
      });
      return;
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})`;

async function navigate(cdp, url) {
  const loaded = cdp.once('Page.loadEventFired');
  await cdp.send('Page.navigate', { url });
  await Promise.race([loaded, sleep(10000)]);
  await waitForViewer(cdp);
  await sleep(750);
}

async function reload(cdp) {
  const loaded = cdp.once('Page.loadEventFired');
  await cdp.send('Page.reload', { ignoreCache: true });
  await Promise.race([loaded, sleep(10000)]);
  await waitForViewer(cdp);
  await sleep(750);
}

async function capture(cdp, file) {
  const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  await writeFile(file, Buffer.from(data, 'base64'));
}

async function measure(cdp) {
  const metrics = await evaluate(cdp, METRICS_EXPRESSION);
  const fps = await evaluate(cdp, FPS_EXPRESSION);
  const shadow = await evaluate(
    cdp,
    `(() => {
      const viewer = window.__ciudadesSagradas.viewer;
      viewer.renderer.info.reset();
      viewer.renderer.shadowMap.needsUpdate = true;
      viewer.renderer.render(viewer.scene, viewer.camera);
      return {
        shadowRefreshCalls: viewer.renderer.info.render.calls,
        shadowRefreshTriangles: viewer.renderer.info.render.triangles,
      };
    })()`,
  );
  return { ...metrics, ...fps, ...shadow };
}

async function resetDevice(cdp) {
  await cdp.send('Emulation.clearDeviceMetricsOverride');
  await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: false });
  await cdp.send('Emulation.setUserAgentOverride', { userAgent: '' });
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true });
  const viteBin = path.join(ROOT, 'node_modules/vite/bin/vite.js');
  const server = NO_SERVER
    ? null
    : spawn(process.execPath, [viteBin, 'preview', '--host', '127.0.0.1', '--port', '4173'], {
        cwd: ROOT,
        stdio: ['ignore', 'pipe', 'pipe'],
        env: { ...process.env },
      });
  server?.stdout.on('data', () => {});
  server?.stderr.on('data', (data) => process.stderr.write(data));
  const chrome = spawn(
    CHROME,
    [
      '--headless=new',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--enable-unsafe-swiftshader',
      '--use-angle=swiftshader',
      '--disable-background-networking',
      '--window-size=1600,900',
      '--no-first-run',
      '--no-default-browser-check',
      `--remote-debugging-port=${DEBUG_PORT}`,
      '--remote-allow-origins=*',
      `--user-data-dir=${path.join(OUT_DIR, 'chrome-profile')}`,
      'about:blank',
    ],
    { stdio: ['ignore', 'ignore', 'pipe'] },
  );
  chrome.stderr.on('data', () => {});

  let cdp = null;
  try {
    await waitForHttp(BASE);
    await waitForHttp(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
    const targets = await (await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`)).json();
    const page = targets.find((target) => target.type === 'page');
    if (!page) throw new Error('Chrome no expuso una pestaña');
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.connect();
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Log.enable');
    await cdp.send('Network.enable');

    const consoleMessages = [];
    cdp.on('Runtime.consoleAPICalled', (params) => {
      if (params.type === 'error' || params.type === 'warning') {
        consoleMessages.push({
          type: params.type,
          text: params.args.map((item) => item.value ?? item.description ?? '').join(' '),
        });
      }
    });
    cdp.on('Log.entryAdded', (params) => {
      if (params.entry.level === 'error' || params.entry.level === 'warning') {
        consoleMessages.push({ type: params.entry.level, text: params.entry.text });
      }
    });

    const results = {};
    const run = async (name, url, device = null) => {
      if (ONLY && ONLY !== name) return;
      await resetDevice(cdp);
      if (device) {
        await cdp.send('Emulation.setDeviceMetricsOverride', {
          width: device.width,
          height: device.height,
          deviceScaleFactor: device.scale || 1,
          mobile: device.mobile === true,
        });
        if (device.mobile) {
          await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
          await cdp.send('Emulation.setUserAgentOverride', { userAgent: device.userAgent });
        }
      }
      consoleMessages.length = 0;
      await navigate(cdp, url);
      const metrics = await measure(cdp);
      await capture(cdp, path.join(OUT_DIR, `${name}.png`));
      results[name] = { ...metrics, console: [...consoleMessages] };
      console.log(`${name}: ${metrics.lod} · ${metrics.calls} calls · ${metrics.modelTriangles} tris · ${metrics.fps} fps · ${metrics.textureMB} MB texturas`);
    };

    const desktop = { width: 1600, height: 900, scale: 1, mobile: false };
    const mobile = {
      width: 390,
      height: 844,
      scale: 3,
      mobile: true,
      userAgent:
        'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    };

    await run('desktop-lod0', `${BASE}?lod=0${CITY_ROUTE}`, desktop);
    await run('desktop-lod1', `${BASE}?lod=1${CITY_ROUTE}`, desktop);
    await run('desktop-debug', `${BASE}?debug=1${CITY_ROUTE}`, desktop);
    await run('desktop-noground', `${BASE}?lod=0&noground=1${CITY_ROUTE}`, desktop);
    await run('mobile-auto', `${BASE}${CITY_ROUTE}`, mobile);

    if (!ONLY || ONLY === 'fallback') {
      await resetDevice(cdp);
      await navigate(cdp, `${BASE}?nosw=1${CITY_ROUTE}`);
      const clearCaches = async () => {
        await cdp.send('Storage.clearDataForOrigin', {
          origin: BASE.replace(/\/$/, ''),
          storageTypes: 'cache_storage,service_workers',
        });
        await evaluate(cdp, `(async () => {
          const registrations = navigator.serviceWorker
            ? await navigator.serviceWorker.getRegistrations()
            : [];
          await Promise.all(registrations.map((registration) => registration.unregister()));
          const keys = await caches.keys();
          await Promise.all(keys.map((key) => caches.delete(key)));
          return true;
        })()`);
      };
      await clearCaches();
      await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
      await cdp.send('Network.setBlockedURLs', { urls: ['*model_lod0.glb*'] });
      consoleMessages.length = 0;
      await navigate(cdp, `${BASE}?nosw=1&lod=0&_=${Date.now()}${CITY_ROUTE}`);
      results['fallback-without-lod0'] = {
        ...(await measure(cdp)),
        console: [...consoleMessages],
      };
      console.log(`fallback-without-lod0: ${results['fallback-without-lod0'].lod}`);

      if (CITY === 'caral') {
        await clearCaches();
        await cdp.send('Network.setBlockedURLs', { urls: ['*model_lod*.glb*'] });
        consoleMessages.length = 0;
        await navigate(cdp, `${BASE}?nosw=1&lod=0&_=${Date.now()}${CITY_ROUTE}`);
        results['fallback-v1'] = { ...(await measure(cdp)), console: [...consoleMessages] };
        console.log(`fallback-v1: ${results['fallback-v1'].lod}`);

        await cdp.send('Network.setBlockedURLs', { urls: [] });
        await resetDevice(cdp);
        await cdp.send('Emulation.setDeviceMetricsOverride', {
          width: mobile.width,
          height: mobile.height,
          deviceScaleFactor: mobile.scale,
          mobile: true,
        });
        await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
        await cdp.send('Emulation.setUserAgentOverride', { userAgent: mobile.userAgent });
        await clearCaches();
        await cdp.send('Network.setBlockedURLs', { urls: ['*model_lod1.glb*'] });
        consoleMessages.length = 0;
        await navigate(cdp, `${BASE}?nosw=1&_=${Date.now()}${CITY_ROUTE}`);
        results['fallback-mobile-v1'] = { ...(await measure(cdp)), console: [...consoleMessages] };
        console.log(`fallback-mobile-v1: ${results['fallback-mobile-v1'].lod}`);
      } else {
        console.log(`fallback-v1/mobile-v1: omitido para ${CITY} (sin fallback v1)`);
      }
      await cdp.send('Network.setBlockedURLs', { urls: [] });
      await cdp.send('Network.setCacheDisabled', { cacheDisabled: false });
    }

    if (!ONLY || ONLY === 'offline') {
      await resetDevice(cdp);
      await navigate(cdp, `${BASE}${CITY_ROUTE}`);
      await evaluate(
        cdp,
        `navigator.serviceWorker.ready.then(() => new Promise((resolve) => {
          const started = performance.now();
          const check = async () => {
            const names = await caches.keys();
            const name = names.find((item) => item.startsWith('ciudades-sagradas-'));
            if (name) {
              const cache = await caches.open(name);
              const keys = await cache.keys();
              if (keys.some((request) => request.url.includes('model_lod'))) return resolve(true);
            }
            if (performance.now() - started > 30000) return resolve(false);
            setTimeout(check, 300);
          };
          check();
        }))`,
      );
      await reload(cdp);
      await cdp.send('Network.emulateNetworkConditions', {
        offline: true,
        latency: 0,
        downloadThroughput: 0,
        uploadThroughput: 0,
      });
      consoleMessages.length = 0;
      await reload(cdp);
      results.offline = { ...(await measure(cdp)), console: [...consoleMessages] };
      console.log(`offline: ${results.offline.lod} · ${results.offline.calls} calls`);
      await cdp.send('Network.emulateNetworkConditions', {
        offline: false,
        latency: 0,
        downloadThroughput: -1,
        uploadThroughput: -1,
      });
    }

    if (args.includes('--qa')) {
      await resetDevice(cdp);
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: 1600,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false,
      });
      await navigate(cdp, `${BASE}?lod=0&_=${Date.now()}${CITY_ROUTE}`);
      const tourCount = await evaluate(cdp, 'window.__ciudadesSagradas.city.tour.length');
      for (let index = 0; index < tourCount; index += 1) {
        await evaluate(cdp, `document.querySelector('[data-tour="${index}"]')?.click()`);
        await sleep(3500);
        const tourCamera = await evaluate(cdp, `(() => {
          const viewer = window.__ciudadesSagradas.viewer;
          return {
            position: viewer.camera.position.toArray().map((value) => +value.toFixed(3)),
            target: viewer.controls.target.toArray().map((value) => +value.toFixed(3)),
            flight: Boolean(viewer.flight),
          };
        })()`);
        console.log(`qa-tour-${index + 1}: ${JSON.stringify(tourCamera)}`);
        await capture(cdp, path.join(OUT_DIR, `qa-lod0-tour-${index + 1}.png`));
      }
      await evaluate(cdp, `document.querySelector('[data-tour="0"]')?.click()`);
      await sleep(2200);
      for (const time of ['noon', 'dusk', 'night']) {
        await evaluate(cdp, `document.querySelector('[data-time="${time}"]')?.click()`);
        await sleep(2400);
        await capture(cdp, path.join(OUT_DIR, `qa-lod0-${time}.png`));
      }
      await evaluate(cdp, `document.querySelector('[data-time="morning"]')?.click()`);
      await evaluate(cdp, `document.body.classList.add('ui-hidden')`);
      await sleep(600);
      await capture(cdp, path.join(OUT_DIR, 'qa-lod0-clean.png'));
      await evaluate(cdp, `document.body.classList.remove('ui-hidden')`);

      await navigate(cdp, `${BASE}?lod=1&_=${Date.now()}${CITY_ROUTE}`);
      await evaluate(cdp, `document.querySelector('[data-tour="5"]')?.click()`);
      await sleep(2200);
      await capture(cdp, path.join(OUT_DIR, 'qa-lod1-altar.png'));
      await evaluate(cdp, `document.querySelector('[data-tour="2"]')?.click()`);
      await sleep(2200);
      await capture(cdp, path.join(OUT_DIR, 'qa-lod1-tour-3.png'));

      await resetDevice(cdp);
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: mobile.width,
        height: mobile.height,
        deviceScaleFactor: mobile.scale,
        mobile: true,
      });
      await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await cdp.send('Emulation.setUserAgentOverride', { userAgent: mobile.userAgent });
      await navigate(cdp, `${BASE}?_=${Date.now()}${CITY_ROUTE}`);
      await evaluate(cdp, `document.querySelector('#info-toggle')?.click()`);
      await sleep(700);
      await capture(cdp, path.join(OUT_DIR, 'qa-mobile-panel.png'));
      const scrollInfo = await evaluate(
        cdp,
        `(() => {
          const el = document.querySelector('.panel-scroll');
          if (!el) return null;
          el.scrollTop = el.scrollHeight;
          return { scrollHeight: el.scrollHeight, clientHeight: el.clientHeight, scrollTop: el.scrollTop };
        })()`,
      );
      console.log('mobile panel scroll', JSON.stringify(scrollInfo));
      await sleep(600);
      await capture(cdp, path.join(OUT_DIR, 'qa-mobile-panel-scrolled.png'));
      await evaluate(cdp, `document.body.classList.add('ui-hidden')`);
      await sleep(500);
      await capture(cdp, path.join(OUT_DIR, 'qa-mobile-clean.png'));
      await evaluate(cdp, `document.body.classList.remove('ui-hidden')`);

      await navigate(cdp, `${BASE}?lod=1&_=${Date.now()}${CITY_ROUTE}`);
      await evaluate(cdp, `document.querySelector('[data-tour="2"]')?.click()`);
      await sleep(2200);
      await evaluate(cdp, `document.body.classList.add('ui-hidden')`);
      await sleep(500);
      await capture(cdp, path.join(OUT_DIR, 'qa-mobile-lod1-tour-3.png'));
      await evaluate(cdp, `document.body.classList.remove('ui-hidden')`);

      await resetDevice(cdp);
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1,
        mobile: false,
      });
      await navigate(cdp, `${BASE}?kiosk=1&_=${Date.now()}${CITY_ROUTE}`);
      await capture(cdp, path.join(OUT_DIR, 'qa-kiosk.png'));
      await resetDevice(cdp);

      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: 1600,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false,
      });
      await cdp.send('Page.navigate', { url: `${BASE}?_=${Date.now()}` });
      await sleep(1200);
      await capture(cdp, path.join(OUT_DIR, 'qa-atlas.png'));
      await cdp.send('Page.navigate', { url: `${BASE}?_=${Date.now()}${CITY_ROUTE}` });
      await sleep(800);
      await capture(cdp, path.join(OUT_DIR, `qa-${CITY}.png`));

      await resetDevice(cdp);
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: mobile.width,
        height: mobile.height,
        deviceScaleFactor: mobile.scale,
        mobile: true,
      });
      await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await cdp.send('Emulation.setUserAgentOverride', { userAgent: mobile.userAgent });
      await cdp.send('Page.navigate', { url: `${BASE}?_=${Date.now()}` });
      await sleep(1200);
      await capture(cdp, path.join(OUT_DIR, 'qa-mobile-atlas.png'));

      await resetDevice(cdp);
      console.log('QA screenshots generados');
    }

    await writeFile(path.join(OUT_DIR, 'bench.json'), JSON.stringify(results, null, 2));
    console.log(`\nResultados: ${path.join(OUT_DIR, 'bench.json')}`);
    console.log(`Capturas: ${OUT_DIR}`);
  } finally {
    cdp?.close();
    chrome.kill('SIGKILL');
    server?.kill('SIGKILL');
    await sleep(500);
  }
}

main()
  .then(() => setTimeout(() => process.exit(0), 200))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
