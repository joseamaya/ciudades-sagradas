# Fuentes Blender

Escenas editables y scripts de exportación del atlas.

```text
blender/
  caral/
    caral_art.blend   # escena de Caral
    export.py         # exporta a GLB
  textures/           # texturas relativas de la escena Caral
```

## Caral

- Abrir `blender/caral/caral_art.blend`.
- Las texturas se resuelven desde `blender/textures/` con rutas relativas.
- Exportar con:
  ```bash
  blender --background blender/caral/caral_art.blend \
    --python blender/caral/export.py -- \
    --out public/cities/caral/model.glb
  ```
- Ver `blender/caral/README.md` para detalles y licencias.

## Convenciones

- Unidades: metros.
- Origen: centro del sitio a nivel del suelo.
- Nombres: `GEO-`, `MAT-`, `CAM-`, `LGT-`.
- Exportar Y-up, sin cámaras ni luces.
- Aplicar modificadores y mantener texturas empaquetadas o en rutas relativas.
- No incluir elementos de juego.

Ver [`docs/pipeline-blender.md`](../docs/pipeline-blender.md).
