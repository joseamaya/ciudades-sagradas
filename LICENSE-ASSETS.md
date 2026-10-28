# Licencias de assets

Este repositorio combina código MIT con assets 3D de distinta procedencia. El código
sigue bajo [`LICENSE`](LICENSE) (MIT). Los assets descritos aquí no se relicencian a MIT.

## Lanzón de Chavín (derivado CyArk)

- **Archivo fuente:** escaneo 3D `Lnzon_Chavin_De_Huantar_glb`, descargado de
  <https://storage.googleapis.com/culturalinstitute-3d-serving/manual-testing/000-PROD-DONT-DELETE/240391958/3QFU2nR_dVV9Lg/model.glb>
  (CyArk / Google Arts & Culture, Open Heritage).
- **SHA256 del GLB original:** `be73151cba3b2c144f712a6a0d82820d092218dba2b3741fb81993ab1973dcec`
  (`9.551.212` bytes). El GLB original **no se versiona** en este repositorio.
- **Derivados publicados:** `blender/chavin/chavin_highpoly_v0.3.blend`,
  `public/cities/chavin/model_lod0.glb`, `public/cities/chavin/model_lod1.glb` y las
  imágenes de documentación `docs/remaster/chavin/highpoly-v0.3-*`.
- **Licencia de los derivados:** **CC BY-NC-SA 4.0**
  (<https://creativecommons.org/licenses/by-nc-sa/4.0/>).
- **Atribución requerida:** «Lanzón de Chavín, escaneo 3D de CyArk / Google Arts &
  Culture; adaptación geométrica del proyecto Ciudades Sagradas».
- **Cambios:** malla decimada de 50.000 a 12.000 triángulos, reparada y reorientada; se
  descartó la textura fotográfica original y se usó un material granítico propio. La
  geometría derivada conserva la licencia de la obra original.
- **Restricción:** CC BY-NC-SA 4.0 **no permite uso comercial** de estos derivados.
  Cualquier uso comercial requiere una licencia aparte de CyArk/Google Arts & Culture.
  La licencia MIT del código no se extiende a estos assets.
- **Compartir igual:** si redistribuyes o modificas la geometría del Lanzón, debes
  mantener CC BY-NC-SA 4.0 y atribuir a CyArk / Google Arts & Culture y a esta
  adaptación.

## Resto de assets

- Geometría arquitectónica, terreno y materiales procedurales: generados por el
  proyecto, sin texturas de IA.
- Texturas ashlar, Portada y terreno: generadas por el proyecto; se registran con
  hash y licencia en [`docs/fuentes/registro-assets.csv`](docs/fuentes/registro-assets.csv).
- No se incorporan fotografías de UNESCO, Ministerio de Cultura, ICOMOS ni museos sin
  permiso escrito.

## Uso del visor

El aviso de la ficha de Chavín enlaza esta atribución y la licencia del Lanzón. Para
un despliegue comercial hay que sustituir el Lanzón por una malla propia o negociar
una licencia con CyArk/Google Arts & Culture.
