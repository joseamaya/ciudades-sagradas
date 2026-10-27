# Chavín — escenas de blockout y look-dev

## Archivo

- **Fuente de la Portada:** `chavin_portada_v0.1.blend`, 7,7 MB.
- **Preview LOD0/LOD1:** `chavin_lod0.blend` y `chavin_lod1.blend`, derivados locales fusionados por capa; se regeneran con `scripts/build_chavin_lod.py` y no se versionan por tamaño.
- **Base texturizada:** `chavin_textured_v0.2.blend`, 4,2 MB.
- **Texturizado anterior:** `chavin_textured_v0.1.blend`, 3,3 MB (histórico).
- **Look-dev anterior:** `chavin_lookdev_v0.2.blend`, 585 KB (histórico).
- **Base de escala:** `chavin_blockout_v0.5.blend`, 176 KB.
- **Versiones anteriores:** `chavin_blockout_v0.4.blend` (patio B), `chavin_blockout_v0.3.blend` (galería), `chavin_blockout_v0.2.blend` (terreno), `chavin_blockout_v0.1.blend` (masas).
- **Estado:** preview web v0.1 con LOD0 de 14.158 tris y LOD1 de 9.422 tris; blockout v0.5, texturizado UV v0.2 y Portada v0.1 aceptados como base.
- **Escala:** metros; el preview usa `scale: 0.08` en `city.json` y `minDistance: 0.25` para las cámaras de detalle.
- **Contenido:** 132 mallas, 7.381 vértices, 14.146 tris y 9 colecciones.
- **Portada:** 47 mallas, 5.292 vértices y 10.364 tris; columnas de 2,30 m, jambas trilíticas, friso de 6,48 m, ocho falcónidas y un escalón de acceso inferido.
- **UVs:** piedra ashlar con proyección de cubo por cara; Portada con smart UV; texturas con repetición.
- **Texturas:** ashlar v2 en `blender/textures/chavin/chavin_ashlar_v2_*` y piedra labrada en `chavin_portada_v1_*`; generadores `scripts/make_chavin_materials_v2.py` y `scripts/make_chavin_portal_materials.py`; empaquetadas.
- **Materiales:** 12; ashlar claro/oscuro, piedra labrada clara/oscura, plaster, tierra, agua, vegetación y galería.
- **Cámaras:** `CAM-Chavin_Hero`, `Plan`, `Core`, `Gallery`, `Portal`, `Lanzon`, `Section`, `CAM-Chavin_PortadaFalconidas`, `CAM-Chavin_PortadaFalconidas_3q` y `CAM-Chavin_PortadaContext`.
- **LOD:** 4 mallas fusionadas por capa (`city`, `terrain`, `props`, `reference`); LOD0 544.756 B, LOD1 466.708 B; 15 draw calls.
- **Luces:** `LGT-Chavin_Sun`, `Fill`, `GalleryFill`, `LanzonFill` y `LGT-Chavin_PortadaFill`.

## Alcance

- Explanada del sitio derivada de los cuatro puntos del plano PE-330.
- Talud perimetral, bancos de río, rampa norte y Cerro Cochas de contexto.
- Terrazas, Edificio A, Edificio B, Plaza Circular/Atrio del Lanzón, Plataforma Norte y Plaza Cuadrada.
- Edificio B con patio de ~12 × 10 m y galería dentro de la masa.
- Una secuencia de galería: corredor, cámara, dinteles, portal, ducto y hornacina.
- Lanzón como prisma ahusado de 4,5 m; sigue sin talla.
- Portada de las Falcónidas: vano, columnas, jambas, friso, cornisa, relieves interpretativos y escalón de acceso inferido.
- Figura de 1,7 m en el atrio como referencia de escala.
- Materiales de piedra ashlar, piedra labrada, plaster, tierra, agua y vegetación.
- Sin las 22 galerías, sin dintel de la Portada, sin escalera completa, sin techos reconstructivos y sin acabado final.

## Convenciones

- `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras, `COL-` colecciones.
- La evidencia y las inferencias están en `docs/remaster/chavin/blockout-v0.5.md`, `lookdev-v0.2.md`, `textured-v0.1.md`, `textured-v0.2.md`, `portada-v0.1.md`, `web-preview.md` y `terrain.md`.
- LOD: `scripts/build_chavin_lod.py` y `scripts/export_chavin_lod.py`; WebP 80, Draco y extras de capa.
- No añadir texturas de IA ni imágenes oficiales sin permiso.

## Siguiente

Continuar con high-poly y QA en hardware real. Dintel omitido, escalera de una grada y relieves abstractos quedan como decisiones documentadas. El terreno se queda procedural por ahora.
