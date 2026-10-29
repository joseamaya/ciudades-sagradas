# Narihualá — preview web v0.2

Fecha: 29 de octubre de 2026.
Estado: **preview interpretativo; no reconstrucción final**.
Modelo: `public/cities/narihuala/model_lod0.glb` y `model_lod1.glb`.
Fuente: `blender/narihuala/narihuala_highpoly_v0.2.blend`.

## Qué se integró

- LOD0: **175.724 tris / 1.739.336 B**; LOD1: **26.894 tris / 393.000 B**.
- 14/13 draw calls; 96/48 MB de texturas; 2K/1K.
- Seis paradas: valle, montículo oeste, plaza, rampas, montículo este y mirador.
- Capas: arquitectura tallán, valle y bosque seco, detalles, escala humana y capilla republicana (`later`, apagada).
- `scale: 0.08`; caché `v29`.

## Vistas

### Hero

![Hero](web-preview-hero.png)

### Montículo oeste

![Montículo oeste](web-preview-west.png)

### Plaza central

![Plaza](web-preview-plaza.png)

### Montículo este

![Montículo este](web-preview-east.png)

## Lectura

- El montículo este y la capilla se apoyan en SIGRID 2018.
- El montículo oeste, la plaza y las rampas son inferencias explícitas.
- La capilla no se muestra en el hero; está en `later`.
- No se asigna la numeración I–III.

## Límites

- No es un plano arqueológico; el cierre de cotas finas sigue abierto.
- No hay QA en hardware real.
- No se copiaron ortofotos ni imágenes oficiales; sin texturas de IA.
- El preview no debe presentarse como reconstrucción final.
