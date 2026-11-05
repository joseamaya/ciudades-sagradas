# Revisión de atmósfera — Aypate

Fecha: 5 de noviembre de 2026.
Alcance: parada 2 (La Plaza Inca) y vista hero, LOD0/LOD1, preset de mañana; revisión de Ushnu y Kallanka.
Herramienta: build de producción, Chromium 1600×900 y SwiftShader. No es una certificación de hardware real.

## Resultado

- **Plaza Inca:** el reencuadre eleva la cámara y muestra la explanada, el ushnu y el muro perimetral en lugar de un primer plano vacío.
- **Horizonte:** la niebla baja a `8–65` y funde el terreno lejano con el cielo; la vista hero gana profundidad de bosque de neblina.
- **Luz:** un override de mañana sube el relleno y la hemisférica para que el terreno y los muros no queden planos.
- **Sin cambios de geometría, GLB, hashes ni caché de modelos.**

## Cambios aplicados

En `public/cities/aypate/city.json`:

- Parada 2: cámara `[2.0, 2.2, 4.5]`, objetivo `[6.5, 0.4, -2.0]`, `fov 32`.
- `fog`: `near 8`, `far 65`.
- `lighting.morning`: `fill 0.45`, `hemiIntensity 0.22`, `envIntensity 0.55`.
- `lighting.night`: `fill 0.18`, `hemiIntensity 0.3`, `envIntensity 0.5` para conservar el contraste nocturno.

## Capturas

Antes:

- [`before-lod0-plaza.png`](./capturas/atmosfera-aypate-2026-11-05/before-lod0-plaza.png)
- [`before-lod0-hero.png`](./capturas/atmosfera-aypate-2026-11-05/before-lod0-hero.png)

Después:

- [`after-lod0-plaza.png`](./capturas/atmosfera-aypate-2026-11-05/after-lod0-plaza.png)
- [`after-lod1-plaza.png`](./capturas/atmosfera-aypate-2026-11-05/after-lod1-plaza.png)
- [`after-lod0-hero.png`](./capturas/atmosfera-aypate-2026-11-05/after-lod0-hero.png)
- [`after-lod1-hero.png`](./capturas/atmosfera-aypate-2026-11-05/after-lod1-hero.png)
- [`after-lod0-ushnu.png`](./capturas/atmosfera-aypate-2026-11-05/after-lod0-ushnu.png)
- [`after-lod0-kallanka.png`](./capturas/atmosfera-aypate-2026-11-05/after-lod0-kallanka.png)

## Verificación

- `npm run validate`: OK.
- `npm run build`: OK.
- `npx playwright test tests/qa/cities.spec.js tests/qa/evidence.spec.js tests/qa/viewer-camera.spec.js tests/qa/desktop-review.spec.js --project=chromium-desktop-1600 --grep "Aypate"`: 6/6.
- Sin errores de consola en las capturas normales.
- Ushnu y Kallanka revisados sin niebla excesiva ni pérdida de lectura.

## Límites

- Las capturas son de SwiftShader; no certifican FPS ni una GPU real.
- El pase es de cámara, niebla y luz. No añade vegetación ni una cresta lejana nueva; si se quiere más contenido de paisaje, requiere un pase de Blender y reexportar LOD0/LOD1.
- La niebla no sustituye un estudio atmosférico medido; es una lectura artística del bosque de neblina.
