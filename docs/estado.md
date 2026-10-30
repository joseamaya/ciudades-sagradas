# Estado del proyecto

El estándar de ciudad publicada y la auditoría están en [`docs/estandares/ciudad.md`](./estandares/ciudad.md) y [`docs/estandares/auditoria-ciudades.md`](./estandares/auditoria-ciudades.md).

## Hecho

- Repositorio independiente con Vite + Three.js.
- OpenCode configurado con MCP de Blender y skills MIT en `.agents/skills/`.
- **Caral Remaster v2 es el estado actual y la referencia técnica del proyecto.**
- Caral v2 queda cerrada bajo el estándar de **ciudad representativa**: volúmenes y sectores principales, high-poly solo en las cuatro zonas hero. No es un inventario 1:1 de los 32 edificios públicos. Ver `docs/remaster/caral/cobertura.md`.
- Chavín Fase 0 cerrada, **blockout v0.5 aceptado**, **texturizado UV v0.2** de la mampostería ashlar y **Portada de las Falcónidas v0.2 aceptada como base**: columnas de 2,30 m, jambas trilíticas, friso de 6,48 m partido en dos, ocho perfiles de falcónidas, relieves interpretativos y un escalón de acceso inferido. **Preview web v0.2 con pase high-poly v0.6**: LOD0 de 249.990 tris / 1.962.740 B y LOD1 de 27.623 tris / 786.816 B, 18/15 draw calls, seis paradas, capas en extras y terreno texturizado; `stage: preview`, caché v36. La Portada usa `fov 28` en la parada 5 y fustes acanalados interpretativos. El Lanzón es una adaptación del escaneo CyArk/Google Arts & Culture (CC BY-NC-SA 4.0), con material propio y sin la textura fotográfica; el bake normal/AO se descartó por artefactos. Edificio A/B, patio de B, Plaza Circular, secuencia de galería y terreno procedural (talud, rampa, ríos). Chavín aprobado en Android con evidencia parcial; ver `docs/remaster/chavin/qa-hardware.md`.
- **Aypate** tiene preview web v0.4 con high-poly navegable: LOD0 de 209.560 tris / 2.139.720 B y LOD1 de 30.663 tris / 443.372 B, 18/16 draw calls, seis paradas y caché v27. Núcleo inca de Ayabaca, Qhapaq Ñan y bosque de neblina. El levantamiento topográfico y arquitectónico de 2013 está publicado como figura general en Campos 2017; la v0.4 conserva el layout macro y corrige escala con el plano; el cierre de cotas de conjunto está en `docs/remaster/aypate/cotas.md` y deja pendientes las cotas finas y la QA de hardware. **Narihualá** tiene preview web v0.2 interpretativo: LOD0 de 162.432 tris / 1.599.008 B y LOD1 de 29.682 tris / 441.800 B, 13/13 draw calls, seis paradas y caché v34. El montículo este y la capilla se apoyan en SIGRID 2018; el montículo oeste, la plaza de 60 × 40 m y los accesos son inferencias documentadas; las rampas no se modelan por falta de cotas y se sustituyen por escalinatas apoyadas. No se asigna la sectorización I–III y no se declara cierre de cotas. Dossieres en `docs/fuentes/aypate.md` y `docs/fuentes/narihuala.md`; planes en `docs/remaster/aypate/` y `docs/remaster/narihuala/`.
- LOD0 high-poly: 230.800 tris, 65 primitivas, 21 materiales, 31 imágenes, **3.277.080 bytes** con Draco.
- LOD1 horneado: 56.332 tris, 38 primitivas, 23 materiales, 39 imágenes 1K, **1.345.092 bytes** con Draco.
- Fallback v1: 55.944 tris, 554 primitivas, 20 materiales, 31 imágenes, 4.778.308 bytes.
- Selección automática LOD0/LOD1 por capacidad, override `?lod=0/1` y orden de fallback específico por dispositivo.
- Ciclo de sombras estático: la shadow map se actualiza al cargar, cambiar hora o capas, no en cada frame.
- Selección de materiales: culling en superficies sólidas, doble cara solo en vegetación/totora/algodón/agua/fuego; agua sin `KHR_materials_transmission`.
- Cielos y entornos PMREM cacheados por hora del día.
- Seis paradas de recorrido, cuatro capas, cuatro momentos de luz y audio ambiental procedural.
- PWA con caché offline del modelo cargado; sin precarga forzada del fallback v1.
- Manifiesto PWA `standalone`/`any`, iconos 192/512 y safe-area en móvil.
- Modo kiosco `?kiosk=1` (congelado) y `?debug=1` con métricas en vivo.
- Benchmark reproducible `scripts/bench.mjs` (Chrome/CDP + SwiftShader) para LOD0, LOD1, móvil, fallback y offline.
- Validación ampliada: cabecera GLB, LOD/cámaras/capas, hashes y tamaños del registro de assets, versión de caché.
- Dossieres de fuentes, registro de assets y política de licencias.
- Piloto histórico con texturas de IA **retirado del repositorio**; los GLB publicados no contienen texturas de IA.
- CI y GitHub Pages en verde; auditoría y fase VRAM LOD1 desplegadas.
- Parche v2.0.1: scroll del panel móvil corregido y mitigación del plano de arena (polygonOffset, `near=0.5`, plano en `-0.36`). El parpadeo **persiste en Android**; queda como incidencia P2 documentada en `docs/remaster/caral/incidencias.md`.

