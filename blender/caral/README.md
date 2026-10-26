# Caral — escena editable

- **Archivo:** `caral_art.blend`
- **Texturas:** `../textures/` (rutas relativas desde `blender/caral/`).
- **Escala:** metros; el visor aplica `0.08`.
- **Estado:** piloto en remasterización.
- **SHA-256 del .blend:** `5a7377f727a2e07931d90aabed7a83c9ef59705176e7f244ae6db4f4d93ab377`
- **Tamaño del .blend:** 7.940.979 bytes

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

## Texturas

La escena usa texturas PBR generadas con IA para el proyecto Caral (Cloudflare Workers AI / FLUX) y texturas procedurales propias. La geometría es del proyecto Ciudades Sagradas.

Las texturas de IA están pendientes de confirmar términos para distribución. Para las próximas ciudades se usarán texturas CC0/procedurales.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras.
- No incluir colliders, spawns, recursos ni HUD del juego.
- Mantener las rutas relativas de texturas.
- Guardar una copia antes de operaciones destructivas.
