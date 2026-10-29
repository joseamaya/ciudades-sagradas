# Aypate — auditoría de escala v0.4

Fecha: 29 de octubre de 2026.
Estado: **v0.4 en preview; dimensiones contrastadas con el plano de 2013 y fuentes publicadas**.

## Método

- Plano base: levantamiento topográfico y arquitectónico de 2013, figura 1 de Campos Napán (2017), escala 1:4000.
- La grilla del plano es UTM, zona 17S, con celdas de 25 m; la barra gráfica va de 0 a 500 m.
- Las medidas del plano se tomaron sobre la grilla y se contrastaron con las descripciones publicadas. No se copió la figura al repositorio.
- La memoria de 36 sectores y el original de alta resolución no son públicos; las cotas finas siguen pendientes.

## Tabla de dimensiones

| Elemento | Plano 2013 / fuente | v0.3 | v0.4 | Decisión |
|---|---|---|---|---|
| Gran Plaza | Trapecio de ~140 × 95 m; ~13.000 m² de envolvente | 140 × 100 m; 10.795 m² | 140 × 100 m; 10.795 m²; muro perimetral bajo | Se conserva la Gran Plaza del plano; el dato de ~2.400 m² de Patrimonio Virtual se refiere a una plaza central menor, no al total |
| Ushnu | 30 × 30 m; >5 m; 25 peldaños; terraza superior 20,7 × 23,7 m | Base 30 × 30; terraza 11 × 11; 5 peldaños; 1,4 m | Base 30 × 30; terraza 20,7 × 23,7; 25 peldaños; pozo 6,6 × 2,14 | Corregido con Campos Napán 2017 y Polia |
| Kallanka | 115 × 12 m; 13 accesos | 120 × 18 m | 115 × 12 m; 13 accesos | Corregido con Huisa Palomino / Qhapaq Ñan |
| Acllawasi | Cuatro canchas con patios; envolvente no publicada | Bloque de 100 × 64 m | 100 × 64 m dividido en cuatro canchas | Envolvente interpretativa; se documenta la compartimentación |
| Terraza monumental | ~500 × 300 m | Meseta plana ~560 × 600 m | Meseta ~500 × 300 m | Ajustada; el terreno total baja a 600 × 600 m |
| Qhapaq Ñan | 8 m; ramal alterno 6 m | 8 m / 6 m | 8 m / 6 m | Sin cambio |
| Altura de cámara hero | — | 85 m | 18 m de cámara, 10 m sobre la plaza | La escala humana vuelve a leerse |
| Figuras humanas | — | 2 | 6 | Referencia de escala, no reconstrucción de población |

## Lectura

La v0.3 no era falsa por el tamaño de la Gran Plaza: el plano muestra una explanada de escala semejante. El problema era la **lectura**: una superficie de arcilla sin límites, un muro perimetral ausente, una cámara a 85 m, un ushnu con terraza superior demasiado pequeña y una kallanka demasiado ancha. La v0.4 corrige esos puntos y mantiene la incertidumbre de las cotas finas.

## Límites

- La planta del acllawasi, el palacio, las colcas y los recintos periféricos sigue siendo una lectura de conjunto.
- El pozo de ofrendas se marca como estructura semihundida; no se reconstruye su contenido.
- No se reconstruyen techos, alturas perdidas ni recintos sin planta.
- No hay QA en hardware real; el bench usa SwiftShader.
