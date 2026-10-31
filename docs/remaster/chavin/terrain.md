# Chavín — decisión de terreno

Fecha: 31 de octubre de 2026.
Estado: **valle procedural v0.7 aceptado para preview; DEM sigue diferido**.
Escena base: `blender/chavin/chavin_highpoly_v0.7.blend`.

## Decisión

Se mantiene un terreno procedural, ahora con un valle encajado y los ríos corregidos. No se incorpora un DEM.

Motivos:

- No hay DEM descargado ni pipeline geodata instalado (`gdal`, `rasterio` y `pyproj` no están disponibles).
- Un DEM público de 30 m sirve para montañas y valle, no para la explanada arqueológica.
- La corrección principal era de lectura: el Mosna debe correr ~30 m por debajo del sitio y el Wacheqsa debe estar al norte, no al sur.
- El terreno actual permite leer el conjunto, el desnivel y la confluencia sin añadir dependencias ni licencias nuevas.

## Qué es documentado y qué es inferido

**Documentado/verificado:**

- Huella del sitio y puntos del plano PE-330.
- Posición relativa de Edificios A/B, Plaza Circular, Plataforma Norte y Plaza Cuadrada.
- Presencia y posición relativa de los ríos Mosna y Huachecsa.
- El Mosna corre unos **30 m por debajo** del Edificio A (Plan de Manejo 2020).

**Inferido/procedural:**

- Trazado fino, meandros, anchos y pendientes de los cauces.
- Bancos, terrazas aluviales, laderas, crestas y plano lejano.
- Alturas y pendientes del terreno.
- Cobertura vegetal y materiales.

Nada de esto se presenta como topografía levantada.

## Estado geométrico v0.7

- Dominio: **1300 × 1300 m**, malla de 96 × 96.
- Explanada: huella PE-330 de **295,9 × 313,7 m**, conservada.
- Mosna: al este, agua a **-26,45 m**; superficie del sitio en `z=0` y arquitectura desde `z=3`.
- Wacheqsa: al norte/noroeste, confluencia al noreste.
- Crestas: seis masas inferidas entre ~900 y ~1450 m del centro.
- Plano lejano: anillo a `z=-25,5` para cerrar el horizonte bajo niebla.
- Vegetación: 138 arbustos y 190 matas; sin árboles inventados.
- Sin DEM; el terreno no reemplaza la huella PE-330 ni las plataformas.

## Si se incorpora un DEM

La opción preferida seguiría siendo **híbrida**:

1. DEM de 30 m (Copernicus GLO-30 o ALOS AW3D30) solo para valle y montañas.
2. Explanada, terrazas y núcleo arqueológico modelados aparte.
3. El DEM no reemplaza la huella PE-330 ni las plataformas.
4. Documentar fuente, licencia, resolución, fecha de descarga y transformación.
5. Evaluar el resultado antes de materiales finales.

Criterio para cambiar: que el valle procedural no sostenga el encuadre hero o que el cliente pida contexto topográfico verificable. No se cambia por defecto en el preview.

## Límites

- No hay curvas de nivel locales ni levantamiento propio.
- Los ríos y las crestas son una lectura de escala y posición, no hidrología ni topografía.
- El terreno no debe citarse como reconstrucción topográfica.
- La explanada sigue siendo una base de blockout; no se inventaron muros perimetrales ni terrazas agrícolas.
- Cualquier DEM futuro debe documentarse con fuente, licencia, resolución y transformación.
