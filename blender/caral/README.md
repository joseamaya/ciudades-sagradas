# Caral — escena editable

- **Archivo:** `caral_art.blend`
- **Texturas:** `../textures/` (rutas relativas desde `blender/caral/`).
- **Escala:** metros; el visor aplica `0.08`.
- **Estado:** piloto en remasterización.
- **SHA-256 del .blend:** `0136f72ae53d553c56d5e98c20d94f6be973891b8acca802c7f415e6d0cf94e1`
- **Tamaño del .blend:** 7.947.400 bytes

## Exportar

```bash
blender --background blender/caral/caral_art.blend \
  --python blender/caral/export.py -- \
  --out public/cities/caral/model.glb
```

El GLB publicado es el piloto optimizado: 20.779.860 bytes, 554 mallas y 44.640 triángulos. Una exportación fresca desde esta escena puede incluir más mallas/materiales; si la usas, valida el resultado y actualiza:

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
