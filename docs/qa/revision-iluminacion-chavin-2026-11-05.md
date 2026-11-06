# Revisión de iluminación — Chavín

Fecha: 5 de noviembre de 2026.
Alcance: paradas 3 (Lanzón) y 5 (Portada), LOD0/LOD1, preset de mañana; comprobación visual de mediodía, atardecer y noche.
Herramienta: build de producción, Chromium 1600×900 y SwiftShader. No es una certificación de hardware real.

## Resultado

- **Lanzón:** la galería deja de ser una masa oscura; el relieve se lee con luz cálida de clave y relleno frío.
- **Portada:** el friso, las columnas y las jambas se leen en mañana; se añadieron luces de fachada y una luz suave en el vano para dar profundidad.
- **Sin cambios de geometría, GLB, hashes ni caché de modelos.**

## Cambios aplicados

En `public/cities/chavin/city.json`:

- Nuevo override `lighting.morning`: `fill 0.75`, `hemiIntensity 0.36`, `envIntensity 0.95`.
- Lanzón: luces puntuales cálida/fría con intensidades `0.12 / 0.06 / 0.05` y distancias `1.0 / 0.9 / 0.8`.
- Portada: tres luces puntuales con intensidades `0.6 / 0.3 / 0.25` y distancias `2.2 / 1.2 / 1.5`.

En `scripts/validate.mjs`:

- Validación de forma de `city.lighting` (`fill`, `hemiIntensity`, `envIntensity` finitos y no negativos; presets reconocidos).

## Capturas

Antes:

- [`before-lod0-lanzon.png`](./capturas/iluminacion-chavin-2026-11-05/before-lod0-lanzon.png)
- [`before-lod0-portada.png`](./capturas/iluminacion-chavin-2026-11-05/before-lod0-portada.png)
- [`before-lod1-lanzon.png`](./capturas/iluminacion-chavin-2026-11-05/before-lod1-lanzon.png)
- [`before-lod1-portada.png`](./capturas/iluminacion-chavin-2026-11-05/before-lod1-portada.png)

Después:

- [`after-lod0-lanzon.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod0-lanzon.png)
- [`after-lod0-portada.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod0-portada.png)
- [`after-lod1-lanzon.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod1-lanzon.png)
- [`after-lod1-portada.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod1-portada.png)
- [`after-lod0-portada-noon.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod0-portada-noon.png)
- [`after-lod0-portada-dusk.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod0-portada-dusk.png)
- [`after-lod0-portada-night.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod0-portada-night.png)
- [`after-lod0-lanzon-night.png`](./capturas/iluminacion-chavin-2026-11-05/after-lod0-lanzon-night.png)

## Verificación

- `npm run validate`: OK.
- `npm run build`: OK.
- `npx playwright test tests/qa/cities.spec.js tests/qa/evidence.spec.js tests/qa/desktop-review.spec.js --project=chromium-desktop-1600 --grep "Chavín"`: 4/4.
- Sin errores de consola en las capturas normales.
- Mediodía, atardecer y noche revisados sin sobreiluminación evidente.

## Límites

- Las capturas son de SwiftShader; no certifican FPS ni una GPU real.
- El vano de la Portada sigue siendo un acceso abierto y oscuro; se ilumina suavemente para dar profundidad, no se reconstruye un interior no conservado.
- Las posiciones de las luces se ajustaron visualmente; no sustituyen un levantamiento fotométrico.
