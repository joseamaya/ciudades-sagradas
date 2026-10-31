# Ciudades Sagradas

Atlas interactivo de los grandes centros ceremoniales y ciudades del Perú antiguo. Reconstrucciones 3D en tiempo real, fichas educativas y fuentes públicas.

**Estado:** atlas en **preview público**. Caral Remaster v2 es la referencia técnica y su contenido está cerrado como ciudad representativa. Chavín, Aypate y Narihualá son previews navegables con distinto nivel de cierre; Chan Chan y Wari son pilotos documentales. Ninguna ciudad se presenta como reconstrucción arqueológica final.

| Ciudad | Cultura / período | Disponibilidad | Madurez | Evidencia | QA |
|---|---|---|---|---|---|
| Caral | Civilización Caral · 3000–1800 a. C. | `available` | `released` · v2 | Mixta | Excepción P2 aceptada |
| Chavín de Huántar | Chavín · 1500–550 a. C. | `available` | `preview` · v0.3 | Mixta | Parcial |
| Aypate | Inca · Qhapaq Ñan · siglo XV | `available` | `preview` · v0.4 | Mixta | Parcial |
| Narihualá | Tallán · Chimú · Inca | `available` | `preview` · v0.2 | Interpretativa | Parcial |
| Chan Chan | Chimú · siglos IX–XV | `research` | `research` | Ficha documental | No aplica |
| Wari | Wari · 600–1100 d. C. | `research` | `research` | Ficha documental | No aplica |

La matriz completa de QA, el protocolo y el registro de resultados están en [`docs/estandares/qa-hardware.md`](./docs/estandares/qa-hardware.md) y [`docs/qa/README.md`](./docs/qa/README.md). La checklist de publicación y el smoke post-deploy están en [`docs/release/preview-publico.md`](./docs/release/preview-publico.md).

## Qué es

Un proyecto independiente, pensado para museos, aulas y público general. No es un videojuego ni un visor técnico. Cada ciudad publicada incluye:

- Una reconstrucción 3D navegable con LOD por capacidad de dispositivo y fallback entre modelos.
- Un recorrido guiado en español, con el nivel de evidencia de cada parada.
- Capas de arquitectura, terreno, detalles y escala humana.
- Luz de amanecer, mediodía, atardecer y noche.
- Ficha con cronología, arquitectura, materiales y fuentes.
- Aviso explícito: reconstrucción artística, no fotografía histórica.

## Estado, madurez y evidencia

El atlas separa cuatro conceptos que antes se mezclaban en `status` y `stage`:

- **Disponibilidad** (`availability`): `available` si hay modelo navegable; `research` si solo hay ficha documental.
- **Madurez** (`maturity`): `research`, `blockout`, `preview` o `released`. `version` indica la entrega publicada.
- **Evidencia** (`evidence`): `documented`, `mixed`, `interpretive` o `not-applicable`. Cada parada añade `documented`, `inferred` o `interpretive`.
- **QA** (`qa`): `passed`, `partial`, `pending`, `waived` o `not-applicable`.

Una ciudad `available` no es automáticamente una ciudad terminada. El estándar obligatorio está en [`docs/estandares/ciudad.md`](./docs/estandares/ciudad.md) y la auditoría en [`docs/estandares/auditoria-ciudades.md`](./docs/estandares/auditoria-ciudades.md).

## Abrir en local

```bash
npm install
npm run dev
```

Abre `http://127.0.0.1:5173/`.

Para ver métricas del visor y copiar el informe QA (GPU, WebGL, PWA, flags y errores): `http://127.0.0.1:5173/?debug=1#/ciudad/caral`.
Para forzar un LOD: `?lod=0` o `?lod=1`.
Para desactivar el service worker en pruebas: `?nosw=1`.
Para QA de render: `?noground=1` oculta el plano de apoyo y `?noshadows=1` desactiva sombras.

## OpenCode + Blender

El repo incluye `opencode.json`, `AGENTS.md` y `.agents/skills/`. Abre OpenCode desde la raíz del proyecto. Para usar el MCP de Blender:

1. Abre Blender 5.2.2.
2. Inicia **MCP for Blender** en el panel `N`, puerto `9876`.
3. Abre una sesión de OpenCode en `ciudades-sagradas`.
4. Verifica con `blender_get_addon_status`.

Guía completa: [`docs/setup.md`](./docs/setup.md).

## Compilar y validar

```bash
npm run validate
npm run build
npm run serve
# benchmark reproducible con Chrome headless (requiere Chrome + build)
npm run bench -- --city caral --out /tmp/caral-bench

# QA funcional automatizada (requiere navegadores Playwright)
npm run qa:playwright:chromium
```

El build queda en `dist/`. Vite usa rutas relativas, así que funciona en GitHub Pages, Cloudflare Pages o un servidor local. El catálogo carga la aplicación base; Three.js y el visor se descargan bajo demanda al abrir una ciudad. El benchmark usa SwiftShader: sirve para comparar draw calls, triángulos, texturas y carga, **no para declarar FPS de hardware real**. La revisión Playwright cubre rutas, LOD, paradas, capas, consola y offline en Chromium/Firefox; su informe está en [`docs/qa/revision-playwright.md`](./docs/qa/revision-playwright.md).

`npm run validate` comprueba datos, estados, evidencia, coherencia índice/ficha, GLB, capas `extras.layer`, rangos de LOD, hashes y assets.

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

