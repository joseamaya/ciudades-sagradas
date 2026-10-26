# Release web — Caral remaster v2

- Fecha: 26 de octubre de 2026.
- Estado: **desplegado en producción**.
- URL: <https://joseamaya.github.io/ciudades-sagradas/>
- PR base: [#5](https://github.com/joseamaya/ciudades-sagradas/pull/5)
- Merge base: `a76fc8b` (`feat(caral): LOD0/LOD1 web v2`)
- Cierre de release: rama `release/caral-v2`.

## Alcance

- Caral LOD0 high-poly + infraestructura fusionada.
- Caral LOD1 horneado con atlas 2K por región.
- Selección automática escritorio/móvil y override `?lod=0/1`.
- Fallback `model_lod0.glb` → `model_lod1.glb` → `model.glb` v1.
- Seis paradas de recorrido, incluida la parada del Altar Circular.
- Capas Arquitectura, Terreno y valle, Detalles y ofrendas, y Escala humana.
- Caché de servicio `v5` y precarga offline del modelo elegido más el fallback v1.
- Portada del catálogo regenerada desde el visor v2.

## Métricas

| Elemento | LOD0 | LOD1 |
|---|---:|---:|
| Triángulos | 230.800 | 56.332 |
| Mallas Blender | 10 | 15 |
| Primitivas Three.js | 65 | 38 |
| Materiales / imágenes | 21 / 31 | 23 / 39 |
| GLB | 22.587.652 bytes | 6.694.356 bytes |
| Draw calls | 125 | 72 |

- LOD0 se acepta en **125 draw calls** para escritorio; LOD1 cumple el objetivo <100.
- Escala de visor: **0,08**, presentación de diorama.
- `model.glb` v1: 4.778.308 bytes, 55.944 tris, fallback y rollback.
- Sin texturas de IA en v1 ni v2.

## QA

- `npm run validate` y `npm run build`: OK.
- Escritorio emulado 1600×900: LOD0, 125 draw calls.
- Móvil emulado 390×844: LOD1, 72 draw calls.
- Seis paradas en ambos LOD; Altar Circular verificado.
- Fallback LOD0 → LOD1 y LOD1 → v1 verificado.
- Offline LOD0 y LOD1 verificado con caché `v5`.
- CI de PR #5 y deploy de GitHub Pages: OK.

Pendiente: validación en iPhone/Safari, Android/Chrome y GPU real; 60 fps a 1080p. El kiosco, el hardware de museo y la escala 1.0 quedan congelados.

## Límites conocidos

- No se modelaron los 20 cubículos del Anfiteatro por falta de una planta publicada suficiente.
- La diferencia de altura norte/sur del Mayor sigue pendiente de sección o DEM.
- LOD1 no conecta AO ni mapa de roughness; usa roughness constante 0,85 y normal 0,35.
- El visor fusiona la infraestructura en seis grupos y conserva las cuatro capas, no la jerarquía individual v1.
- La distribución de piedras, erosión y cortes de shicras es inferida/interpretativa.

## Rollback

- En la aplicación: dejar que el visor use `model.glb` v1 como fallback.
- En Git: revertir el merge `a76fc8b` y volver a desplegar `main`.
- La caché `v5` se elimina automáticamente al activarse una versión posterior.
