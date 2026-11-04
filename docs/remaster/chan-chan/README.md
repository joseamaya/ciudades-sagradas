# Chan Chan — preview de Nik An

Estado: **preview web v0.1 de Nik An**, `availability: available`, `maturity: preview`, `qa: partial`.
Fecha: 4 de noviembre de 2026.

## Alcance

El piloto documental se conserva como base de evidencia. El preview 3D se limita a **Nik An**, el conjunto amurallado visitable, no a las nueve ciudadelas ni a los 20 km² de la ciudad.

- GLB LOD0/LOD1, `hero.jpg`, seis paradas, cuatro capas y cuatro presets de luz.
- LOD0: 156.624 tris / 1,9 MB; LOD1: 27.192 tris / 0,5 MB; 14/13 draw calls; texturas 208/64 MB de VRAM estimada.
- Se modelan plaza principal, corredor, altarcillo, audiencias, segunda plaza, depósitos, reservorio y plataforma funeraria.
- No se copian fotografías oficiales de UNESCO/Mincul/ICOMOS; no hay texturas de IA.

## Evidencia

- Dossier: [`docs/fuentes/chan-chan.md`](../../fuentes/chan-chan.md)
- Cobertura: [`cobertura.md`](./cobertura.md)
- Plan 3D: [`plan-3d.md`](./plan-3d.md)
- Plan histórico del piloto: [`plan.md`](./plan.md)
- Ficha publicada: `public/cities/chan-chan/city.json`

## Decisión

**Decisión actual (4 de noviembre de 2026):** se construye un preview 3D de Nik An. Las alturas originales, techos, colores, relieves y posición de algunos recintos se presentan como inferidos o interpretativos, nunca como hechos cerrados. La QA de hardware sigue pendiente; no se publica como `released`.

El siguiente paso es Wari, con el mismo criterio de núcleo representativo y evidencia explícita. Ver [`plan-3d.md`](./plan-3d.md).

## Documentos

- [`plan-3d.md`](./plan-3d.md): alcance, fases y límites del preview.
- [`plan.md`](./plan.md): plan histórico del piloto solo-datos.
- [`cobertura.md`](./cobertura.md): elementos modelados, inferidos y diferidos.
