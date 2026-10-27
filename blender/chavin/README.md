# Chavín — escena de blockout

## Archivo

- **Fuente actual:** `chavin_blockout_v0.4.blend`, 175 KB.
- **Versiones anteriores:** `chavin_blockout_v0.3.blend` (galería), `chavin_blockout_v0.2.blend` (terreno), `chavin_blockout_v0.1.blend` (masas).
- **Estado:** blockout v0.4, núcleo B cerrado; revisión pendiente.
- **Escala:** metros; el visor aplicará su escala cuando exista `city.json`.
- **Contenido:** 95 mallas, 1.990 vértices, 3.544 tris y 8 colecciones.
- **Texturas:** ninguna. Materiales planos de blockout.
- **Cámaras:** `CAM-Chavin_Hero`, `CAM-Chavin_Plan`, `CAM-Chavin_Core`, `CAM-Chavin_Gallery`, `CAM-Chavin_Lanzon`, `CAM-Chavin_Section`.
- **Luces:** `LGT-Chavin_Sun`, `LGT-Chavin_Fill`, `LGT-Chavin_GalleryFill`, `LGT-Chavin_LanzonFill`.

## Alcance

- Explanada del sitio derivada de los cuatro puntos del plano PE-330.
- Talud perimetral, bancos de río, rampa norte y Cerro Cochas de contexto.
- Terrazas, Edificio A, Edificio B, Plaza Circular/Atrio del Lanzón, Plataforma Norte y Plaza Cuadrada.
- Edificio B con patio de ~12 × 10 m y galería dentro de la masa.
- Una secuencia de galería: corredor, cámara, dinteles, portal, ducto y hornacina.
- Lanzón como volumen ahusado.
- Sin las 22 galerías, sin relieves, sin techos reconstructivos y sin materiales finales.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras, `COL-` colecciones.
- La evidencia y las inferencias están en `docs/remaster/chavin/blockout-v0.4.md` y `terrain.md`.
- No añadir texturas de IA ni imágenes oficiales sin permiso.

## Siguiente

Revisar el patio de B, el portal y la escala del Lanzón. Después: decidir DEM vs. procedural antes de look-dev y avanzar a materiales/LOD.
