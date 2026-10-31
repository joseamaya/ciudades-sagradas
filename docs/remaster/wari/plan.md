# Wari — plan del piloto solo-datos

Fecha: 31 de octubre de 2026.

## Objetivo

Cerrar Wari como ficha documental `research` y validar que el esquema de Chan Chan se reutiliza sin código específico ni assets 3D.

## No objetivos

- No crear modelo 3D, portada, LOD, recorrido ni capas.
- No cambiar `availability`, `maturity`, `evidence` ni `qa`.
- No modificar `public/sw.js` ni el registro de assets.
- No presentar la ficha como reconstrucción final ni como ciudad inca.

## Entregables

1. Dossier de fuentes actualizado y con alcance explícito.
2. Cobertura por elemento y nivel de evidencia.
3. `city.json` sin configuración 3D sin uso, con fuentes, créditos y disclaimer coherentes.
4. Documentación de estado y auditoría actualizada.
5. Pruebas de ficha documental en Chromium y Firefox desktop.

## Fases

1. **Auditoría:** comparar ficha y dossier con el estándar.
2. **Datos:** actualizar `city.json` y `docs/fuentes/wari.md`.
3. **Cobertura:** documentar elementos, evidencia y límites.
4. **Validación:** `npm run validate`, `npm run build` y Playwright de fichas.
5. **Publicación:** PR, CI, merge y verificación en Pages.

## Criterios de aceptación

- `npm run validate` en verde.
- `npm run build` en verde.
- Wari y Chan Chan siguen sin canvas y sin errores de consola.
- La ficha muestra fuentes, disclaimer y créditos.
- No hay assets nuevos ni cambio de caché.
- Wari sigue en `research`.

## Riesgos

- **Trazado urbano discutido:** se documenta como discusión, no como planta cerrada.
- **Fuentes insuficientes para 3D:** se mantiene la ficha documental.
- **Licencias de imágenes:** no se usan imágenes oficiales; solo enlaces citados.
- **Confusión con lo inca:** se explicita que Wari es anterior y distinto.
- **Presión por publicar `available`:** no se acepta sin modelo, cobertura, licencias y QA.
