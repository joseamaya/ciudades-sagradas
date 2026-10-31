const CACHE = 'ciudades-sagradas-v37';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon.svg', './icons/icon-192.png', './icons/icon-512.png'];
const ASSET = /\.(?:glb|gltf|jpg|jpeg|png|webp|svg|woff2?|wasm)$/i;

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

async function fetchAndCache(request) {
  const response = await fetch(request);
  if (response.ok) {
    const copy = response.clone();
    const cache = await caches.open(CACHE);
    await cache.put(request, copy);
  }
  return response;
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  const cached = caches.match(request, { ignoreVary: true });

  if (ASSET.test(url.pathname)) {
    event.respondWith(cached.then((hit) => hit || fetchAndCache(request)));
    return;
  }

  event.respondWith(
    fetchAndCache(request).catch(() =>
      cached.then((hit) => hit || caches.match('./index.html', { ignoreVary: true })),
    ),
  );
});
