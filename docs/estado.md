# Estado del proyecto

Actualizado: 31 de octubre de 2026.

El estándar de ciudad publicada está en [`docs/estandares/ciudad.md`](./estandares/ciudad.md); la auditoría en [`docs/estandares/auditoria-ciudades.md`](./estandares/auditoria-ciudades.md); el protocolo de QA en [`docs/estandares/qa-hardware.md`](./estandares/qa-hardware.md).

## Semántica de estado

Cada ciudad declara cuatro ejes independientes:

| Campo | Valores | Significado |
|---|---|---|
| `availability` | `available`, `research` | Hay modelo navegable o solo ficha documental. |
| `maturity` | `research`, `blockout`, `preview`, `released` | Grado de cierre de la ciudad. `version` indica la entrega. |
| `evidence` | `documented`, `mixed`, `interpretive`, `not-applicable` | Nivel general de evidencia de la reconstrucción. |
| `qa` | `passed`, `partial`, `pending`, `waived`, `not-applicable` | Estado de la QA en hardware real. |

Cada parada del recorrido declara además `evidence`: `documented`, `inferred` o `interpretive`. La UI lo muestra con etiquetas discretas y una leyenda.

## Estado actual

| Ciudad | Disponibilidad | Madurez | Evidencia | QA |
|---|---|---|---|---|
| Caral | `available` | `released` · v2 | Mixta | `waived` (P2 Android) |
| Chavín | `available` | `preview` · v0.3 | Mixta | `partial` |
| Aypate | `available` | `preview` · v0.4 | Mixta | `partial` |
| Narihualá | `available` | `preview` · v0.2 | Interpretativa | `partial` |
| Chan Chan | `research` | `research` | No aplica | No aplica |
| Wari | `research` | `research` | No aplica | No aplica |

## Hecho

- Repositorio independiente con Vite + Three.js.
- OpenCode configurado con MCP de Blender y skills MIT en `.agents/skills/`.
- **Caral Remaster v2** es la referencia técnica. Contenido cerrado como ciudad representativa: volúmenes y sectores principales, high-poly en Pirámide Mayor, Plaza Mayor, Anfiteatro y Altar Circular. No es un inventario 1:1 de los 32 edificios públicos.
- **Chavín** tiene preview web v0.3 con pase de valle v0.7: LOD0 de 249.942 tris y LOD1 de 42.842 tris medidos por accessors; 19/16 draw calls; seis paradas; Mosna ~30 m abajo, Wacheqsa al norte y confluencia al noreste; Lanzón derivado del escaneo CyArk/Google Arts & Culture (CC BY-NC-SA 4.0). El blockout v0.5, el texturizado UV v0.2 y la Portada v0.2 quedan como base de revisión; el terreno es procedural.
- **Aypate** tiene preview web v0.4: LOD0 de 209.560 tris y LOD1 de 30.663 tris; 17/15 draw calls; seis paradas; layout macro y escala contrastados con el plano de 2013. Cierre de cotas de conjunto documentado; cotas finas pendientes. Desktop integrado 1600×900 con LOD0/LOD1 a ~58–60 fps; QA móvil/1080p pendiente.
- **Narihualá** tiene preview interpretativo v0.2: LOD0 de 162.432 tris y LOD1 de 29.682 tris; 14/13 draw calls; seis paradas. Montículo este y capilla desde SIGRID 2018; montículo oeste, plaza y accesos inferidos; rampas documentadas no modeladas. No se asigna la sectorización I–III. Desktop integrado 1600×900 con LOD0/LOD1 a ~58–60 fps; QA móvil/1080p y plano de sectores pendientes.
- LOD0/LOD1 con Draco, override `?lod=0/1` y fallback por dispositivo. Caral conserva el fallback v1.
- Ciclo de sombras estático: la shadow map se actualiza al cargar, cambiar hora o capas, no en cada frame.
- Materiales: culling en superficies sólidas; doble cara genérica para vegetación, textiles, fuego y agua; agua sin `KHR_materials_transmission`.
- Cielos y entornos PMREM cacheados por hora del día.
- Suelo configurable por ciudad (`ground`): Caral y Narihualá conservan el plano de arena; Chavín y Aypate lo desactivan.
- Niebla configurable por ciudad (`fog`): Chavín y Aypate tienen rangos propios para el valle y el bosque de montaña.
- Capas resueltas por `extras.layer`; clasificador genérico por tokens para el fallback v1 legado. Sin nombres de ciudad en el código del visor.
- Evidencia por parada y estado general visibles en catálogo y ficha.
- PWA con caché offline del modelo cargado; sin precarga forzada de otros modelos.
- Manifiesto PWA `standalone`/`any`, iconos 192/512 y safe-area en móvil.
- Modo kiosco `?kiosk=1` y `?debug=1` con métricas en vivo e informe QA copiable (GPU, WebGL, PWA, flags y errores).
- Benchmark reproducible `scripts/bench.mjs` (Chrome/CDP + SwiftShader) para LOD0, LOD1, móvil, fallback y offline.
- Revisión Playwright en Chromium desktop/mobile y Firefox desktop: rutas, LOD0/LOD1, paradas, luces, capas, consola, offline, kiosco y selección automática de LOD. Sin errores de consola. WebKit quedó bloqueado por dependencias del host. Informe en `docs/qa/revision-playwright.md`.
- Validación ampliada: estados, evidencia, coherencia índice/ficha, cabecera y nodos GLB, capas `extras.layer`, rangos de LOD, hashes y tamaños del registro.
- Auditoría de calidad desktop del 31 de octubre de 2026: consistencia de caché `v38`, accesibilidad del panel/canvas, movimiento reducido, estado recuperable ante fallo de GLB y regresión Chromium/Firefox. Informe en [`qa/auditoria-calidad-desktop-2026-10-31.md`](./qa/auditoria-calidad-desktop-2026-10-31.md).
- CI y GitHub Pages en verde; caché global **v38**.
- Piloto histórico con texturas de IA retirado del repositorio.
- **Chan Chan** tiene un piloto solo-datos: ficha documental ampliada, cobertura por elemento y plan; sigue en `research`, sin GLB, portada, recorrido, capas ni QA. Informe en [`remaster/chan-chan/`](./remaster/chan-chan/README.md).

