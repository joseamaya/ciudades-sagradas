# Registro de QA del atlas

Actualizado: 31 de octubre de 2026.
Protocolo: [`../estandares/qa-hardware.md`](../estandares/qa-hardware.md). Base de producción: `https://joseamaya.github.io/ciudades-sagradas/`.
Revisión funcional automatizada: [`revision-playwright.md`](./revision-playwright.md).
Auditoría de calidad desktop: [`auditoria-calidad-desktop-2026-10-31.md`](./auditoria-calidad-desktop-2026-10-31.md).

Este registro guarda los informes reales de `?debug=1`. No se marca un resultado como aprobado sin dispositivo, navegador, GPU, LOD, viewport y JSON completo.

## Reglas

- Un informe = un escenario. No mezclar LOD0 y LOD1 en el mismo JSON.
- Guardar el JSON completo en `docs/qa/resultados/` con nombre `YYYY-MM-DD_<ciudad>_<dispositivo>_<lod>[_<flags>].json`.
- Anotar aparte lo que el JSON no captura: paradas recorridas, capas, luces, PWA instalada, offline, 10 minutos y percepción visual.
- Un `pass` de producto no es un `pass` de rendimiento.
- Si falta GPU, navegador o viewport, el resultado es **parcial**, no aprobado.
- No se declara 1080p si la pantalla física no es 1080p.


## Playwright

```bash
npm run qa:playwright          # todos los proyectos por defecto (incluye 1080p emulado)
npm run qa:playwright:review   # Chromium desktop + Firefox + Chromium mobile
npm run qa:playwright:chromium # solo Chromium desktop 1600×900
npm run qa:playwright:smoke    # atlas + lazy-viewer + accesibilidad en Chromium
npm run qa:playwright:webkit   # opcional; requiere dependencias del host
```

Los artefactos quedan en `qa-output/` (ignorado por git) y el informe HTML en `playwright-report/`. Los JSON seleccionados se copian a `docs/qa/resultados/playwright/`.

La suite incluye `lazy-viewer.spec.js`: verifica que el catálogo no descarga el visor, que una ciudad sí lo carga y que un fallo del chunk muestra el estado recuperable.

CI ejecuta `qa:playwright:smoke` en cada PR y push a `main`: atlas, lazy-viewer y accesibilidad en Chromium desktop. Tarda ~3–4 min con instalación de navegador; la suite completa de 36 pruebas queda como revisión manual.

El workflow manual `.github/workflows/qa-playwright.yml` ejecuta Chromium desktop en CI y sube los artefactos.

WebKit no está activo por defecto: en este host faltan dependencias del sistema. Requiere `sudo npx playwright install-deps` o las librerías `libavif16`, `libgav1-1`, `libyuv0` y `libjxl0.8`. Playwright headless no certifica FPS ni GPU reales.

## Resultados recibidos

| Fecha | Ciudad | Escenario | Dispositivo / GPU | Navegador | LOD | Viewport | FPS | Frame | Calls | Tris | Texturas | Carga | PWA / offline | Issues | Estado | JSON |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 2026-10-30 | Caral | Desktop GPU integrada | Intel RPL-S (Mesa) | Chrome 139 / Linux | 0/1 | 1600×900 | 58–60 | 16,6–17,3 ms | 31–44 | 56.332–230.800 | 208–373,3 MB | Offline y standalone probados | 0 | **Desktop 1600×900 completo**; faltan 1080p y móvil | [`JSON`](./resultados/2026-10-30-caral-desktop-intel-lod0.json) |
| 2026-10-31 | Chavín v0.7 | Desktop GPU integrada | Intel RPL-S (Mesa) | Chrome 139 / Linux | 0/1 | 1600×900 | 60,0 | 16,7 ms | 19/16 | 42.842–249.942 | 72,0–136,0 MB | No probado en esta pasada | 0 | **Desktop 1600×900 v0.7 completo**; móvil/1080p pendientes | [`JSON`](./resultados/chavin-v07-desktop-2026-10-31/desktop.json) |
| 2026-10-31 | Atlas | Calidad desktop | Intel RPL-S (Mesa) | Chromium + Firefox / Linux | — | 1600×900 y 1920×1080 emulado | — | — | — | — | — | — | 0 | **Auditoría desktop completa**; móvil/kiosco/1080p real pendientes | [`Informe`](./auditoria-calidad-desktop-2026-10-31.md) |

Lectura: el equipo es una GPU integrada Intel, no dedicada. A 1600×900 las cuatro ciudades sostienen ~58–60 fps en LOD0/LOD1. Caral pasó flags, offline, standalone y 10 minutos con heap estable. Chavín v0.7 se repitió tras el pase de valle y la revisión visual: 59,8/60,0 fps, 19/16 calls y 0 errores. No certifica 1080p ni móvil. La auditoría desktop añade regresión Chromium/Firefox, accesibilidad, movimiento reducido y fallo recuperable de GLB; 1080p es emulación, no hardware. Detalle: [`resultados/desktop-2026-10-30/`](./resultados/desktop-2026-10-30/) y [`resultados/chavin-v07-desktop-2026-10-31/`](./resultados/chavin-v07-desktop-2026-10-31/).

## Matriz pendiente

### Escritorio actual (Intel RPL-S, Chrome/Linux, 1600×900)

