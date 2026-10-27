# Chavín — escenas de blockout y look-dev

## Archivo

- **Look-dev actual:** `chavin_lookdev_v0.2.blend`, 585 KB.
- **Base de escala:** `chavin_blockout_v0.5.blend`, 176 KB.
- **Versiones anteriores:** `chavin_blockout_v0.4.blend` (patio B), `chavin_blockout_v0.3.blend` (galería), `chavin_blockout_v0.2.blend` (terreno), `chavin_blockout_v0.1.blend` (masas).
- **Estado:** blockout v0.5 aceptado; look-dev v0.2 de mampostería ashlar procedural.
- **Escala:** metros; el visor aplicará su escala cuando exista `city.json`.
- **Contenido:** 97 mallas, 2.148 vértices, 3.852 tris y 8 colecciones.
- **Texturas:** `blender/textures/chavin/chavin_ashlar_{diffuse,roughness,normal}`; generadas por `scripts/make_chavin_materials.py`.
- **Materiales:** 10; piedra clara y oscura usan texturas 2K propias de mampostería ashlar, empaquetadas. Hay una normal 2K generada para el bake, aún sin conectar.
- **Cámaras:** `CAM-Chavin_Hero`, `CAM-Chavin_Plan`, `CAM-Chavin_Core`, `CAM-Chavin_Gallery`, `CAM-Chavin_Portal`, `CAM-Chavin_Lanzon`, `CAM-Chavin_Section`.
- **Luces:** `LGT-Chavin_Sun`, `LGT-Chavin_Fill`, `LGT-Chavin_GalleryFill`, `LGT-Chavin_LanzonFill`.

## Alcance

- Explanada del sitio derivada de los cuatro puntos del plano PE-330.
- Talud perimetral, bancos de río, rampa norte y Cerro Cochas de contexto.
- Terrazas, Edificio A, Edificio B, Plaza Circular/Atrio del Lanzón, Plataforma Norte y Plaza Cuadrada.
- Edificio B con patio de ~12 × 10 m y galería dentro de la masa.
- Una secuencia de galería: corredor, cámara, dinteles, portal, ducto y hornacina.
- Lanzón como prisma ahusado de 4,5 m; sigue sin talla.
- Figura de 1,7 m en el atrio como referencia de escala.
- Materiales de piedra ashlar, plaster, tierra, agua y vegetación.
- Sin las 22 galerías, sin relieves, sin techos reconstructivos y sin acabado final.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras, `COL-` colecciones.
- La evidencia y las inferencias están en `docs/remaster/chavin/blockout-v0.5.md`, `lookdev-v0.2.md` y `terrain.md`.
- No añadir texturas de IA ni imágenes oficiales sin permiso.

## Siguiente

Crear UVs y hornear color, rugosidad y normal antes del GLB. El terreno se queda procedural por ahora. Después: Portada de las Falcónidas, relieves, cabezas clavas y LOD.
