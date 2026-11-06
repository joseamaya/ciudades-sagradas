# Chavín de Huántar — preview v0.3

<!-- metrics:city:chavin:start -->
**Estado canónico:** `available` · `preview` · v0.3 · evidencia mixta · QA `partial`.

| Modelo | Triángulos | Bytes | Imágenes | Draw calls |
|---|---:|---:|---:|---:|
| LOD0 | 249.942 | 1.741.708 | 15 | 19 |
| LOD1 | 42.842 | 746.544 | 15 | 16 |
<!-- metrics:city:chavin:end -->

- Estado: **preview de revisión**, no remaster final. La versión pública del visor es `v0.3`; el pase de escena es `v0.7`.
- Portada: `hero.jpg`, render propio de la Portada de las Falcónidas.
- Metadatos: `city.json`.
- Fuente Blender: `blender/chavin/chavin_highpoly_v0.7.blend`; la Portada parte de `chavin_portada_v0.2.blend`.
- LODs: `blender/chavin/chavin_lod0.blend` y `chavin_lod1.blend` (no versionados).
- Sin imágenes oficiales ni texturas de IA.
- Terreno procedural; dintel y escalera cerrados en `docs/remaster/chavin/decisiones.md`. La parada 5 usa `fov 28` y fustes acanalados interpretativos; caché por hash generada en build.
- Iluminación: pase del 5 de noviembre de 2026 con luces de galería para el Lanzón y de fachada para la Portada; ver `docs/qa/revision-iluminacion-chavin-2026-11-05.md`.
- Licencia: el Lanzón derivado del escaneo CyArk es CC BY-NC-SA 4.0; el resto es geometría y texturas propias. El kiosco comercial requiere sustituir el Lanzón o negociar licencia.
- QA: desktop 1600×900 v0.7 aprobado en LOD0/LOD1; móvil, 1080p real y kiosco pendientes. Ver `docs/remaster/chavin/qa-hardware.md`.
- Documentación: `docs/remaster/chavin/web-preview.md`.