## Métricas comparables

| Ciudad | LOD0 tris / bytes | LOD1 tris / bytes | Draw calls LOD0/LOD1 | Paradas | Caché |
|---|---|---|---:|---:|---|
| Caral | 230.800 / 3.277.080 B | 56.332 / 1.345.092 B | 44 / 31 | 6 | v38 |
| Chavín | 249.942 / 1.741.708 B | 42.842 / 746.544 B | 19 / 16 | 6 | v38 |
| Aypate | 209.560 / 2.139.720 B | 30.663 / 443.372 B | 17 / 15 | 6 | v38 |
| Narihualá | 162.432 / 1.599.008 B | 29.682 / 441.800 B | 14 / 13 | 6 | v38 |

- Triángulos y bytes: medición de accessors GLB en `npm run validate`. Los informes de exportación pueden variar en ±1 triángulo por triangulación/degenerados; la tabla usa el conteo reproducible del validador.
- Draw calls: cámara inicial, 1600×900, Chrome headless/SwiftShader, según los informes de cada preview. No mezclar con FPS de hardware.
- Caral: LOD1 usa atlas 1K; ~208 MB de VRAM estimada. LOD0 ~373 MB. El detalle de Caral está más abajo.
- Chavín, Aypate y Narihualá usan 2K/1K según sus informes; no se declara una cifra de VRAM si no está medida.
- Última ejecución de `npm run bench` (31 de octubre de 2026): Caral 44/31, Chavín 19/16, Aypate 17/15 y Narihualá 14/13 draw calls; sin errores de consola en cargas normales. Los únicos warnings son los fallos deliberados al bloquear LOD0 para probar el fallback. Siguen siendo datos de SwiftShader, no FPS de hardware real.
- QA de hardware: desktop Intel RPL-S (Chrome 139/Linux, 1600×900) completado para Caral, Chavín, Aypate y Narihualá en LOD0/LOD1, a ~58–60 fps. Caral pasó flags, offline, standalone y sesión de 10 min con heap estable. Faltan 1080p real, Android/iPhone y kiosco. Registro en `docs/qa/resultados/desktop-2026-10-30/` y `docs/qa/resultados/chavin-v07-desktop-2026-10-31/`.

## Caral v2 — detalle

