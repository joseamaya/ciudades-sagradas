# QA en hardware real — Caral v2

Fecha de preparación: 27 de octubre de 2026.
Estado: **protocolo listo; mediciones en dispositivos físicos pendientes.**

## URLs

- Producción: <https://joseamaya.github.io/ciudades-sagradas/?debug=1#/ciudad/caral>
- Forzar LOD0: `?lod=0&debug=1#/ciudad/caral`
- Forzar LOD1: `?lod=1&debug=1#/ciudad/caral`
- Kiosco: `?kiosk=1#/ciudad/caral`

El overlay `?debug=1` muestra LOD, draw calls, triángulos, FPS, frame time, sombras, texturas y carga. El botón **Copiar métricas** copia el JSON completo de `window.__ciudadesSagradas.metrics()`. Para aislar render: `?noground=1` y `?noshadows=1`.

## Matriz mínima

| Dispositivo | Navegador | LOD esperado | Carga fría | 6 paradas | 4 luces | Offline | 10 min | Consola | Resultado |
|---|---|---|---|---|---|---|---:|---|
| iPhone (Safari) | Safari | LOD1 |  |  |  |  |  |  | Pendiente |
| Android medio (Chrome) | Chrome | LOD1 |  |  |  |  |  |  | Pendiente |
| Desktop GPU integrada | Chrome/Edge | LOD0 |  |  |  |  |  |  | Pendiente |
| Desktop GPU dedicada | Chrome/Edge | LOD0 |  |  |  |  |  |  | Pendiente |
| Kiosco 1920×1080 | Chromium | LOD0 |  |  |  |  |  |  | Congelado |

## Protocolo

1. Abrir la URL con `?debug=1` y anotar dispositivo, navegador, versión y resolución.
2. Comprobar el LOD elegido y que `?lod=0/1` lo fuerza.
3. Esperar a que desaparezca el loading y pulsar **Copiar métricas**.
4. Recorrer las 6 paradas y las 4 luces; repetir métricas en la parada 06 (Altar).
5. Probar las 4 capas y el panel de ficha.
6. Instalar la PWA, abrirla y repetir una carga.
7. Tras una visita online, activar modo avión y recargar; verificar que el LOD cargado sigue funcionando.
8. Dejar la escena 10 minutos con órbitas suaves y comprobar que no hay errores ni crecimiento raro de memoria.
9. Anotar FPS medio, frame time, draw calls, texturas, carga y cualquier warning.

## Android: métricas profundas

```text
chrome://inspect  →  dispositivo por USB  →  Inspect
window.__ciudadesSagradas.metrics()
```

## iOS

Safari no expone FPS al usuario. Usar el overlay, **Copiar métricas** y una captura de pantalla. Web Inspector remoto solo si hay un Mac disponible.

## Verificación del panel móvil

- Scroll del panel comprobado en emulación 390×844: `scrollHeight=1378`, `clientHeight=488`, `scrollTop=890`.
- Capas y Luz son accesibles deslizando dentro de la ficha.

## Resultados de emulación (referencia, no sustituyen hardware)

| Escenario | LOD | Draw calls | Refresh sombras | Triángulos | Texturas | FPS SwiftShader |
|---|---|---:|---:|---:|---:|---:|
| Desktop 1600×900 | 0 | 44 | 100 | 230.800 | 373 MB | ~2 |
| Desktop 1600×900 | 1 | 31 | 60 | 56.332 | 208 MB | ~2 |
| Móvil 390×844 | 1 | 31 | 60 | 56.332 | 208 MB | ~5–6 |

## Criterio de aceptación

- LOD0 en desktop y LOD1 en móvil.
- Sin errores de consola.
- Offline y PWA funcionando.
- Sesión de 10 minutos sin regresión visible.
- FPS objetivo: 60 en desktop GPU media y al menos 30 en móvil; documentar lo medido aunque no se alcance.
