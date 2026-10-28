# Chavín — escenas de blockout, look-dev y high-poly

## Archivo

- **Fuente de la Portada:** `chavin_portada_v0.1.blend`, 7,7 MB.
- **Fuente high-poly:** `chavin_highpoly_v0.4.blend`, 13,4 MB; deriva de v0.3 y sustituye las columnas de la Portada con `scripts/build_chavin_portada_columns.py`. El Lanzón viene de `scripts/build_chavin_lanzon_scan_v0_3.py`; el escaneo original no se versiona. v0.3 se conserva como versión anterior.
- **Preview LOD0/LOD1:** `chavin_lod0.blend` y `chavin_lod1.blend`, derivados locales fusionados por capa; se regeneran con `scripts/build_chavin_lod.py` y no se versionan por tamaño.
- **Base texturizada:** `chavin_textured_v0.2.blend`, 4,2 MB.
- **Texturizado anterior:** `chavin_textured_v0.1.blend`, 3,3 MB (histórico).
- **Look-dev anterior:** `chavin_lookdev_v0.2.blend`, 585 KB (histórico).
- **Base de escala:** `chavin_blockout_v0.5.blend`, 176 KB.
- **Versiones anteriores:** `chavin_blockout_v0.4.blend` (patio B), `chavin_blockout_v0.3.blend` (galería), `chavin_blockout_v0.2.blend` (terreno), `chavin_blockout_v0.1.blend` (masas).
- **Estado:** preview web v0.1 con pase high-poly v0.4; LOD0 de 250.866 tris y LOD1 de 28.499 tris; blockout v0.5, texturizado UV v0.2 y Portada v0.1 aceptados como base.
- **Escala:** metros; el preview usa `scale: 0.08` en `city.json` y `minDistance: 0.1` para el primer plano del Lanzón.
- **Contenido:** 2.813 mallas y ~250.866 tris en la fuente high-poly; 9 colecciones.
- **Portada:** columnas de 2,30 m con fustes acanalados interpretativos, jambas trilíticas, friso de 6,48 m, ocho falcónidas con relieve y un escalón de acceso inferido.
- **UVs:** piedra ashlar con proyección de cubo por cara; Portada con smart UV; texturas con repetición.
- **Texturas:** ashlar v2 en `blender/textures/chavin/chavin_ashlar_v2_*` y piedra labrada en `chavin_portada_v1_*`; generadores `scripts/make_chavin_materials_v2.py`, `scripts/make_chavin_portal_materials.py` y `scripts/make_chavin_terrain_materials.py`; empaquetadas.
- **Materiales:** ashlar claro/oscuro, ashlar high-poly A/B/C, piedra labrada clara/oscura, plaster, tierra, agua, vegetación, galería y Lanzón.
- **Cámaras:** `CAM-Chavin_Hero`, `Plan`, `Core`, `Gallery`, `Portal`, `Lanzon`, `Section`, `CAM-Chavin_PortadaFalconidas`, `CAM-Chavin_PortadaFalconidas_3q`, `CAM-Chavin_PortadaContext` y las cámaras de QA `CAM-Chavin_HP_*`.
- **LOD:** 4 mallas fusionadas por capa (`city`, `terrain`, `props`, `reference`); LOD0 1.963.916 B / 250.866 tris / 19 draw calls, LOD1 788.012 B / 28.499 tris / 15 draw calls; terreno con texturas propias 1K.
- **Luces:** `LGT-Chavin_Sun`, `Fill`, `GalleryFill`, `LanzonFill`, `LGT-Chavin_PortadaFill` y `LGT-Chavin_HP_LanzonFill` (solo QA).

## Alcance

- Explanada del sitio derivada de los cuatro puntos del plano PE-330.
- Talud perimetral, bancos de río, rampa norte y Cerro Cochas de contexto.
- Terrazas, Edificio A, Edificio B, Plaza Circular/Atrio del Lanzón, Plataforma Norte y Plaza Cuadrada.
- Edificio B con patio de ~12 × 10 m y galería dentro de la masa.
- Una secuencia de galería: corredor, cámara, dinteles, portal, ducto y hornacina.
- Lanzón de 4,5 m derivado del escaneo CyArk/Google Arts & Culture, decimado y con material granítico propio; licencia CC BY-NC-SA 4.0, sin uso comercial.
- Portada de las Falcónidas: vano, columnas, jambas, friso, cornisa, relieves interpretativos y escalón de acceso inferido.
- Figura de 1,7 m en el atrio como referencia de escala.
- Materiales de piedra ashlar, piedra labrada, plaster, tierra, agua y vegetación.
- Sin las 22 galerías, sin dintel de la Portada, sin escalera completa, sin techos reconstructivos y sin acabado final.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras, `COL-` colecciones.
- La evidencia y las inferencias están en `docs/remaster/chavin/blockout-v0.5.md`, `lookdev-v0.2.md`, `textured-v0.1.md`, `textured-v0.2.md`, `portada-v0.1.md`, `highpoly-v0.1.md`, `highpoly-v0.2.md`, `highpoly-v0.3.md`, `highpoly-v0.4.md`, `web-preview.md` y `terrain.md`.
- LOD: `scripts/build_chavin_lod.py` y `scripts/export_chavin_lod.py`; WebP 80, Draco y extras de capa. Columnas: `scripts/build_chavin_portada_columns.py`.
- No añadir texturas de IA ni imágenes oficiales sin permiso.
- El Lanzón derivado del escaneo es CC BY-NC-SA 4.0; el código sigue en MIT. Ver `LICENSE-ASSETS.md`.

## Siguiente

QA en hardware real y deuda de detalle: dintel omitido, escalera de una grada, relieves interpretativos y mampostería de fachada como relieve aplicado. El frente del Lanzón requiere una luz de galería y un plano cercano menor para verse en el recorrido. El terreno se queda procedural por ahora.
