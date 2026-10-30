---
name: qa-playwright
description: Revisa el atlas Ciudades Sagradas con Playwright MCP y la suite Playwright. Cubre rutas, LOD0/LOD1, seis paradas, luces, capas, consola, informe QA, capturas y offline en Chromium. No certifica hardware real ni FPS de GPU física.
---

# QA con Playwright — Ciudades Sagradas

## Cuándo usar

- Revisión funcional/visual tras cambios en `src/`, `city.json` o assets.
- Verificación de rutas, LOD, paradas, luces, capas y estados de evidencia.
- Captura de `qaReport()` para el registro de `docs/qa/`.
- Smoke cross-browser antes de publicar.

No usar para declarar FPS reales, QA Android/iPhone ni cierre de hardware.

## Requisitos

```bash
npm run build
npx playwright install chromium firefox webkit
```

WebKit solo se activa con `PLAYWRIGHT_WEBKIT=1` y requiere dependencias del host (`libavif16`, `libgav1-1`, `libyuv0`, `libjxl0.8`) o `sudo npx playwright install-deps`.

El MCP está en `opencode.json` como `playwright` y arranca con:

```bash
npx -y @playwright/mcp@latest --headless
```

## Suite

```bash
npm run qa:playwright                 # Chromium desktop, Firefox desktop y Chromium mobile
npm run qa:playwright:chromium        # solo Chromium desktop 1600×900
npm run qa:playwright:review          # Chromium desktop + Firefox + Chromium mobile
npm run qa:playwright:webkit          # opcional; requiere dependencias
npx playwright test --project=chromium-mobile
npx playwright test tests/qa/atlas.spec.js
npx playwright show-report
```

Artefactos:

- `qa-output/qa-reports/*.json`
- `qa-output/qa-shots/*.png`
- `playwright-report/`

## Flujo con MCP

1. `browser_navigate` a la URL.
2. `browser_snapshot` para leer la estructura.
3. `browser_evaluate` para llamar `window.__ciudadesSagradas.qaReport()`.
4. `browser_take_screenshot` para la evidencia visual.
5. `browser_console_messages` para errores.
6. Guardar el JSON en `docs/qa/resultados/playwright/` si el escenario es válido.

Los nombres exactos de las herramientas MCP pueden variar; usar las que exponga el servidor Playwright.

## URLs

Base de producción: `https://joseamaya.github.io/ciudades-sagradas/`.
Base local: `http://127.0.0.1:4173/`.

```text
Atlas:                 /
Caral LOD0:            /?debug=1&lod=0#/ciudad/caral
Caral LOD1:            /?debug=1&lod=1#/ciudad/caral
Caral sin suelo:       /?debug=1&lod=0&noground=1#/ciudad/caral
Caral sin sombras:     /?debug=1&lod=0&noshadows=1#/ciudad/caral
Caral ambas:           /?debug=1&lod=0&noground=1&noshadows=1#/ciudad/caral
Chavín:                /?debug=1&lod=0#/ciudad/chavin
Aypate:                /?debug=1&lod=0#/ciudad/aypate
Narihualá:             /?debug=1&lod=0#/ciudad/narihuala
Chan Chan:             /#/ciudad/chan-chan
Wari:                  /#/ciudad/wari
Kiosco:                /?kiosk=1#/ciudad/caral
```

## Criterios de revisión

- Las 4 ciudades disponibles cargan y tienen seis paradas.
- Caral LOD0/LOD1 y flags no generan errores de consola.
- Chavín, Aypate y Narihualá cargan LOD0/LOD1.
- Chan Chan y Wari muestran ficha documental sin canvas.
- El atlas muestra estados, evidencia y aviso de preview.
- `qaReport()` incluye `metrics`, `environment.webgl` y `issues`.
- La navegación atlas → ciudad → atlas funciona.

## Evidencia

- Informe de revisión: `docs/qa/revision-playwright.md`.
- JSON: `docs/qa/resultados/playwright/`.
- Capturas y artefactos: `qa-output/` (ignorado por git).

## Límites

- Playwright headless usa renderizado software: no publicar sus FPS como hardware.
- WebKit de escritorio no es iOS Safari.
- La emulación móvil no reproduce GPU, memoria ni táctil real.
- No cambiar `qa: passed` de una ciudad por esta revisión.
- No declarar 1080p real si la pantalla física no es 1080p.
