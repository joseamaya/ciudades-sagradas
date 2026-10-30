# Revisión Playwright — preview público

Fecha: 30 de octubre de 2026.
Alcance: revisión funcional, visual y de consola del atlas publicado. No es una certificación de hardware.

## Herramientas

- `@playwright/test` 1.64.1.
- Playwright MCP configurado en `opencode.json`.
- Navegadores: Chromium y Firefox en local. WebKit quedó bloqueado por dependencias del host.
- Entorno: Linux; Chromium con SwiftShader y Firefox headless con GPU enmascarada.

## Comandos ejecutados

```bash
npm run validate
npm run build
npx playwright test tests/qa/atlas.spec.js
npx playwright test tests/qa/cities.spec.js --project=chromium-desktop-1600 --project=firefox-desktop
npx playwright test tests/qa/lod1.spec.js --project=chromium-desktop-1600 --project=firefox-desktop --project=chromium-mobile
npx playwright test tests/qa/flags.spec.js --project=chromium-desktop-1600
npx playwright test tests/qa/offline.spec.js --project=chromium-desktop-1600 --project=chromium-mobile
npx playwright test tests/qa/kiosk.spec.js --project=chromium-desktop-1600
npx playwright test tests/qa/evidence.spec.js --project=chromium-desktop-1600 --project=firefox-desktop --project=chromium-mobile
npx playwright test tests/qa/auto-lod.spec.js --project=chromium-desktop-1600 --project=chromium-mobile
npx playwright test tests/qa/screenshots.spec.js --project=chromium-desktop-1600 --project=chromium-mobile
```

## Resultado funcional

| Área | Chromium desktop | Firefox desktop | Chromium mobile | Estado |
|---|---|---|---|---|
| Atlas: 6 tarjetas, aviso y badges | Sí | Sí | Sí | OK |
| Chan Chan y Wari sin canvas | Sí | Sí | Sí | OK |
| Navegación atlas → ciudad → atlas | Sí | Sí | Sí | OK |
| Caral LOD0: 6 paradas, 4 luces, 4 capas | Sí | Sí | Caral sí | OK |
| Chavín/Aypate/Narihualá LOD0 completo | Sí | Sí | Parcial | OK en desktop |
| LOD1 forzado en las 4 ciudades | Sí | Sí | Sí | OK |
| Selección automática de LOD | LOD0 | — | LOD1 | OK |
| Flags `noground`, `noshadows`, ambos | Sí | — | — | OK |
| Offline tras cachear Caral | Sí | — | Sí | OK |
| Kiosco Caral | Sí | — | — | OK |
| Errores de consola | 0 | 0 | 0 | OK |

La primera pasada de capturas agotó el timeout de 20 s de `page.screenshot` bajo SwiftShader. Se corrigió el test con timeout de 90 s y `test.slow()`; no es un fallo del producto.

## Métricas de referencia

Los FPS y tiempos de carga de Playwright headless **no representan hardware real**. Se guardan solo como comparación entre ciudades y LOD.

### Chromium desktop 1600×900 — SwiftShader

| Ciudad | LOD0 | LOD1 |
|---|---|---|
| Caral | 44 calls / 230.800 tris / 373,3 MB / 8.023 ms | 31 calls / 56.332 tris / 208 MB / 3.864 ms |
| Chavín | 18 calls / 249.990 tris / 133,3 MB / 3.102 ms | 14 calls / 27.622 tris / 69,3 MB / 472 ms |
| Aypate | 17 calls / 209.560 tris / 160 MB / 3.167 ms | 15 calls / 30.663 tris / 80 MB / 908 ms |
| Narihualá | 14 calls / 162.432 tris / 96 MB / 1.338 ms | 13 calls / 29.682 tris / 48 MB / 406 ms |

### Chromium mobile — Pixel 7 emulado

La app selecciona LOD1 automáticamente. Las pruebas de LOD0 son forzadas.

