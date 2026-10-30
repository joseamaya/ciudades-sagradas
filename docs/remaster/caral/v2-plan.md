> **Documento histórico.** Las referencias a `stage` y a la caché `v7` corresponden al release de Caral v2. El esquema vigente usa `maturity`/`version` y la caché global `v36`.

# Caral remaster v2 — plan y Fases A–D web

Fecha: 26 de octubre de 2026. Rama de cierre: `release/caral-v2`, desde `a76fc8b`.

**Estado:** Fases A–D web completadas y desplegadas. LOD0 de **230.800 tris / 44 draw calls** y LOD1 de **56.332 tris / 31 draw calls** en régimen estable, ambos con Draco. Los GLB `model_lod0.glb` y `model_lod1.glb` están integrados en `public/`, con `model.glb` v1 como fallback. PR #5 mergeado en `a76fc8b`; `stage: "v2"` y caché `v7`. Kiosco, hardware de museo y escala métrica 1.0 quedan congelados. Cierre y métricas en `auditoria-v2.md`.

## Objetivo v2

- High-poly solo del hero: Pirámide Mayor, Plaza Mayor, Anfiteatro y Altar Circular.
- **LOD0:** high-poly del hero + resto de v1; 150.000–250.000 tris.
- **LOD1:** geometría v1 actual; 50.000–80.000 tris, con base color y normal del high-poly horneados al hero mediante atlas UV. Roughness constante 0,85 y AO no incluido.
- LOD0 y LOD1 en archivos separados; selección automática en el visor y override `?lod=0/1`.
- Fusión por capa+material, capa en `extras`; LOD1 y LOD0 <100 draw calls en régimen estable.
- Sin texturas de IA. Solo web; kiosco y hardware de museo quedan congelados.

## 1. Expediente UNESCO 1269 verificado

