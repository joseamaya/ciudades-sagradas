# QA en hardware real — Chavín preview v0.3

Fecha: 28 de octubre de 2026.
Estado: **Chavín aprobado en Android; iPhone/Safari y desktop GPU pendientes**.
Modelo probado: `model_lod0.glb` / `model_lod1.glb` v0.3, caché `v20`. La v0.4 (columnas acanaladas y `fov 28`) está pendiente de repetir en el mismo dispositivo.

## Resultado Android

| Campo | Valor |
|---|---|
| Resultado | **Pass** en Chavín |
| Dispositivo | No registrado |
| Android / Chrome | No registrado |
| GPU | No registrada (`chrome://gpu` pendiente) |
| LOD observado | No registrado; el móvil debe seleccionar LOD1 |
| Pruebas realizadas | Carga y recorrido de Chavín |
| Evidencia | Sin captura ni JSON de `?debug=1` |

El usuario confirmó que Chavín funciona bien en Android. El resultado se registra como
**pass de producto**, no como certificación de rendimiento: faltan modelo, versión,
GPU, métricas y evidencia.

## Matriz

| Dispositivo | Navegador | LOD esperado | Resultado |
|---|---|---|---|
| Android | Chrome | LOD1 | **Pass parcial**; datos pendientes |
| iPhone | Safari | LOD1 | Pendiente |
| Desktop GPU integrada | Chrome/Edge | LOD0 | Pendiente |
| Desktop GPU dedicada | Chrome/Edge | LOD0 | Pendiente |
| Kiosco 1920×1080 | Chromium | LOD0 | Congelado |

## Protocolo pendiente

1. Abrir `https://joseamaya.github.io/ciudades-sagradas/?debug=1#/ciudad/chavin`.
2. Anotar modelo, Android/Chrome, GPU, resolución y si es PWA.
3. Probar LOD automático, `?lod=0` y `?lod=1`.
4. Recorrer las seis paradas; revisar la 3 (Lanzón) y la 5 (Portada).
5. Probar las cuatro luces, cuatro capas y el scroll de la ficha.
6. Instalar la PWA y repetir offline.
7. Dejar 10 minutos con órbitas suaves.
8. Guardar “Copiar métricas” y captura/vídeo.

## Límites

- No se declara Android aprobado para Caral: el parpadeo de suelo sigue abierto en
  el issue #10.
- No hay medición de FPS/frame time en hardware; SwiftShader no certifica rendimiento.
- La parada 3 del Lanzón recorta la cresta por el ancho de la galería; el relieve se
  lee con la luz de relleno.
- La aprobación Android no cubre la v0.4: hay que repetir al menos la parada 5 y el
  recorrido completo con la caché `v21`.