| Ciudad | LOD0 forzado | LOD1 |
|---|---|---|
| Caral | 44 calls / 230.800 tris / 373,3 MB / 5.117 ms | 31 calls / 56.332 tris / 208 MB / 2.979 ms |
| Chavín | 18 calls / 249.990 tris / 133,3 MB / 2.002 ms | 14 calls / 27.622 tris / 69,3 MB / 1.774 ms |
| Aypate | 15 calls / 209.560 tris / 160 MB / 2.542 ms | 13 calls / 30.663 tris / 80 MB / 1.220 ms |
| Narihualá | 14 calls / 162.432 tris / 96 MB / 1.536 ms | 13 calls / 29.682 tris / 48 MB / 555 ms |

### Firefox desktop 1600×900 — headless

| Ciudad | LOD0 | LOD1 |
|---|---|---|
| Caral | 44 calls / 230.800 tris / 373,3 MB / 1.260 ms | 31 calls / 56.332 tris / 208 MB / 789 ms |
| Chavín | 18 calls / 249.990 tris / 133,3 MB / 550 ms | 14 calls / 27.622 tris / 69,3 MB / 371 ms |
| Aypate | 17 calls / 209.560 tris / 160 MB / 697 ms | 15 calls / 30.663 tris / 80 MB / 392 ms |
| Narihualá | 14 calls / 162.432 tris / 96 MB / 659 ms | 13 calls / 29.682 tris / 48 MB / 335 ms |

## Hallazgos visuales

- **Caral:** estable. La vista inicial, las capas, las paradas y los badges se leen bien. No se detectó regresión.
- **Chavín:** el terreno sigue leyéndose como desierto procedural. El suelo de arena está desactivado, pero el material del terreno es el que domina la paleta. Es el mayor déficit visual pendiente y requiere contenido, no más edificios.
- **Aypate:** la lectura general funciona, pero el terreno verde se ve plano y la niebla es sutil. La integración de bosque de montaña sigue pendiente de contenido ambiental.
- **Narihualá:** la parada 1 elevada corrige el encuadre bloqueado por árboles. La materialidad de adobe y plataformas sigue siendo de preview; los badges interpretativos cumplen su función.
- **Móvil:** el panel abierto ocupa buena parte de la pantalla, pero el scroll, los badges y la barra de recorrido funcionan. No hay overflow detectado.
- **Atlas:** el aviso de preview, los estados y las evidencias se leen correctamente en desktop y móvil.

## Limitaciones

- WebKit no se pudo ejecutar: faltan `libavif16`, `libgav1-1`, `libyuv0` y `libjxl0.8` en el host. No es un fallo del atlas.
- Chromium usa SwiftShader; Firefox headless reporta una GPU enmascarada. Los FPS de ambos no son válidos para hardware.
- Los perfiles Desktop Chrome/Firefox de Playwright usan UA de Windows aunque el host sea Linux; es emulación de dispositivo, no hardware.
- Pixel 7 e iPhone 13 son emulaciones; no sustituyen GPU, memoria ni táctil reales.
- No se probó 1080p real.
- No se probó Android/iPhone físico ni la incidencia `CARAL-ANDROID-GROUND-001`.
- No se cambió `qa` de ninguna ciudad.

## Evidencia

- Informes JSON: [`resultados/playwright/`](./resultados/playwright/).
- Capturas de la revisión: `qa-output/qa-shots/` en local (no versionado).
- Informe HTML de Playwright: `playwright-report/` en local (no versionado).

## Próximos pasos

1. Instalar dependencias de WebKit si se quiere una aproximación a Safari:
   ```bash
   sudo npx playwright install-deps
   PLAYWRIGHT_WEBKIT=1 npm run qa:playwright
   ```
2. Repetir la matriz en Android/Chrome e iPhone/Safari reales.
3. Abordar el terreno/valle de Chavín como pase de contenido.
4. Abordar vegetación/atmósfera de Aypate y materialidad de Narihualá.
5. Mantener Playwright para regresiones funcionales; no usarlo para FPS.
