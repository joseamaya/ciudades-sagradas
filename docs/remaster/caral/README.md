# Remaster de Caral

Rama: `feat/caral-remaster-phase-2`. El piloto actual sigue vivo en `main` hasta que el remaster pase QA.

Estado: materiales procedurales aplicados a arquitectura, plazas y suelo; visor alineado con AgX/PMREM, cámara sur, recorrido revisado y QA móvil/kiosco; terreno v1 con arena macro; falta roca/vegetación, hardware real y bake.

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

## Criterios de aceptación

- La Pirámide Mayor y las plazas coinciden con los planos y la escala.
- Piedra, revoque, terreno y vegetación se leen en primer plano.
- No hay cerámica, metales, rueda, llamas ni imaginería inca.
- Techos y elementos no documentados están marcados como inferidos.
- GLB <25 MB, LOD0 150k–250k tris, LOD1 50k–80k, <100 draw calls.
- 60 fps a 1080p en GPU media; offline y kiosco funcionando.
- Manifiesto, créditos, capturas y caché actualizados.
