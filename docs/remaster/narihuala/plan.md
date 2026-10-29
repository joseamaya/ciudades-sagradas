# Plan de Narihualá — Fase 0

Fecha: 28 de octubre de 2026.
Estado: **Fase 0 con envolvente oficial documentada; no se abre Blender hasta obtener el plano arqueológico de sectores**.

## Objetivo

Reconstruir el conjunto monumental de adobe de Narihualá como centro político-ceremonial tallán del valle bajo del Piura, con lectura clara de sus dos montículos, la plaza, las rampas y los corredores. No se modela el pueblo actual ni se inventan alturas perdidas.

## Zonas hero

1. **Montículo mayor / Sector III** y su relación con la plaza.
2. **Plaza de 60 × 40 m** y accesos por rampas.
3. **Montículo menor / Sector I** y sus compartimentos.
4. **Sector II:** recintos, patios y corredores.
5. **Faldeos y rellenos de adobe** con erosión visible.
6. **Valle del Piura y bosque seco** como contexto.

## Fuera de alcance inicial

- Reconstruir el pueblo actual de Narihualá o el museo como arquitectura prehispánica.
- Inventar techos, alturas o recintos sin planta.
- Incluir la capilla republicana en el hero o en el recorrido prehispánico.
- Copiar imágenes oficiales o usar texturas de IA.

## Presupuesto técnico

| Elemento | Objetivo |
|---|---|
| LOD0 escritorio | 120.000–200.000 tris |
| LOD1 móvil | 30.000–50.000 tris |
| Draw calls | <100 en régimen estable |
| GLB | <25 MB por LOD |
| Texturas | 2K hero, 1K móvil; WebP 80 |
| Compresión | Draco en LOD0/LOD1 |
| Escala | Metros en Blender; diorama del visor a decidir en blockout |
| Capas | Adobe, terreno/valle, detalles, escala humana, capilla republicana |
| Paradas | 6 |
| Luces | Amanecer, mediodía, atardecer, noche |

## Recorrido preliminar

1. **Llegada al valle.** Catacaos, bosque seco y posición del conjunto.
2. **Fachada de adobe.** Rellenos, plataformas y erosión.
3. **Plaza de 60 × 40 m.** Rampas, accesos y organización.
4. **Sector II.** Patios, recintos y corredores.
5. **Montículo mayor.** Plataformas y lectura del poder tallán.
6. **Mirador del valle.** Relación con el río, la ciudad y el paisaje.

## Evidencia y licencias

- Base: Mincetur 364, Municipalidad de Catacaos, RVM 000084-2023-VMPCIC/MC, Museo de Sitio Narihualá, SciELO 2023 y Fernández Villegas 1990.
- No se copian fotografías oficiales.
- Sin texturas de IA; adobe, barro, arena y vegetación con materiales propios o CC0.
- La capilla republicana se documenta y, si se modela, va en `later`, desactivada por defecto.

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Alturas originales desconocidas | Invención | Usar vacíos y cortes; no completar |
| Erosión del adobe | Difícil lectura de muros | Relieve geométrico y texturas propias |
| Mezcla con capilla/museo | Anacronismo | Capa `later` y fuera del hero |
| Escala del conjunto | Pérdida de monumentalidad | Blockout con plaza y cotas |
| Presión urbana actual | Confusión de época | Modelar solo el sitio arqueológico |
| Licencias de imágenes | Bloqueo | Renders propios y registro |

## Gate de Fase 0

- [x] Dossier de fuentes.
- [x] Ficha de investigación en el atlas.
- [x] Alcance hero/fondo y límites.
- [ ] Planta arqueológica de sectores y cotas de detalle. La envolvente legal y la lectura SIGRID 2018 están en `planta-cotas.md`; la ortofoto no separa los sectores.
- [x] Capilla documentada como añadido republicano; no se modela en el núcleo; capa `later` si se incluye.
- [x] Licencias resueltas para el alcance documental: fuentes citadas, sin copiar imágenes ni planos.
- [x] Presupuesto y recorrido aprobados; el blockout queda bloqueado por la planta.

## Siguiente

La ortofoto y el DTM libres de SIGRID localizan los montículos y las alturas, pero no cierran la planta. Sin un plano arqueológico o un levantamiento propio no hay blockout: no se inventan montículos, rampas ni recintos. La capilla queda documentada y, si se incluye, en capa `later`.
