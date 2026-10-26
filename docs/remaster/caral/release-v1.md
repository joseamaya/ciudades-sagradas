# Remaster v1

Rama: `release/caral-remaster-final`. **Pendiente de PR y merge**: `main` y GitHub Pages siguen con el piloto.

## Modelo

- Archivo: `public/cities/caral/model.glb`
- Tamaño: 4.778.308 bytes
- Mallas: 554
- Triángulos: 55.944
- Materiales: 20
- Imágenes: 31 WebP
- SHA-256: `c6bbe07b27640951373b96db4f6a610b7618224e37fc52eda8893ac79670bb34`
- Fuente: `blender/caral/caral_remaster.blend` (SHA-256 `52d79bb5db315fcc22f703665d6dc39f49d9bc9be7b729f93800face301d1f5f`)

## Metadatos actualizados

- `public/cities/caral/README.md` con hash, tamaño, tris, materiales, imágenes, licencias y estado v1.
- `docs/fuentes/registro-assets.csv` con la fila del nuevo GLB.
- `city.json`: `stage: "v1"` y créditos del remaster.
- Badge de la ficha: **Remaster · v1**.
- `public/sw.js` y `src/main.js`: caché `ciudades-sagradas-v3`.
- `README.md`, `CREDITS.md`, `docs/estado.md`, `hero.jpg` y dossier de remaster actualizados.

## QA local

- `npm run validate`: OK.
- `npm run build`: OK.
- `npm run serve`: el visor carga el GLB v1.
- Escritorio 1600×900: carga correcta.
- Offline: primera carga online, luego recarga sin red; el modelo y las 5 paradas siguen disponibles desde la caché `v3`.
- Badge **Remaster · v1** visible.
- Modelo sin texturas de IA; auditoría en `licencias-assets.md`.

## Pendiente para publicar v1

- Abrir PR, pasar CI, mergear y verificar GitHub Pages.
- Probar kiosco offline y sesión larga en hardware de museo.

## Pendiente para v2

- Muros high-poly + bake de normales/AO.
- LOD1 y reducción de draw calls.
- Arte final del hero/atardecer.

## Probar en local

```bash
npm run validate
npm run build
npm run serve
```

Abrir:

```text
http://127.0.0.1:4173/#/ciudad/caral
http://127.0.0.1:4173/?kiosk=1#/ciudad/caral
```

Para volver al piloto, cambiar de rama o restaurar `public/cities/caral/model.glb` desde `main`.

## Captura

- `release-v1.jpg`
