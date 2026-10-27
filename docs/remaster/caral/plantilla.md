# Plantilla técnica — nueva ciudad

Checklist derivado de Caral Remaster v2.

## Estándar de completitud

- [ ] Fijar el estándar antes de modelar: **ciudad representativa** (volúmenes y sectores principales) o inventario 1:1.
- [ ] Crear `cobertura.md` con elemento documentado → presente en GLB → nivel de detalle → evidencia.
- [ ] Marcar los huecos por fuente como diferidos; no inventar para “completar”.
- [ ] Definir qué zonas son hero y cuáles quedan como fondo.

## Escena

- [ ] Unidades en metros y origen estable en el centro del sitio.
- [ ] Colecciones por capa: `city`, `terrain`, `props`, `reference`.
- [ ] Nombres `GEO-`, `MAT-`, `LGT-`, `CAM-`.
- [ ] Sin colliders, spawns, HUD ni assets de juego.
- [ ] Evidencia marcada como documentada, inferida o interpretativa.

## Geometría y LOD

- [ ] LOD0 para escritorio y LOD1 para móvil, con presupuesto acordado.
- [ ] LOD1 conserva silueta, capas y lectura de las paradas.
- [ ] Fallback v1 o equivalente, sin Draco, como último recurso.
- [ ] `city.json` con `lod.levels`, `fallbackModel`, `scale`, `verticalScale`, `camera`, `tour` y `layers`.

## Materiales y texturas

- [ ] WebP 80 y Draco en LOD0/LOD1.
- [ ] Culling en sólidos; doble cara solo en vegetación, textiles, agua y fuego.
- [ ] Sin `KHR_materials_transmission` salvo justificación medida.
- [ ] Texturas móviles a 1K; 2K solo si la QA visual lo exige.
- [ ] Sin texturas de IA; licencias registradas.

## Visor

- [ ] Sombras cacheadas y actualizadas al cargar, cambiar hora o capas.
- [ ] Shadow map 2048/1024 y cámara ajustada a casters.
- [ ] PMREM/cielos cacheados por preset.
- [ ] Fallback móvil: LOD1 → v1 → LOD0.
- [ ] `?lod=0/1`, `?debug=1`, `?nosw=1`, `?noground=1`, `?noshadows=1`.
- [ ] Offline cachea el LOD cargado, no el fallback.

## Validación

- [ ] `npm run validate`
- [ ] `npm run build`
- [ ] `npm run bench`
- [ ] QA visual en Android/iPhone real: `lod=0/1`, `noground=1`, `noshadows=1`, vídeo y métricas.
- [ ] Fallback bloqueando LOD0/LOD1.
- [ ] Offline tras primera visita.
- [ ] 6 paradas, 4 luces, capas, móvil y kiosco.
- [ ] Sin errores de consola.
- [ ] Hashes/tamaños en `docs/fuentes/registro-assets.csv`.
- [ ] `CACHE` de `public/sw.js` actualizada si cambian assets.

## Cierre

- [ ] Capturas y portada.
- [ ] `release-*.md`, `auditoria-*.md`, `cobertura.md` e `incidencias.md`.
- [ ] QA en hardware real registrada; incidencias P2 aceptadas explícitamente.
- [ ] Tag/release.
