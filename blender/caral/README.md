# Caral — escenas de trabajo

## Archivos versionados

- **Fuente v1:** `caral_remaster.blend`; 1.128.020 bytes, SHA-256 `52d79bb5db315fcc22f703665d6dc39f49d9bc9be7b729f93800face301d1f5f`. Es la base reproducible del GLB v1 y de la escena v2.
- **Escenas locales (no versionadas):**
  - `caral_remaster_v2.blend`: high-poly de Mayor, Plaza Mayor, Anfiteatro y Altar Circular; v1 en `COL-Caral_LowPoly`.
  - `caral_lod0.blend`: high-poly fusionado por región + 6 mallas de infraestructura; 230.800 tris.
  - `caral_lod1.blend`: 9 objetos horneados + 6 mallas de infraestructura; 56.332 tris.
  - `blender/textures/baked/caral/`: atlas 2K de LOD1.
  - Se excluyen del repo por tamaño; se regeneran con los scripts de `scripts/`.
- **Texturas:** `../textures/generated/remaster/` (procedurales, versionadas); los atlas de LOD1 se generan en `../textures/baked/caral/`.
- **Escala:** metros; el visor aplica `0.08`.
- **Estado:** remaster v2 desplegado en GitHub Pages; `stage: "v2"` y caché `v6`. `model.glb` v1 queda como fallback.
- **Piloto histórico:** el antiguo `caral_art.blend` y sus texturas de IA fueron retirados del repositorio por licencia pendiente. No se usan en v1 ni v2.

## Regenerar v2 desde la fuente versionada

```bash
cp blender/caral/caral_remaster.blend blender/caral/caral_remaster_v2.blend
blender --background blender/caral/caral_remaster_v2.blend \
  --python scripts/build_caral_highpoly_mayor.py
blender --background blender/caral/caral_remaster_v2.blend \
  --python scripts/build_caral_highpoly_hero.py
```

Renders de la Fase B:

```bash
blender --background blender/caral/caral_remaster_v2.blend \
  --python scripts/render_caral_v2_phase_b.py -- \
  --out-dir docs/remaster/caral
```

## Exportar v1 fallback

```bash
blender --background blender/caral/caral_remaster.blend \
  --python blender/caral/export.py -- \
  --out public/cities/caral/model.glb \
  --image-format WEBP --image-quality 80
```

El GLB v1 tiene 4.778.308 bytes, 554 mallas, 55.944 tris, 20 materiales y 31 imágenes WebP. La reexportación conserva tamaño/estructura, pero el SHA-256 puede variar por la codificación WebP. Actualiza `public/cities/caral/README.md`, `docs/fuentes/registro-assets.csv` y la caché si cambia el archivo.

## Exportar LOD0

```bash
blender --background blender/caral/caral_remaster_v2.blend \
  --python scripts/assemble_caral_lod0.py -- \
  --out-blend blender/caral/caral_lod0.blend

blender --background blender/caral/caral_lod0.blend \
  --python scripts/export_caral_lod.py -- --lod 0 \
  --out public/cities/caral/model_lod0.glb
```

El exportador usa WebP 80, `extras` y Draco por defecto (`--no-draco` para depurar). También aplica culling a materiales sólidos, deja doble cara en vegetación/totora/algodón/agua/fuego y anula la transmisión del agua.

## Exportar LOD1

```bash
blender --background blender/caral/caral_remaster_v2.blend \
  --python scripts/bake_caral_lod1.py -- \
  --out-blend blender/caral/caral_lod1.blend \
  --texture-dir blender/textures/baked/caral \
  --resolution 2048

blender --background blender/caral/caral_lod1.blend \
  --python scripts/optimize_caral_lod1.py

blender --background blender/caral/caral_lod1.blend \
  --python scripts/export_caral_lod.py -- --lod 1 \
  --out public/cities/caral/model_lod1.glb
```

El bake usa base color y normal tangente; la roughness se fija en **0,85** y la normal en **0,35**. El AO no se conecta ni se incluye en el GLB. La optimización fusiona `Terrain`, `LowerHalf`, `UpperHalf`, `Residential`, `Props` y `Reference` en seis mallas y asigna capas.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras.
- No incluir colliders, spawns, recursos ni HUD del juego.
- Mantener las rutas relativas de texturas.
- Guardar una copia antes de operaciones destructivas.
- No añadir texturas de IA.
