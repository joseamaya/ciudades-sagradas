# Modelo de Caral — v2 preview y v1 fallback

## v2 preview (web)

- **LOD0:** `model_lod0.glb`, **22.587.652 bytes**.
  - **10 mallas**, 21 materiales, 31 imágenes WebP, **230.800 triángulos**.
  - Prueba de escritorio: **125 draw calls** con sombras del hero y la infraestructura fusionada como receptora.
  - SHA-256: `7757b125006a7704f32a739a9db87ca799e9f5aec918df1030eeaca734ca6d7d`.
- **LOD1:** `model_lod1.glb`, **6.694.356 bytes**.
  - **15 mallas**, 23 materiales, 39 imágenes WebP, **56.332 triángulos**.
  - Prueba de escritorio: **72 draw calls**.
  - SHA-256: `60990a98f893bd148ca937deb341808a415cad3e99b261438320372c39a23fbb`.
- **Escala:** el visor aplica `0.08`; es una presentación de diorama, no una escala métrica de recorrido.
- **Fuente editable:** `blender/caral/caral_lod0.blend` (SHA-256 `6db1c092a168272fa6ab3ff43fb4f503d809d81626b7f798029cc8c9191fdd4b`) y `blender/caral/caral_lod1.blend` (SHA-256 `9da242aa0e92f7b43ffa014af7af2fe11c27c47c2d027c65cc4515244856df9a`).
- **Export reproducible:** `scripts/assemble_caral_lod0.py`, `scripts/optimize_caral_lod1.py` y `scripts/export_caral_lod.py`, WebP calidad 80.
- **LOD:** `city.json` declara `lod.levels` 0/1 y `fallbackModel`; escritorio usa LOD0 y móvil usa LOD1.
- **Estado:** preview web; no reemplaza el GLB v1.

## v1 fallback

- **Archivo:** `model.glb`
- **Tamaño:** 4.778.308 bytes
- **Mallas:** 554
- **Triángulos:** 55.944
- **Materiales:** 20
- **Imágenes:** 31, todas WebP
- **SHA-256:** `c6bbe07b27640951373b96db4f6a610b7618224e37fc52eda8893ac79670bb34`
- **Origen:** escena de trabajo del remaster, Blender 5.2.
- **Fuente editable:** `blender/caral/caral_remaster.blend` (SHA-256 `52d79bb5db315fcc22f703665d6dc39f49d9bc9be7b729f93800face301d1f5f`).
- **Geometría:** proyecto Ciudades Sagradas / José Amaya.
- **Texturas:** procedurales propias en arquitectura, plazas, suelo, arena, roca, vegetación, adobe, totora y madera. **Sin texturas de IA en este GLB.**
- **Licencia:** geometría CC BY 4.0; texturas procedurales del proyecto. El piloto histórico queda como material de archivo; el GLB de esta versión no contiene texturas de IA.
- **Escala:** el visor aplica `0.08`.
- **Estado:** remaster v1 publicado en `main` y GitHub Pages (2026-10-26); se conserva como rollback.
- **Export reproducible:** `blender/caral/export.py`, WebP calidad 80.
