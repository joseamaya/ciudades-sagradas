# Caral — escena editable

- **Archivo piloto:** `caral_art.blend`; 7.940.979 bytes, SHA-256 `5a7377f727a2e07931d90aabed7a83c9ef59705176e7f244ae6db4f4d93ab377`.
- **Archivo de trabajo:** `caral_remaster.blend`; 1.128.020 bytes, SHA-256 `52d79bb5db315fcc22f703665d6dc39f49d9bc9be7b729f93800face301d1f5f`.
- **Escena v2:** `caral_remaster_v2.blend`; 6.755.204 bytes, SHA-256 `386cc18bb141d167801157b4fa05bc16dd79ab86c4ac6ce24b19249522ae85d1`. High-poly de Mayor, Plaza Mayor, Anfiteatro y Altar Circular en `COL-Caral_HighPoly`; v1 conservado en `COL-Caral_LowPoly`.
- **LOD0:** `caral_lod0.blend`; 13.479.232 bytes, SHA-256 `6db1c092a168272fa6ab3ff43fb4f503d809d81626b7f798029cc8c9191fdd4b`. 4 mallas high-poly por región + 6 mallas `COL-Caral_LOD0_Infra`; 230.800 tris.
- **LOD1:** `caral_lod1.blend`; 7.747.386 bytes, SHA-256 `9da242aa0e92f7b43ffa014af7af2fe11c27c47c2d027c65cc4515244856df9a`. 9 objetos baked (`MAT-Caral_LOD1_*`) + 6 mallas `COL-Caral_LOD1_Infra`; 56.332 tris. Mapas en `../textures/baked/caral/`.
- **Texturas:** `../textures/` (piloto) y `../textures/generated/remaster/` (pase procedural), con rutas relativas desde `blender/caral/`.
- **Escala:** metros; el visor aplica `0.08`.
- **Estado:** remaster v2 desplegado en GitHub Pages; `stage: "v2"` y caché `v5`. `model.glb` v1 queda como fallback.

## Exportar

```bash
blender --background blender/caral/caral_art.blend \
  --python blender/caral/export.py -- \
  --out public/cities/caral/model.glb
```

El GLB v1 de respaldo se reproduce con `export.py`: 4.778.308 bytes, 554 mallas y 55.944 triángulos. Si cambias la escena, reexporta, valida el resultado y actualiza:

- `public/cities/caral/README.md` (hash y tamaño).
- `docs/fuentes/registro-assets.csv`.
- `docs/estado.md`.
- La versión de caché en `public/sw.js` si cambia el modelo.

Para probar el remaster sin publicarlo:

```bash
python3 scripts/make_caral_materials.py

blender --background blender/caral/caral_remaster.blend \
  --python scripts/remaster_caral_materials.py -- \
  --out blender/caral/caral_remaster.blend \
  --hero /tmp/caral_materials_hero.png \
  --close /tmp/caral_materials_close.png \
  --scope all

blender --background blender/caral/caral_remaster.blend \
  --python blender/caral/export.py -- \
  --out /tmp/caral_remaster_test.glb \
  --image-format WEBP --image-quality 80
```

GLB v1: 4.778.308 bytes, 554 mallas, 55.944 tris, 20 materiales y 31 imágenes WebP.
- **v1:** `release/caral-remaster-final`; GLB SHA-256 `c6bbe07b27640951373b96db4f6a610b7618224e37fc52eda8893ac79670bb34`.

Regenerar la escena v2 desde una copia limpia de `caral_remaster.blend` (no exporta GLB):

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

Cámaras nuevas: `CAM-Caral_V2_Plaza`, `CAM-Caral_V2_PlazaDetail`, `CAM-Caral_V2_Anfiteatro`, `CAM-Caral_V2_Altar` y `CAM-Caral_V2_AltarDetail`.

LOD0: ensamblar high-poly por región + infraestructura y exportar:

```bash
blender --background blender/caral/caral_remaster_v2.blend \
  --python scripts/assemble_caral_lod0.py -- \
  --out-blend blender/caral/caral_lod0.blend

blender --background blender/caral/caral_lod0.blend \
  --python scripts/export_caral_lod.py -- --lod 0 \
  --out public/cities/caral/model_lod0.glb
```

LOD1: bake 2K, fusión de infraestructura y exportación:

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

El bake usa base color y normal tangente; la roughness se fija en **0,85** y la normal en **0,35**. El AO se hornea pero no se conecta. La optimización fusiona `Terrain`, `LowerHalf`, `UpperHalf`, `Residential`, `Props` y `Reference` en seis mallas, asigna capas (`terrain`, `city`, `props`, `reference`) y oculta las colecciones originales. El LOD1 conserva 9 objetos baked. LOD0 y LOD1 se exportan con WebP 80 y `extras`; `model.glb` v1 queda como fallback.

## Texturas

El piloto histórico usa texturas PBR generadas con IA para el proyecto Caral (Cloudflare Workers AI / FLUX) y texturas procedurales propias. El pase de remaster usa texturas CC0/procedurales en `../textures/generated/remaster/`; el LOD1 de v2 usa un atlas 2K horneado desde el high-poly propio.

Las texturas de IA del piloto no se publican y quedan pendientes de archivo definitivo. Los GLB v1 y v2 no contienen imágenes de IA.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras.
- No incluir colliders, spawns, recursos ni HUD del juego.
- Mantener las rutas relativas de texturas.
- Guardar una copia antes de operaciones destructivas.
