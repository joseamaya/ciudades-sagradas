# Chavín de Huántar — remaster

Estado: **preview web v0.1 con pase high-poly v0.3; blockout v0.5, texturizado UV v0.2 y Portada v0.1 aceptados como base**. LOD0 de 249.266 tris y LOD1 de 26.898 tris, con fallback LOD1. El Lanzón es una adaptación del escaneo CyArk/Google Arts & Culture (CC BY-NC-SA 4.0), no una reconstrucción final. Fuentes UNESCO/Mincul, Plan de Manejo 2020 e ICOMOS 1999 verificados; ICOMOS 1985 y las secciones finas quedan como pendientes no bloqueantes.

Chavín se abre después del cierre de contenido de Caral v2. El blockout v0.5 está aceptado como base de escala y `chavin_textured_v0.2.blend` añade UVs de proyección cúbica, texturas 2K repetidas, tinte cálido y una difusa oscura propia. El bake 2K se probó y se descartó por pérdida de detalle. La Portada v0.1 corrige el placeholder a escala documentada, añade relieves interpretativos y queda aceptada como base; el dintel se omite por evidencia y la escalera se reduce a un escalón inferido. El pase high-poly v0.3 conserva la mampostería de fachada, las lomas y el friso integrado, y sustituye el rostro inciso del Lanzón por una malla derivada del escaneo CyArk; el LOD1 conserva una copia de 12.000 tris con relieve. El uso comercial de esa geometría está restringido por CC BY-NC-SA 4.0. El preview web usa esa geometría como LOD0/LOD1 y sirve para validar cámaras, capas, fallback y caché; el terreno sigue siendo procedural y el pase no es una reconstrucción final.

## Documentos

- `plan.md`: alcance, presupuesto técnico, paradas, capas, luces, riesgos y gate.
- `cobertura.md`: elementos documentados, nivel de detalle objetivo y huecos.
- `referencias.md`: fuentes públicas, licencias y material pendiente.
- `terrain.md`: decisión de terreno procedural y criterio para un DEM futuro.
- `blockout-v0.1.md`: alcance, métricas, evidencia y límites del primer blockout.
- `blockout-v0.2.md`: pase de terreno, talud, rampa, ríos y Cerro Cochas.
- `blockout-v0.3.md`: galería acotada, Lanzón y sección de revisión (histórico).
- `blockout-v0.4.md`: cierre del patio de B, portal y relleno del núcleo (histórico).
- `blockout-v0.5.md`: revisión de Lanzón, portal y escala humana (aceptado).
- `lookdev-v0.1.md`: base de materiales procedurales (histórico).
- `lookdev-v0.2.md`: mampostería ashlar, texturas propias y límites de exportación (histórico).
- `textured-v0.1.md`: UVs de proyección cúbica, texturas 2K y prueba de GLB; incluye el bake descartado (histórico).
- `textured-v0.2.md`: ashlar con tinte cálido, difusa oscura, hiladas variables y normal más marcada; GLB de prueba de 5,5 MB.
- `portada-v0.1.md`: escala corregida, columnas, jambas, friso, vano y relieves interpretativos.
- `highpoly-v0.1.md`: mampostería en relieve, talla del Lanzón, lomas, rocas, métricas y límites del pase anterior (superado).
- `highpoly-v0.2.md`: friso integrado y rostro inciso del Lanzón (superado por v0.3).
- `highpoly-v0.3.md`: Lanzón derivado del escaneo CyArk, licencia, métricas y límites del pase actual.
- `web-preview.md`: assets, métricas, QA, límites y limitación de LOD0/LOD1.

## Reglas

- Sin texturas de IA; solo CC0, procedurales o permisos documentados.
- No copiar imágenes de UNESCO/Mincul/ICOMOS sin permiso.
- Separar documentado, inferido e interpretativo.
- No inventar techos, galerías ni esculturas ausentes.
- No publicar imágenes oficiales ni piezas de museo sin permiso.
