# Narihualá — planta y cotas de control

Fecha: 29 de octubre de 2026; búsqueda de plano actualizada el 4 de noviembre de 2026.
Estado: **preview interpretativo v0.2; envolvente legal y SIGRID documentados; búsqueda de plano de sectores sin resultado público; cierre bloqueado**.
Modelo: v0.2 interpretativo; no es cierre de cotas ni plano arqueológico.

## Lo que sí está documentado

| Dato | Valor | Fuente | Confianza |
|---|---|---|---|
| Área legal | **62.959,36 m²** (6,295936 ha) | RVM N.º 000084-2023-VMPCIC/MC | Alta |
| Perímetro legal | **1.014,38 m** | RVM 2023 | Alta |
| Centroide UTM | **534.788,2567 E / 9.414.759,7812 N**, WGS84 17S | RVM 2023 | Alta |
| Área turística citada | ~60.000,04 m² (6 ha) | Mincetur 364 | Media |
| Plaza | **60 × 40 m**; 2.400 m² | Mincetur 364 / RVM | Alta |
| Altura máxima del montículo | ~40 m | RVM 2023 / fichas | Media |
| Adobe | ~60 × 30 × 10 cm | Mincetur 364 | Alta |
| Muros | 1,10–1,20 m de ancho | Mincetur 364 | Alta |
| Muros del sector I | 1,60 m de espesor y más de 2 m de altura | RVM 2023 | Media; conflicto de sectorización |
| Sector II | Tres hileras de muros paralelos, relleno de arena, rampas y corredores | RVM 2023 / Mincetur | Media |
| Capilla | Republicana, sobre la plataforma oriental | Mincetur 364 / SciELO 2023 | Alta |
| Museo | Infraestructura contemporánea al pie del sitio | Mincetur 364 | Alta |

## Conflicto de sectorización

Las fuentes no coinciden ni en el número ni en la numeración:

- **RVM 2023:** tres sectores. Sector I = mayor volumen y altura; sector II = parte intermedia; sector III = tres plataformas superpuestas y único sector investigado.
- **Mincetur 364:** tres sectores. Sector I = montículo menor al oeste; sector II = plaza y recintos; sector III = montículo mayor al este, con la capilla.
- **Tríptico del Museo de Sitio (Ministerio de Cultura):** tres sectores. Sector I = montículo mayor con la capilla; sector II = parte intermedia con la plaza; sector III = montículo menor.
- **Arnaldoa 30(3), 2023 (SciELO):** menciona **ocho sectores** en el resumen en inglés, sin plano ni lista.
- **PROMPERÚ:** menciona **cuatro sectores**, sin plano.

No se resuelve por mayoría ni por interpretación. Hasta tener el plano arqueológico, el modelo no debe asignar sectores I/II/III. Se usan nombres descriptivos: **montículo oeste**, **plaza central**, **montículo este**.

## Búsqueda de plano de sectores (4 de noviembre de 2026)

Se revisaron las fuentes públicas disponibles:

| Fuente | Qué aporta | Qué falta |
|---|---|---|
| RVM N.º 000084-2023-VMPCIC/MC | Aprueba el Expediente Técnico con Memoria Descriptiva, Ficha Técnica y **Plano Perimétrico** `PP-021-MC-DGPA-DSFL-2023`; área y perímetro legales | El PDF de la RVM tiene 5 páginas de texto; no incluye el plano perimétrico ni un plano de sectores |
| Mincetur 364 | Tres sectores y la plaza de 60 × 40 m | Sin plano; su numeración contradice a la RVM y al tríptico |
| Tríptico del Museo de Sitio | Tres sectores con la capilla en el sector I | Sin plano; contradice a Mincetur |
| RVM 2023 / Urbipedia | Tres sectores funcionales | Sin plano de detalle |
| Arnaldoa 30(3), 2023 | Dice “ocho sectores” en el resumen | Sin plano, sin lista y sin desarrollo en el texto |
| PROMPERÚ | Dice “cuatro sectores” | Sin plano ni numeración |
| SIGRID 2018 | Ortofoto 3,8 cm/px y DTM 0,19 m/px | El montículo oeste está cubierto por el museo; la plaza no tiene borde arqueológico legible |

