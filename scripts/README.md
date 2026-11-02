# Scripts

Organización por ciudad:

```text
scripts/caral/       remaster, LOD, materiales y renders de Caral
scripts/chavin/      high-poly, valle, materiales y export de Chavín
scripts/aypate/      blockout, high-poly, LOD y export de Aypate
scripts/narihuala/   blockout, high-poly, LOD y export de Narihualá
scripts/tools/       utilidades Blender transversales
scripts/archive/     scripts de revisión históricos sin referencias vigentes
```

En la raíz quedan las herramientas de producto: `validate.mjs`, `bench.mjs`, `build-sw.mjs`, `check-dist.mjs`, `asset-hash.mjs`, `sw.template.js` y `kiosk.sh`.

Las versiones antiguas de los scripts se conservan junto a las actuales porque `docs/fuentes/registro-assets.csv` y los informes de remaster las referencian para reproducir assets históricos. Los renders de revisión sin referencias se mueven a `scripts/archive/`; no se versionan `__pycache__`.

Los scripts de Aypate y Narihualá se importan entre sí y resuelven la raíz del repo desde `__file__`; se pueden ejecutar desde la raíz del repositorio.
