# Aypate — remaster

Estado: **preview web v0.3 con high-poly navegable; layout macro según el plano de 2013; QA de hardware pendiente**.
Fuente: `blender/aypate/aypate_highpoly_v0.3.blend` (7,9 MB).
LOD0: **226.408 tris / 1.983.580 B**; LOD1: **28.735 tris / 424.772 B**; 14/13 draw calls.
Caché `v25`.

Aypate es un centro administrativo y ceremonial inca del siglo XV, en el bosque de neblina de Ayabaca. El high-poly modela el núcleo documentado —plaza, ushnu, kallanka, acllawasi, palacio, colcas, fuente, andenes y Qhapaq Ñan— con una composición macro basada en el levantamiento publicado de 2013; los detalles no conservados siguen siendo interpretativos. La puerta escaneada de Sketchfab se usa como referencia, no como asset del GLB.

## Documentos

- `plan.md`: alcance, presupuesto, recorrido, riesgos y gate de Fase 0.
- `cobertura.md`: elementos documentados, inferidos y diferidos.
- `referencias.md`: fuentes, licencias y criterios de imagen.
- `web-preview.md`: assets, métricas, QA y límites del preview.
- `auditoria-plano-2013.md`: comparación y corrección del layout macro.
- Dossier de fuentes: [`../../fuentes/aypate.md`](../../fuentes/aypate.md).

## Vistas

### High-poly, cámara hero

![High-poly de Aypate](highpoly-v0.3-hero.jpg)

### Plaza Inca en el visor

![Plaza Inca](web-preview-plaza.png)

### Kallanka

![Kallanka](web-preview-kallanka.png)

## Límites

- El plano general de 2013 está publicado como figura en Campos 2017; la memoria de 36 sectores y el original de alta resolución no son públicos.
- La v0.3 rehízo el layout macro con ese plano; ver `auditoria-plano-2013.md`.
- Quedan pendientes las cotas finas y la QA de hardware.
- No se reconstruyen techos, alturas perdidas ni todos los recintos periféricos.
- La vegetación y la niebla son una lectura de ambiente, no un inventario botánico.
- No hay QA v0.3 en hardware real.
- El escaneo de la puerta no se incorporó; si se integra, requiere retopología, material propio y atribución CC BY.
