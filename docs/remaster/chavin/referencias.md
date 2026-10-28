# Referencias y licencias — Chavín de Huántar

Fecha: 27 de octubre de 2026.
Estado: **Fase 0 cerrada; tablero verificado; permisos de publicación pendientes**.

## Fuentes públicas

| Fuente | Tipo | Uso previsto | Imágenes | Estado |
|---|---|---|---|---|
| [UNESCO 330](https://whc.unesco.org/en/list/330/) | Ficha y documentos | Cronología, valores, contexto | No copiar sin permiso | Consultada |
| [UNESCO — documentos](https://whc.unesco.org/en/list/330/documents) | Expediente y evaluación | Arquitectura, conservación | No copiar sin permiso | Consultada |
| [ICOMOS 1985](https://whc.unesco.org/document/153206) | Evaluación | Evidencia y estado del sitio | No copiar sin permiso | 403 en el entorno; revisar manualmente |
| [ICOMOS — seguimiento 1999](https://whc.unesco.org/document/139527) | Informe | Conservación, turismo y riesgos | No copiar sin permiso | Consultada |
| [Periodic Reporting 2024](https://whc.unesco.org/document/216550) | Informe periódico | Superficie, gestión y conservación | No copiar sin permiso | Consultada |
| [Ministerio de Cultura — Chavín](https://patrimoniomundial.cultura.pe/sitiosdelpatrimoniomundial/sitio-arqueol%C3%B3gico-chav%C3%ADn) | Ficha oficial | Datos generales | No copiar sin permiso | Consultada |
| [Expediente de Nominación (Mincul)](https://patrimoniomundial.cultura.pe/sites/default/files/pm/pdf/CHAVIN%20Sitio%20arqueologico.pdf) | PDF oficial | Ficha y metadatos | No copiar sin permiso | Consultada |
| [Plano del Sitio (Mincul)](https://patrimoniomundial.cultura.pe/sites/default/files/pm/pdf/PE-330%20Chav%C3%ADn%20WGS84.pdf) | Plano PDF | Huella y ubicación | No copiar sin permiso | Consultada; puntos usados en blockout v0.2 |
| [Plan de Manejo 2020](https://patrimoniomundial.cultura.pe/sites/default/files/pm/pdf/RM%20292-2020-DM-MC%20-%20ANEXO.pdf.pdf) | PDF oficial | Conservación y gestión | No copiar sin permiso | Consultada |
| [Decisiones del Comité](https://patrimoniomundial.cultura.pe/sites/default/files/pm/pdf/Decisiones%20Chavin%207%20a%2044%20COM.pdf) | PDF oficial | Estado de conservación | No copiar sin permiso | Consultada |
| [Museo Nacional Chavín](https://museos.cultura.pe/museos/museo-nacional-chav%C3%ADn) | Museo | Piezas y contexto | Requiere permiso | Consultada |
| [MNAAHP — sala Chavín](https://mnaahp.cultura.pe/exposiciones/salas-permanentes/chavin) | Museo | Estela, Obelisco, piezas | Requiere permiso | Consultada |
| [Stanford — John Rick](https://news.stanford.edu/stories/2016/04/stanford-archaeologist-traces-origins-authority-andes-peru) | Divulgación académica | Galerías, ritual, investigación | Uso referencial | Consultada |
| [Wikipedia — Portada de las Falcónidas](https://es.wikipedia.org/wiki/Portada_de_las_Falc%C3%B3nidas) | Enciclopedia | Medidas, componentes y dualidad | Texto CC BY-SA 4.0; no copiar | Consultada; medida secundaria |
| [Wikimedia Commons — Portada de las Falcónidas](https://commons.wikimedia.org/wiki/Category:Portada_de_las_Falc%C3%B3nidas) | Fotografías | Proporciones y lectura visual | Licencia por archivo | Consultada; no incorporada |
| [CyArk / Google Arts & Culture — Lanzón](https://storage.googleapis.com/culturalinstitute-3d-serving/manual-testing/000-PROD-DONT-DELETE/240391958/3QFU2nR_dVV9Lg/model.glb) | Escaneo 3D | Geometría y relieve del Lanzón | CC BY-NC-SA 4.0; sin uso comercial | Incorporado como malla derivada; textura fotográfica descartada |

- Los PDFs oficiales se consultaron para verificar datos; no se copian al repositorio.
- El PDF de ICOMOS 1985 devolvió 403 en el entorno de trabajo; se revisará manualmente o con otra vía.
- El plano se usó para la explanada y los ejes; faltan secciones de detalle. Las decisiones del Comité ya se revisaron.

## Material pendiente

- Planos y secciones de los templos con escala verificable.
- Levantamiento de galerías y ventilación.
- DEM o topografía del valle para pendientes y encuadre.
- Fotos de referencia con licencia o permiso para modelado.
- Sección o levantamiento métrico de la Portada que cierre el ancho de 6,48 m y el número de falcónidas (8 frente a 14 en algunas fuentes).
- Cota de la escalera de acceso y del dintel de tres piezas.
- Inventario y ubicación de esculturas in situ y en museo.
- Estado de conservación y cambios modernos del sitio.

## Política de licencias

- No se copian imágenes de UNESCO, Mincul, ICOMOS ni museos sin permiso escrito.
- Las texturas serán procedurales o CC0; se registrarán en `docs/fuentes/registro-assets.csv`.
- Las piezas de museo se representan como réplica o referencia señalizada, no como original in situ.
- Los datos y textos citan la fuente; las imágenes se sustituyen por material propio o con permiso.
- Sin texturas de IA.
- El Lanzón derivado del escaneo CyArk/Google Arts & Culture es CC BY-NC-SA 4.0; se atribuye en el visor y en `LICENSE-ASSETS.md`.

## Criterio para aprobar una referencia

- [ ] Tiene autor, institución y fecha.
- [ ] La licencia permite el uso previsto.
- [ ] Se puede citar sin copiar la imagen.
- [ ] Distingue documento, inferencia e interpretación.
- [ ] No contradice el expediente UNESCO ni la ficha del Ministerio de Cultura.
