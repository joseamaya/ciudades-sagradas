> **Documento histórico.** Las referencias a `stage` y a la caché `v7` corresponden al release de Caral v2. El esquema vigente usa `maturity`/`version` y la caché global `v36`.

# Plan de remaster de Caral

## Estado 2026-10-26

- **v2 completado y desplegado** en GitHub Pages; `stage: "v2"` y caché `v7`.
- LOD0: 230.800 tris / 3,28 MB con Draco / 44 draw calls en régimen estable.
- LOD1: 56.332 tris / 1,35 MB con Draco / 31 draw calls; atlas exportado a 1K, roughness 0,85 y normal 0,35.
- Fallback v1 (`model.glb`) intacto; seis paradas; portada v2.
- PR #5 mergeado (`a76fc8b`); release web en `release-v2.md`.
- Escala 0,08 validada como diorama web.
- Kiosco, hardware de museo y escala 1.0: congelados.
- Pendiente de contenido: 20 cubículos del Anfiteatro y perfil norte/sur del Mayor, ambos limitados por fuentes y diferidos.
- Cierre de contenido bajo el estándar de **ciudad representativa**; cobertura en `cobertura.md`.
- Incidencia Android P2 de parpadeo de suelo documentada en `incidencias.md`; no bloquea el cierre.

## Fase 0 — Auditoría y referencia

- [x] Auditar la escena y generar `auditoria.json`.
- [x] Corregir rutas de texturas y excluir colecciones de juego del export.
- [x] Confirmar que el GLB publicado se reproduce con `export.py`.
- [x] Recopilar planos y referencias públicas; expediente UNESCO 1269 verificado.
- [x] Fijar dimensiones y niveles de la Pirámide Mayor, Plaza Mayor, Anfiteatro y Altar Circular.
- [ ] Crear tablero de referencias con estado de evidencia.

## Fase 1 — Blockout y terreno

- [x] Verificar escala, origen y unidades; visor en diorama 0,08.
- [x] Separar terreno, arquitectura, props y referencia.
- [x] Modelar terraza, valle, río, campos y accesos.
- [x] Primer pase de colinas con subdivisión y desplazamiento procedural (ver `terrain.md`).
- [x] Verificar la Pirámide Mayor contra UNESCO 1269: núcleo 170,80 × 149,69 m y 29,88 m al norte; no rescalado global en v2 (p. 351).
- [x] Definir encuadre hero y portada v2 desde el visor.

## Fase 2 — Arquitectura high-poly

- [x] Muros con hiladas, juntas, erosión y esquinas.
- [x] Escaleras, atrios, recintos y plataformas.
- [x] Revoques blanco, amarillo y rojo; zonas erosionadas.
- [x] Shicras en cortes y rellenos.
- [x] Techos de caña/madera/totora donde correspondan.
- [x] Plazas circulares, altar y huellas de fuego.
- [x] Anfiteatro y Altar Circular.

## Fase 3 — Materiales

- [x] Revoque blanco/amarillo/rojo, piedra cortada, piedra irregular, arena y suelo con texturas procedurales.
- [x] Densidad de texel uniforme verificada en la Pirámide Mayor (1/16 UV por metro).
- [x] Biblioteca PBR procedural completa (madera, totora, vegetación).
- [x] UVs y atlas horneado por región; exportado a 1K.
- [x] Normales horneadas; AO no incluido en LOD1.
- [x] Eliminar texturas de IA del remaster v1 y v2.

## Fase 4 — Ambiente

- [x] Terreno con erosión, rocas, arena y grava.
- [x] Vegetación instanciada con viento suave.
- [x] Campos y canales legibles.
- [x] Figuras humanas simples de 1,6–1,8 m.
- [x] Iluminación de amanecer/atardecer, sombras y polvo.

## Fase 5 — Bake, LOD y export

- [x] High-poly → low-poly con normales/AO.
- [x] LOD0 150k–250k tris; 230.800.
- [x] LOD1 50k–80k tris; 56.332.
- [x] Fusionar por capa/material; LOD0/LOD1 con sombras estáticas y sin transmisión.
- [x] WebP 80 + Draco; LOD0 3,28 MB y LOD1 1,35 MB.
- [x] Validar UVs, normales, materiales y escala.

## Fase 6 — Visor

- [x] Actualizar cámaras, recorrido y capas; seis paradas.
- [x] Añadir LOD y selección automática.
- [x] Iluminación y cámara inicial alineadas; encuadre hero y stops revisados.
- [x] Actualizar `city.json`, README, manifiesto y créditos.
- [x] Subir la versión de caché de `public/sw.js` a `v7`.
- [x] Probar escritorio, móvil emulado y offline; kiosco congelado.

## Fase 7 — QA y publicación

- [x] Comparar contra referencias y contra el piloto (retirado).
- [ ] Revisar rendimiento en GPU real y dispositivos físicos (parcial: Android con incidencia P2).
- [x] Capturas nuevas y portada v2.
- [x] Commit, PR #5, merge y deploy.
- [x] Retirar la etiqueta “piloto”; Caral queda como “Remaster v2”.

## Cierre de contenido

- [x] Definir el estándar de ciudad representativa.
- [x] Documentar cobertura por elemento y nivel de detalle.
- [x] Aceptar la incidencia Android P2 y enlazarla al release.
- [x] Diferir 20 cubículos, perfil N/S, high-poly de pirámides secundarias y 32/32 individual.
- [x] No planificar v3 sin una decisión de producto y fuentes nuevas.

## Presupuesto

| Elemento | Objetivo |
|---|---|
| GLB | <25 MB |
| LOD0 | 150k–250k tris |
| LOD1 | 50k–80k tris |
| Draw calls | LOD1 <100; LOD0 <100 en régimen estable |
| Texturas | 2K héroes, 1K fondo |
| FPS | 60 a 1080p en GPU media; pendiente de hardware real |
| Kiosco | Congelado |