| Elemento | LOD0 | LOD1 | v1 fallback |
|---|---:|---:|---:|
| Triángulos | 230.800 | 56.332 | 55.944 |
| Primitivas Three.js | 65 | 38 | 554 |
| Draw calls en régimen estable* | 44 | 31 | 342 |
| GLB con Draco | 3.277.080 B | 1.345.092 B | 4.778.308 B (sin Draco) |
| Materiales / imágenes | 21 / 31 | 23 / 39 | 20 / 31 |
| Texturas decodificadas estimadas** | 373 MB | 208 MB | 373 MB |
| Shadow map | 2048² escritorio | 1024² móvil | 2048² escritorio |

\* Cámara inicial, 1600×900, Chrome headless/SwiftShader; sombras cacheadas. Al refrescar sombras se suman los casters: **100 draw calls** en LOD0 y **60** en LOD1, solo en el frame de actualización.
\** Estimación RGBA8 + mipmaps; no es el peso de descarga.

- La carga local terminó en ~1,2–1,7 s de respuesta de red y ~6–7 s hasta el primer render en SwiftShader; en GPU real el primer render baja de forma importante. El dato de FPS de SwiftShader no representa hardware real.
- Fallback verificado: LOD0 → LOD1 → v1 en escritorio; LOD1 → v1 → LOD0 en móvil.
- Offline verificado con caché global `v38` y `?nosw=1` como escape de QA.

## Pendiente

1. **QA de hardware real:** desktop integrado 1600×900 completado para las cuatro ciudades; 1080p, Android/iPhone, GPU dedicada y kiosco siguen pendientes. **No hay dispositivo móvil disponible**, así que móvil/1080p real quedan bloqueados por hardware y no se certifican con emulación. Ver [`qa-hardware.md`](./estandares/qa-hardware.md) y [`qa/README.md`](./qa/README.md).
2. **Caral Android P2:** `CARAL-ANDROID-GROUND-001`; falta aislar con `?noground=1`/`?noshadows=1` y datos del dispositivo. No bloquea el resto del atlas.
3. **Chavín:** QA móvil/1080p del valle v0.7, decidir dintel/escalera y revisar la licencia CC BY-NC-SA 4.0 del Lanzón antes de uso comercial.
4. **Aypate:** cotas finas y recintos periféricos; no reabrir el layout de la v0.4.
5. **Narihualá:** plano arqueológico de sectores y cotas finas; mantener el preview interpretativo.
6. **Chan Chan:** piloto solo-datos completado; no se abre geometría mientras no haya fuentes, licencias y QA suficientes.
7. **Wari:** siguiente ficha solo-datos; después se decide si alguna ciudad pasa a 3D.
8. **Kiosco y narración:** congelados hasta cerrar QA de hardware.

## Limitaciones conocidas

- Caral v2 está publicado; `model.glb` v1 se conserva como fallback y rollback, pero tiene 342 draw calls en la vista inicial y ~782 al refrescar sombras.
- LOD1 de Caral no conecta AO ni mapa de roughness: usa base color, normal, roughness constante 0,85 y normal 0,35. El AO no está incluido en los GLB.
- LOD1 de Caral usa texturas 1K y ~208 MB estimados de VRAM; sigue por encima de un LOD ideal.
- La escala **0,08** está validada como diorama web; la escala métrica 1.0 queda fuera de esta entrega.
- No se implementó LOD dinámico por distancia: la selección es por dispositivo/capacidad. No se justifica todavía.
- No se modelaron los 20 cubículos del Anfiteatro de Caral por falta de una planta publicada suficiente.
- La diferencia de altura norte/sur del Mayor sigue pendiente de sección o DEM.
- No hay 32/32 edificios públicos individuales de alta fidelidad en Caral: la cobertura es representativa.
- El parpadeo de suelo en Android persiste; es una incidencia P2 abierta, no un fallo resuelto.
- Chavín mantiene terreno procedural y la Portada conserva relieves interpretativos; no es una reconstrucción final.
- Aypate no reconstruye techos, alturas perdidas ni todos los recintos periféricos.
- Narihualá no tiene plano arqueológico de sectores; su sectorización I–III no se asigna.
- Wari no está en la Lista del Patrimonio Mundial; su ficha se basa en Ministerio de Cultura y academia.

## Próximo paso recomendado

Mantener la calidad desktop ya auditada y no abrir otra ciudad 3D mientras móvil/1080p/kiosco sigan sin evidencia. El siguiente paso de producto es **Wari como piloto solo-datos**, reutilizando el esquema de Chan Chan sin añadir geometría. No abrir una nueva ronda de geometría en Caral, Aypate, Chavín ni Chan Chan.
