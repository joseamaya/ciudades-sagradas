# Narihualá — planta y cotas de control

Fecha: 29 de octubre de 2026.
Estado: **envolvente oficial y cotas de control documentadas; plano arqueológico de sectores pendiente**.
Modelo: no iniciado. No se abre Blender hasta resolver la planta de los sectores I–III.

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

Las fuentes no coinciden en la numeración:

- **RVM 2023:** sector I = mayor volumen y altura; sector II = parte intermedia; sector III = tres plataformas superpuestas y único sector investigado.
- **Mincetur 364:** sector I = montículo menor al oeste; sector II = plaza y recintos; sector III = montículo mayor al este, con la capilla.

No se resuelve por mayoría ni por interpretación. Hasta tener el plano arqueológico, el modelo no debe asignar sectores I/II/III. Se usan nombres descriptivos: **montículo oeste**, **plaza central**, **montículo este**.

## Lo que falta para abrir Blender

1. **Plano arqueológico de sectores**, no solo el plano perimétrico. La RVM aprueba el plano `PP-021-MC-DGPA-DSFL-2023`, pero el expediente técnico y el plano de detalle no están publicados.
2. Huellas y cotas de los dos montículos.
3. Ancho y trazado de rampas, corredores y tres hileras de muros del sector II.
4. Niveles de plataforma y relación entre la capilla y la cima.
5. Confirmación de la sectorización oficial.

## Decisiones

- **Capilla:** se documenta como añadido republicano. No se modela en el núcleo prehispánico; si se incluye, va en capa `later`, desactivada por defecto.
- **Museo:** fuera de alcance.
- **Licencias:** se citan las fuentes oficiales y no se copian fotografías ni planos. Renders y geometría propios; sin texturas de IA.
- **Presupuesto y recorrido:** se mantienen los del plan, pero el blockout queda bloqueado por la planta.
- **Modelo:** no se inicia.

## Próxima acción

Solicitar a la Dirección Desconcentrada de Cultura de Piura / Dirección de Catastro la copia del expediente técnico y del plano arqueológico de sectores. Mientras no llegue, Narihualá queda en Fase 0 y no se modela.