Fuente primaria: [Nomination file 1269](https://whc.unesco.org/uploads/nominations/1269.pdf), consultada en línea el 26 de octubre de 2026. PDF de 429 páginas y 46.766.791 bytes. No se copian sus imágenes al repositorio.

| Elemento | Evidencia y página PDF | Dimensión/documentación | Estado | Lectura para el modelo |
|---|---|---|---|---|
| Plano general | p. 349, Fig. 1 | Plano de la Ciudad Sagrada de Caral, sectores y curvas | Documentado | Referencia espacial general |
| Pirámide Mayor | pp. 350–351, Fig. 2 y texto | 149,69 m N–S × 170,80 m E–O; altura 19,27 m al sur y 29,88 m al norte; siete plataformas | Documentado | Usar 170,80 × 149,69 m y 29,88 m como núcleo |
| Plaza circular de la Mayor | p. 351 | Diámetro externo 36,5 m; interno 21,5 m; plataforma de 7 m; muros internos de 3 m y externos de 1–1,6 m | Documentado | La plaza v1 ya coincide en 36,5/21,5 m |
| Técnica y revoques | pp. 350–352 | Piedra con argamasa, revoques blanco/amarillo/rojo y uso masivo de shicras en rellenos/enterramientos | Documentado | Hiladas y colores sí; disposición de cada piedra es inferida |
| Anfiteatro | p. 358, Fig. 10 | Plaza circular hundida más grande, dos escalinatas, dos plataformas concéntricas y 20 cubículos | Documentado | No hay dimensión global métrica en el texto; no inventar una corrección de escala |
| Altar Circular | p. 359, Fig. 11 | Altar de 2,7 m de diámetro medio; paredes conservadas de 1,5 m y originales estimadas de 2 m | Documentado | Corregido en Fase B: anillo de 2,7 m y pared de 1,5 m; aro v1 de 8 m oculto |
| Erosión y cortes visibles | Interpretación de la evidencia material | Patrón concreto de pérdida de revoque, desportillado y shicras expuestas | Interpretativo/inferido | Se documenta como reconstrucción artística, no como registro exacto |

Las figuras 2–16 están en pp. 350–365; las páginas 366–370 continúan el expediente gráfico/contextual. La antigua cifra del plan, **150 × 110 × 28 m**, procede de fuentes secundarias y queda sustituida por la medida primaria del expediente.

## 2. Decisión de escala: no rescalado global

El núcleo v1 ya coincide con UNESCO:

- `GEO-Caral_PyramideMayor_Terrace_01`: **170,80 × 149,69 m**.
- Siete terrazas de 4,269 m: **29,883 m**, equivalente a 29,88 m.
- La caja completa v1, **173,8 × 159,19 × 32,68 m**, incluye el zócalo, la prolongación de la escalera y los recintos/cubiertas de la cima. No es una escala global incorrecta.

Por tanto, **no se aplicó ningún factor de escala**. Se corrigieron `docs/fuentes/caral.md`, `plan.md` y `referencias.md` para eliminar el objetivo secundario de 150 × 110 × 28 m.

La altura desigual documentada —19,27 m al sur y 29,88 m al norte— queda anotada para una futura revisión de topografía/perfil; no se inventó una corrección sin plano de sección o DEM.

### Decisión para el visor web

`city.json` aplica `scale: 0.08` a un modelo cuya escena ya está en metros. Se conserva como **diorama web**: la ciudad se lee completa y las figuras humanas funcionan como referencia, no como recorrido a escala real. La escala 1.0 y la recalibración de cámaras quedan fuera de esta entrega y del kiosco congelado.

## 3. Escena y high-poly del hero

Archivo de trabajo: `blender/caral/caral_remaster_v2.blend`.

- Tamaño: **6.755.204 bytes**.
- SHA-256: `386cc18bb141d167801157b4fa05bc16dd79ab86c4ac6ce24b19249522ae85d1`.
- La fuente `caral_remaster.blend` permanece intacta con SHA-256 `52d79bb5db315fcc22f703665d6dc39f49d9bc9be7b729f93800face301d1f5f`.
- Scripts reproducibles: `scripts/build_caral_highpoly_mayor.py` (semilla 1269) y `scripts/build_caral_highpoly_hero.py` (semilla 1270, Fase B).
- `COL-Caral_HighPoly` contiene `..._Mayor`, `..._PlazaMayor`, `..._Anfiteatro` y `..._AltarCircular`, visibles.
- `COL-Caral_LowPoly` conserva la geometría v1 de las cuatro zonas, oculta por defecto para alternar LOD/bake.
- **119 mallas high-poly** en total: 73 del Mayor y 46 nuevas de Fase B.
- Objetos con `layer="city"`, `sublayer`, `lod`, `units`, `source` y `evidence` listos para futuros `extras`.

El prototipo contiene:

- 1.782 piedras de fachada en 28 paños, con hiladas, juntas, aparejo escalonado, huecos y profundidad variable.
- 196 sillares de esquina en las siete terrazas.
- Siete tramos de escalera reconstruidos con 16 peldaños por tramo y 336 piedras de arista/huella.
- Diez shicras con piedras en un corte de la fachada sur; su presencia en rellenos está documentada, el corte concreto es inferido.
- Mortero en nichos de erosión y una variante de piedra meteorizada usando materiales existentes.
- Sin imágenes nuevas ni texturas de IA. Solo se añadió `MAT-Caral_Remaster_Mortar`, material de color/roughness sin imagen.
- UVMap en todas las mallas high-poly.

### Fase B — Plaza Mayor, Anfiteatro y Altar Circular

- **Plaza Mayor:** anillo reconstruido a 128 segmentos, banda roja, cornisa, zócalo, aro de fogón, tres escaleras con peldaños y parches de piedra/mortero en los muros interno y externo. Se conservan 36,5 m externos y 21,5 m internos.
- **Anfiteatro:** anillo de 128 segmentos, tres graderías semicirculares de 72 segmentos con narices de piedra, parches en el muro circular, terrazas del templo, zócalo, cornisas y escalinatas. Se mantuvo la planta v1 y no se inventó una dimensión global.
- **Altar Circular:** el aro v1 de 8 m quedó oculto y se modeló el altar documentado de **2,7 m de diámetro**, con pared de 1,5 m, remate de piedra y fogón de 0,82 m. La terraza, el recinto de cima y las escaleras se detallaron con hiladas y esquinas.
- El patrón de erosión, los cortes y la posición exacta de cada piedra son **inferidos/interpretativos**; las dimensiones principales son documentadas.
- **No se modelaron los 20 cubículos del Anfiteatro**: el expediente los menciona, pero no ofrece una planta suficiente para distribuirlos sin inventar. Quedan como pendiente documentado.

## 4. Medición de triángulos

Cómputo con mallas evaluadas, equivalente al exportador con modificadores aplicados.

| Métrica | Antes / LOD1 v1 | Después / LOD0 v2 |
|---|---:|---:|
| Total de la ciudad | 55.944 tris | **230.800 tris** |
| Pirámide Mayor | 6.484 tris / 102 objetos | **114.176 tris / 73 objetos** |
| Plaza Mayor | 8.096 tris / 17 objetos | **19.736 tris / 18 objetos** |
| Anfiteatro | 5.996 tris / 19 objetos | **46.040 tris / 18 objetos** |
| Altar Circular | 1.308 tris / 8 objetos | **16.788 tris / 10 objetos** |
| Resto de la ciudad | 34.060 tris | Sin cambios |
| Hero high-poly | — | **196.740 tris / 119 mallas** |
| Caja completa del Mayor | 173,8 × 159,19 × 32,68 m | **173,8 × 159,202 × 32,701 m** |
| Imágenes nuevas | — | **0** |

El cálculo es `34.060 + 196.740 = 230.800` tris. La Fase B añade **82.564 tris** de high-poly nuevo y retira 15.400 tris de hero v1, con un incremento neto de **67.164 tris**. Queda un margen de **19.200 tris** hasta el máximo de 250.000. El objetivo de 40.000–70.000 tris adicionales se cumplió en 67.164.

### LOD0/LOD1 integrados (Fases C–D)

| Métrica | LOD0 | LOD1 |
|---|---:|---:|
| Triángulos | **230.800** | **56.332** |
| Mallas en Blender | **10** (4 high-poly + 6 infra) | **15** (9 baked + 6 infra) |
| Primitivas en Three.js | **65** | **38** |
| Materiales / imágenes | **21 / 31** | **23 / 39** |
| GLB en `public/` | **3.277.080 bytes** | **1.345.092 bytes** |
| Draw calls en régimen estable | **44** | **31** |
| Capas | city, terrain, props, reference | city, terrain, props, reference |

El LOD1 conserva la geometría v1 y añade un atlas horneado por región con base color y normal del high-poly, exportado a 1K. La roughness se fija en **0,85** (sin mapa) y la normal se conecta a **0,35**. El AO no se conecta ni se incluye en el GLB. La infraestructura se fusionó en seis mallas por grupo; el LOD0 fusiona además el high-poly por región. Los draw calls bajaron de **1.507 a 44** en LOD0 y de **1.177 a 31** en LOD1 (cámara inicial, sombras cacheadas).

## 5. Renders antes/después

Mismas cámaras, iluminación y ajustes en cada par. EEVEE, 1600 × 900, 64 muestras, AgX.

| Vista | Antes | Después |
|---|---|---|
| Mayor y Plaza Circular, 3/4 suroeste | `v2-before-mayor.jpg` | `v2-after-mayor.jpg` |
| Detalle de fachada y shicras del Mayor | `v2-before-detail.jpg` | `v2-after-detail.jpg` |
| Plaza Mayor, 3/4 suroeste | `v2-before-plaza.jpg` | `v2-after-plaza.jpg` |
| Anfiteatro, 3/4 suroeste | `v2-before-anfiteatro.jpg` | `v2-after-anfiteatro.jpg` |
| Altar Circular, 3/4 suroeste | `v2-before-altar.jpg` | `v2-after-altar.jpg` |
| Detalle del anillo de la Plaza Mayor | — | `v2-after-plaza-detail.jpg` |
| Detalle del altar de 2,7 m | — | `v2-after-altar-detail.jpg` |

Se verificaron visualmente las hiladas, juntas, erosión, esquinas, peldaños, graderías, shicras y el altar de 2,7 m. Las imágenes son renders propios, no material de UNESCO. El script de renders es `scripts/render_caral_v2_phase_b.py`.

### QA web integrada

Los GLB `model_lod0.glb` y `model_lod1.glb` se copiaron a `public/cities/caral/`; `model.glb` v1 queda intacto como rollback. `city.json` declara `lod.levels` 0/1, `fallbackModel` v1 y `stage: "v2"`. El visor usa LOD0 en escritorio y LOD1 en móvil/táctil, con override `?lod=0/1`.

- LOD0: **3.277.080 bytes**, 10 mallas, 65 primitivas, 230.800 tris, 21 materiales, 31 imágenes, **44 draw calls**; Draco + WebP.
- LOD1: **1.345.092 bytes**, 15 mallas, 38 primitivas, 56.332 tris, 23 materiales, 39 imágenes 1K, **31 draw calls**; Draco + WebP.
- Capas verificadas en ambos LOD: `city`, `terrain`, `props` y `reference`; los toggles ocultan sus grupos.
- Fallback verificado: al bloquear `model_lod0.glb`, el visor carga LOD1.
- Tour de **6 paradas** con Altar Circular; cámara y texto verificados.
- Capturas: `web-lod0.png`, `web-lod1.png`, `web-altar.png` y portada `hero.jpg` regenerada desde el visor v2.
- Caché de servicio actualizada a **v7**; el preview temporal de `/tmp` ya no es necesario.
- Promovido a `stage: "v2"`, PR #5 mergeado y desplegado en GitHub Pages.
- Kiosco, hardware de museo y escala métrica 1.0 no forman parte de esta entrega.

## 6. Fases

### Fase B — completada

1. Plaza Mayor high-poly con 36,5/21,5 m, banda roja, cornisa, zócalo y escaleras.
2. Anfiteatro high-poly con anillo, tres graderías semicirculares y templo, sin inventar una dimensión global.
3. Altar Circular corregido: anillo de **2,7 m** y paredes de **1,5 m**, no el aro v1 de 8 m.
4. LOD0 final en **230.800 tris**, dentro del rango 150.000–250.000.
5. La discrepancia norte/sur de altura del Mayor sigue pendiente de sección o topografía; no se inventó.

### Fase C — completada

- Geometría v1 + atlas UV horneado por región, exportado a 1K: Mayor, Plaza Mayor, Anfiteatro y Altar Circular. LOD1 final: **56.332 tris**, dentro de 50.000–80.000.
- Bake DIFFUSE/COLOR y NORMAL tangente desde high-poly con `cage_extrusion=0.55`, `max_ray_distance=1.0`, margen 12 px. Normal a **0,35**; roughness constante **0,85**; AO no incluido en el GLB.
- Plaza: `BandaRoja`, `PisoAnilloRojo`, `PisoRojo`, `Fogon` y `FogonAro` se mantienen separados con sus materiales originales; el piso high-poly se incluye por nombre exacto.
- Mapas en `blender/textures/baked/caral/`; blend `blender/caral/caral_lod1.blend` (SHA-256 `9da242aa0e92f7b43ffa014af7af2fe11c27c47c2d027c65cc4515244856df9a`).
- `scripts/bake_caral_lod1.py` y `scripts/optimize_caral_lod1.py` reproducen el bake y la fusión de infraestructura.
- Validado en Three.js: **31 draw calls** en producción y capas correctas; capturas `web-lod1.png`.

### Fase D — integración web (completada)

1. LOD0: high-poly fusionado por región + infraestructura en seis grupos; LOD1: infraestructura fusionada con capas `terrain`, `city`, `props` y `reference`.
2. `model_lod0.glb` (3,28 MB) y `model_lod1.glb` (1,35 MB) exportados con WebP 80 + Draco, `extras` y sin cámaras/luces.
3. Draw calls medidos en el visor real: **44 en LOD0** y **31 en LOD1** en régimen estable; ver `auditoria-v2.md`.
4. `city.json` con `lod.levels`, `fallbackModel` v1, `stage: "v2"` y parada de Altar.
5. Selección automática escritorio/móvil, override `?lod=0/1` y fallback LOD0 → LOD1 → v1 (escritorio) / LOD1 → v1 → LOD0 (móvil) verificados.
6. Escala **0,08** confirmada como diorama; la escala métrica 1.0 queda fuera de esta entrega.
7. QA web, promoción a v2, PR #5, merge y deploy completados; hardware real y kiosco congelado quedan pendientes.

## 7. Límites de esta fase

- Los LOD0/LOD1 están integrados, promovidos a `stage: "v2"` y desplegados en GitHub Pages; `model.glb` v1 sigue como fallback.
- El LOD1 no conecta AO ni mapa de roughness: usa base color + normal + roughness constante 0,85.
- La escala **0,08** se mantiene como diorama; la escala métrica 1.0 y la recalibración del visor quedan fuera de esta entrega.
- Kiosco, hardware de museo, pruebas de 8 horas y perfil LOD específico quedan congelados.
- El visor fusiona la infraestructura en grupos; no conserva la jerarquía individual de cada edificio v1 en el GLB, pero mantiene las cuatro capas.
- No se añadieron cerámica, metales, rueda, llamas, caballos ni imaginería inca.
- La distribución de piedras, el patrón de erosión y los cortes de shicras son reconstrucción inferida/interpretativa, no una afirmación arqueológica exacta.
- Los 20 cubículos del Anfiteatro no se modelaron por falta de una planta publicada suficiente; no se inventó su distribución.
- El Altar Circular usa el diámetro documentado de 2,7 m; la altura original de 2 m se estima en la fuente, por lo que la pared modelada conserva 1,5 m.
- Falta resolver la representación de la altura norte/sur del Mayor.
