# Ciudades Sagradas

Atlas interactivo de los grandes centros ceremoniales y ciudades del Perú antiguo. Reconstrucciones 3D en tiempo real, fichas educativas y fuentes públicas.

**Estado:** Caral tiene un preview local del remaster; el piloto sigue publicado en `main`. Chavín de Huántar, Chan Chan y Wari están en investigación.

## Qué es

Un proyecto independiente, pensado para museos, aulas y público general. No es un videojuego ni un visor técnico. Cada ciudad tendrá:

- Una reconstrucción 3D navegable.
- Un recorrido guiado en español.
- Capas de arquitectura, terreno, detalles y escala humana.
- Luz de amanecer, mediodía, atardecer y noche.
- Ficha con cronología, arquitectura, materiales y fuentes.
- Aviso explícito: reconstrucción artística, no fotografía histórica.

## Abrir en local

```bash
npm install
npm run dev
```

Abre `http://127.0.0.1:5173/`.

## OpenCode + Blender

El repo incluye `opencode.json`, `AGENTS.md` y `.agents/skills/`. Abre OpenCode desde la raíz del proyecto. Para usar el MCP de Blender:

1. Abre Blender 5.2.2.
2. Inicia **MCP for Blender** en el panel `N`, puerto `9876`.
3. Abre una sesión de OpenCode en `ciudades-sagradas`.
4. Verifica con `blender_get_addon_status`.

Guía completa: [`docs/setup.md`](./docs/setup.md).

## Compilar

```bash
npm run validate
npm run build
npm run serve
```

El build queda en `dist/`. Vite usa rutas relativas, así que funciona en GitHub Pages, Cloudflare Pages o un servidor local.

## Modo museo / kiosco

```bash
npm run build
npm run serve
# abrir: http://127.0.0.1:4173/?kiosk=1
```

En el kiosco:

- Pantalla completa y botones grandes.
- Audio ambiental procedural, activado al primer toque.
- Regreso automático al atlas tras 90 segundos de inactividad.
- Pensado para 1080p táctil y Chromium en modo kiosco.

Más detalles en [`docs/kiosco.md`](./docs/kiosco.md).

## Ciudades

| Ciudad | Cultura | Período | Estado |
|---|---|---|---|
| Caral | Civilización Caral | 3000–1800 a. C. | Preview remaster |
| Chavín de Huántar | Chavín | 1500–550 a. C. | En investigación |
| Chan Chan | Chimú | Siglos IX–XV d. C. | En investigación |
| Wari | Wari | 600–1100 d. C. | En investigación |

Los dossieres de fuentes están en [`docs/fuentes/`](./docs/fuentes/). El estado, el setup, el pipeline Blender y el remaster de Caral están en [`docs/estado.md`](./docs/estado.md), [`docs/setup.md`](./docs/setup.md), [`docs/pipeline-blender.md`](./docs/pipeline-blender.md) y [`docs/remaster/caral/`](./docs/remaster/caral/).

## Estructura

```text
public/cities/<slug>/     city.json + modelo + portada
src/core/                 visor, audio, cámara, luz
src/ui/                   catálogo y ficha de ciudad
docs/fuentes/             dossier por ciudad
scripts/validate.mjs      validación de datos y assets
```

Cada ciudad se describe con un `city.json`. Para añadir una ciudad nueva:

1. Crear `public/cities/<slug>/city.json`.
2. Añadir el modelo en `public/cities/<slug>/model.glb`.
3. Añadir la entrada en `public/cities/index.json`.
4. Escribir el dossier en `docs/fuentes/<slug>.md`.
5. Ejecutar `npm run validate`.

## Realismo y evidencia

La prioridad es el impacto visual, pero sin presentar invenciones como hechos. Cada ficha distingue:

- **Documentado:** planos, excavaciones, materiales y fuentes.
- **Inferido:** reconstrucción razonable a partir de la evidencia.
- **Interpretativo:** decisiones artísticas para completar vacíos.

El visor no usa fotografías históricas como textura. Las imágenes oficiales se citan como referencia; para publicar se usan materiales propios, CC0 o con permiso.

## Licencias

- Código: MIT. Ver [`LICENSE`](./LICENSE).
- Textos y modelos: CC BY 4.0, salvo indicación contraria. Ver [`LICENSE-CONTENT.md`](./LICENSE-CONTENT.md).
- Terceros y procedencia: [`CREDITS.md`](./CREDITS.md).
- Avisos de dependencias: [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md).
- Política de assets: [`docs/licencias.md`](./docs/licencias.md).

> **Nota de licencia:** el preview del remaster usa materiales procedurales y su GLB no incluye texturas de IA. El piloto publicado en `main` todavía conserva texturas de IA y sigue pendiente de auditoría. Ver `CREDITS.md` y `docs/licencias.md`.

## Despliegue

El repo incluye un workflow de GitHub Pages en `.github/workflows/pages.yml`. Para Cloudflare Pages, usa:

- Build command: `npm run build`
- Output directory: `dist`

## Hoja de ruta

1. Caral: remaster de alta fidelidad y recorrido completo.
2. Chavín de Huántar.
3. Chan Chan.
4. Wari.
5. Renders cinematográficos con Cycles y modo foto.
