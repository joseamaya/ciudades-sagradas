# Auditoría de assets del remaster v1

## Resultado

El GLB del remaster v1 no contiene texturas de IA. Todas las imágenes provienen de `blender/textures/generated/remaster/` y fueron generadas por los scripts procedurales del proyecto.

## Materiales con textura procedural

- `MAT-Caral_Remaster_Plaster_White`
- `MAT-Caral_Remaster_Plaster_Yellow`
- `MAT-Caral_Remaster_Plaster_Red`
- `MAT-Caral_Remaster_Stone_Cut`
- `MAT-Caral_Remaster_Stone_Field`
- `MAT-Caral_Remaster_Sand`
- `MAT-Caral_Remaster_Earth`
- `MAT-Caral_Remaster_Terrain`
- `MAT-Caral_Remaster_Rock`
- `MAT-Caral_Remaster_Grass`
- `MAT-Caral_Remaster_Leaves`
- `MAT-Caral_Remaster_Adobe`
- `MAT-Caral_Remaster_Thatch`

## Materiales sin imagen

`MAT-Caral_Remaster_Wood`, `MAT-Caral_Water`, `MAT-Caral_Fire`, `MAT-Caral_Cotton`, `MAT-Caral_Skin`, `MAT-Caral_Shicra` y `MAT-Caral_Stone_Dark` usan color, emisión o parámetros procedurales sin textura de imagen.

## Verificación

- GLB: 20 materiales, 31 imágenes WebP.
- Nombres de materiales del GLB: solo `MAT-Caral_Remaster_*` y materiales sin imagen.
- El exportador no incluye las colecciones de juego ni materiales no usados.

## Alcance

- **Remaster v1:** limpio, sin texturas de IA.
- **Piloto histórico:** todavía contiene texturas de IA; no se publica.
