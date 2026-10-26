# Release candidate local

Rama: `release/caral-remaster-preview`. **No publicado**: `main` y GitHub Pages siguen con el piloto.

## Modelo

- Archivo: `public/cities/caral/model.glb`
- Tamaño: 8.928.092 bytes
- Mallas: 554
- Triángulos: 55.944
- Materiales: 22
- Imágenes: 37 WebP
- SHA-256: `7c5e2538a93448afa59fbb4a106f9f523fc18a578f243411d136f67e5042fcb6`
- Fuente: `blender/caral/caral_remaster.blend` (SHA-256 `631af87f5f00630b3196092361c3d0f766404dcb805078ec2116f60987426863`)

## Metadatos actualizados

- `public/cities/caral/README.md` con hash, tamaño, tris, materiales, imágenes y estado preview.
- `docs/fuentes/registro-assets.csv` con la fila del nuevo GLB.
- `city.json`: `stage: "preview"` y créditos de preview.
- Badge de la ficha: **Remaster · preview**.
- `public/sw.js` y `src/main.js`: caché `ciudades-sagradas-v3`.
- `README.md`, `CREDITS.md`, `docs/estado.md` y dossier de remaster actualizados.

## QA local

- `npm run validate`: OK.
- `npm run build`: OK.
- `npm run serve`: el visor carga el GLB del RC.
- Escritorio 1600×900: carga correcta.
- Offline: primera carga online, luego recarga sin red; el modelo y las 5 paradas siguen disponibles desde la caché `v3`.
- Badge **Remaster · preview** visible.

## Pendiente antes de mergear

- Prueba en hardware de museo y durante una sesión larga.
- Roca/vegetación procedurales o aceptar las texturas del piloto.
- Auditoría de licencias de las texturas restantes.
- Muros high-poly + bake de normales/AO.
- Aprobación visual del reemplazo.
- Prueba de kiosco offline en el hardware final.

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

- `release-preview.jpg`
