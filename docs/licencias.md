# Política de licencias y assets

## Regla principal

Todo asset publicado debe tener una licencia compatible con un proyecto educativo público. Si no hay licencia clara, se usa solo como referencia y no se incluye en el build.

## Licencias aceptadas

| Tipo | Uso |
|---|---|
| CC0 / dominio público | Libre, con crédito opcional. |
| CC BY 4.0 / CC BY-SA 4.0 | Permitido con atribución; CC BY-SA obliga a compartir igual. |
| MIT / Apache / BSD | Código y utilidades. |
| Material propio | CC BY 4.0 salvo excepción. |
| Permiso escrito del autor | Guardar el permiso en `docs/permisos/`. |

## Licencias que evitar

- CC BY-NC: bloquea el uso museístico/comercial.
- CC BY-ND: impide adaptar o integrar.
- “Todos los derechos reservados” sin permiso.
- Imágenes de UNESCO, Ministerio de Cultura, ICOMOS o museos sin autorización.
- Capturas de Google Earth, Google Maps o Street View.

## Registro

Cada asset debe registrarse en `docs/fuentes/registro-assets.csv` con:

- `id`, `tipo`, `titulo`, `url`, `autor`, `licencia`, `uso`, `fecha_consulta`, `notas`.

## Texturas de Caral

El GLB de Caral del remaster v1 usa solo materiales procedurales propios y no incluye texturas de IA. El piloto histórico conserva texturas de IA y no se publica. Antes de un lanzamiento oficial:

1. Confirmar los términos de Cloudflare Workers AI y del modelo generador.
2. Documentar la licencia resultante.
3. Si no permite la distribución, sustituir por texturas CC0 o procedurales y reexportar el GLB.

Hasta entonces, el modelo de Caral se considera material de trabajo. El código y los textos sí pueden publicarse.

## Imágenes oficiales

Las páginas de UNESCO, ICOMOS, Ministerio de Cultura y museos se citan como fuentes documentales. Sus fotografías suelen tener derechos reservados. No se copian al repositorio; si se necesita una imagen, se solicita permiso o se usa una alternativa CC0/CC BY.

## Créditos

- Atribución visible en la ficha de cada ciudad.
- `CREDITS.md` global para terceros.
- En el pie de cada render: “Reconstrucción artística, no fotografía histórica”.
