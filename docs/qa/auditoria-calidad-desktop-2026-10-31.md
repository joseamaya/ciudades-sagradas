# Auditoría de calidad desktop

Fecha: 31 de octubre de 2026.
Alcance: web de escritorio. **No incluye móvil, tableta, kiosco físico ni 1080p real** porque no hay dispositivos disponibles.
Base: `https://joseamaya.github.io/ciudades-sagradas/` y build local.

## Objetivo

Cerrar deuda de calidad del atlas existente antes de abrir otra ciudad 3D: consistencia documental, accesibilidad, movimiento reducido, recuperación ante fallos y regresión funcional en escritorio.

## Hallazgos corregidos

1. **Deriva de caché:** `public/sw.js` usa `ciudades-sagradas-v38`, pero 13 documentos vigentes seguían citando `v36`. Se actualizaron las referencias actuales; las menciones históricas a versiones anteriores se conservan.
2. **Accesibilidad de la ficha:**
   - El canvas 3D ahora declara `role="img"`, etiqueta y descripción enlazada.
   - `#info-toggle` expone `aria-controls` y `aria-expanded`.
   - El panel usa `aria-hidden` e `inert` cuando está cerrado.
   - Al abrir/cerrar el panel se gestiona el foco; `Escape` cierra el panel en móvil antes de salir de la ciudad.
   - Las horas usan `aria-pressed`; la parada activa usa `aria-current`.
   - `loading` y `toast` son regiones `status` con `aria-live`.
3. **Movimiento reducido:** con `prefers-reduced-motion: reduce`, el visor desactiva el damping y salta directamente a la cámara de la parada.
4. **Fallo de modelo:** si el GLB no carga, se muestra un estado visible con `role="alert"`, botón **Reintentar** y enlace **Volver al atlas**, en vez de dejar solo un toast.
5. **Fechas:** se alinearon `docs/estado.md`, `docs/estandares/auditoria-ciudades.md` y `docs/qa/README.md` al 31 de octubre de 2026.

## Evidencia

| Prueba | Alcance | Resultado |
|---|---|---|
| `npm run validate` | 6 ciudades, 4 modelos | **OK** |
| `npm run build` | producción | **OK**; catálogo 25,18 kB (8,93 kB gzip); visor diferido 652,21 kB (167,98 kB gzip) |
| Playwright Chromium desktop 1600×900 | 32 pruebas | **32/32 pass** (16,6 min) |
| Playwright Firefox desktop 1600×900 | atlas, ciudades y accesibilidad | **11/11 pass** (23,9 s) |
| Playwright Chromium 1920×1080 emulado | atlas y accesibilidad | **7/7 pass** (1,3 min) |
| Accesibilidad | panel, estados ARIA, movimiento reducido y fallo de GLB | **3/3 pass** en Chromium y Firefox |
| `qa:playwright:chromium` | rutas, LOD0/LOD1, flags, kiosco, offline y capturas | **32/32 pass** |
| `lazy-viewer.spec.js` | catálogo sin visor, ciudad con visor y fallo de chunk | **2/2 pass** en Chromium y Firefox |

La prueba de fallo bloquea `**/cities/caral/*.glb` con `?nosw=1` y verifica el estado recuperable. La prueba de lazy-load comprueba que `/` no solicita el chunk `viewer-*.js`, que una ciudad sí lo carga y que un fallo del chunk muestra el estado recuperable.

**Nota de regresión:** en la pasada posterior al lazy-load, 15/16 pruebas de ciudad/LOD/offline pasaron. Chavín LOD0 agotó 20 s en un clic de parada y pasó aislado en 4,6 min. Se registra como flake de SwiftShader; no se cambió código por ese evento.

## Límites

- **Móvil real:** no probado; no hay dispositivo. Los estados `qa: partial` y `qa: waived` no cambian.
- **1080p real:** no certificado; la prueba a 1920×1080 es emulación de viewport, no hardware.
- **Kiosco físico:** no probado; solo se verificó la clase/ruta `?kiosk=1` en Chromium.
- **Caral Android P2:** `CARAL-ANDROID-GROUND-001` sigue abierto; no se puede aislar sin dispositivo.
- **WebKit:** no ejecutado; faltan dependencias del host.
- **Órbita/zoom 3D:** sigue siendo pointer-only; las paradas, capas y horas tienen controles accesibles equivalentes, pero no hay navegación de cámara por teclado.
- **Chunk del visor:** el catálogo ya no descarga Three.js/CityViewer. El bundle inicial bajó de 676,13 kB a 25,18 kB (8,93 kB gzip); el visor se carga bajo demanda en un chunk de 652,21 kB (167,98 kB gzip). El aviso de Vite persiste para ese chunk diferido y queda documentado, sin ocultarlo con `chunkSizeWarningLimit`.

## Criterio

Esta pasada **no eleva** ninguna ciudad a `qa: passed`. Solo cierra deuda de accesibilidad, recuperación y consistencia documental verificable en escritorio. La matriz móvil/1080p/kiosco sigue pendiente y debe declararse como tal.
