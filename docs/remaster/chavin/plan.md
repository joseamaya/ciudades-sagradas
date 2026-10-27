# Plan de Chavín de Huántar — Fase 0

Fecha: 27 de octubre de 2026.
Estado: **Fase 0 en curso; modelado bloqueado**.
Estándar heredado de Caral: **ciudad representativa**, no inventario 1:1.

## Objetivo

Preparar una reconstrucción 3D navegable de Chavín de Huántar con evidencia, licencias y presupuesto cerrados antes de tocar Blender. El producto final debe leerse como centro ceremonial en el valle, no como una maqueta exhaustiva de cada galería.

## Alcance propuesto

### Zonas hero

1. **Templo Antiguo y Lanzón.** Volumen principal, acceso, relación con la plaza y el espacio del Lanzón.
2. **Templo Nuevo y Portada de las Falcónidas.** Fachada, escalinata y lectura exterior.
3. **Plaza Circular Hundida.** Gradas, accesos y relación con los templos.
4. **Una secuencia de galería y ventilación.** Solo lo que la evidencia permita; no un laberinto completo inventado.

### Fondo y contexto

- Terrazas, plataformas y plazas rectangulares.
- Ríos Mosna y Huachecsa, quebradas y valle altoandino.
- Estela Raimondi, Obelisco Tello y cabezas clavas solo si hay fuente y licencia; pueden quedar como referencia o réplica señalizada.
- Vegetación de altura, piedra, humedad y niebla.

### Fuera de alcance inicial

- Reconstruir todas las galerías internas una por una.
- Inventar techos, cubiertas o alturas no conservadas.
- Copiar piezas de museo sin permiso.
- Modelar la totalidad del área UNESCO de 14,79 ha a alta fidelidad.

## Presupuesto técnico

| Elemento | Objetivo |
|---|---|
| LOD0 escritorio | 150.000–250.000 tris |
| LOD1 móvil | 50.000–80.000 tris |
| Draw calls | <100 en régimen estable por LOD |
| GLB | <25 MB por LOD |
| Texturas | Hero 2K, móvil 1K; WebP 80 |
| Compresión | Draco en LOD0/LOD1; fallback sin Draco |
| Fallback | GLB simplificado o LOD1 sin Draco, según QA |
| Escala | Metros en Blender; escala de visor a decidir en blockout |
| Capas | Arquitectura, terreno/valle, esculturas/detalles, escala humana |
| Paradas | 6 |
| Luces | Amanecer, mediodía, atardecer, noche |

No se decide la escala final del visor hasta medir la huella del sitio y el encuadre hero.

## Recorrido preliminar

1. **Llegada al valle.** Río, quebradas y posición del centro ceremonial.
2. **Plaza Circular Hundida.** Gradas y umbral ritual.
3. **Templo Antiguo.** Acceso y Lanzón.
4. **Galería y ventilación.** Oscuridad, aire y relación con el exterior.
5. **Templo Nuevo.** Portada de las Falcónidas y fachada.
6. **Mirador del conjunto.** Templos, plazas y paisaje.

Los textos deben distinguir documentado, inferido e interpretativo; no afirmar función ritual como certeza absoluta.

## Evidencia y licencias

- Base documental: UNESCO 330, ICOMOS 1985, Ministerio de Cultura, Museo Nacional Chavín, MNAAHP y proyecto de John Rick/Stanford.
- Las imágenes oficiales se consultan, no se copian. Para publicar se necesita permiso o una alternativa CC0/CC BY.
- Sin texturas de IA. Materiales procedurales o texturas CC0 con registro.
- Cada escultura trasladada al museo se señala como réplica o referencia, no como pieza in situ.

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Galerías interiores complejas | Alto coste y poca evidencia visible | Modelar una secuencia hero, no el sistema completo |
| Techos y alturas no conservados | Invención histórica | No reconstruir sin fuente; usar cortes o vacíos señalizados |
| Licencias de imágenes y esculturas | Bloqueo de publicación | Tablero de licencias antes de modelar |
| Iluminación interior | La oscuridad es clave, pero difícil de leer | Presets y luces de visita; no “inventar” iluminación ritual |
| Escala y pendientes | Errores de conjunto | DEM/planos y blockout antes de detalle |
| Piezas emblemáticas (Lanzón, Estela, Obelisco) | Alta expectativa visual | Priorizar Lanzón; las demás como referencia si falta licencia |

## Gate de Fase 0

No se abre Blender hasta completar:

- [ ] `docs/fuentes/chavin.md` ampliado con tablero de fuentes.
- [ ] `referencias.md` con licencias y permisos.
- [ ] `cobertura.md` aprobado.
- [ ] Alcance hero/fondo y exclusiones aprobados.
- [ ] Presupuesto técnico y escala preliminar aprobados.
- [ ] Recorrido, capas y luces preliminares aprobados.
- [ ] Riesgos y huecos de evidencia aceptados.
- [ ] Cero imágenes oficiales copiadas sin permiso.

## Siguiente hito

**Chavín blockout v0.1:** terreno, ríos, plataformas y volúmenes de los templos, sin materiales finales ni esculturas detalladas. Se revisa contra `cobertura.md` antes de continuar.
