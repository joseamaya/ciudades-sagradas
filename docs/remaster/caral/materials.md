# Materiales — pase procedural

## Objetivo

Sustituir las texturas de IA del piloto por un set PBR procedural propio para todas las superficies visibles de Caral, sin generar nuevas texturas con IA.

## Alcance aplicado

- Todos los materiales visibles del remaster v1 son procedurales.
- La última pasada reasignó 220 slots de objetos `GEO-Caral_`.
- 14 materiales procedurales:
  - `MAT-Caral_Remaster_Plaster_White`
  - `MAT-Caral_Remaster_Plaster_Yellow`
  - `MAT-Caral_Remaster_Plaster_Red`
  - `MAT-Caral_Remaster_Stone_Cut`
  - `MAT-Caral_Remaster_Stone_Field`
  - `MAT-Caral_Remaster_Sand`
  - `MAT-Caral_Remaster_Earth`
  - `MAT-Caral_Remaster_Terrain`
  - `MAT-Caral_Remaster_Rock`
  - `MAT-Caral_Remaster_Grass`
  - `MAT-Caral_Remaster_Leaves`
  - `MAT-Caral_Remaster_Adobe`
  - `MAT-Caral_Remaster_Thatch`
  - `MAT-Caral_Remaster_Wood`
- `MAT-Caral_Stone_Megalith` usa `Stone_Field`; `MAT-Caral_ResourceRock` usa `Rock`.
- El GLB v1 no incluye texturas de IA.

## Corrección del banding

El primer pase mostraba bandas horizontales y verticales. La auditoría de UV de `Terrace_06` y `Terrace_07` dio una relación UV/3D uniforme de `0.0625` (1 UV = 4 m), sin estiramiento. Un render con material plano confirmó que las bandas venían de la textura, no de la geometría ni de las sombras.

La causa era la variación de baja frecuencia del revoque, repetida cada 4 m. Se aplanó la variación de color, se conservó grano fino y se reforzó el normal map isotrópico. El test de tiling 1× y 5× ya no muestra una retícula de manchas; el render final no presenta banding.

## Texturas generadas

Directorio: `blender/textures/generated/remaster/`

- Revoque: `plaster_white_diffuse.jpg`, `plaster_white_normal.png`, `plaster_white_roughness.jpg`, `plaster_yellow_diffuse.jpg`, `plaster_red_diffuse.jpg`.
- Piedra: `stone_cut_*`, `stone_field_*`.
- Suelo: `ground_sand_diffuse.jpg`, `ground_earth_diffuse.jpg`, `ground_normal.png`, `ground_roughness.jpg`.
- Terreno: `terrain_sand_diffuse.jpg`.
- Roca: `rock_face_diffuse.jpg`, `rock_face_normal.png`, `rock_face_roughness.jpg`.
- Vegetación: `dry_grass_*`, `foliage_*`.
- Adobe: `adobe_*`.
- Totora: `thatch_*`.

Peso total: ~17 MB. El GLB usa 31 imágenes WebP.

## Mapeo

| Material del piloto | Material nuevo |
|---|---|
| `MAT-Caral_Plaster_White` | `MAT-Caral_Remaster_Plaster_White` |
| `MAT-Caral_Plaster_Yellow` | `MAT-Caral_Remaster_Plaster_Yellow` |
| `MAT-Caral_Plaster_Red` | `MAT-Caral_Remaster_Plaster_Red` |
| `MAT-Caral_Stone_Cut` | `MAT-Caral_Remaster_Stone_Cut` |
| `MAT-Caral_Stone_Field` | `MAT-Caral_Remaster_Stone_Field` |
| `MAT-Caral_Sand` (site apron, base, shore, ravine) | `MAT-Caral_Remaster_Terrain` |
| `MAT-Caral_Sand` (otros), `MAT-Sand_Desert` | `MAT-Caral_Remaster_Sand` |
| `MAT-Caral_Dirt`, `MAT-Caral_Terrace` | `MAT-Caral_Remaster_Earth` |
| `MAT-Caral_Path` | `MAT-Caral_Remaster_Sand` |
| `MAT-Caral_Rock` | `MAT-Caral_Remaster_Rock` |
| `MAT-Caral_Grass` | `MAT-Caral_Remaster_Grass` |
| `MAT-Caral_Leaves` | `MAT-Caral_Remaster_Leaves` |
| `MAT-Caral_Quincha` | `MAT-Caral_Remaster_Adobe` |
| `MAT-Caral_Thatch` | `MAT-Caral_Remaster_Thatch` |
| `MAT-Caral_Stone_Megalith` | `MAT-Caral_Remaster_Stone_Field` |
| `MAT-Caral_Wood` | `MAT-Caral_Remaster_Wood` |
| `MAT-Caral_ResourceRock` | `MAT-Caral_Remaster_Rock` |

Escalas UV: terreno `SiteApron` 0,05; `Terrain_Base`/`Terrain_Shore` 0,02; `Terrain_DryRavine` 0,05; colinas 0,25; campos 0,05. Así las texturas cubren áreas grandes y no aparece una retícula de 4 m.

## Scripts

```bash
python3 scripts/make_caral_materials.py

blender --background blender/caral/caral_remaster.blend \
  --python scripts/remaster_caral_materials.py -- \
  --out blender/caral/caral_remaster.blend \
  --hero /tmp/caral_materials_hero.png \
  --close /tmp/caral_materials_close.png \
  --scope all
```

`--scope all` es el valor por defecto. `--scope mayor` queda como modo de depuración.

## Resultado

- Escena de trabajo: `blender/caral/caral_remaster.blend`, 1.128.020 bytes, SHA-256 `52d79bb5db315fcc22f703665d6dc39f49d9bc9be7b729f93800face301d1f5f`.
- GLB v1: 4.778.308 bytes, 554 mallas, 55.944 tris, 20 materiales, 31 imágenes WebP, SHA-256 `c6bbe07b27640951373b96db4f6a610b7618224e37fc52eda8893ac79670bb34`.
- El piloto histórico sigue intacto como archivo: 20.749.488 bytes, 554 mallas, 44.640 tris.
- Capturas: `materials-hero.jpg`, `materials-close.jpg`, `materials-detail.jpg`, `terrain-sand-hero.jpg`, `viewer-terrain.jpg`.

## Limitaciones

- El bake de AO/normales se completó en v2; LOD1 usa atlas 2K, normal 0,35 y roughness constante 0,85.
- La geometría high-poly se completó en v2 para el hero; el resto conserva la base v1.
- El encuadre hero y la luz de atardecer definitivos aún requieren una pasada de arte.
- Caral v2 está desplegado; `model.glb` v1 queda como fallback y el piloto histórico como archivo.
- Falta validación en hardware real; el kiosco está congelado.

## Siguiente paso

- Validación en hardware web real y ajuste de rendimiento si hace falta.
- Pasada de arte final y nuevas ciudades; el kiosco queda congelado.
- Ver `v2-plan.md` y `release-v2.md` para el cierre.
