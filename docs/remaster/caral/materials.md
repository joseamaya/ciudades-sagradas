# Materiales — pase procedural

## Objetivo

Sustituir las texturas de IA del piloto por un set PBR CC0/procedural para la arquitectura y las superficies visibles de Caral, sin generar nuevas texturas con IA.

## Alcance aplicado

- 134 slots reasignados en objetos `GEO-Caral_`: edificios, plazas, caminos, suelo y aterrazados.
- 7 materiales nuevos:
  - `MAT-Caral_Remaster_Plaster_White`
  - `MAT-Caral_Remaster_Plaster_Yellow`
  - `MAT-Caral_Remaster_Plaster_Red`
  - `MAT-Caral_Remaster_Stone_Cut`
  - `MAT-Caral_Remaster_Stone_Field`
  - `MAT-Caral_Remaster_Sand`
  - `MAT-Caral_Remaster_Earth`
- Se mantienen los materiales del piloto para roca de colinas, vegetación, totora, madera, agua, fuego y props pequeños.
- Texturas 2K para arquitectura y 1K para suelo; diffuse, normal y roughness; exportación WebP.

## Corrección del banding

El primer pase mostraba bandas horizontales y verticales. La auditoría de UV de `Terrace_06` y `Terrace_07` dio una relación UV/3D uniforme de `0.0625` (1 UV = 4 m), sin estiramiento. Un render de prueba con material plano confirmó que las bandas venían de la textura, no de la geometría ni de las sombras.

La causa era la variación de baja frecuencia del revoque, repetida cada 4 m. Se aplanó la variación de color, se conservó grano fino y se reforzó el normal map isotrópico para que el revoque tenga relieve sin una retícula de color. El test de tiling 1× y 5× ya no muestra una retícula de manchas; el render final no presenta banding.

## Texturas generadas

Directorio: `blender/textures/generated/remaster/`

- `plaster_white_diffuse.jpg`, `plaster_white_normal.png`, `plaster_white_roughness.jpg`
- `plaster_yellow_diffuse.jpg`
- `plaster_red_diffuse.jpg`
- `stone_cut_diffuse.jpg`, `stone_cut_normal.png`, `stone_cut_roughness.jpg`
- `stone_field_diffuse.jpg`, `stone_field_normal.png`, `stone_field_roughness.jpg`
- `ground_sand_diffuse.jpg`
- `ground_earth_diffuse.jpg`
- `ground_rock_diffuse.jpg` (reservada para el terreno)
- `ground_normal.png`, `ground_roughness.jpg`

Peso total: ~13 MB.

## Mapeo

| Material del piloto | Material nuevo |
|---|---|
| `MAT-Caral_Plaster_White` | `MAT-Caral_Remaster_Plaster_White` |
| `MAT-Caral_Plaster_Yellow` | `MAT-Caral_Remaster_Plaster_Yellow` |
| `MAT-Caral_Plaster_Red` | `MAT-Caral_Remaster_Plaster_Red` |
| `MAT-Caral_Stone_Cut` | `MAT-Caral_Remaster_Stone_Cut` |
| `MAT-Caral_Stone_Field` | `MAT-Caral_Remaster_Stone_Field` |
| `MAT-Caral_Sand`, `MAT-Sand_Desert` | `MAT-Caral_Remaster_Sand` |
| `MAT-Caral_Dirt`, `MAT-Caral_Terrace` | `MAT-Caral_Remaster_Earth` |
| `MAT-Caral_Path` | `MAT-Caral_Remaster_Sand` |

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

`--scope all` es el valor por defecto. `--scope mayor` queda como modo de depuración para la Pirámide Mayor.

## Resultado de prueba

- Escena de trabajo: `blender/caral/caral_remaster.blend`, 1.133.592 bytes, SHA-256 `74de593fb4348225632e1d5d4bdcc1c5fe52f17162acca08da3e241d410f80f5`.
- GLB de prueba: 8.915.420 bytes, 554 mallas, 55.944 tris, 21 materiales, 36 imágenes, todas WebP.
- El piloto publicado sigue intacto: 20.749.488 bytes, 554 mallas, 44.640 tris.
- Capturas: `materials-hero.jpg`, `materials-close.jpg` y `materials-detail.jpg`.
- El GLB de prueba se cargó en el visor web; después se restauró el modelo piloto en `public/`.

## Limitaciones

- El terreno, las colinas y la vegetación siguen con materiales del piloto; el suelo nuevo es plano y sin variación macro.
- No hay bake de AO ni normales desde high-poly; los normales son procedurales.
- La cámara y la luz del hero definitivo aún no están ajustadas.
- El GLB de prueba no se publica; `main` conserva el piloto.
- La auditoría de licencias del piloto sigue pendiente, aunque este pase ya no añade texturas de IA.

## Siguiente paso

- Revisar el pase en el visor con cámara y luz de atardecer.
- Aplicar material procedural a colinas y terreno con una escala que no repita el patrón.
- Pasar a muros high-poly y bake de normales/AO para la Pirámide Mayor.
