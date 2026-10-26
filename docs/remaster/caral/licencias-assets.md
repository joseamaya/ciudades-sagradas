# Auditoría de assets de Caral

## Resultado

Los GLB publicados de Caral —v1 y v2— no contienen texturas de IA. Todas las imágenes provienen de los scripts procedurales del proyecto o del bake del high-poly propio.

## Remaster v1

Materiales procedurales con textura:

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

Materiales sin imagen: `MAT-Caral_Remaster_Wood`, `MAT-Caral_Water`, `MAT-Caral_Fire`, `MAT-Caral_Cotton`, `MAT-Caral_Skin`, `MAT-Caral_Shicra` y `MAT-Caral_Stone_Dark`.

Verificación: GLB de 20 materiales y 31 imágenes WebP; nombres `MAT-Caral_Remaster_*` o materiales sin imagen.

## Remaster v2

- LOD0 conserva los materiales procedurales del remaster, más `MAT-Caral_Remaster_Mortar` sin imagen.
- LOD1 usa nueve materiales horneados `MAT-Caral_LOD1_*` y un atlas 2K por región con base color y normal.
- El atlas se generó desde el high-poly propio con Cycles; no incorpora imágenes externas ni de IA.
- No se añadieron fotografías de UNESCO, ICOMOS o Ministerio de Cultura.

## Alcance

- **Remaster v1:** limpio, sin texturas de IA.
- **Remaster v2:** limpio; atlas propio horneado desde geometría del proyecto.
- **Piloto histórico:** conserva texturas de IA; no se publica y queda pendiente de archivo definitivo.

Ver también `docs/licencias.md`, `CREDITS.md` y `docs/remaster/caral/release-v2.md`.
