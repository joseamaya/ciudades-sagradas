# Wari — piloto solo-datos

Estado: **piloto documental**, `availability: research`, `maturity: research`, sin modelo 3D y sin QA de hardware.
Fecha: 31 de octubre de 2026.

## Alcance

Wari es el segundo piloto solo-datos del atlas. Valida que una ciudad `research` puede cerrar dossier, cobertura y ficha **sin añadir geometría ni tocar `src/`**.

- No hay GLB, `hero.jpg`, cámaras, recorrido ni capas de modelo.
- No se cambia la caché global: no hay assets nuevos.
- No se copian fotografías oficiales de Ministerio de Cultura, museos ni academia.
- No se presenta como ciudad inca ni como reconstrucción arqueológica final.

## Evidencia

- Dossier: [`docs/fuentes/wari.md`](../../fuentes/wari.md)
- Cobertura: [`cobertura.md`](./cobertura.md)
- Plan del piloto: [`plan.md`](./plan.md)
- Ficha publicada: `public/cities/wari/city.json`

## Decisión

Wari se mantiene en `research`. El trazado urbano completo, las alturas, los techos, la policromía y la población se presentan como discutidos, inferidos o interpretativos, nunca como hechos cerrados.

Wari no figura en la Lista del Patrimonio Mundial; su ficha se apoya en Ministerio de Cultura, museos y academia. Abrir una reconstrucción 3D exige un gate separado de fuentes, licencias, cobertura, blockout, QA y presupuesto de assets.
