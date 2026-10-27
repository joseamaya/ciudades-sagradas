# Auditoría de cierre — Caral Remaster v2

- Fecha: 26 de octubre de 2026.
- Alcance: estado actual del repositorio `ciudades-sagradas`, sin Chavín, Chan Chan ni Wari.
- Método: lectura de código, parseo de GLB, `npm run validate`, `npm run build` y benchmark reproducible con Chrome headless/SwiftShader.
- Estado de publicación: cambios validados en local; **no se ha hecho commit ni deploy** en esta pasada.

## Estado general

🟡 **Estable y utilizable como plantilla técnica**, con dos riesgos abiertos: la VRAM de texturas de LOD1 y la falta de QA en hardware real. No se encontró ningún P0 funcional.

## Performance

| Métrica | LOD0 | LOD1 | v1 fallback |
|---|---:|---:|---:|
| Triángulos del modelo | 230.800 | 56.332 | 55.944 |
| Primitivas / mallas | 65 / 10 | 38 / 15 | 554 / 554 |
| Draw calls en régimen estable* | **44** | **31** | 342 |
| Draw calls al refrescar sombras** | **100** | **60** | n/d |
| GLB con Draco | **3.277.080 B** | **3.206.848 B** | 4.778.308 B |
| Materiales / imágenes | 21 / 31 | 23 / 39 | 20 / 31 |
| Texturas decodificadas estimadas*** | 373 MB | **544 MB** | 373 MB |
| Respuesta de red local | ~1,2 s | ~1,5 s | ~1,9 s |
| Hasta primer render (SwiftShader) | ~6,3 s | ~7,1 s | ~5,4 s |
| FPS SwiftShader (no representativo) | ~2,0 | ~1,8 | ~2,2 |

\* Cámara inicial 1600×900, shadow map cacheada, sin transmisión.
\** Frame puntual al cargar, cambiar hora o capas.
\*** RGBA8 + mipmaps estimados; no es el peso de descarga.

El benchmark móvil (390×844, DPR 3, pixel ratio 1,25) carga LOD1 con **31 draw calls** y shadow map de 1024².

## LOD

- **Escritorio:** LOD0 por defecto; `?lod=0/1` fuerza el nivel.
- **Móvil/táctil/iPad moderno/baja memoria o núcleos:** LOD1.
- **Fallback escritorio:** LOD0 → LOD1 → v1.
- **Fallback móvil:** LOD1 → v1 → LOD0 (no descarga el LOD0 de 3,28 MB antes del fallback v1).
- **Fallback verificado:** bloqueando LOD0 carga LOD1; bloqueando ambos carga v1; en móvil, bloqueando LOD1 carga v1.
- **Descargas:** el visor carga un solo LOD. `warmOfflineCache()` ya no descarga el fallback v1 si no se usa.
- **Fallback v1:** 342 draw calls en régimen estable y ~782 al refrescar sombras; es un último recurso, no un perfil de rendimiento.
- **Offline:** verificado con caché `v6`; el LOD cargado y sus recursos quedan disponibles sin red.

## Problemas encontrados

### P0 — crítico

Ninguno.

### P1 — importante (corregidos)

1. **Transmisión del agua**: `KHR_materials_transmission` forzaba una pasada extra de toda la escena y explica buena parte de los 125/72 draw calls documentados. Se anuló en GLB y en runtime.
2. **Materiales de doble cara**: los 21/23 materiales eran `doubleSided`; se activó culling en sólidos y se dejó doble cara solo en vegetación, totora, algodón, agua y fuego. Sin huecos visibles en las 6 paradas.
3. **Sombras por frame**: la shadow map se re-renderizaba cada frame con una escena estática. Ahora se actualiza solo al cargar, cambiar hora o capas; el régimen estable bajó a 44/31 draw calls.
4. **Fallback móvil incorrecto**: descargaba LOD0 antes que v1. Corregido y verificado.
5. **Precarga offline innecesaria**: `warmOfflineCache()` descargaba siempre el fallback v1. Eliminado; ahora cachea lo cargado y evita duplicados con `cache.match()`.
6. **Licencia desactualizada**: `LICENSE-CONTENT.md` decía que `model.glb` incluía texturas de IA. Corregido; los GLB publicados no las incluyen.
7. **Piloto histórico en el repo**: `.blend`, texturas y capturas con IA fueron retirados; las capturas públicas se regeneraron desde v2.

### P1 — importante (abiertos, documentados)

1. **VRAM de LOD1**: 544 MB estimados frente a 373 MB de LOD0. El LOD “móvil” ahorra geometría/draw calls, pero no memoria de texturas por los atlas 2K. Recomendación: KTX2/BasisU con gltfpack o atlas LOD1 a 1K.
2. **QA en hardware real**: no se midió 60 fps en iPhone/Safari, Android/Chrome ni GPU media. SwiftShader solo sirve para comparar. El kiosco sigue congelado.

