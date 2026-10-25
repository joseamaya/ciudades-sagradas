# Fuentes Blender

Este directorio está reservado para las escenas editables y los scripts de exportación.

## Caral

La escena de trabajo actual está en el proyecto Blender local:

```text
/home/jamaya/Projects/blender/scenes/caral_art.blend
```

Para publicar el repositorio:

1. Copiar la escena a `blender/caral/caral_art.blend` (o usar Git LFS).
2. Copiar el GLB a `public/cities/caral/model.glb`.
3. Documentar hash, tamaño y licencias en `CREDITS.md`.
4. Ejecutar `npm run validate`.

## Convenciones

- Unidades: metros.
- Origen: centro del sitio a nivel del suelo.
- Nombres: `GEO-`, `MAT-`, `CAM-`, `LGT-`.
- Exportar Y-up, sin cámaras ni luces.
- Aplicar modificadores y empaquetar texturas.

Ver [`docs/pipeline-blender.md`](../docs/pipeline-blender.md).
