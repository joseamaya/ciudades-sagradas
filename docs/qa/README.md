# Registro de QA del atlas

Actualizado: 30 de octubre de 2026.
Protocolo: [`../estandares/qa-hardware.md`](../estandares/qa-hardware.md). Base de producción: `https://joseamaya.github.io/ciudades-sagradas/`.
Revisión funcional automatizada: [`revision-playwright.md`](./revision-playwright.md).

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
npm run qa:playwright:webkit   # opcional; requiere dependencias del host
```

Los artefactos quedan en `qa-output/` (ignorado por git) y el informe HTML en `playwright-report/`. Los JSON seleccionados se copian a `docs/qa/resultados/playwright/`.

El workflow manual `.github/workflows/qa-playwright.yml` ejecuta Chromium desktop en CI y sube los artefactos.

WebKit no está activo por defecto: en este host faltan dependencias del sistema. Requiere `sudo npx playwright install-deps` o las librerías `libavif16`, `libgav1-1`, `libyuv0` y `libjxl0.8`. Playwright headless no certifica FPS ni GPU reales.

## Resultados recibidos

| Fecha | Ciudad | Escenario | Dispositivo / GPU | Navegador | LOD | Viewport | FPS | Frame | Calls | Tris | Texturas | Carga | PWA / offline | Issues | Estado | JSON |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 2026-10-30 | Caral | Desktop GPU integrada | Intel RPL-S (Mesa) | Chrome 139 / Linux | 0 | 1600×900 | 60 | 16,67 ms | 44 | 230.800 | 373,3 MB | Navegador, SW activo, online | 0 | **Pass parcial 1600×900**; faltan 1080p, LOD1, offline, 10 min y móvil | [`JSON`](./resultados/2026-10-30-caral-desktop-intel-lod0.json) |

Lectura: el equipo es una GPU integrada Intel, no dedicada. A 1600×900 Caral LOD0 sostiene 60 fps con 44 draw calls y carga subjetivamente rápida (957 ms). No certifica 1080p ni móvil.

## Matriz pendiente

### Escritorio actual (Intel RPL-S, Chrome/Linux, 1600×900)

| Escenario | URL | Estado | JSON |
|---|---|---|---|
| Caral LOD0 | `?debug=1&lod=0#/ciudad/caral` | Hecho | [`2026-10-30...`](./resultados/2026-10-30-caral-desktop-intel-lod0.json) |
| Caral LOD1 | `?debug=1&lod=1#/ciudad/caral` | Pendiente | — |
| Caral sin suelo | `?debug=1&lod=0&noground=1#/ciudad/caral` | Pendiente | — |
| Caral sin sombras | `?debug=1&lod=0&noshadows=1#/ciudad/caral` | Pendiente | — |
| Caral sin suelo ni sombras | `?debug=1&lod=0&noground=1&noshadows=1#/ciudad/caral` | Pendiente | — |
| Caral PWA instalada | Instalar y abrir `?debug=1&lod=0#/ciudad/caral` | Pendiente | — |
| Caral offline | Cargar online, esperar caché, modo avión y recargar | Pendiente | — |
| Caral 10 minutos | Escena quieta con órbitas suaves; informe final | Pendiente | — |
| Chavín LOD0 | `?debug=1&lod=0#/ciudad/chavin` | Pendiente | — |
| Chavín LOD1 | `?debug=1&lod=1#/ciudad/chavin` | Pendiente | — |
| Aypate LOD0 | `?debug=1&lod=0#/ciudad/aypate` | Pendiente | — |
| Aypate LOD1 | `?debug=1&lod=1#/ciudad/aypate` | Pendiente | — |
| Narihualá LOD0 | `?debug=1&lod=0#/ciudad/narihuala` | Pendiente | — |
| Narihualá LOD1 | `?debug=1&lod=1#/ciudad/narihuala` | Pendiente | — |

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
