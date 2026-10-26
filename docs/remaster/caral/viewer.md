# Visor — alineación con el render

## Objetivo

Acercar el aspecto del visor web al render de Blender del remaster y corregir la cámara inicial, que estaba en el lado opuesto de la Pirámide Mayor.

## Cambios aplicados

- **Color management:** ACES Filmic → **AgX**, con exposición ajustada.
- **Ambiente:** mapa de entorno PMREM generado desde el cielo; `scene.environmentIntensity` por hora del día.
- **Sol:** dirección invertida para coincidir con la luz clave de Blender; luz cálida más intensa y relleno neutro.
- **Sombras:** `PCFSoftShadowMap`.
- **Cámara inicial:** equivalente a `CAM-Caral_RTS_Hero` de Blender, desde el sur, con `fov` vertical 25,4°.
- **Encuadre:** objetivo desplazado para que la Pirámide Mayor quede a la izquierda del panel de ficha.
- **Recorrido:** stops 2–5 recentrados desde el sur; Plaza Circular y Anfiteatro reencuadrados.
- **Móvil:** FOV responsivo en vertical (hasta 60°) para que la ciudad no quede recortada.
- **Suelo del visor:** color de arena ajustado al material del remaster.

## Capturas

- `viewer-before.jpg`: cámara antigua y ACES.
- `viewer-after.jpg`: cámara sur, AgX y PMREM, luz de amanecer.
- `viewer-dusk.jpg`: misma cámara, preset atardecer.
- `viewer-tour-03.jpg`: Plaza Circular.
- `viewer-tour-05.jpg`: conjunto del Anfiteatro.
- `viewer-mobile.jpg` y `viewer-mobile-panel.jpg`: 390×844.
- `viewer-kiosk.jpg`: 1920×1080 con `?kiosk=1`.

## Resultado

- El GLB del remaster carga en el visor.
- La Pirámide Mayor queda visible fuera del panel.
- Los seis stops del recorrido se probaron en escritorio y móvil emulado; el kiosco queda congelado.
- El suelo ya no presenta la retícula del pase anterior.
- La luz cálida y el ambiente del cielo se acercan más al render de Blender.

## Limitaciones

- Los stops están revisados, pero falta validación en hardware real y una pasada de arte final.
- El panel de ficha sigue ocupando el lado derecho en escritorio.
- El terreno, las colinas y la vegetación conservan materiales del piloto.
- El encuadre hero y la luz de atardecer definitivos aún requieren una pasada de arte.
- Caral v2 está publicado con LOD0/LOD1; la escala 0,08 se mantiene como diorama y la 1.0 queda fuera.

## Probar

```bash
npm run build
npm run serve
# http://127.0.0.1:4173/?lod=0#/ciudad/caral
# http://127.0.0.1:4173/?lod=1#/ciudad/caral
```

La caché de servicio actual es `ciudades-sagradas-v5`.