| Escenario | URL | Estado | JSON |
|---|---|---|---|
| Caral LOD0 | `?debug=1&lod=0#/ciudad/caral` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-lod0.json) |
| Caral LOD1 | `?debug=1&lod=1#/ciudad/caral` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-lod1.json) |
| Caral sin suelo | `?debug=1&lod=0&noground=1#/ciudad/caral` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-flags-noground.json) |
| Caral sin sombras | `?debug=1&lod=0&noshadows=1#/ciudad/caral` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-flags-noshadows.json) |
| Caral sin suelo ni sombras | `?debug=1&lod=0&noground=1&noshadows=1#/ciudad/caral` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-flags-noground-noshadows.json) |
| Caral standalone/app | Abrir en modo app | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-standalone-lod0.json) |
| Caral offline | Cargar online, esperar caché, modo avión y recargar | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-offline-lod0.json) |
| Caral 10 minutos | Escena quieta con órbitas suaves; informe final | Hecho | [`JSON`](./resultados/desktop-2026-10-30/caral-long-session-lod0.json) |
| Chavín LOD0 v0.7 | `?debug=1&lod=0#/ciudad/chavin` | Hecho | [`JSON`](./resultados/chavin-v07-desktop-2026-10-31/desktop.json) |
| Chavín LOD1 v0.7 | `?debug=1&lod=1#/ciudad/chavin` | Hecho | [`JSON`](./resultados/chavin-v07-desktop-2026-10-31/desktop.json) |
| Aypate LOD0 | `?debug=1&lod=0#/ciudad/aypate` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/aypate-lod0.json) |
| Aypate LOD1 | `?debug=1&lod=1#/ciudad/aypate` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/aypate-lod1.json) |
| Narihualá LOD0 | `?debug=1&lod=0#/ciudad/narihuala` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/narihuala-lod0.json) |
| Narihualá LOD1 | `?debug=1&lod=1#/ciudad/narihuala` | Hecho | [`JSON`](./resultados/desktop-2026-10-30/narihuala-lod1.json) |

### Móvil real

| Escenario | Android/Chrome | iPhone/Safari |
|---|---|---|
| Caral LOD1 + 6 paradas | Pendiente | Pendiente |
| Caral `?noground=1` / `?noshadows=1` | Pendiente; incidencia `CARAL-ANDROID-GROUND-001` | Pendiente |
| Caral PWA + offline | Pendiente | Pendiente |
| Caral 10 minutos | Pendiente | Pendiente |
| Chavín LOD1 | Pendiente | Pendiente |
| Aypate LOD1 | Pendiente | Pendiente |
| Narihualá LOD1 | Pendiente | Pendiente |

### 1080p real

Pendiente. La pantalla del equipo actual es 1600×900; no se puede declarar el gate de 60 fps a 1080p sin una pantalla física 1080p. La emulación de viewport no cuenta como hardware real.

## Secuencia de captura

### A. Caral en escritorio

1. Abrir `https://joseamaya.github.io/ciudades-sagradas/?debug=1&lod=0#/ciudad/caral`.
2. Comprobar que el LOD es `0` y que el panel muestra GPU y WebGL.
3. Pulsar **Copiar informe QA**.
4. Repetir con `?lod=1`.
5. Repetir con `?noground=1`, `?noshadows=1` y la combinación.
6. Instalar la PWA, abrirla y repetir LOD0.
7. Cargar online, esperar a que el modelo quede en caché, activar modo avión y recargar.
8. Dejar la escena 10 minutos y capturar el informe final.

### B. Chavín, Aypate y Narihualá en escritorio

1. Abrir cada ciudad con `?debug=1&lod=0#/ciudad/<id>`.
2. Recorrer las seis paradas y probar las cuatro luces y las cuatro capas.
3. Copiar el informe QA.
4. Repetir con `?lod=1`.
5. Guardar cada JSON con el nombre acordado.

### C. Móvil real

1. Android/Chrome: Caral LOD1, `?noground=1`, `?noshadows=1`, combinación, PWA, offline y 10 minutos.
2. iPhone/Safari: el mismo recorrido; usar **Copiar informe QA** y guardar el JSON en Notas o Archivos si el portapapeles falla.
3. Anotar modelo, versión de SO, navegador y GPU si está disponible.
4. No cerrar `CARAL-ANDROID-GROUND-001` hasta completar la matriz.

## Cómo guardar un resultado

1. Copiar el JSON del botón.
2. Guardarlo como `docs/qa/resultados/YYYY-MM-DD_<ciudad>_<dispositivo>_<lod>[_<flags>].json`.
3. Añadir una fila a la tabla de resultados con el enlace al archivo.
4. Si el resultado cambia el estado de una ciudad, actualizar `docs/estandares/auditoria-ciudades.md`, `docs/estado.md` y el `qa` de `city.json` en el mismo PR.
5. No cambiar `maturity` ni `evidence` por un resultado de rendimiento.

## Criterio de cierre por ciudad

- Escritorio LOD0 y LOD1.
- Móvil real en LOD1.
- PWA instalada y offline.
- Seis paradas, cuatro luces y cuatro capas.
- 10 minutos sin errores ni crecimiento anómalo.
- 1080p real si el gate lo exige.
- JSON, captura o vídeo y dispositivo/GPU documentados.
