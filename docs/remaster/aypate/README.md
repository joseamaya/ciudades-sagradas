# Aypate — remaster

Estado: **preview web v0.2 con high-poly navegable; layout no coincidente con el plano de 2013; v0.3 pendiente**.
Fuente: `blender/aypate/aypate_highpoly_v0.2.blend` (8,1 MB).
LOD0: **241.436 tris / 2.101.584 B**; LOD1: **31.623 tris / 459.108 B**; 16/14 draw calls.
Caché `v24`.

Aypate es un centro administrativo y ceremonial inca del siglo XV, en el bosque de neblina de Ayabaca. El high-poly modela el núcleo documentado —plaza, ushnu, kallanka, acllawasi, palacio, colcas, fuente, andenes y Qhapaq Ñan— con una composición interpretativa. La auditoría contra el plano de 2013 muestra que esa composición no coincide con el levantamiento publicado; la v0.3 corregirá el layout. La puerta escaneada de Sketchfab se usa como referencia, no como asset del GLB.

## Documentos

- `plan.md`: alcance, presupuesto, recorrido, riesgos y gate de Fase 0.
- `cobertura.md`: elementos documentados, inferidos y diferidos.
- `referencias.md`: fuentes, licencias y criterios de imagen.
- `web-preview.md`: assets, métricas, QA y límites del preview.
- Dossier de fuentes: [`../../fuentes/aypate.md`](../../fuentes/aypate.md).

## Vistas

### High-poly, cámara hero

![High-poly de Aypate](highpoly-v0.2-hero.jpg)

### Plaza Inca en el visor

![Plaza Inca](web-preview-plaza.png)

### Kallanka

![Kallanka](web-preview-kallanka.png)

## Límites

- El plano general de 2013 está publicado como figura en Campos 2017; la memoria de 36 sectores y el original de alta resolución no son públicos.
- La composición de v0.2 no coincide con ese plano; ver `auditoria-plano-2013.md`.
- La v0.3 debe rehacer el layout; no es una corrección cosmética.
- No se reconstruyen techos, alturas perdidas ni todos los recintos periféricos.
- La vegetación y la niebla son una lectura de ambiente, no un inventario botánico.
- No hay QA v0.2 en hardware real.
- El escaneo de la puerta no se incorporó; si se integra, requiere retopología, material propio y atribución CC BY.
