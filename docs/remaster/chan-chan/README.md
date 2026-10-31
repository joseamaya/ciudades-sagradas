# Chan Chan — piloto solo-datos

Estado: **piloto documental**, `availability: research`, `maturity: research`, sin modelo 3D y sin QA de hardware.
Fecha: 31 de octubre de 2026.

## Alcance

Este piloto valida que Chan Chan puede enriquecerse como ficha documental **sin añadir geometría ni tocar `src/`**. No se publica como ciudad `available` y no se le asigna un estado `qa`.

- No hay GLB, `hero.jpg`, cámaras, recorrido ni capas de modelo.
- No se cambia la caché global: no hay assets nuevos.
- No se copian fotografías oficiales de UNESCO/Mincul/ICOMOS.
- La ficha sigue siendo documental; no es una reconstrucción arqueológica.

## Evidencia

- Dossier: [`docs/fuentes/chan-chan.md`](../../fuentes/chan-chan.md)
- Cobertura: [`cobertura.md`](./cobertura.md)
- Plan del piloto: [`plan.md`](./plan.md)
- Ficha publicada: `public/cities/chan-chan/city.json`

## Decisión

Chan Chan se mantiene en `research`. Las alturas originales, techos, colores y usos no conservados se presentan como inferidos o interpretativos, nunca como hechos cerrados.

El siguiente piloto solo-datos es Wari. Abrir una reconstrucción 3D de Chan Chan exige un gate separado: fuentes, licencias, cobertura, blockout, QA y presupuesto de assets.
