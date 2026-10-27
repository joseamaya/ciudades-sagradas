# Fuentes Blender

Escenas editables y scripts de exportación del atlas.

```text
blender/
  caral/
    caral_remaster.blend  # fuente v1 y base de v2 (versionada)
    caral_remaster_v2.blend  # escena v2 local (no versionada)
    caral_lod0.blend / caral_lod1.blend  # LODs locales (no versionados)
    export.py             # exporta v1 a GLB
  textures/
    generated/remaster/   # texturas procedurales del remaster
    baked/caral/          # atlas LOD1 generados (no versionados)
```

## Caral

- La fuente versionada es `blender/caral/caral_remaster.blend`.
- Las escenas v2 y LOD se regeneran con `scripts/` (ver `blender/caral/README.md`).
- Exportar v1:

  ```bash
  blender --background blender/caral/caral_remaster.blend \
    --python blender/caral/export.py -- \
    --out public/cities/caral/model.glb \
    --image-format WEBP --image-quality 80
  ```

- Los LOD0/LOD1 se exportan con `scripts/export_caral_lod.py` (WebP 80 + Draco).
- El piloto histórico con texturas de IA fue retirado del repositorio.

## Convenciones

- Unidades: metros.
- Origen: centro del sitio a nivel del suelo.
- Nombres: `GEO-`, `MAT-`, `CAM-`, `LGT-`.
- Exportar Y-up, sin cámaras ni luces.
- Aplicar modificadores y mantener texturas empaquetadas o en rutas relativas.
- No incluir elementos de juego ni texturas de IA.

Ver [`docs/pipeline-blender.md`](../docs/pipeline-blender.md).
