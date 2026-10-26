# Terreno — primer pase

## Objetivo

Empezar a romper la silueta de blockout sin tocar todavía la arquitectura ni las texturas.

## Cambio aplicado

- Subdivisión simple nivel 3 y desplazamiento procedural suave en las **6 colinas** de `COL-Caral_Terrain`.
- Textura `CLOUDS`, escala 38, fuerza 7 m.
- Script reproducible: `scripts/remaster_caral_terrain.py`.
- Escena de trabajo: `blender/caral/caral_remaster.blend`.
- El piloto `caral_art.blend` no se modifica.

## Qué se dejó fuera

- **Base del terreno y site apron:** el desplazamiento producía artefactos en el río y los campos. Se mantuvieron planos.
- **Arquitectura:** sin cambios.
- **Materiales:** el terreno y las colinas siguen con los materiales del piloto; el pase procedural posterior cubrió arquitectura, plazas y suelo.
- **Vegetación y rocas:** sin cambios.

## Resultado de prueba

- GLB de prueba: 21.545.084 bytes, 554 mallas, 55.944 tris.
- El piloto mide 20.749.488 bytes y 44.640 tris.
- La diferencia son ~11.300 tris de detalle en las colinas.

## QA

- Auditoría: sin texturas faltantes.
- Modificadores: 247 Bevel + 6 Subdivision + 6 Displace.
- UV faltantes solo en los LOD de juego, fuera del preview.

## Decisión

Las colinas ganan silueta, pero el cambio es insuficiente para reemplazar el piloto. Se conserva como escena de trabajo para la siguiente iteración.

## Siguiente paso

- Diseñar una máscara de terreno que excluya río, campos y site apron.
- Reemplazar las colinas cónicas por un heightfield con erosión real.
- Añadir rocas y vegetación instanciada.
- Pasar a la arquitectura high-poly de la Pirámide Mayor.

## Capturas

- `terrain-before.jpg`
- `terrain-after.jpg`

## Materiales de terreno v1

- Nueva textura `terrain_sand_diffuse.jpg` 2K: variación macro de arena, sin patrón direccional.
- Material `MAT-Caral_Remaster_Terrain` en `SiteApron`, `Terrain_Base`, `Terrain_Shore` y `Terrain_DryRavine`.
- UVs reescaladas: `SiteApron` 0,05; `Terrain_Base`/`Terrain_Shore` 0,02; `Terrain_DryRavine` 0,05.
- La textura cubre entre 80 y 200 m por tile; no aparece la retícula de 4 m.
- Se probó una roca procedural para las colinas, pero producía manchas grandes; se descartó y las colinas conservan el material del piloto.
- Los campos y la vegetación siguen con texturas del piloto.

### Capturas

- `terrain-sand-hero.jpg`: render de Blender.
- `viewer-terrain.jpg`: visor web con el GLB de prueba.

### Pendiente

- Roca específica para colinas, con detalle de alta frecuencia y normales.
- Vegetación y campos procedurales.
- Geometría de colinas con erosión real.
