# Fuentes Blender

Escenas editables y scripts de exportación del atlas.

Los `.blend` versionados usan **Git LFS**. Tras clonar:

```bash
git lfs install
git lfs pull
```

CI y el build web no descargan LFS porque no necesitan escenas Blender.

## Historial y tamaño del clon

Medición del 4 de noviembre de 2026: `.git` ocupa ~514 MB y el pack ~308 MB. La mayor parte son GLB, texturas y escenas anteriores a la política de LFS.

**Decisión: no reescribir el historial en esta fase.** Evita un `force-push`, la rotura de clones existentes y una ventana de mantenimiento sin beneficio inmediato para el build web.

- Para colaboradores que no necesitan escenas: `git clone --filter=blob:none <url>` y omitir `git lfs pull`.
- Para QA/build web: no hace falta LFS.
- Si se decide limpiar más adelante, hacerlo en una copia con `git lfs migrate import --include="*.blend"` o `git filter-repo`, medir antes/después y coordinar el reset de todos los clones.
- Las escenas históricas que no sean fuente ni referencia se pueden archivar fuera del repositorio antes de esa limpieza.

```text
blender/
  caral/
    caral_remaster.blend  # fuente v1 y base de v2 (versionada)
    caral_remaster_v2.blend  # escena v2 local (no versionada)
    caral_lod0.blend / caral_lod1.blend  # LODs locales (no versionados)
    export.py             # exporta v1 a GLB
  chan-chan/
    chanchan_highpoly_v0.1.blend  # fuente del preview Nik An (versionada)
    chanchan_lod0.blend / chanchan_lod1.blend  # LODs locales (no versionados)
  wari/
    wari_highpoly_v0.1.blend  # fuente del preview del núcleo (versionada)
    wari_lod0.blend / wari_lod1.blend  # LODs locales (no versionados)
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

- Los LOD0/LOD1 se exportan con `scripts/caral/export_caral_lod.py` (WebP 80 + Draco).
- El piloto histórico con texturas de IA fue retirado del repositorio.

## Chan Chan

- La fuente versionada es `blender/chan-chan/chanchan_highpoly_v0.1.blend`.
- Los LOD0/LOD1 se generan con `scripts/chan-chan/build_chanchan_lod.py` y se exportan con `scripts/chan-chan/export_chanchan_lod.py`.
- El preview se limita a Nik An; no se versionan los LODs.

## Wari

- La fuente versionada es `blender/wari/wari_highpoly_v0.1.blend`.
- Los LOD0/LOD1 se generan con `scripts/wari/build_wari_lod.py` y se exportan con `scripts/wari/export_wari_lod.py`.
- El preview se limita al núcleo monumental; no se versionan los LODs.

## Convenciones

- Unidades: metros.
- Origen: centro del sitio a nivel del suelo.
- Nombres: `GEO-`, `MAT-`, `CAM-`, `LGT-`.
- Exportar Y-up, sin cámaras ni luces.
- Aplicar modificadores y mantener texturas empaquetadas o en rutas relativas.
- No incluir elementos de juego ni texturas de IA.

Ver [`docs/pipeline-blender.md`](../docs/pipeline-blender.md).
