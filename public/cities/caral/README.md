# Modelo de Caral — v2 estable y v1 fallback

## v2 (web)

- **LOD0:** `model_lod0.glb`, **3.277.080 bytes** (Draco + WebP).
  - **10 mallas**, 65 primitivas, 21 materiales, 31 imágenes WebP, **230.800 triángulos**.
  - **44 draw calls** en régimen estable con la cámara inicial (sombras cacheadas; al refrescar sombras se suman los casters).
  - SHA-256: `d11247a3bf17807abe3667b01e75439be0071a70f01f8a34b6196bd1a7e4ded7`.
- **LOD1:** `model_lod1.glb`, **1.345.092 bytes** (Draco + WebP, texturas 1K).
  - **15 mallas**, 38 primitivas, 23 materiales, 39 imágenes WebP, **56.332 triángulos**.
  - **31 draw calls** en régimen estable.
  - SHA-256: `e1567c59390c52e947a9e948f94a18baa8ccd919d030381a70bb6c21cca165bf`.
- **Escala:** el visor aplica `0.08`; es una presentación de diorama, no una escala métrica de recorrido.
- **Fuente editable:** `blender/caral/caral_remaster.blend` (v1) y las escenas locales `caral_remaster_v2.blend`, `caral_lod0.blend` y `caral_lod1.blend`, que no se versionan por tamaño. Se regeneran con los scripts de `scripts/`.
- **Export reproducible:** `scripts/assemble_caral_lod0.py`, `scripts/optimize_caral_lod1.py` y `scripts/export_caral_lod.py`, WebP 80 + Draco; LOD1 con `--max-texture-size 1024`.
- **LOD:** `city.json` declara `lod.levels` 0/1 y `fallbackModel`; escritorio usa LOD0 y móvil usa LOD1, con override `?lod=0/1`.
- **Fallback:** LOD0 → LOD1 → v1 en escritorio; LOD1 → v1 → LOD0 en móvil.
- **Portada:** `hero.jpg` generada desde el visor v2.
- **Estado:** remaster v2 desplegado en GitHub Pages (`maturity: "released"`, `version: "v2"`, caché global `v36`); el GLB v1 se conserva como fallback y rollback.
- **Texturas:** LOD1 usa 39 imágenes a 1K; el AO no se incluye y la roughness es constante.

## v1 fallback

- **Archivo:** `model.glb`
- **Tamaño:** 4.778.308 bytes
- **Mallas:** 554
- **Triángulos:** 55.944
- **Materiales:** 20
- **Imágenes:** 31, todas WebP
- **SHA-256:** `c6bbe07b27640951373b96db4f6a610b7618224e37fc52eda8893ac79670bb34`
- **Origen:** `blender/caral/caral_remaster.blend` (Blender 5.2). Reexportar produce el mismo tamaño y estructura, aunque el hash puede variar por la codificación WebP.
- **Geometría:** proyecto Ciudades Sagradas / José Amaya.
- **Texturas:** procedurales propias en arquitectura, plazas, suelo, arena, roca, vegetación, adobe, totora y madera. **Sin texturas de IA en este GLB.**
- **Licencia:** geometría CC BY 4.0; texturas procedurales del proyecto. El piloto histórico con texturas de IA fue retirado del repositorio.
- **Escala:** el visor aplica `0.08`.
- **Estado:** fallback y rollback de v2.
