# Plan de Aypate — Fase 0

Fecha: 28 de octubre de 2026.
Estado: **high-poly v0.4 y preview web; escala contrastada con el plano de 2013; QA de hardware pendiente**.

## Objetivo

Construir una reconstrucción navegable del núcleo inca de Aypate que se lea como centro administrativo-ceremonial de altura, articulado al Qhapaq Ñan y al bosque de neblina. No se modelará la totalidad de las 156–200 ha ni cada tramo de camino.

## Zonas hero

1. **Plaza Inca trapezoidal** y relación con el cerro.
2. **Ushnu** de tres plataformas.
3. **Kallanka** y su fachada de accesos.
4. **Acllawasi** y patio.
5. **Puerta monumental / acceso** y **fuente o Baño del Inca**.
6. **Andenes, Qhapaq Ñan y bosque de neblina** como contexto.

## Fuera de alcance inicial

- Reconstruir todos los recintos periféricos, colcas y kanchas sin planta.
- Inventar techos, cubiertas o alturas no conservadas.
- Copiar fotografías oficiales o el modelo de Sketchfab como asset del GLB.
- Modelar la ciudad actual de Ayabaca o el santuario del Señor Cautivo.

## Presupuesto técnico

| Elemento | Objetivo |
|---|---|
| LOD0 escritorio | 150.000–250.000 tris; actual: 209.560 |
| LOD1 móvil | 25.000–80.000 tris; actual: 30.663 |
| Draw calls | <100 en régimen estable |
| GLB | <25 MB por LOD |
| Texturas | 2K hero, 1K móvil; WebP 80 |
| Compresión | Draco en LOD0/LOD1 |
| Escala | Metros en Blender; diorama del visor a decidir en blockout |
| Capas | Arquitectura, terreno/bosque, detalles, escala humana |
| Paradas | 6 |
| Luces | Amanecer, mediodía, atardecer, noche |

## Recorrido preliminar

1. **Llegada por el Qhapaq Ñan.** Bosque de neblina, camino y control de acceso.
2. **Plaza Inca.** Lectura del conjunto y del cerro.
3. **Ushnu.** Plataformas, ritual y visibilidad.
4. **Kallanka.** Alojamiento, fachada y accesos.
5. **Acllawasi y fuente ritual.** Patio, producción y agua.
6. **Mirador del cerro.** Andenes, caminos y paisaje.

Los textos deben distinguir documentado, inferido e interpretativo; la atribución a Túpac Yupanqui se marca como reportada.

## Evidencia y licencias

- Base: Proyecto Integral Aypate (Qhapaq Ñan), Mincetur 374, Ministerio de Cultura, revista UNF y UNESCO Qhapaq Ñan.
- El modelo de la puerta monumental de Sketchfab es **CC BY**; si se integra, se registra autoría y atribución. En v0.4 se usa como referencia.
- No se copian imágenes de Qhapaq Ñan/Mincul/Mincetur.
- Sin texturas de IA; materiales procedurales o CC0.
- La planta topográfica y arquitectónica de 2013 está publicada en Campos 2017; se usa para el layout macro, sin copiar la figura ni asumir cotas finas.
- La memoria de 36 sectores y el original de alta resolución siguen pendientes para detalles.

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Planta topográfica incompleta | Trazado inventado | Gate de Fase 0; modelar solo el núcleo y marcar huecos |
| Bosque de neblina | Coste de vegetación y niebla | Fondo procedural, LOD y niebla de visor |
| Pendientes y terrazas | Escala y colisiones visuales | Blockout de terreno antes del detalle |
| Techos y alturas no conservados | Invención | No reconstruir; usar vacíos señalizados |
| Modelo escaneado aislado | Estilo y escala inconsistentes | Referencia en v0.4; integración solo con retopo y material propio |
| Licencias de imágenes | Bloqueo de publicación | Registro y renders propios |

## Gate de Fase 0

- [x] Dossier de fuentes.
- [x] Ficha de investigación en el atlas.
- [x] Alcance hero/fondo y límites.
- [x] Plano general localizado: levantamiento de 2013 publicado en Campos 2017; sirve para relaciones macro, no para cotas finas.
- [x] Layout macro cotejado con el plano de 2013; cotas finas pendientes.
- [x] Cronología y atribución revisadas con fuentes oficiales, marcando lo reportado.
- [x] Licencias: sin imágenes oficiales; Sketchfab solo referencia CC BY.
- [x] Presupuesto y recorrido aprobados para blockout.

## Siguiente

High-poly v0.4 completado con plaza, ushnu, kallanka, acllawasi, palacio, colcas, fuente, andenes y camino. Se corrigieron la terraza superior y escalinata del ushnu, el ancho de la kallanka, la meseta y las cámaras. Siguiente: QA visual, QA en hardware real y cierre de cotas finas. El layout v0.4 no es una reconstrucción histórica final.
