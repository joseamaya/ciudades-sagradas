# Narihualá — remaster

Estado: **preview web v0.2 interpretativo con apoyos corregidos; no reconstrucción final**.
Fuente: `blender/narihuala/narihuala_highpoly_v0.2.blend` (6,2 MB).
LOD0: **162.432 tris / 1.599.008 B**; LOD1: **29.682 tris / 441.800 B**; 14/13 draw calls.
Caché global `v38`.

Apoyos: plataformas macizas hasta terreno o plataforma inferior; plaza y montículo oeste con recorte local y transición. Luz de relleno específica para que las caras este no queden negras.

Narihualá es el principal conjunto monumental de adobe de la cultura Tallán, en Catacaos. Dos montículos, una plaza de 60 × 40 m, accesos y corredores organizan el sitio, ocupado también por chimúes e incas. La capilla republicana de la cima se trata como añadido posterior.

## Documentos

- `plan.md`: alcance, presupuesto, recorrido, riesgos y gate.
- `planta-cotas.md`: envolvente legal, SIGRID y límites de la planta.
- `planta-interpretativa.md`: qué es visible, qué es inferido y qué no se modela.
- `cobertura.md`: elementos documentados, inferidos y diferidos.
- `referencias.md`: fuentes, licencias y criterios de imagen.
- `web-preview.md`: assets, métricas, QA y límites.
- Dossier de fuentes: [`../../fuentes/narihuala.md`](../../fuentes/narihuala.md).

## Vistas

### High-poly

![High-poly de Narihualá](highpoly-v0.2-hero.jpg)

### Montículo oeste

![Montículo oeste](web-preview-west.png)

### Plaza central

![Plaza](web-preview-plaza.png)

### Montículo este

![Montículo este](web-preview-east.png)

## Límites

- El montículo este y la capilla se apoyan en SIGRID 2018; el montículo oeste y la plaza son inferencias.
- No hay plano arqueológico de sectores; la numeración I–III no se asigna.
- No se reconstruyen techos, alturas originales ni recintos interiores.
- La capilla va en `later`, apagada por defecto.
- Desktop integrado 1600×900: LOD0/LOD1 OK. Quedan QA móvil/1080p y el plano arqueológico de sectores.