## Métricas medidas

| Elemento | LOD0 | LOD1 | v1 fallback |
|---|---:|---:|---:|
| Triángulos | 230.800 | 56.332 | 55.944 |
| Primitivas Three.js | 65 | 38 | 554 |
| Draw calls en régimen estable* | 44 | 31 | 342 |
| GLB con Draco | 3.277.080 B | 1.345.092 B | 4.778.308 B (sin Draco) |
| Materiales / imágenes | 21 / 31 | 23 / 39 | 20 / 31 |
| Texturas decodificadas estimadas** | 373 MB | 208 MB | 373 MB |
| Shadow map | 2048² escritorio | 1024² móvil | 2048² escritorio |

\* Cámara inicial, 1600×900, Chrome headless/SwiftShader; las sombras ya están cacheadas y no hay pasada de transmisión. Al refrescar sombras se suman los casters: **100 draw calls** en LOD0 y **60** en LOD1, solo en el frame de actualización.
\** Estimación RGBA8 + mipmaps de las texturas del modelo; no es el peso de descarga.

- La carga local terminó en ~1,2–1,7 s de respuesta de red y ~6–7 s hasta el primer render en SwiftShader; en GPU real el primer render baja de forma importante. El dato de FPS de SwiftShader no representa hardware real.
- `npm run validate` y `npm run build`: OK.
- Fallback verificado: LOD0 → LOD1 → v1 en escritorio; LOD1 → v1 → LOD0 en móvil.
- Offline verificado con caché `v36` y `?nosw=1` como escape de QA.

## Pendiente

1. **Caral**: QA en hardware real (iPhone/Safari, Android/Chrome, GPU media) y medición de 60 fps a 1080p. El kiosco y el hardware de museo siguen congelados.
2. **Incidencia Android P2**: parpadeo de suelo en `CARAL-ANDROID-GROUND-001`; falta aislar con `?noground=1`/`?noshadows=1` y datos del dispositivo. No bloquea Chavín.
3. **QA de hardware real**: falta medir FPS/frame time en iPhone/Safari, Android/Chrome y GPU media. KTX2/BasisU queda como mejora futura de VRAM.
4. **Contenido**: 20 cubículos del Anfiteatro y perfil norte/sur del Mayor, limitados por fuentes y diferidos.
5. **Narración en español**: guion y grabación; congelada junto con el kiosco.
6. **Renders cinematográficos**: Cycles con los assets high-poly.
7. **Publicación**: mantener GitHub Pages actualizado y evaluar Cloudflare Pages para assets grandes.

## Limitaciones conocidas

- Caral v2 está publicado; `model.glb` v1 se conserva como fallback y rollback, pero tiene 342 draw calls en la vista inicial y ~782 al refrescar sombras.
- LOD1 no conecta AO ni mapa de roughness: usa base color, normal, roughness constante 0,85 y normal 0,35. El AO no está incluido en los GLB.
- LOD1 usa texturas 1K y ~208 MB estimados de VRAM; sigue por encima de un LOD ideal, pero ya no duplica la VRAM de LOD0.
- La escala **0,08** está validada como diorama web; la escala métrica 1.0 queda fuera de esta entrega.
- No se implementó LOD dinámico por distancia: la selección es por dispositivo/capacidad.
- No se modelaron los 20 cubículos del Anfiteatro por falta de una planta publicada suficiente.
- La diferencia de altura norte/sur del Mayor sigue pendiente de sección o DEM.
- No hay 32/32 edificios públicos individuales de alta fidelidad: la cobertura es representativa y varios sectores están agregados. Ver `docs/remaster/caral/cobertura.md`.
- El parpadeo de suelo en Android persiste en v2.0.1; es una incidencia P2 abierta, no un fallo resuelto.
- La reexportación de v1 con WebP no es byte-a-byte determinista: mismo tamaño y estructura, hash distinto. El GLB v1 publicado es la referencia.
- Wari no está en la Lista del Patrimonio Mundial; su ficha se basa en Ministerio de Cultura y academia.

## Próximo paso recomendado

Revisar la QA de Aypate v0.4 en hardware real y cerrar las cotas finas que falten. Cerrar las cotas finas de Narihualá con un plano arqueológico o levantamiento propio; el preview v0.2 ya está publicado como interpretativo. Documentar y aceptar la incidencia Android P2; no bloquear el cierre de contenido. Chavín ya tiene un preview web v0.2 con pase high-poly v0.6, LOD0/LOD1, seis paradas, el Lanzón escaneado y la Portada legible; el siguiente hito es QA en hardware real, decidir dintel/escalera y revisar la licencia CC BY-NC-SA 4.0 antes de cualquier uso comercial. El terreno se queda procedural por ahora. KTX2/BasisU sigue como mejora opcional si 208 MB de VRAM no bastan.
