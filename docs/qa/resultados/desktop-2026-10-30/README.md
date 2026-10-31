# Desktop real — 30 de octubre de 2026

Equipo: Linux, Google Chrome 139, Intel RPL-S (Mesa Intel Graphics), 24 núcleos, 8 GB reportados, pantalla 1600×900.
GPU: `ANGLE (Intel, Mesa Intel(R) Graphics (RPL-S), OpenGL 4.6)`.
No es 1080p: la pantalla física es 1600×900.

## Escenarios

| Escenario | LOD | FPS | Frame | Calls | Carga | Estado | JSON |
|---|---:|---:|---:|---:|---:|---|---|
| Caral | 0 | 58,1 | 17,21 ms | 44 | 1.135 ms | Pass 1600×900 | [`caral-lod0.json`](./caral-lod0.json) |
| Caral | 1 | 57,9 | 17,27 ms | 31 | 743 ms | Pass 1600×900 | [`caral-lod1.json`](./caral-lod1.json) |
| Chavín | 0 | 59,5 | 16,81 ms | 18 | 1.433 ms | Pass 1600×900 | [`chavin-lod0.json`](./chavin-lod0.json) |
| Chavín | 1 | 60,2 | 16,61 ms | 14 | 270 ms | Pass 1600×900 | [`chavin-lod1.json`](./chavin-lod1.json) |
| Aypate | 0 | 60,0 | 16,68 ms | 17 | 521 ms | Pass 1600×900 | [`aypate-lod0.json`](./aypate-lod0.json) |
| Aypate | 1 | 58,2 | 17,20 ms | 15 | 301 ms | Pass 1600×900 | [`aypate-lod1.json`](./aypate-lod1.json) |
| Narihualá | 0 | 58,4 | 17,12 ms | 14 | 387 ms | Pass 1600×900 | [`narihuala-lod0.json`](./narihuala-lod0.json) |
| Narihualá | 1 | 59,9 | 16,68 ms | 13 | 218 ms | Pass 1600×900 | [`narihuala-lod1.json`](./narihuala-lod1.json) |

## Caral: flags, PWA y sesión

| Escenario | Resultado | JSON |
|---|---|---|
| `?noground=1` | 60,1 fps · 43 calls · sin errores | [`caral-flags-noground.json`](./caral-flags-noground.json) |
| `?noshadows=1` | 58,0 fps · 44 calls · sin errores | [`caral-flags-noshadows.json`](./caral-flags-noshadows.json) |
| `?noground=1&noshadows=1` | 60,0 fps · 43 calls · sin errores | [`caral-flags-noground-noshadows.json`](./caral-flags-noground-noshadows.json) |
| Offline tras cachear | `online: false`, modelo listo, sin errores | [`caral-offline-lod0.json`](./caral-offline-lod0.json) |
| App/standalone | `display-mode: standalone`, modelo listo | [`caral-standalone-lod0.json`](./caral-standalone-lod0.json) |
| Sesión de 10 min | 59,9–60,4 fps; JS heap ~29,5–31,5 MB; sin errores | [`caral-long-session-lod0.json`](./caral-long-session-lod0.json) |

La sesión de 10 minutos orbitó la cámara cada 30 s. No hubo crecimiento anómalo del heap ni errores de consola.

## Lectura

- El desktop integrado sostiene ~60 fps en las cuatro ciudades, en LOD0 y LOD1, a 1600×900.
- Offline y modo standalone funcionan en Chrome desktop.
- Sigue pendiente 1080p real, Android/iPhone y la incidencia Android de Caral.
- Este informe sí es hardware real; no mezclarlo con los JSON de Playwright/SwiftShader.
