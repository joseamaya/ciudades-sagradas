# Aypate — auditoría del layout v0.2 contra el plano de 2013

Fecha: 28 de octubre de 2026.  
Estado: **auditoría cerrada; v0.2 no coincide con el plano publicado; v0.3 pendiente**.  
Alcance: comparación de relaciones espaciales, no levantamiento ni corrección del GLB.

## Fuente del plano

Carlos E. Campos Napán, *Dominando el paisaje sagrado: los incas y la construcción del ushnu de Aypate*, **Cuadernos del Qhapaq Ñan** 5 (2017), pp. 68–98.

- Figura 1: “Plano general del Complejo Arqueológico de Aypate, señalándose la localización del ushnu o Sector 11”.
- El plano lleva el rótulo **“Levantamiento topográfico y arquitectónico en el sitio arqueológico Aypate”**, UTM WGS84 Zona 17S, escala nominal 1/4000, febrero de 2013.
- URL del artículo: <https://revistas.cultura.gob.pe/index.php/cuadernosqn/article/view/499>
- PDF: <https://revistas.cultura.gob.pe/index.php/cuadernosqn/article/download/499/584>

No se copia la figura al repositorio. Se usa como referencia de comparación y se cita la fuente.

## Método

1. Extracción de la figura 1 del PDF y recorte del núcleo arquitectónico.
2. Lectura de la barra gráfica: 500 m equivalen a unos 289 px en la imagen publicada; referencia aproximada, no medida de precisión.
3. Render ortogonal superior del `aypate_highpoly_v0.2.blend`, sin terreno, vegetación ni losa de plaza, para leer huellas.
4. Comparación de las relaciones relativas alrededor de la plaza: ushnu, kallanka, acllawasi, palacio, colcas y Qhapaq Ñan.
5. Verificación de que el desajuste no se explica por una sola rotación o espejo.

La figura publicada mide 947 × 1368 px y está reducida para la revista. No tiene rótulos de sector legibles ni cotas suficientes para reconstruir dimensiones finas. Por eso la auditoría distingue **topología** de **medida**.

## Resultado

| Elemento | Plano de 2013 | v0.2 | Desajuste |
|---|---|---|---|
| Plaza | Trapecio, con el eje mayor aproximadamente NE–SO | Rectángulo de 120 × 90 m, eje E–O | Forma y orientación |
| Ushnu | Borde **este/noreste** de la plaza | Borde **oeste** | Posición cardinal invertida |
| Kallanka | Edificio largo en el borde **oeste/noroeste**, eje N–S | Edificio largo al **sur**, eje E–O | Posición y giro cercanos a 90° |
| Acllawasi | Conjunto al **sur/suroeste** de la plaza | Conjunto al **este** | Posición |
| Palacio | Conjunto al **noroeste**, detrás de la kallanka | Recintos al **sur**, detrás de la kallanka | Posición |
| Colcas | Edificios alargados al **norte**, junto al camino | Al **noroeste** | Posición |
| Qhapaq Ñan | Acceso desde el **sur**, recorre el borde oeste | Eje recto al **norte** | Posición y trazado |
| Fuente ritual | Próxima al ushnu; identificación exacta no concluyente en la figura | Al suroeste del núcleo | No verificable |

## Confianza

- **Alta:** plaza, ushnu, kallanka y acllawasi; son legibles y su relación mutua es clara.
- **Media:** palacio y colcas; la lectura funcional es compatible, pero la figura no rotula cada recinto.
- **Baja:** fuente ritual y recintos menores; no se usan para la conclusión principal.

## Lectura

- El desajuste es **macro y sistemático**: no es una diferencia de detalle ni un pequeño error de escala.
- No se corrige con una rotación o un espejo simple, porque las relaciones entre ushnu, kallanka, acllawasi y palacio no guardan la misma geometría relativa.
- La v0.2 conserva valor como **maqueta interpretativa** y como ejercicio de high-poly, materiales y LOD. No debe presentarse como layout documentado.
- La auditoría no cambia el GLB: mover una pieza aislada empeoraría la lectura. La corrección requiere rehacer el blockout y el recorrido.

## Límites

- La escala nominal 1/4000 y la barra gráfica del PDF reducido no coinciden de forma limpia; no se usan para cotas de precisión.
- La figura no permite leer todos los sectores ni distinguir con seguridad algunos recintos periféricos.
- La memoria descriptiva de los 36 sectores y el levantamiento original de alta resolución siguen sin ser públicos.
- La identificación de la fuente ritual y de algunos recintos menores queda como **no concluyente**.

## Consecuencia

La v0.2 queda marcada como **layout interpretativo no coincidente** con el plano publicado. El siguiente paso es una **v0.3** que rehaga el blockout a partir de las relaciones del plano de 2013, reutilice los generadores de arquitectura y materiales, y vuelva a construir cámaras, recorrido y evidencia visual.

La v0.3 debe:

- fijar un norte de escena explícito;
- situar la plaza, el ushnu, la kallanka, el acllawasi, el palacio, las colcas y el camino según el plano;
- mantener fuera techos, alturas perdidas y recintos sin evidencia;
- actualizar el hero, las seis paradas, los hashes, el registro de assets y la caché;
- repetir `validate`, `build` y `bench`.

## Decisión de esta auditoría

No se modifica el GLB ni se actualizan hashes. Solo se documenta el hallazgo, se corrige la afirmación de que la planta no estaba publicada y se rebaja el estado de cumplimiento de Aypate a **parcial** hasta la v0.3.
