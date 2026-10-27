# Release web — Caral remaster v2

- Fecha: 26 de octubre de 2026.
- Estado: **desplegado en producción** con Draco, LOD1 a 1K y caché `v7`. Tags: `caral-v2.0.0` (cierre) y `caral-v2.0.1` (scroll móvil + mitigación del suelo).
- Cierre de contenido: **ciudad representativa**, no inventario 1:1 de los 32 edificios públicos. Ver `cobertura.md`.
- Incidencia abierta: parpadeo de suelo en Android; ver `incidencias.md` e issue [#10](https://github.com/joseamaya/ciudades-sagradas/issues/10).
- URL: <https://joseamaya.github.io/ciudades-sagradas/>
- PR base: [#5](https://github.com/joseamaya/ciudades-sagradas/pull/5)
- Merge base: `a76fc8b` (`feat(caral): LOD0/LOD1 web v2`)
- Cierre de release: rama `release/caral-v2`.

## Alcance

- Caral LOD0 high-poly + infraestructura fusionada.
- Caral LOD1 horneado por región y exportado con texturas 1K.
- Selección automática escritorio/móvil y override `?lod=0/1`.
- Fallback `model_lod0.glb` → `model_lod1.glb` → `model.glb` v1 en escritorio; `model_lod1.glb` → `model.glb` v1 → `model_lod0.glb` en móvil.
- Seis paradas de recorrido, incluida la parada del Altar Circular.
- Capas Arquitectura, Terreno y valle, Detalles y ofrendas, y Escala humana.
- Caché de servicio `v7` y precarga offline del modelo elegido; el fallback v1 ya no se descarga si no se usa.
- Portada del catálogo regenerada desde el visor v2.

## Métricas

| Elemento | LOD0 | LOD1 |
|---|---:|---:|
| Triángulos | 230.800 | 56.332 |
| Mallas Blender | 10 | 15 |
| Primitivas Three.js | 65 | 38 |
| Materiales / imágenes | 21 / 31 | 23 / 39 |
| GLB con Draco | 3.277.080 bytes | 1.345.092 bytes |
| Draw calls en régimen estable | 44 | 31 |

- LOD0 y LOD1 quedan por debajo de 100 draw calls en régimen estable. El refresco de sombras suma los casters solo en el frame de actualización.
- Escala de visor: **0,08**, presentación de diorama.
- `model.glb` v1: 4.778.308 bytes, 55.944 tris, fallback y rollback.
- Sin texturas de IA en v1 ni v2.

## Cobertura

Caral v2 se cierra como **ciudad representativa**: las seis pirámides, plazas y sectores principales están presentes; el high-poly se concentra en Pirámide Mayor, Plaza Mayor, Anfiteatro y Altar Circular. El resto usa la geometría v1. Los 20 cubículos del Anfiteatro y el perfil norte/sur del Mayor quedan diferidos por falta de fuente. Detalle en `cobertura.md`.

## QA

- `npm run validate` y `npm run build`: OK.
- Escritorio emulado 1600×900: LOD0, 44 draw calls en régimen estable.
- Móvil emulado 390×844: LOD1, 31 draw calls en régimen estable.
- Seis paradas en ambos LOD; Altar Circular verificado.
- Fallback LOD0 → LOD1 → v1 y móvil LOD1 → v1 → LOD0 verificado.
- Offline LOD0 verificado con caché `v7`; el LOD cargado se cachea y el fallback v1 no se precarga.
- CI de PR #5 y deploy de GitHub Pages: OK.

Pendiente: validación en iPhone/Safari y GPU real; 60 fps a 1080p. Android/Chrome tiene una **incidencia P2 de parpadeo de suelo** documentada; no se declara resuelta. El benchmark reproducible con SwiftShader mide draw calls y triángulos, no FPS real. El kiosco, el hardware de museo y la escala 1.0 quedan congelados.

## Límites conocidos

- No se modelaron los 20 cubículos del Anfiteatro por falta de una planta publicada suficiente.
- La diferencia de altura norte/sur del Mayor sigue pendiente de sección o DEM.
- No hay 32/32 edificios individuales de alta fidelidad; la cobertura es representativa y varios sectores están agregados.
- Parpadeo de suelo en Android: incidencia P2 abierta, aceptada para este cierre. No hay workaround confirmado.
- LOD1 no conecta AO ni mapa de roughness; usa roughness constante 0,85 y normal 0,35. El AO no se incluye en el GLB.
- LOD1 usa texturas 1K: ~208 MB estimados de VRAM, frente a ~544 MB con 2K. KTX2/BasisU queda como mejora futura si se necesita aún menos VRAM.
- El visor fusiona la infraestructura en seis grupos y conserva las cuatro capas, no la jerarquía individual v1.
- La distribución de piedras, erosión y cortes de shicras es inferida/interpretativa.

## Rollback

- En la aplicación: dejar que el visor use `model.glb` v1 como fallback.
- En Git: revertir el merge `a76fc8b` y volver a desplegar `main`.
- La caché `v7` se elimina automáticamente al activarse una versión posterior.
