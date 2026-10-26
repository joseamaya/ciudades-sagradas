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
- Fase 1 iniciada: primer pase de colinas en `blender/caral/caral_remaster.blend`; base y apron se mantienen planos por artefactos en río/campos.
- Fase 3 (materiales) iniciada: pase procedural en 134 slots de arquitectura, plazas y suelo; banding corregido; GLB de prueba de 8,5 MB y 55.944 tris.
- Visor alineado: AgX, PMREM, luz cálida y cámara inicial desde el sur; recorrido 2–5 revisado y FOV responsivo en móvil; capturas en `docs/remaster/caral/viewer-*.jpg`.
- Capturas en `docs/capturas/` y `docs/remaster/caral/`.

## Pendiente

1. **Remaster de Caral**: completar terreno, arquitectura high-poly, bake y QA visual; el pase de materiales ya está iniciado.
2. **Auditoría de texturas de Caral**: confirmar términos de las texturas de IA del piloto o sustituirlas por CC0/procedurales.
3. **Chavín, Chan Chan y Wari**: modelos 3D, recorridos y fichas visuales.
4. **Narración en español**: guion y grabación para el kiosco.
5. **Renders cinematográficos**: Cycles con los assets high-poly.
6. **Pruebas en hardware de museo**: 1080p táctil, arranque automático, 8 horas de funcionamiento.
7. **Publicación**: mantener GitHub Pages actualizado y evaluar Cloudflare Pages para assets grandes.

## Limitaciones conocidas

- El modelo de Caral es un piloto visual; la geometría es esquemática.
- El pase procedural de materiales ya cubre arquitectura, plazas y suelo, pero el terreno y la vegetación siguen con materiales del piloto.
- El GLB del piloto pesa ~20,7 MB; el GLB de prueba del pase procedural pesa 8,5 MB y todavía no se publica.
- La arena del visor se aplana para evitar patrones de repetición.
- Wari no está en la Lista del Patrimonio Mundial; su ficha se basa en Ministerio de Cultura y academia.
- La narración aún no existe; solo hay ambiente procedural.

## Próximo paso recomendado

Revisar el pase de materiales en el visor con cámara y luz de atardecer, aplicar materiales procedurales al terreno y continuar con muros high-poly → bake → PBR.