- **Caral:** remaster v2 cerrado como ciudad representativa; LOD0/LOD1 con Draco y fallback v1. Queda una incidencia Android P2 de suelo y QA de hardware pendiente.
- **Chavín de Huántar:** preview web v0.3 con pase de valle v0.7, Mosna ~30 m abajo, Wacheqsa al norte, Lanzón derivado de CyArk (CC BY-NC-SA 4.0) y Portada de las Falcónidas. El terreno es procedural y no es una reconstrucción final.
- **Aypate:** preview v0.4 con layout y escala contrastados con el plano de 2013. No se reabren dimensiones; quedan cotas finas y QA móvil/1080p.
- **Narihualá:** preview interpretativo v0.2. Montículo este y capilla desde SIGRID 2018; oeste, plaza y accesos inferidos. No es un plano arqueológico; quedan plano de sectores y QA móvil/1080p.
- **Chan Chan:** piloto solo-datos; ficha documental ampliada, sin modelo 3D ni QA de hardware.
- **Wari:** piloto solo-datos; ficha documental ampliada, sin modelo 3D ni QA de hardware.

Los dossieres de fuentes están en [`docs/fuentes/`](./docs/fuentes/). El estado detallado, el setup y el pipeline Blender están en [`docs/estado.md`](./docs/estado.md), [`docs/setup.md`](./docs/setup.md) y [`docs/pipeline-blender.md`](./docs/pipeline-blender.md).

## Estructura

```text
public/cities/<slug>/     city.json + LOD0/LOD1/fallback + portada
src/core/                 visor, audio, cámara, luz, métricas
src/ui/                   catálogo, ficha y semántica de estado
docs/fuentes/             dossier por ciudad
scripts/validate.mjs      validación de datos, GLB, hashes y assets
scripts/bench.mjs         benchmark y QA con Chrome/CDP
docs/remaster/            auditoría, pipeline y release por ciudad
```

Cada ciudad se describe con un `city.json`. Para añadir una quinta ciudad:

1. Crear `public/cities/<slug>/city.json` con `availability`, `maturity`, `version`, `evidence`, `qa`, `camera`, `tour`, `layers`, `lod.levels`, `fallbackModel`, `ground` y, si aplica, `fog`.
2. Añadir los GLB LOD0/LOD1 y la portada `hero.jpg`. Cada nodo con mesh debe traer `extras.layer` (`city`, `terrain`, `props`, `reference` o una capa adicional justificada).
3. Añadir la entrada en `public/cities/index.json` con los mismos campos canónicos.
4. Escribir el dossier en `docs/fuentes/<slug>.md`, la cobertura en `docs/remaster/<slug>/cobertura.md` y registrar los assets.
5. Ejecutar `npm run validate`, `npm run build` y `npm run bench`.

No debería hacer falta tocar `src/` para una ciudad nueva si el GLB trae capas y la configuración está completa.

## Realismo y evidencia

La prioridad es el impacto visual, pero sin presentar invenciones como hechos. Cada ficha distingue:

- **Documentado:** planos, excavaciones, materiales y fuentes.
- **Inferido:** reconstrucción razonable a partir de la evidencia.
- **Interpretativo:** decisiones artísticas para completar vacíos.

El visor muestra el nivel de evidencia de cada parada y el estado general de la ciudad. No se usan fotografías históricas como textura. Las imágenes oficiales se citan como referencia; para publicar se usan materiales propios, CC0 o con permiso. Los GLB publicados usan WebP y Draco; Caral LOD1 usa además un atlas horneado. No incluyen texturas de IA.

## Licencias

- Código: MIT. Ver [`LICENSE`](./LICENSE).
- Textos y modelos: CC BY 4.0, salvo indicación contraria. El Lanzón de Chavín derivado del escaneo CyArk es CC BY-NC-SA 4.0. Ver [`LICENSE-CONTENT.md`](./LICENSE-CONTENT.md) y [`LICENSE-ASSETS.md`](./LICENSE-ASSETS.md).
- Terceros y procedencia: [`CREDITS.md`](./CREDITS.md).
- Avisos de dependencias: [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md).
- Política de assets: [`docs/licencias.md`](./docs/licencias.md).

> **Nota de licencia:** los GLB publicados no incluyen texturas de IA. El piloto histórico con texturas de IA fue retirado del repositorio. Ver `CREDITS.md`, `LICENSE-CONTENT.md`, `LICENSE-ASSETS.md` y `docs/licencias.md`.

## Despliegue

El repo incluye un workflow de GitHub Pages en `.github/workflows/pages.yml`. Para Cloudflare Pages, usa:

- Build command: `npm run build`
- Output directory: `dist`

## Hoja de ruta

1. **Caral:** mantener v2 estable; cerrar o mantener la excepción Android P2 y completar QA en iPhone/Safari y GPU de escritorio.
2. **Chavín:** QA móvil/1080p del valle v0.7, decidir dintel/escalera y revisar la licencia CC BY-NC-SA del Lanzón antes de cualquier uso comercial.
3. **Aypate:** QA de hardware y cotas finas; no reabrir el layout de la v0.4.
4. **Narihualá:** plano arqueológico de sectores y cotas finas; mantener el carácter interpretativo.
5. **Chan Chan:** piloto solo-datos completado; ficha documental y cobertura cerradas sin modelo 3D.
6. **Wari:** piloto solo-datos completado; no se abre geometría sin fuentes, licencias y QA.
7. **Siguiente decisión:** elegir entre una ciudad 3D con fuentes/licencias/QA o una mejora técnica como el lazy-load del visor.

Release web de Caral: [`docs/remaster/caral/release-v2.md`](./docs/remaster/caral/release-v2.md).