### P2 — mejoras (corregidas)

- Detección de iPad moderno y portátiles táctiles; ya no se usa `pointer: coarse` como único criterio.
- Shadow map 2048/1024, cámara de sombras ajustada a los casters y refresco bajo demanda.
- Cielos y PMREM cacheados; se liberan los render targets al destruir el visor.
- Nombre de caché centralizado en `sw.js`; `validate.mjs` comprueba GLB, LOD, cámaras, capas, hashes y tamaños.
- Manifiesto PWA `standalone`/`any`, iconos 192/512, safe-area y foco visible.
- `?debug=1`, `window.__ciudadesSagradas.metrics()` y `npm run bench` reproducibles.
- Estrellas sin fog en el preset noche.

### P3 — nice-to-have (no bloquea)

- La reexportación de v1 con WebP conserva tamaño/estructura pero no el hash byte a byte.
- `verticalScale` ya se aplica, pero Caral usa 1.0.
- El LOD sigue siendo por dispositivo, no por distancia.
- Faltan los 20 cubículos del Anfiteatro y la corrección norte/sur del Mayor por fuentes.
- El chunk JS de Three.js supera 500 kB (aviso de Vite); no afecta al runtime de forma medible con la caché actual.

## Cambios realizados

- `src/core/viewer.js`: sombras estáticas y ajustadas, LOD/fallback, detección de dispositivo, culling, agua sin transmisión, PMREM cacheado, `verticalScale`, capas por defecto, métricas y render inicial antes de `onReady`.
- `src/main.js`: `?debug=1`, `?nosw=1`, métricas globales, caché offline sin fallback forzado, guardas de navegación y errores de audio.
- `src/styles.css`: panel móvil sobre la barra de recorrido, safe-area, foco visible y panel de diagnóstico.
- `public/manifest.webmanifest` y `public/icons/icon-192.png`/`icon-512.png`: PWA instalable.
- `public/sw.js` y `public/draco/`: caché `v6`, iconos en CORE, decoder Draco local y `.wasm` como asset.
- `scripts/export_caral_lod.py`: Draco, WebP 80, culling y agua sin transmisión.
- `scripts/bench.mjs` y `package.json`: benchmark/QA reproducible.
- `scripts/validate.mjs`: validación de GLB, LOD, tour, capas, caché y registro de assets.
- `public/cities/caral/model_lod0.glb` y `model_lod1.glb`: reexportados con Draco (230.800 / 56.332 tris).
- `scripts/remaster_caral_materials.py`, `scripts/bake_caral_lod1.py` y `blender/caral/export.py`: pipeline alineado (culling, WebP 80).
- Piloto retirado: `blender/caral/caral_art.blend`, texturas pilot-only y capturas antiguas.
- Documentación y capturas actualizadas; nuevo `docs/remaster/caral/auditoria-v2.md`.

## Problemas que NO deben tocarse todavía

- No implementar LOD por distancia ni streaming: el LOD por dispositivo es suficiente para Caral.
- No añadir KTX2 hasta medir VRAM/calidad con gltfpack y comparar atlas 1K.
- No rehacer el visor ni cambiar Three.js/Vite.
- No abrir Chavín, Chan Chan ni Wari hasta cerrar hardware real de Caral.
- No eliminar sombras globalmente ni cambiar la escala 0,08 sin una decisión de producto.

## Recomendaciones siguientes (máximo 5)

1. Validar en hardware real (iPhone/Safari, Android/Chrome, GPU media) y registrar FPS/frame time a 1080p.
2. Reducir la VRAM de LOD1: probar KTX2/BasisU con gltfpack o rehacer los atlas a 1K y comparar visualmente.
3. Añadir una prueba de hardware/kiosco de sesión larga y memoria.
4. Mantener el registro de hashes y la caché sincronizados en cada cambio de GLB.
5. Usar Caral v2 como plantilla de LOD/fallback, validación y benchmark para la siguiente ciudad.

## Veredicto

**¿Caral Remaster v2 está suficientemente estable para utilizarse como plantilla de las siguientes ciudades?**

**Sí, como plantilla técnica y de pipeline**, con dos condiciones: validar hardware real y resolver o aceptar explícitamente la VRAM de LOD1. La experiencia web está estable, el fallback y el offline funcionan, la licencia publicada es coherente y el rendimiento en régimen estable está por debajo de 100 draw calls. No debe presentarse todavía como certificación de 60 fps en hardware real ni como reconstrucción histórica final.
