# Estado del proyecto

## Hecho

- Repositorio independiente con Vite + Three.js.
- OpenCode configurado con MCP de Blender y skills MIT en `.agents/skills/`.
- Escena editable `blender/caral/caral_art.blend` con texturas relativas en `blender/textures/`.
- Script de exportación `blender/caral/export.py` y guía `docs/setup.md`.
- Catálogo de cuatro ciudades: Caral, Chavín, Chan Chan y Wari.
- Caral como piloto 3D con recorrido de seis paradas.
- Capas de arquitectura, terreno, detalles y escala humana.
- Luz de amanecer, mediodía, atardecer y noche.
- Audio ambiental procedural; narración en español pendiente.
- PWA con caché offline y modo kiosco `?kiosk=1`, este último congelado.
- Interfaz responsive para 1080p táctil y móvil.
- Dossieres de fuentes públicas para las cuatro ciudades.
- Registro de assets y política de licencias.
- Validación automática y workflows de CI / GitHub Pages.
- Fase 0 del remaster de Caral: auditoría de escena, export reproducible y dossier de remaster en `docs/remaster/caral/`.
- Remaster v1: GLB de 4,8 MB, 20 materiales y 31 imágenes, sin texturas de IA; desplegado el 2026-10-26.
- Remaster v2 web: LOD0 high-poly de 230.800 tris (22,6 MB, 125 draw calls) y LOD1 horneado de 56.332 tris (6,7 MB, 72 draw calls), con capas y fallback v1.
- `city.json` de Caral con `lod.levels` 0/1, `fallbackModel` v1, seis paradas y `stage: "v2"`.
- Caral v2 promovido de preview a remaster v2, con portada actualizada y caché `v5`.
- PR #5 mergeado (`a76fc8b`) y v2 desplegado en GitHub Pages: <https://joseamaya.github.io/ciudades-sagradas/>.
- Release web documentado en `docs/remaster/caral/release-v2.md`.
- Capturas en `docs/capturas/` y `docs/remaster/caral/`.

## Pendiente

1. **Caral**: QA en hardware real y red lenta; medir 60 fps a 1080p y validar Safari/iOS y Android. El kiosco y el hardware de museo están congelados.
2. **Texturas del piloto histórico**: confirmar el archivo definitivo de las texturas de IA; no se publican. Los GLB v1 y v2 no contienen texturas de IA.
3. **Chavín, Chan Chan y Wari**: modelos 3D, recorridos y fichas visuales.
4. **Narración en español**: guion y grabación; congelada junto con el kiosco.
5. **Renders cinematográficos**: Cycles con los assets high-poly.
6. **Publicación**: mantener GitHub Pages actualizado y evaluar Cloudflare Pages para assets grandes.

## Limitaciones conocidas

- Caral v2 está publicado; `model.glb` v1 se conserva como fallback y rollback.
- LOD0 mide 125 draw calls con sombras; se acepta como perfil de escritorio. LOD1 mide 72 y cumple el objetivo <100.
- LOD1 no conecta AO ni mapa de roughness: usa base color, normal y roughness constante 0,85.
- La escala **0,08** está validada como diorama web; la escala métrica 1.0 queda fuera de esta entrega.
- No se modelaron los 20 cubículos del Anfiteatro por falta de una planta publicada suficiente.
- La diferencia de altura norte/sur del Mayor sigue pendiente de sección o DEM.
- La sesión de 60 fps en GPU media y los dispositivos reales aún no se han medido.
- El visor añade un plano de arena bajo el modelo; el terreno del GLB ya tiene variación macro.
- Wari no está en la Lista del Patrimonio Mundial; su ficha se basa en Ministerio de Cultura y academia.
- La narración aún no existe; solo hay ambiente procedural.

## Próximo paso recomendado

Cerrar la QA web en hardware real y abrir el bloque de Chavín. El kiosco, la escala 1.0 y la narración quedan congelados hasta nuevo aviso.
