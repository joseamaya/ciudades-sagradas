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
    export_image_format="WEBP",
    export_image_quality=80,
    export_extras=True,
    export_draco_mesh_compression_enable=True,
)
```

- Aplicar modificadores antes de exportar.
- Incluir UVs en todas las mallas.
- Empaquetar imágenes en el GLB, preferentemente WebP 80.
- Usar Draco para geometría (nivel 6; posición 14, normal 10, UV 12).
- Activar `use_backface_culling` en superficies sólidas; dejar doble cara solo en vegetación, totora, algodón, agua y fuego.
- Revisar que el material no dependa de nodos procedurales no exportables.

## Integración en el atlas

1. Copiar los GLB a `public/cities/<slug>/` (`model_lod0.glb`, `model_lod1.glb`, `model.glb` de fallback).
2. Declarar `lod.levels`, `fallbackModel`, `scale` y `verticalScale` en `public/cities/<slug>/city.json`.
3. Ajustar cámaras y recorrido; validar las capas.
4. Añadir la portada `public/cities/<slug>/hero.jpg`.
5. Registrar hashes/tamaños en `docs/fuentes/registro-assets.csv`.
6. Ejecutar `npm run validate`, `npm run build`, `npm run bench` y probar en navegador/kiosco.

## Presupuesto

- Objetivo: <25 MB por ciudad; Caral v2 está en 3,28 MB (LOD0) y 1,35 MB (LOD1) con Draco.
- Draco está implementado; KTX2/BasisU queda pendiente por VRAM de texturas y requiere gltfpack/BasisU.
- LOD0 para la vista cercana; LOD1 para móvil y atlas.
- 60 fps en GPU media a 1080p; 30 fps mínimo en kiosco 4K. La medición real sigue pendiente.

## Calidad

- Sin caras invertidas ni UVs faltantes.
- Sin materiales negros por nodos no exportados.
- Sin texturas gigantes sin comprimir.
- Sin elementos de juego: colliders, spawns, recursos o HUD.
- Revisar la ficha de fuentes y el estado de evidencia.

## Fuentes actuales

La fuente v1 versionada es `blender/caral/caral_remaster.blend`. Las escenas v2 y LOD se regeneran con los scripts y se mantienen como artefactos locales por tamaño; no se versionan. Documentar sus hashes en `blender/caral/README.md` y `docs/remaster/caral/`.

## Texturas

- Preferir CC0 (Poly Haven, ambientCG) o texturas propias.
- No se añaden texturas de IA. El piloto histórico fue retirado del repositorio por licencia pendiente.
- Si no se puede publicar una textura, sustituirla por una procedural o por un color PBR.
- WebP es el formato publicado; LOD1 se exporta con `--max-texture-size 1024`. Evaluar KTX2 solo si se reduce la VRAM de forma medible.
