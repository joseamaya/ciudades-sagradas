# Ciudades Sagradas

Atlas interactivo de los grandes centros ceremoniales y ciudades del Perú antiguo. Reconstrucciones 3D en tiempo real, fichas educativas y fuentes públicas.

**Estado:** Caral remaster v2 es el estado actual. LOD0 de 230.800 tris y LOD1 de 56.332 tris, ambos con Draco; el piloto histórico con texturas de IA fue retirado del repositorio. Incluye la auditoría de estabilización y LOD1 con texturas 1K, desplegada en GitHub Pages. Chavín de Huántar, Chan Chan y Wari están en investigación.

## Qué es

Un proyecto independiente, pensado para museos, aulas y público general. No es un videojuego ni un visor técnico. Cada ciudad tendrá:

- Una reconstrucción 3D navegable con LOD por capacidad de dispositivo y fallback entre modelos.
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

Para ver métricas del visor: `http://127.0.0.1:5173/?debug=1#/ciudad/caral`.
Para forzar un LOD: `?lod=0` o `?lod=1`.
Para desactivar el service worker en pruebas: `?nosw=1`.
Para QA de render: `?noground=1` oculta el plano de arena y `?noshadows=1` desactiva sombras.

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
# benchmark reproducible con Chrome headless (requiere Chrome + build)
npm run bench -- --out /tmp/caral-bench
```

El build queda en `dist/`. Vite usa rutas relativas, así que funciona en GitHub Pages, Cloudflare Pages o un servidor local. El benchmark usa SwiftShader: sirve para comparar draw calls, triángulos, texturas y carga, no para declarar FPS de hardware real.

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
| Caral | Civilización Caral | 3000–1800 a. C. | Remaster v2 · LOD0/LOD1 |
| Chavín de Huántar | Chavín | 1500–550 a. C. | En investigación |
| Chan Chan | Chimú | Siglos IX–XV d. C. | En investigación |
| Wari | Wari | 600–1100 d. C. | En investigación |

Los dossieres de fuentes están en [`docs/fuentes/`](./docs/fuentes/). El estado, el setup, el pipeline Blender y el remaster de Caral están en [`docs/estado.md`](./docs/estado.md), [`docs/setup.md`](./docs/setup.md), [`docs/pipeline-blender.md`](./docs/pipeline-blender.md) y [`docs/remaster/caral/`](./docs/remaster/caral/).

## Estructura

```text
public/cities/<slug>/     city.json + LOD0/LOD1/fallback + portada
src/core/                 visor, audio, cámara, luz, métricas
src/ui/                   catálogo y ficha de ciudad
docs/fuentes/             dossier por ciudad
scripts/validate.mjs      validación de datos, GLB, hashes y assets
scripts/bench.mjs         benchmark y QA con Chrome/CDP
docs/remaster/            auditoría, pipeline y release de Caral
```

Cada ciudad se describe con un `city.json`. Para añadir una ciudad nueva:

1. Crear `public/cities/<slug>/city.json` con `stage`, `camera`, `tour`, `layers`, `lod.levels` y `fallbackModel`.
2. Añadir los GLB (LOD0/LOD1 y fallback) y la portada `hero.jpg`.
3. Añadir la entrada en `public/cities/index.json`.
4. Escribir el dossier en `docs/fuentes/<slug>.md` y registrar los assets.
5. Subir `CACHE` en `public/sw.js` si cambian assets existentes y ejecutar `npm run validate`, `npm run build` y `npm run bench`.

## Realismo y evidencia

La prioridad es el impacto visual, pero sin presentar invenciones como hechos. Cada ficha distingue:

- **Documentado:** planos, excavaciones, materiales y fuentes.
- **Inferido:** reconstrucción razonable a partir de la evidencia.
- **Interpretativo:** decisiones artísticas para completar vacíos.

El visor no usa fotografías históricas como textura. Las imágenes oficiales se citan como referencia; para publicar se usan materiales propios, CC0 o con permiso. Los GLB publicados usan WebP, Draco y, en LOD1, atlas horneados; no incluyen texturas de IA.

## Licencias

- Código: MIT. Ver [`LICENSE`](./LICENSE).
- Textos y modelos: CC BY 4.0, salvo indicación contraria. Ver [`LICENSE-CONTENT.md`](./LICENSE-CONTENT.md).
- Terceros y procedencia: [`CREDITS.md`](./CREDITS.md).
- Avisos de dependencias: [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md).
- Política de assets: [`docs/licencias.md`](./docs/licencias.md).

> **Nota de licencia:** los remasters v1 y v2 usan materiales procedurales y sus GLB no incluyen texturas de IA. El piloto histórico con texturas de IA fue retirado del repositorio. Ver `CREDITS.md`, `LICENSE-CONTENT.md` y `docs/licencias.md`.

## Despliegue

El repo incluye un workflow de GitHub Pages en `.github/workflows/pages.yml`. Para Cloudflare Pages, usa:

- Build command: `npm run build`
- Output directory: `dist`

## Hoja de ruta

1. Caral: remaster v2 desplegado, LOD0/LOD1 con Draco, LOD1 a 1K y QA reproducible; quedan hardware real y mejoras de contenido. KTX2 queda como mejora opcional.
2. Chavín de Huántar.
3. Chan Chan.
4. Wari.
5. Renders cinematográficos con Cycles y modo foto.

Release web de Caral: [`docs/remaster/caral/release-v2.md`](./docs/remaster/caral/release-v2.md).
