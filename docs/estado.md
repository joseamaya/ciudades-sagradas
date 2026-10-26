# Estado del proyecto

## Hecho

- Repositorio independiente con Vite + Three.js.
- OpenCode configurado con MCP de Blender y skills MIT en `.agents/skills/`.
- Escena editable `blender/caral/caral_art.blend` con texturas relativas en `blender/textures/`.
- Script de exportación `blender/caral/export.py` y guía `docs/setup.md`.
- Catálogo de cuatro ciudades: Caral, Chavín, Chan Chan y Wari.
- Caral como piloto en 3D con recorrido de cinco paradas.
- Capas de arquitectura, terreno, detalles y escala humana.
- Luz de amanecer, mediodía, atardecer y noche.
- Audio ambiental procedural; narración en español pendiente.
- PWA con caché offline y modo kiosco `?kiosk=1`.
- Interfaz responsive para 1080p táctil y móvil.
- Dossieres de fuentes públicas para las cuatro ciudades.
- Registro de assets y política de licencias.
- Validación automática y workflows de CI / GitHub Pages.
- Fase 0 del remaster de Caral: auditoría de escena, export reproducible y dossier de remaster en `docs/remaster/caral/`.
- Capturas en `docs/capturas/`.

## Pendiente

1. **Remaster de Caral**: reemplazar el modelo piloto low-poly por una versión de alta fidelidad.
2. **Auditoría de texturas de Caral**: confirmar términos de las texturas de IA o sustituirlas por CC0/procedurales.
3. **Chavín, Chan Chan y Wari**: modelos 3D, recorridos y fichas visuales.
4. **Narración en español**: guion y grabación para el kiosco.
5. **Renders cinematográficos**: Cycles con los assets high-poly.
6. **Pruebas en hardware de museo**: 1080p táctil, arranque automático, 8 horas de funcionamiento.
7. **Publicación**: mantener GitHub Pages actualizado y evaluar Cloudflare Pages para assets grandes.

## Limitaciones conocidas

- El modelo de Caral es un piloto visual; la geometría es esquemática.
- La arena del visor se aplana para evitar patrones de repetición.
- El GLB de Caral pesa ~20,7 MB y se reproduce con `export.py`; el objetivo es bajarlo con KTX2/meshopt tras el remaster.
- Wari no está en la Lista del Patrimonio Mundial; su ficha se basa en Ministerio de Cultura y academia.
- La narración aún no existe; solo hay ambiente procedural.

## Próximo paso recomendado

Remasterizar Caral con el pipeline high-poly → bake → PBR, y en paralelo cerrar la auditoría de licencias del GLB actual.
