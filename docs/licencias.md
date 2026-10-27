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

Los GLB publicados de Caral (v1, LOD0 y LOD1) usan solo materiales procedurales propios o atlas horneados desde geometría propia, y no incluyen texturas de IA. Usan WebP y Draco; el decoder Draco es Apache 2.0.

El piloto histórico con texturas de IA fue **retirado del repositorio** por licencia pendiente. No forma parte de los assets publicados ni del build. Si en el futuro se quisiera recuperar:

1. Confirmar los términos de Cloudflare Workers AI y del modelo generador.
2. Documentar la licencia resultante.
3. Si no permite la distribución, mantenerlo fuera del repo o sustituir por texturas CC0/procedurales y reexportar.

El código, los textos y los GLB v1/v2 sí pueden publicarse.

## Imágenes oficiales

Las páginas de UNESCO, ICOMOS, Ministerio de Cultura y museos se citan como fuentes documentales. Sus fotografías suelen tener derechos reservados. No se copian al repositorio; si se necesita una imagen, se solicita permiso o se usa una alternativa CC0/CC BY.

## Créditos

- Atribución visible en la ficha de cada ciudad.
- `CREDITS.md` global para terceros.
- En el pie de cada render: “Reconstrucción artística, no fotografía histórica”.
