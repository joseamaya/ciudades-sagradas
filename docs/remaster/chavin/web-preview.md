# Chavín — preview web v0.1

Fecha: 27 de octubre de 2026.
Estado: **preview público controlado; no es un remaster final ni un LOD de producción**.
Modelo: `public/cities/chavin/model_lod0.glb` y `model_lod1.glb`.
Fuente Blender: `chavin_portada_v0.1.blend`; los derivados `chavin_lod0.blend` / `chavin_lod1.blend` se regeneran con scripts y no se versionan.

## Vistas

### Escritorio, LOD0

![Preview LOD0](web-preview-lod0.png)

### Móvil, LOD1

![Preview móvil](web-preview-mobile.png)

### Parada de la Portada

![Portada en el visor](web-preview-portada.png)

### Catálogo

![Chavín en el atlas](web-preview-atlas.png)

## Qué se integró

- `city.json` con `status: "available"` y `stage: "preview"`.
- Dos niveles: LOD0 de 14.158 tris y LOD1 de 9.422 tris.
- `scale: 0.08`, cámara inicial y seis paradas de recorrido.
- Capas `city`, `terrain`, `props` y `reference`, exportadas en los extras del GLB.
- `hero.jpg` propio desde la Portada, sin imágenes oficiales.
- Terreno con textura propia 1K en el GLB.
- Caché del service worker `v12`.

## Métricas del preview

| Métrica | LOD0 | LOD1 |
|---|---:|---:|
| Triángulos | 14.158 | 9.422 |
| Mallas exportadas | 4 | 4 |
| Draw calls en la vista inicial | 15 | 15 |
| GLB | 732.780 B | 654.732 B |
| Texturas decodificadas estimadas | 133,3 MB | 69,3 MB |
| Imágenes | 13 | 13, a 1024 px |

- `?lod=0` fuerza LOD0; `?lod=1` fuerza LOD1.
- Móvil emulado selecciona LOD1.
- Sin LOD0, el visor cae a LOD1.
- No hay fallback v1 independiente: LOD1 es el fallback de este preview.
- Offline probado con LOD0 antes del pase de textura; repetir en QA de hardware.

## QA ejecutado

- `npm run validate`: OK.
- `npm run build`: OK.
- LOD0/LOD1 y las cámaras del recorrido se midieron con `bench --city chavin`; la corrida completa con `--qa` agotó el tiempo del entorno después de generar las capturas. El benchmark de hardware queda pendiente.
- Escritorio 1600×900: LOD0, 15 draw calls.
- Móvil 390×844: LOD1, 15 draw calls.
- Seis paradas verificadas; la cámara de la Portada se acerca a 0,86 m de escena.
- Capas presentes en los extras: `city`, `terrain`, `props`, `reference`.
- Consola sin errores en las cargas medidas.

Los FPS de SwiftShader no representan hardware real y no se usan como certificación.

## Cambios de visor

- Se añadió `city.minDistance` y `city.maxDistance` a `CityViewer`.
- Chavín usa `minDistance: 0.25` para permitir las cámaras de detalle de la Portada y el Lanzón; Caral conserva el valor por defecto de 5.
- El resto de la lógica de LOD, capas y fallback se reutiliza sin cambios.

## Límites

- El LOD0 está muy por debajo del presupuesto de producción de 150.000–250.000 tris.
- El LOD1 no es un bake de alta fidelidad; elimina ojos, colmillos y serpentinas del relieve.
- El terreno es procedural; sus tres texturas propias (difusa, rugosidad y normal) se generan por `scripts/make_chavin_terrain_materials.py` y no constituyen topografía levantada.
- La Portada mantiene relieves abstractos; el dintel no se modela y la escalera es un solo escalón inferido.
- No hay QA en hardware real ni certificación de 60 fps.
- No se copiaron imágenes oficiales ni se usaron texturas de IA.
- El preview no debe presentarse como remaster v2.

## Reproducir

```bash
blender --background blender/chavin/chavin_portada_v0.1.blend \
  --python scripts/build_chavin_lod.py -- --lod 0 \
  --out-blend blender/chavin/chavin_lod0.blend

blender --background blender/chavin/chavin_lod0.blend \
  --python scripts/export_chavin_lod.py -- \
  --out public/cities/chavin/model_lod0.glb

npm run validate
npm run build
npm run bench -- --city chavin --out /tmp/chavin-final --qa
```
