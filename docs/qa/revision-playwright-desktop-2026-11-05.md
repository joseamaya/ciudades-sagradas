# Revisión Playwright — desktop

Fecha: 5 de noviembre de 2026.
Alcance: **desktop**. No incluye Android, iPhone, kiosco físico ni 1080p real.
Herramienta: `@playwright/test` con Chromium 1600×900, Chromium 1920×1080 emulado y Firefox 1600×900.

## Resultado

| Suite | Resultado |
|---|---|
| Chromium desktop 1600×900, suite completa | **84/84** |
| Revisión desktop 1600×900, seis ciudades | **6/6** |
| Revisión desktop 1920×1080, Chan Chan/Wari LOD0/LOD1 | **4/4** |
| Firefox desktop 1600×900, atlas/ciudades/accesibilidad/evidencia | **32/32** |
| Errores de consola en cargas normales | **0** |

La suite completa de Chromium incluye ahora `desktop-review.spec.js`, que recorre las seis paradas, prueba las cuatro luces y las capas, guarda capturas y genera el informe QA. El smoke de Pages sigue en 44 pruebas.

## Métricas 1600×900 (headless, SwiftShader)

| Ciudad | LOD0 calls / tris / texturas / carga | LOD1 calls / tris / texturas / carga |
|---|---|---|
| Caral | 45 / 230.800 / 373,3 MB / 2.181 ms | 31 / 56.332 / 40 MB / 282 ms |
| Chavín | 19 / 249.942 / 136 MB / 1.173 ms | 16 / 42.842 / 72 MB / 793 ms |
| Aypate | 15 / 209.560 / 160 MB / 962 ms | 15 / 30.663 / 80 MB / 283 ms |
| Narihualá | 14 / 162.432 / 96 MB / 326 ms | 13 / 29.682 / 48 MB / 259 ms |
| Chan Chan | 14 / 156.624 / 208 MB / 1.031 ms | 13 / 27.192 / 64 MB / 268 ms |
| Wari | 15 / 158.216 / 176 MB / 924 ms | 13 / 26.224 / 80 MB / 292 ms |

No son FPS ni certificación de hardware. La carga incluye el primer render bajo SwiftShader.

## Hallazgos

### Corregidos en esta revisión

1. **Chan Chan, audiencias:** la cámara de la parada 4 estaba demasiado cerca y mostraba paredes en primer plano. Se reencuadró para leer el conjunto de audiencias y el patio.
2. **Chan Chan, iluminación:** el preset de mañana usaba el `fill` por defecto (0,08) y dejaba los muros muy oscuros. Se añadió `lighting.fill: 0.42` y `hemiIntensity: 0.26`.
3. **Wari, Monqachayoc:** la cámara miraba demasiado dentro del patio hundido y las sombras tapaban el mausoleo. Se reencuadró y se añadió `lighting.fill: 0.45` y `hemiIntensity: 0.30`.
4. **Revisión repetible:** nuevo `tests/qa/desktop-review.spec.js` con capturas de hero y seis paradas, capas, luces, 1080p y JSON de QA.

### Pendientes (no bloquean)

- **Chavín, Lanzón y Portada:** las paradas 3 y 5 siguen muy oscuras en el preset de mañana. Es una deuda visual P2; requiere un pase de iluminación interior, no un cambio de geometría. Evidencia: [`capturas/desktop-2026-11-05/chavin-1600-portada.png`](./capturas/desktop-2026-11-05/chavin-1600-portada.png).
- **Aypate, Plaza Inca:** la explanada se lee plana y el horizonte queda vacío. Es una mejora de contenido/atmósfera, no un fallo funcional.
- **Chan Chan, texturas LOD0:** 208 MB de VRAM estimada es el presupuesto más alto del atlas. En desktop headless no falla, pero conviene medirlo en una GPU integrada real antes de ampliar la ciudad.
- **Wari, texturas LOD0:** 176 MB; mismo seguimiento.
- **1080p:** el panel derecho ocupa más espacio, pero no tapa el recorrido ni el canvas. La prueba es de viewport, no de hardware 1080p.

## Evidencia versionada

- Informes QA: [`resultados/desktop-review-2026-11-05/`](./resultados/desktop-review-2026-11-05/).
- Capturas: [`capturas/desktop-2026-11-05/`](./capturas/desktop-2026-11-05/).
- Capturas completas de la pasada: `qa-output/qa-shots/` (ignorado por git).
- Informe HTML: `playwright-report/` (ignorado por git).

## Límites

- Chromium y Firefox corren con SwiftShader/GPU enmascarada; los FPS no son válidos.
- 1920×1080 es emulación de viewport, no una pantalla física 1080p.
- No se probó Android/iPhone ni kiosco; #10 y #71 siguen fuera de esta revisión.
- WebKit no se ejecutó por dependencias del host.
- No se cambió geometría, GLB, hashes ni caché.

## Próximos pasos

1. Pase de iluminación de Chavín para Lanzón y Portada.
2. Pase de atmósfera/vegetación de Aypate.
3. Medir Chan Chan/Wari en una GPU integrada real y decidir si bajar texturas LOD0 a 1K.
4. Mantener #10 como P2 Android abierto y #71 como gate de hardware.
