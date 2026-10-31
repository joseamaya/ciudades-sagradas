# Remaster de Caral

Rama de cierre: `release/caral-v2`. Remaster v1: `release/caral-remaster-final`.

Estado: **remaster v2 desplegado y contenido cerrado** en GitHub Pages bajo el estándar de ciudad representativa; LOD0 de 230.800 tris y LOD1 de 56.332 tris, ambos con Draco y WebP. Los GLB LOD0/LOD1 y `city.json` están integrados en `public/`, con v1 como fallback. PR #5 mergeado en `a76fc8b`; `maturity: "released"`, `version: "v2"` y caché global `v38`. Queda una incidencia Android P2 de parpadeo de suelo. Kiosco, hardware y escala métrica 1.0 quedan congelados.

## Decisiones fijadas

- **Alcance inicial:** vertical slice — Pirámide Mayor, Plaza Mayor, Plaza Circular, Anfiteatro, Altar Circular, terraza y valle.
- **Estándar de cierre:** ciudad representativa; no inventario 1:1 de los 32 edificios públicos. High-poly solo en las cuatro zonas hero.
- **Texturas:** CC0 o procedurales; sin nuevas texturas de IA.
- **Publicación:** v2 reemplaza al piloto; `model.glb` v1 se conserva como fallback y rollback. El piloto con texturas de IA fue retirado.
- **Interiores:** solo lo visible desde plazas y altares; no galerías completas.
- **Hero shot:** Pirámide Mayor + Plaza Circular; portada v2 capturada desde el visor.

## Estado de partida

- 578 objetos, 557 mallas, 47.322 tris base, 33 materiales, 42 imágenes.
- 247 modificadores Bevel.
- GLB del piloto (histórico): 554 mallas, 23 materiales, 44.640 tris, 20,7 MB. Retirado del repo.
- Texturas de escena: 38 de 512 px y 23 de 1024 px.
- 2 mallas sin UV: `GEO-Caral_ScenarioCity_LOD0/LOD1`, que no pertenecen a la escena publicada.
- El exportador ya excluye las colecciones de juego.

## Archivos

- `auditoria.json`: inventario completo de la escena.
- `auditoria.md`: resumen legible.
- `plan.md`: fases, tareas y criterios de aceptación.
- `referencias.md`: fuentes y material de referencia pendiente.
- `terrain.md`: primer pase de terreno y capturas antes/después.
- `materials.md`: pase procedural, corrección del banding, mapeo y GLB de prueba.
- `viewer.md`: alineación de cámara, AgX, PMREM y capturas antes/después.
- `release-v1.md`: remaster v1 histórico, metadatos, caché v3 y QA offline.
- `release-v2.md`: release web de Caral v2, métricas, QA, fallback y límites.
- `licencias-assets.md`: auditoría de los GLB v1 y v2, sin texturas de IA.
- `v2-plan.md`: evidencia UNESCO, decisión de escala, high-poly, LOD0/LOD1, métricas y fases v2.
- `auditoria-v2.md`: auditoría de cierre, rendimiento medido, LOD, problemas y veredicto.
- `qa-hardware.md`: protocolo y matriz de QA en dispositivos reales.
- `cobertura.md`: qué elementos están en el GLB, con qué nivel de detalle y qué queda diferido.
- `incidencias.md`: incidencias conocidas; incluye el parpadeo de suelo Android P2.
- `plantilla.md`: checklist para reutilizar Caral v2 en la siguiente ciudad.
- `v2-before-*.jpg` / `v2-after-*.jpg`: comparativas del Mayor, Plaza Mayor, Anfiteatro y Altar Circular.
- `lod1-general.png`, `lod1-plaza.png`, `lod1-anfiteatro.png`, `lod1-altar.png`: capturas históricas del preview LOD1.
- `web-lod0.png`, `web-lod1.png`, `web-altar.png`: capturas del visor real en `public/`.
- `../../../scripts/build_caral_highpoly_mayor.py` y `build_caral_highpoly_hero.py`: generadores reproducibles del high-poly.
- `../../../scripts/render_caral_v2_phase_b.py`: renders comparativos de la Fase B.
- `../../../scripts/bake_caral_lod1.py`: bake del LOD1 por región; el GLB se exporta con texturas 1K.
- `../../../scripts/assemble_caral_lod0.py`: ensamblado del LOD0 por región high-poly + infraestructura.
- `../../../scripts/optimize_caral_lod1.py`: fusión de la infraestructura LOD1 en seis mallas y capas.
- `../../../scripts/export_caral_lod.py`: exportador común LOD0/LOD1 con WebP 80, Draco, `extras` y `--max-texture-size 1024` para LOD1.

## Criterios de aceptación

- La Pirámide Mayor y las plazas coinciden con los planos y la escala.
- Piedra, revoque, terreno y vegetación se leen en primer plano.
- No hay cerámica, metales, rueda, llamas ni imaginería inca.
- Techos y elementos no documentados están marcados como inferidos.
- GLB <25 MB, LOD0 150k–250k tris, LOD1 50k–80k. Con sombras estáticas y sin transmisión: **44 draw calls** LOD0 y **31** LOD1 en la cámara inicial; al refrescar sombras se suman los casters.
- 60 fps a 1080p en GPU media: pendiente de hardware real. Offline web verificado; kiosco congelado.
- Escala **0,08** confirmada como diorama; 1.0 métrico fuera de esta entrega.
- Manifiesto, créditos, capturas y portada actualizados; la caché global vigente es `v38`.
- Cobertura de ciudad representativa documentada; 32/32 individual, 20 cubículos, perfil N/S y high-poly secundario quedan fuera de alcance o diferidos.
- Incidencia Android P2 aceptada; no se presenta v2.0.1 como suelo resuelto.
