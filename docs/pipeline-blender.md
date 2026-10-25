# Pipeline Blender → web

## Principios

- Escala real en metros durante el modelado.
- Un origen estable por ciudad: centro del sitio a nivel del suelo.
- Y-up en el GLB; el visor aplica la escala de conversión indicada en `city.json`.
- Materiales PBR con nombres estables (`MAT-<Ciudad>_<Material>`).
- Nada de texturas con licencia incierta.

## Estructura de la escena

```text
COL-<Ciudad>_Terrain
COL-<Ciudad>_City
COL-<Ciudad>_Props
COL-<Ciudad>_Reference
COL-<Ciudad>_Export
```

- `GEO-<Ciudad>_<Elemento>` para mallas.
- `MAT-<Ciudad>_<Material>` para materiales.
- `CAM-<Ciudad>_<Vista>` para cámaras de referencia.
- `LGT-<Ciudad>_<Luz>` para luces de revisión.

## Exportación GLB

```python
import bpy

bpy.ops.export_scene.gltf(
    filepath="/ruta/model.glb",
    export_format="GLB",
    export_apply=True,
    export_yup=True,
    export_cameras=False,
    export_lights=False,
    export_animations=False,
)
```

- Aplicar modificadores antes de exportar.
- Incluir UVs en todas las mallas.
- Empaquetar imágenes en el GLB.
- Revisar que el material no dependa de nodos procedurales no exportables.

## Integración en el atlas

1. Copiar el GLB a `public/cities/<slug>/model.glb`.
2. Ajustar `scale` en `public/cities/<slug>/city.json`.
3. Ajustar cámaras y recorrido.
4. Añadir la portada `public/cities/<slug>/hero.jpg`.
5. Ejecutar `npm run validate` y `npm run build`.
6. Probar en navegador y en modo kiosco.

## Presupuesto

- Objetivo: <25 MB por ciudad.
- Preferir KTX2/Draco o meshopt para la versión publicada.
- LOD0 para la vista cercana; LOD1 para el atlas.
- 60 fps en GPU media a 1080p; 30 fps mínimo en kiosco 4K.

## Calidad

- Sin caras invertidas ni UVs faltantes.
- Sin materiales negros por nodos no exportados.
- Sin texturas gigantes sin comprimir.
- Sin elementos de juego: colliders, spawns, recursos o HUD.
- Revisar la ficha de fuentes y el estado de evidencia.

## Fuentes actuales

El `.blend` de Caral vive en el proyecto Blender de trabajo. Para publicar el repositorio, copiar la escena editable a `blender/caral/` o usar Git LFS, y documentar su hash en `CREDITS.md`.

## Texturas

- Preferir CC0 (Poly Haven, ambientCG) o texturas propias.
- Las texturas generadas con IA requieren revisar los términos del proveedor y del modelo.
- Si no se puede publicar una textura, sustituirla por una procedural o por un color PBR.
