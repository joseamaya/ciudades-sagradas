# Plan de Chavín de Huántar — Fase 0

Fecha: 27 de octubre de 2026.
Estado: **Fase 0 cerrada; preview web v0.2 con LOD0/LOD1; blockout y Portada aceptados como base**.
Estándar heredado de Caral: **ciudad representativa**, no inventario 1:1.

## Objetivo

Preparar una reconstrucción 3D navegable de Chavín de Huántar con evidencia, licencias y presupuesto cerrados antes de tocar Blender. El producto final debe leerse como centro ceremonial en el valle, no como una maqueta exhaustiva de cada galería.

## Alcance propuesto

### Zonas hero

1. **Edificio B / Templo del Lanzón** (tradicional “Templo Antiguo”). Volumen, acceso, Galería del Lanzón y relación con la plaza.
2. **Edificio A / Pirámide Mayor / “Castillo”** (tradicional “Templo Nuevo”), con la **Portada de las Falcónidas**.
3. **Plaza Circular Hundida y Atrio del Lanzón.** Pavimento, gradas, escalinatas y umbral ritual.
4. **Una secuencia de galería y ventilación.** Solo lo que la evidencia permita; no las 22 galerías inventadas.

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

1. **Llegada al valle.** Confluencia Mosna/Wacheqsa y posición del centro ceremonial.
2. **Plaza Circular y Atrio del Lanzón.** Gradas, pavimento y umbral ritual.
3. **Edificio B / Templo del Lanzón.** Acceso, galería y espacio del ídolo.
4. **Galería y ventilación.** Oscuridad, aire y relación con el exterior.
5. **Edificio A / Pirámide Mayor.** Portada de las Falcónidas y fachada.
6. **Mirador del conjunto.** Templos, plazas, ríos y paisaje.

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

## Estado del gate (27 de octubre de 2026)

| Ítem | Estado |
|---|---|
| Fuentes UNESCO/Mincul | Verificadas |
| ICOMOS 1985 | Pendiente de acceso (403); cubierto por ICOMOS 1999 |
| Plano | Consultado; puntos usados en blockout; faltan secciones finas |
| Cobertura | Aprobada para blockout |
| Alcance hero/fondo | Aprobado para blockout |
| Presupuesto y escala | Aprobados para blockout; escala final pendiente |
| Recorrido, capas y luces | Aprobados para blockout |
| Licencias de imágenes/esculturas | Política aprobada; permisos de publicación pendientes |
| Imágenes oficiales copiadas | 0 |
| Blockout v0.1 | Generado y revisado; base de masas |
| Blockout v0.2 | Pase de terreno en `blender/chavin/chavin_blockout_v0.2.blend`; aceptado para blockout |
| Blockout v0.3 | Galería/Lanzón en `blender/chavin/chavin_blockout_v0.3.blend`; histórico |
| Blockout v0.4 | Cierre del patio B en `blender/chavin/chavin_blockout_v0.4.blend`; histórico |
| Blockout v0.5 | Revisión de Lanzón, portal y escala en `blender/chavin/chavin_blockout_v0.5.blend`; aceptado |
| Look-dev v0.1 | Materiales procedurales en `blender/chavin/chavin_lookdev_v0.1.blend`; histórico |
| Look-dev v0.2 | Mampostería ashlar procedural en `blender/chavin/chavin_lookdev_v0.2.blend`; histórico |
| Texturizado UV v0.1 | UVs de cubo y texturas 2K en `blender/chavin/chavin_textured_v0.1.blend`; histórico |
| Texturizado UV v0.2 | Ashlar cálido, difusa oscura, hiladas variables y normal marcada; base aceptada |
| Portada v0.1 | Escala corregida, relieves abstractos, dintel omitido y escalón inferido; aceptada como base de trabajo |
| Preview web v0.1 | LOD0 14.158 tris / LOD1 9.422 tris, 15 draw calls, seis paradas, capas y fallback LOD1 |
| High-poly v0.1 | 174.582 tris / 1.846.904 B en LOD0 y 18.738 tris / 751.384 B en LOD1; 20/15 draw calls; relieves y terreno detallado (superado) |
| High-poly v0.2 | 235.098 tris / 1.814.248 B en LOD0 y 14.902 tris / 713.952 B en LOD1; 19/14 draw calls; friso integrado y rostro inciso (histórico) |
| High-poly v0.3 | 249.266 tris / 1.960.828 B en LOD0 y 26.898 tris / 785.260 B en LOD1; 19/15 draw calls; Lanzón del escaneo CyArk (CC BY-NC-SA 4.0) |
| High-poly v0.4 | 249.906 tris / 1.962.060 B en LOD0 y 27.539 tris / 786.136 B en LOD1; 19/15 draw calls; columnas acanaladas y parada 5 con fov 28 |
| High-poly v0.5 | 249.930 tris / 1.962.280 B en LOD0 y 27.563 tris / 786.356 B en LOD1; 18/15 draw calls; remates A/B integrados en piedra (histórico) |
| High-poly v0.6 | 249.990 tris / 1.962.740 B en LOD0 y 27.622 tris / 786.816 B en LOD1 (accessors); 18/14 draw calls; apoyos visibles bajo Tier_04/Tier_02 |

## Decisión de gate

**27 de octubre de 2026 — se aprueba el paso a blockout v0.1 con estas condiciones:**

- Base: Edificio A/B, Plaza Circular/Atrio del Lanzón y una secuencia de galería.
- Evidencia: UNESCO 330, Ministerio de Cultura, Plan de Manejo 2020 e ICOMOS 1999; ICOMOS 1985 no bloquea.
- Licencias: cero imágenes oficiales copiadas; el blockout usa geometría propia; publicar piezas de museo requiere permiso.
- Sin texturas de IA.
- El alcance se congela hasta revisar el blockout contra `cobertura.md`.

## Gate de Fase 0

No se abre Blender hasta completar:

- [x] `docs/fuentes/chavin.md` ampliado con tablero de fuentes.
- [x] `referencias.md` con política de licencias y permisos de publicación identificados.
- [x] `cobertura.md` aprobado para blockout.
- [x] Alcance hero/fondo y exclusiones aprobados.
- [x] Presupuesto técnico y escala preliminar aprobados.
- [x] Recorrido, capas y luces preliminares aprobados.
- [x] Riesgos y huecos de evidencia aceptados.
- [x] Cero imágenes oficiales copiadas sin permiso.

## Siguiente hito

**High-poly y QA:** el pase high-poly v0.6 deja el LOD0 en 249.990 tris (dentro del techo nominal), con friso integrado, Lanzón derivado del escaneo CyArk, columnas acanaladas y apoyos visibles bajo Tier_04/Tier_02 y remates A/B en piedra. La parada 5 usa `fov 28` para que la Portada entre en cuadro. Falta QA en hardware real y decidir dintel/escalera; el bake normal/AO del Lanzón se descartó por artefactos. La licencia CC BY-NC-SA 4.0 limita el uso comercial del Lanzón. Ver `highpoly-v0.6.md`, `web-preview.md`, `portada-v0.1.md` y `terrain.md`.
