# Chan Chan — plan del piloto solo-datos

Fecha: 31 de octubre de 2026.

## Objetivo

Probar que una ciudad `research` puede mejorar su ficha, sus fuentes y su cobertura sin añadir un GLB ni código específico en `src/`.

## No objetivos

- No crear modelo 3D, portada, LOD, recorrido ni capas.
- No cambiar `availability`, `maturity`, `evidence` ni `qa`.
- No modificar `public/sw.js` ni el registro de assets.
- No presentar la ficha como reconstrucción final.

## Entregables

1. Dossier de fuentes actualizado y con alcance explícito.
2. Cobertura por elemento y nivel de evidencia.
3. `city.json` con fuentes, créditos y disclaimer coherentes.
4. Documentación de estado y auditoría actualizada.
5. Pruebas de ficha documental en Chromium y Firefox desktop.

## Fases

1. **Auditoría:** comparar ficha y dossier con el estándar.
2. **Datos:** actualizar `city.json` y `docs/fuentes/chan-chan.md`.
3. **Cobertura:** documentar elementos, evidencia y límites.
4. **Validación:** `npm run validate`, `npm run build` y Playwright de fichas.
5. **Publicación:** PR, CI, merge y verificación en Pages.

## Criterios de aceptación

- `npm run validate` en verde.
- `npm run build` en verde.
- Chan Chan y Wari siguen sin canvas y sin errores de consola.
- La ficha muestra fuentes, disclaimer y créditos.
- No hay assets nuevos ni cambio de caché.
- Chan Chan sigue en `research`.

## Riesgos

- **Fuentes insuficientes para 3D:** se resuelve manteniendo la ficha documental.
- **Licencias de imágenes:** no se usan imágenes oficiales; solo enlaces citados.
- **Exceso de detalle inventado:** cada elemento dudoso queda como inferido o interpretativo.
- **Presión por publicar `available`:** no se acepta sin modelo, cobertura, licencias y QA.
