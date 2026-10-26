# Caral — escena editable

- **Archivo piloto:** `caral_art.blend`; 7.940.979 bytes, SHA-256 `5a7377f727a2e07931d90aabed7a83c9ef59705176e7f244ae6db4f4d93ab377`.
- **Archivo de trabajo:** `caral_remaster.blend`; 1.133.592 bytes, SHA-256 `74de593fb4348225632e1d5d4bdcc1c5fe52f17162acca08da3e241d410f80f5`.
- **Texturas:** `../textures/` (piloto) y `../textures/generated/remaster/` (pase procedural), con rutas relativas desde `blender/caral/`.
- **Escala:** metros; el visor aplica `0.08`.
- **Estado:** piloto en remasterización; materiales procedurales aplicados a arquitectura, plazas y suelo.

## Exportar

```bash
blender --background blender/caral/caral_art.blend \
  --python blender/caral/export.py -- \
  --out public/cities/caral/model.glb
```

El GLB publicado se reproduce con `export.py`: 20.749.488 bytes, 554 mallas y 44.640 triángulos. Si cambias la escena, reexporta, valida el resultado y actualiza:

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

GLB de prueba del pase procedural: 8.915.420 bytes, 554 mallas, 55.944 tris, 21 materiales y 36 imágenes WebP.

## Texturas

El piloto usa texturas PBR generadas con IA para el proyecto Caral (Cloudflare Workers AI / FLUX) y texturas procedurales propias. El pase de remaster usa texturas CC0/procedurales en `../textures/generated/remaster/`.

Las texturas de IA del piloto están pendientes de confirmar términos para distribución. Las texturas del remaster no añaden imágenes de IA.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras.
- No incluir colliders, spawns, recursos ni HUD del juego.
- Mantener las rutas relativas de texturas.
- Guardar una copia antes de operaciones destructivas.