**Conclusión:** no existe un plano arqueológico de sectores publicado y coherente. El plano aprobado por la RVM es perimétrico, no sectorial. La sectorización 3/4/8 sigue en conflicto y no se puede asignar sin inventar.

**Siguiente acción:** solicitar copia certificada del Expediente Técnico y, si existe, el plano arqueológico de detalle al Ministerio de Cultura (DDC Piura) o al Proyecto Integral Narihualá. Mientras no se obtenga, no se cambia la geometría ni se etiquetan sectores.

## Lo que falta para abrir Blender

1. **Plano arqueológico de sectores**, no solo el plano perimétrico. La RVM aprueba el plano `PP-021-MC-DGPA-DSFL-2023`, pero el expediente técnico y el plano de detalle no están publicados.
2. Huellas y cotas de los dos montículos.
3. Ancho y trazado de rampas, corredores y tres hileras de muros del sector II.
4. Niveles de plataforma y relación entre la capilla y la cima.
5. Confirmación de la sectorización oficial y de su numeración.

## Decisiones

- **Capilla:** se documenta como añadido republicano. No se modela en el núcleo prehispánico; si se incluye, va en capa `later`, desactivada por defecto.
- **Museo:** fuera de alcance.
- **Licencias:** se citan las fuentes oficiales y no se copian fotografías ni planos. Renders y geometría propios; sin texturas de IA.
- **Presupuesto y recorrido:** se mantienen; el blockout v0.2 se ejecutó como preview interpretativo, no como cierre de planta.
- **Modelo:** no se inicia.

## Próxima acción

No se solicitó el expediente. Se usó la ortofoto/DTM libres de SIGRID y se construyó un preview interpretativo v0.2; el cierre de cotas finas sigue pendiente.

## SIGRID 2018 — ortofoto y DTM

Se descargaron los productos libres de CENEPRED para Narihualá, Campiña y Pedregal:

- Orto mosaico: <https://sigrid.cenepred.gob.pe/sigridv3/documento/6778>
- Modelo digital del terreno: <https://sigrid.cenepred.gob.pe/sigridv3/documento/6779>
- Curvas de nivel: <https://sigrid.cenepred.gob.pe/sigridv3/documento/5367>
- Vuelo: 24/05/2018; DJI Inspire 2; RGB; puntos de control en tierra.
- Ortofoto decodificada: **0,038 m/píxel**, EPSG:32717.
- DTM decodificado: **0,19 m/píxel**, EPSG:32717.
- Recorte de trabajo: 266 × 266 m, desde 534.656,93 E / 9.414.872,45 N.

### Lectura de la ortofoto

- El **montículo este** con la capilla republicana es visible.
- El **montículo oeste** está cubierto por el museo y las construcciones modernas; no se puede leer su huella.
- La **plaza de 60 × 40 m** no tiene un borde arqueológico legible en la ortofoto: el área está erosionada y transformada.
- Se ven terrazas, cárcavas y caminos, pero no un conjunto de muros continuo.
- La capilla y el cementerio moderno ocupan la cima del montículo este.

### Cotas del DTM

| Punto | Cota aproximada |
|---|---:|
| Base norte | 24,3 m |
| Base sur | 23,6 m |
| Montículo oeste / museo | 31,1 m |
| Plaza aproximada | 37,5 m |
| Cima del montículo este | 42,7 m |
| Capilla | 42,3 m |

La diferencia entre la base y la cima es de unos **19 m**; el dato de “40 m” de las fichas corresponde a la altura del conjunto sobre el valle, no a un edificio de 40 m.

### Consecuencia

La ortofoto libre **no cierra la planta arqueológica**. Permite localizar los montículos y medir alturas, pero no separar los sectores I–III ni reconstruir la plaza, las rampas y los recintos con la precisión del estándar. El cierre de cotas sigue bloqueado; el preview v0.2 se construyó como interpretación explícita, no como plano arqueológico.
