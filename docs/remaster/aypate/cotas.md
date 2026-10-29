# Aypate — cierre de cotas de conjunto

Fecha: 29 de octubre de 2026.
Estado: **cierre documental de conjunto cerrado; cotas finas pendientes**.
Modelo: v0.4. No se modifica geometría en este cierre.

## Alcance

Este documento cierra las **dimensiones de conjunto** que se pueden leer en el plano de 2013 y en las fuentes publicadas. No es un levantamiento topográfico nuevo ni un cierre de cotas finas de todos los recintos.

- Plano: levantamiento topográfico y arquitectónico de 2013, figura 1 de Campos Napán (2017), escala nominal 1:4000, UTM WGS84 17S.
- La figura publicada está reducida; se usó una copia de trabajo local y no se incorpora al repositorio.
- La memoria de los 36 sectores y el original de alta resolución no son públicos.
- OpenHeritage3D tiene fotogrametría parcial (20,3 GB aérea + 72,7 GB terrestre, CC BY-NC-SA), pero no cubre todo el conjunto ni sustituye la memoria del proyecto.

## Calibración

- Barra gráfica del plano: **500 m = 579 px** en la copia de trabajo a 300 dpi.
- Factor: **1,158 px/m**; 25 m ≈ 29 px.
- Las medidas se tomaron sobre la grilla y se redondearon a 5 m; la incertidumbre de lectura es del orden de ±5–10 m en huellas grandes y ±2–3 m en edificios.
- Las cotas verticales del plano son curvas de nivel de 25 m; no sirven para niveles de piso finos.

## Tabla de cierre

| Elemento | Plano 2013 / fuente | v0.4 | Diferencia | Confianza | Decisión |
|---|---|---|---|---|---|
| Gran Plaza | Envolvente ~135 × 110 m; ~13.000–15.000 m²; trapecio | 140 × 100 m; 10.795 m² | Área dentro de la incertidumbre del plano | Media | Se conserva v0.4; no se justifica v0.5 |
| Plaza central menor | ~2.400 m² (Patrimonio Virtual) | No modelada como plaza separada | — | Media | Se documenta como espacio menor, no como la Gran Plaza |
| Ushnu | 30 × 30 m; >5 m; 25 peldaños; terraza 20,7 × 23,7 m; pozo 6,6 × 2,14 m | 30 × 30 m; 5,3 m; 25 peldaños; terraza 20,7 × 23,7 m; pozo 6,6 × 2,14 m | Sin diferencia significativa | Alta | Cerrado |
| Kallanka | 115 × 12 m; 13 accesos | 115 × 12 m; 13 accesos | Sin diferencia significativa | Alta | Cerrado |
| Acllawasi | Envolvente ~75 × 75 m; cuatro canchas | 100 × 64 m; cuatro canchas | Envolvente interpretativa; área compatible dentro de la lectura | Media-baja | Se conserva; planta fina pendiente |
| Palacio | Envolvente ~50 × 100 m; recintos alrededor de patio | 64 × 52 m | Diferencia de huella; función y límites no concluyentes | Baja | No se cambia sin original |
| Colcas | Edificios alargados ~50 × 7 m, al norte | Tres cuerpos de 52 × 7 m | Compatible | Media | Cerrado como huella |
| Terraza monumental | ~500 × 300 m | ~500 × 300 m | Sin diferencia significativa | Alta | Cerrado |
| Qhapaq Ñan | 8 m; ramal alterno 6 m | 8 m / 6 m | Sin diferencia | Alta | Cerrado |
| Fuente ritual | Estructura rectangular pequeña, seis hornacinas | 8 × 6 m; seis hornacinas | Huella compatible; detalles interpretativos | Media | Cerrado como huella |
| Andenes | Terrazas siguiendo el relieve | Cinco fajas al este | No medible con precisión | Baja | Se conserva como lectura |
| Cima / Templo del Sol | Documentados, fuera del núcleo | No modelados | — | Baja | Diferido |
| Techos y alturas originales | No conservados | No reconstruidos | — | — | Fuera de alcance |

## Resultado

- **Cierre de conjunto:** cerrado con las dimensiones de la tabla.
- **Cotas finas:** abiertas. Requieren la memoria de 36 sectores, el plano original o un levantamiento propio.
- **Modelo:** v0.4 se mantiene. Las diferencias de acllawasi y palacio no superan la incertidumbre de la fuente y no justifican rehacer el GLB.
- **Plaza:** la Gran Plaza del plano no es la plaza central de ~2.400 m²; el modelo representa la explanada mayor.
- **Vertical:** no hay cotas de nivel fiables más allá de las alturas publicadas del ushnu y de la lectura de curvas de nivel.

## Evidencia pendiente

1. Memoria descriptiva de los 36 sectores y plano original en alta resolución.
2. Levantamiento propio o fotogrametría completa del núcleo.
3. Niveles de piso y secciones de los recintos periféricos.
4. Cima del cerro y Templo del Sol.
5. QA en hardware real, que es un gate independiente.
