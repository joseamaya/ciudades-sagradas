# Remaster de Caral

Rama técnica: `feat/caral-remaster-phase-2`. Remaster v1: `release/caral-remaster-final`. El piloto actual sigue vivo en `main` hasta el merge.

Estado: remaster v1 desplegado en GitHub Pages; v2 Fases A–D web en `feat/caral-remaster-v2` con LOD0 de 230.800 tris y LOD1 horneado de 56.332 tris. Los GLB LOD0/LOD1 y `city.json` están integrados en `public/`, con v1 como fallback. Sin PR ni deploy; kiosco, hardware y escala métrica 1.0 quedan para el final.

## Decisiones fijadas

- **Alcance inicial:** vertical slice — Pirámide Mayor, Plaza Mayor, Plaza Circular, Anfiteatro, Altar Circular, terraza y valle.
- **Texturas:** CC0 o procedurales; sin nuevas texturas de IA.
- **Publicación:** mantener el piloto live; reemplazar el GLB solo al final.
- **Interiores:** solo lo visible desde plazas y altares; no galerías completas.
- **Hero shot:** Pirámide Mayor + Plaza Circular al atardecer.

## Estado de partida

- 578 objetos, 557 mallas, 47.322 tris base, 33 materiales, 42 imágenes.
- 247 modificadores Bevel.
- GLB publicado: 554 mallas, 23 materiales, 44.640 tris, 20,7 MB.
- Texturas de escena: 38 de 512 px y 23 de 1024 px.
- 2 mallas sin UV: `GEO-Caral_ScenarioCity_LOD0/LOD1`, que no pertenecen al preview.
- El exportador ya excluye las colecciones de juego.

## Archivos

- `auditoria.json`: inventario completo de la escena.
- `auditoria.md`: resumen legible.
- `plan.md`: fases, tareas y criterios de aceptación.
- `referencias.md`: fuentes y material de referencia pendiente.
- `terrain.md`: primer pase de terreno y capturas antes/después.
- `materials.md`: pase procedural, corrección del banding, mapeo y GLB de prueba.
- `viewer.md`: alineación de cámara, AgX, PMREM y capturas antes/después.
- `release-v1.md`: remaster v1, metadatos, caché v3 y QA offline.
- `licencias-assets.md`: auditoría del GLB v1, sin texturas de IA.
- `v2-plan.md`: evidencia UNESCO, decisión de escala, high-poly, LOD0/LOD1, métricas y fases v2.
- `v2-before-*.jpg` / `v2-after-*.jpg`: comparativas del Mayor, Plaza Mayor, Anfiteatro y Altar Circular.
- `lod1-general.png`, `lod1-plaza.png`, `lod1-anfiteatro.png`, `lod1-altar.png`: capturas históricas del preview LOD1.
- `web-lod0.png`, `web-lod1.png`, `web-altar.png`: capturas del visor real en `public/`.
- `../../../scripts/build_caral_highpoly_mayor.py` y `build_caral_highpoly_hero.py`: generadores reproducibles del high-poly.
- `../../../scripts/render_caral_v2_phase_b.py`: renders comparativos de la Fase B.
- `../../../scripts/bake_caral_lod1.py`: bake del LOD1 por región y atlas 2K.
- `../../../scripts/assemble_caral_lod0.py`: ensamblado del LOD0 por región high-poly + infraestructura.
- `../../../scripts/optimize_caral_lod1.py`: fusión de la infraestructura LOD1 en seis mallas y capas.
- `../../../scripts/export_caral_lod.py`: exportador común LOD0/LOD1 con WebP 80 y `extras`.

## Criterios de aceptación

- La Pirámide Mayor y las plazas coinciden con los planos y la escala.
- Piedra, revoque, terreno y vegetación se leen en primer plano.
- No hay cerámica, metales, rueda, llamas ni imaginería inca.
- Techos y elementos no documentados están marcados como inferidos.
- GLB <25 MB, LOD0 150k–250k tris, LOD1 50k–80k. LOD1 medido en **72 draw calls**; LOD0 en **125** con sombras.
- 60 fps a 1080p en GPU media; offline y kiosco quedan pendientes de hardware real.
- Escala **0,08** confirmada como diorama; 1.0 métrico fuera de esta entrega.
- Manifiesto, créditos, capturas y caché actualizados.
