# QA en hardware real — protocolo del atlas

Actualizado: 30 de octubre de 2026.
Ámbito: Caral, Chavín, Aypate, Narihualá y cualquier ciudad futura.

Registro de resultados y secuencia de captura: [`../qa/README.md`](../qa/README.md). Revisión funcional Playwright: [`../qa/revision-playwright.md`](../qa/revision-playwright.md).

Este documento separa tres cosas que no son equivalentes:

- **Validación automática:** `npm run validate` y `npm run build`.
- **Benchmark técnico:** `npm run bench` con Chrome headless y SwiftShader. Sirve para comparar triángulos, draw calls, texturas, carga, fallback y consola. **No mide FPS reales.**
- **QA de hardware:** pruebas en dispositivos físicos, PWA instalada, offline, memoria y sesión prolongada.

## Estado actual

| Ciudad | Android/Chrome | iPhone/Safari | GPU integrada | GPU dedicada | Kiosco | Evidencia |
|---|---|---|---|---|---|---|
| Caral v2 | Parcial: incidencia P2 de suelo | Pendiente | **Pass 1600×900**: LOD0/LOD1, flags, offline, standalone y 10 min | Pendiente | Congelado | `docs/qa/resultados/desktop-2026-10-30/` |
| Chavín v0.6 | Pass de producto en v0.3; v0.6 pendiente | Pendiente | **Pass 1600×900**: LOD0/LOD1 | Pendiente | Congelado | `docs/qa/resultados/desktop-2026-10-30/` |
| Aypate v0.4 | Pendiente | Pendiente | **Pass 1600×900**: LOD0/LOD1 | Pendiente | Congelado | `docs/qa/resultados/desktop-2026-10-30/` |
| Narihualá v0.2 | Pendiente | Pendiente | **Pass 1600×900**: LOD0/LOD1 | Pendiente | Congelado | `docs/qa/resultados/desktop-2026-10-30/` |

No se registra un “pass” de rendimiento sin dispositivo, navegador, GPU, resolución, LOD y métricas. Un pass de producto solo confirma que la escena se abre y se puede recorrer.

## Matriz mínima

| Dispositivo | Navegador | LOD esperado | Carga fría | 6 paradas | 4 luces | 4 capas | Offline/PWA | 10 min | Consola |
|---|---|---|---|---|---|---|---|---|---|
| Android medio | Chrome | LOD1 |  |  |  |  |  |  |  |
| iPhone | Safari | LOD1 |  |  |  |  |  |  |  |
| Desktop GPU integrada | Chrome/Edge | LOD0 |  |  |  |  |  |  |  |
| Desktop GPU dedicada | Chrome/Edge | LOD0 |  |  |  |  |  |  |  |
| Kiosco 1920×1080 | Chromium | LOD0 |  |  |  |  |  |  |  |

## Protocolo reproducible

1. Abrir `https://joseamaya.github.io/ciudades-sagradas/?debug=1#/ciudad/<id>`.
2. Anotar dispositivo, modelo, SO, navegador, versión, GPU (`chrome://gpu` en Chromium) y resolución.
3. Comprobar el LOD elegido y forzar `?lod=0` y `?lod=1`.
4. Pulsar **Copiar informe QA** y guardar el JSON completo.
5. Recorrer las seis paradas, las cuatro luces y las cuatro capas.
6. Abrir la ficha, comprobar scroll, fuentes y cierre del panel.
7. Instalar la PWA, abrirla y repetir una carga.
8. Tras una visita online, activar modo avión y recargar; verificar el LOD ya cargado.
9. Dejar la escena 10 minutos con órbitas suaves y anotar errores o crecimiento anómalo de memoria.
10. Guardar captura/vídeo y el informe QA junto al resultado.

## Informe QA

El botón **Copiar informe QA** de `?debug=1` genera un JSON local con:

- `route`, `city` y `cityName`.
- `metrics`: LOD, triángulos, draw calls, texturas, VRAM estimada, carga, flags, capas y FPS de la sesión.
- `environment`: user agent, plataforma, pantalla, densidad, memoria, núcleos, PWA/standalone, service worker, online y datos WebGL/GPU.
- `issues`: últimos errores de ventana y promesas rechazadas, si los hubo.

El informe no se envía a ningún servidor. Se copia al portapapeles y el tester decide dónde pegarlo. Si el navegador oculta la GPU por privacidad, `unmaskedRenderer` puede venir vacío; se conserva el `renderer` enmascarado.

Esqueleto:

```json
{
  "schemaVersion": 1,
  "generatedAt": "2026-10-30T00:00:00.000Z",
  "route": "#/ciudad/caral",
  "city": "caral",
  "cityName": "Caral",
  "metrics": { "lod": "0", "calls": 44, "modelTriangles": 230800 },
  "environment": {
    "userAgent": "…",
    "standalone": false,
    "serviceWorker": true,
    "online": true,
    "webgl": { "vendor": "…", "renderer": "…", "version": "WebGL 2.0", "maxTextureSize": 8192 }
  },
  "issues": []
}
```

Adjuntar el informe al issue de Caral Android o al PR de QA, junto con dispositivo, versión de SO/navegador, captura o vídeo.

## Aislamiento de incidencias

Para Caral Android `CARAL-ANDROID-GROUND-001`, probar en este orden:

1. `?debug=1`
2. `?lod=0&debug=1`
3. `?lod=1&debug=1`
4. `?noground=1`
5. `?noshadows=1`
6. `?noground=1&noshadows=1`
7. PWA instalada frente a navegador

No declarar la incidencia resuelta hasta completar la matriz y registrar GPU, versión y vídeo.

## Criterio de aceptación

- LOD0 en escritorio y LOD1 en móvil, con fallback probado.
- Sin errores de consola nuevos.
- PWA y offline funcionando.
- Seis paradas, cuatro luces y capas accesibles.
- Sesión de 10 minutos sin regresión visible.
- FPS objetivo: 60 en escritorio GPU media y al menos 30 en móvil; documentar lo medido aunque no se alcance.
- Cualquier excepción P2 debe tener impacto, responsable y fecha de revisión.
