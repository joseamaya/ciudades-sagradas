# Aypate — remaster

Estado: **preview web v0.4 con high-poly navegable; escala contrastada con el plano de 2013; QA de hardware pendiente**.
Fuente: `blender/aypate/aypate_highpoly_v0.4.blend` (8,9 MB).
LOD0: **209.560 tris / 2.139.720 B**; LOD1: **30.663 tris / 443.372 B**; 17/15 draw calls.
Caché global `v38`.

Aypate es un centro administrativo y ceremonial inca del siglo XV, en el bosque de neblina de Ayabaca. El high-poly modela el núcleo documentado —plaza, ushnu, kallanka, acllawasi, palacio, colcas, fuente, andenes y Qhapaq Ñan— con una composición macro basada en el levantamiento publicado de 2013; los detalles no conservados siguen siendo interpretativos. La puerta escaneada de Sketchfab se usa como referencia, no como asset del GLB.

## Documentos

- `plan.md`: alcance, presupuesto, recorrido, riesgos y gate de Fase 0.
- `cobertura.md`: elementos documentados, inferidos y diferidos.
- `referencias.md`: fuentes, licencias y criterios de imagen.
- `web-preview.md`: assets, métricas, QA y límites del preview.
- `auditoria-plano-2013.md`: comparación y corrección del layout macro.
- `escala.md`: tabla de dimensiones y decisiones de escala v0.4.
- `cotas.md`: cierre documental de cotas de conjunto y límites.
- Dossier de fuentes: [`../../fuentes/aypate.md`](../../fuentes/aypate.md).

## Vistas

### High-poly, cámara hero

![High-poly de Aypate](highpoly-v0.4-hero.jpg)

### Plaza Inca en el visor

![Plaza Inca](web-preview-plaza.png)

### Kallanka

![Kallanka](web-preview-kallanka.png)

## Límites

- El plano general de 2013 está publicado como figura en Campos 2017; la memoria de 36 sectores y el original de alta resolución no son públicos.
- La v0.4 conserva el layout macro y corrige escala; ver `escala.md` y `auditoria-plano-2013.md`.
- Quedan pendientes las cotas finas y la QA móvil/1080p; el desktop integrado 1600×900 pasó LOD0/LOD1.
- No se reconstruyen techos, alturas perdidas ni todos los recintos periféricos.
- La vegetación y la niebla son una lectura de ambiente, no un inventario botánico.
- No hay QA v0.4 en hardware real.
- El escaneo de la puerta no se incorporó; si se integra, requiere retopología, material propio y atribución CC BY.
