# Plan de remaster de Caral

## Fase 0 — Auditoría y referencia

- [x] Auditar la escena y generar `auditoria.json`.
- [x] Corregir rutas de texturas y excluir colecciones de juego del export.
- [x] Confirmar que el GLB publicado se reproduce con `export.py`.
- [ ] Descargar/recopilar planos y referencias públicas.
- [ ] Fijar dimensiones y niveles de la Pirámide Mayor, Plaza Mayor y Plaza Circular.
- [ ] Crear tablero de referencias con estado de evidencia.

## Fase 1 — Blockout y terreno

- [ ] Verificar escala, origen y unidades.
- [ ] Separar terreno, arquitectura, props y referencia.
- [ ] Modelar terraza, valle, río, campos y accesos.
- [ ] Ajustar la Pirámide Mayor a ~150 × 110 × 28 m.
- [ ] Definir el encuadre hero: Mayor + Plaza Circular al atardecer.

## Fase 2 — Arquitectura high-poly

- [ ] Muros con hiladas, juntas, erosión y esquinas.
- [ ] Escaleras, atrios, recintos y plataformas.
- [ ] Revoques blanco, amarillo y rojo; zonas erosionadas.
- [ ] Shicras en cortes y rellenos.
- [ ] Techos de caña/madera/totora donde correspondan.
- [ ] Plazas circulares, altar y huellas de fuego.
- [ ] Anfiteatro y Altar Circular.

## Fase 3 — Materiales

- [ ] Biblioteca PBR CC0/procedural.
- [ ] Piedra irregular, piedra cortada, revoque, arcilla, madera, totora, arena, suelo y vegetación.
- [ ] Densidad de texel uniforme.
- [ ] UVs y atlas por región.
- [ ] Normales y AO horneados.
- [ ] Eliminar texturas de IA del preview final.

## Fase 4 — Ambiente

- [ ] Terreno con erosión, rocas, arena y grava.
- [ ] Vegetación instanciada con viento suave.
- [ ] Campos y canales legibles.
- [ ] Figuras humanas simples de 1,6–1,8 m.
- [ ] Iluminación de amanecer/atardecer, sombras y polvo.

## Fase 5 — Bake, LOD y export

- [ ] High-poly → low-poly con normales/AO.
- [ ] LOD0 150k–250k tris.
- [ ] LOD1 50k–80k tris.
- [ ] Fusionar por capa/material; <100 draw calls.
- [ ] KTX2 o WebP optimizado; GLB <25 MB.
- [ ] Validar UVs, normales, materiales y escala.

## Fase 6 — Visor

- [ ] Actualizar cámaras, recorrido y capas.
- [ ] Añadir LOD si hace falta.
- [ ] Ajustar iluminación y encuadre hero.
- [ ] Actualizar `city.json`, README, manifiesto y créditos.
- [ ] Subir la versión de caché de `public/sw.js`.
- [ ] Probar escritorio, móvil, kiosco y offline.

## Fase 7 — QA y publicación

- [ ] Comparar contra referencias y contra el piloto.
- [ ] Revisar rendimiento en GPU real.
- [ ] Capturas nuevas.
- [ ] Commit, PR, merge y deploy.
- [ ] Retirar la etiqueta “piloto” cuando corresponda.

## Presupuesto

| Elemento | Objetivo |
|---|---|
| GLB | <25 MB |
| LOD0 | 150k–250k tris |
| LOD1 | 50k–80k tris |
| Draw calls | <100 |
| Texturas | 2K héroes, 1K fondo |
| FPS | 60 a 1080p en GPU media |
| Kiosco | 1080p táctil, offline |
