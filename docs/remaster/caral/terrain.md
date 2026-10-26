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
- **Materiales:** en la fase 1 seguían los materiales del piloto; la pasada v2 posterior cubrió arquitectura, plazas, suelo, roca y vegetación.
- **Vegetación y rocas:** sin cambios en la fase 1; la pasada v2 las sustituyó por materiales procedurales.

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

## Materiales de terreno v2

- Arena macro 2K en `SiteApron`, `Terrain_Base`, `Terrain_Shore` y `Terrain_DryRavine`; UVs a gran escala (80–200 m por tile).
- Roca procedural de celdas y craquelado en las 6 colinas; UV 0,25 para que las celdas se lean a escala de montaña.
- Campos con `dry_grass` procedural y UV 0,05; hojas con `foliage`.
- Adobe, totora, madera, megalitos y rocas pequeñas también pasaron a materiales procedurales.
- El GLB v1 no incluye texturas de IA.

### Capturas

- `terrain-sand-hero.jpg`: render de Blender.
- `terrain-final-iso.jpg`: vista isométrica con roca, campos y cubiertas.
- `viewer-terrain.jpg`: visor web con el GLB v1.

### Pendiente

- Geometría de colinas con erosión real.
- Muros high-poly + bake de normales/AO.
- Validación en hardware real.
