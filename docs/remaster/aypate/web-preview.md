# Aypate — preview web v0.4

Fecha: 29 de octubre de 2026.
Estado: **preview público controlado; high-poly con layout y escala contrastados, no reconstrucción final**.
Modelo: `public/cities/aypate/model_lod0.glb` y `model_lod1.glb`.
Fuente: `blender/aypate/aypate_highpoly_v0.4.blend`; los LOD se regeneran con `scripts/build_aypate_lod.py` y no se versionan.

## Qué se integró

- `city.json` con `status: "available"` y `stage: "preview"`.
- LOD0 de 209.560 tris / 2.139.720 B; LOD1 de 30.663 tris / 443.372 B.
- 18 y 16 draw calls en la vista inicial; 12/9 materiales y 15 imágenes 2K/1K px.
- Seis paradas: Qhapaq Ñan, plaza, ushnu, kallanka, acllawasi y fuente ritual.
- Capas: arquitectura inca, cerro y bosque de neblina, detalles y escala humana.
- `scale: 0.08`, `minDistance: 0.1` y `maxDistance: 180`.
- Caché `v27`.

## Vistas

### Plaza Inca

![Plaza Inca](web-preview-plaza.png)

### Kallanka

![Kallanka](web-preview-kallanka.png)

### Acllawasi

![Acllawasi](web-preview-acllawasi.png)

## Métricas

| Métrica | LOD0 | LOD1 |
|---|---:|---:|
| Triángulos | 209.560 | 30.663 |
| GLB | 2.139.720 B | 443.372 B |
| Mallas exportadas | 4 | 4 |
| Draw calls | 18 | 16 |
| Materiales / imágenes | 12 / 15 | 9 / 15 |
| Texturas decodificadas | 160 MB | 80 MB |

- `?lod=0` fuerza LOD0; `?lod=1` fuerza LOD1.
- Móvil emulado selecciona LOD1.
- No hay fallback v1 independiente: LOD1 es el fallback.
- El bench de SwiftShader no certifica FPS.

## QA ejecutado

- `npm run validate`: OK (6 ciudades, 3 disponibles).
- `npm run build`: OK.
- Bench LOD0/LOD1/móvil: OK, sin errores de consola.
- Seis paradas capturadas; revisadas la llegada, plaza, ushnu, kallanka, acllawasi y fuente.
- Sin imágenes oficiales ni texturas de IA.

## Límites

- El plano general de 2013 está publicado en Campos 2017; la memoria de 36 sectores no es pública.
- La v0.4 conserva el layout macro y corrige escala: ushnu de 30 × 30 m con terraza superior de 20,7 × 23,7 m y 25 peldaños; kallanka de 115 × 12 m; acllawasi en cuatro canchas. Ver `escala.md`, `cotas.md` y `auditoria-plano-2013.md`.
- Los edificios se muestran sin techos y con volúmenes de high-poly; el layout macro es documentado y los detalles siguen siendo interpretativos.
- La vegetación y la niebla son una lectura ambiental, no un inventario.
- No hay QA en hardware real todavía.
- La puerta escaneada de Sketchfab no se incorporó al GLB; solo se usó como referencia.
- El preview no debe presentarse como remaster final.
