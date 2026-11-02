const CACHE = '__CACHE_VERSION__';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon.svg', './icons/icon-192.png', './icons/icon-512.png'];
const ASSET = /\.(?:glb|gltf|jpg|jpeg|png|webp|svg|woff2?|wasm)$/i;
const NETWORK_TIMEOUT_MS = 3500;

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(CORE)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))),
    ),
  );
  self.clients.claim();
});

async function cacheResponse(request, response) {
  if (response.status !== 200) return;
  try {
    const cache = await caches.open(CACHE);
    await cache.put(request, response.clone());
  } catch {}
}

async function fetchAndCache(request) {
  const response = await fetch(request);
  await cacheResponse(request, response);
  return response;
}

async function fetchWithTimeout(request) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), NETWORK_TIMEOUT_MS);
  try {
    return await fetch(request, { signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function networkFirst(request) {
  try {
    const response = await fetchWithTimeout(request);
    await cacheResponse(request, response);
    return response;
  } catch {
    const hit = await caches.match(request, { ignoreVary: true });
    if (hit) return hit;
    return (await caches.match('./index.html', { ignoreVary: true })) || Response.error();
  }
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (ASSET.test(url.pathname)) {
    if (request.headers.has('range')) {
      event.respondWith(fetchAndCache(request));
      return;
    }
    event.respondWith(
      caches.match(request, { ignoreVary: true }).then((hit) => hit || fetchAndCache(request)),
    );
    return;
  }

  event.respondWith(networkFirst(request));
});
