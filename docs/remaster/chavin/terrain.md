# Chavín — decisión de terreno

Fecha: 27 de octubre de 2026.
Estado: **terreno procedural aceptado para blockout y look-dev; DEM diferido a la fase de detalle**.
Escena base: `blender/chavin/chavin_blockout_v0.5.blend`; look-dev: `blender/chavin/chavin_lookdev_v0.2.blend`.

## Decisión

Para el blockout, el look-dev v0.2 y el texturizado UV v0.2 se mantiene el terreno procedural de v0.2. No se incorpora un DEM todavía.

Motivos:

- No hay DEM descargado ni pipeline geodata instalado (`gdal`, `rasterio` y `pyproj` no están disponibles).
- Un DEM público de 30 m sirve para valle y montañas, no para la explanada arqueológica ni para las galerías.
- El terreno actual ya permite leer el conjunto y no bloquea galería, Lanzón ni materiales.
- Meter un DEM ahora añadiría licencia, descarga, reproyección, alineación y tiempo antes de resolver el núcleo hero.

## Qué es documentado y qué es inferido

**Documentado/verificado:**

- Huella del sitio y puntos del plano PE-330.
- Posición relativa de Edificios A/B, Plaza Circular, Plataforma Norte y Plaza Cuadrada.
- Presencia de los ríos Mosna y Huachecsa en el valle.

**Inferido/procedural:**

- Talud perimetral de 40 m y tapa de 0,3 m.
- Bancos de río, laderas y Cerro Cochas.
- Rampa norte de 60 m y aterrizaje en la terraza 2.
- Pendientes, alturas y espesores del terreno.

Nada de esto se presenta como topografía levantada.

## Estado geométrico

- Explanada: huella PE-330 de **295,9 × 313,7 m**.
- Talud: baja de `z=0` a `z=-2,8` en 40 m.
- Rampa norte: sube de `z≈0,1` a `z≈3,0` y aterriza en la terraza 2.
- Cerro Cochas: volumen de fondo; sombra desactivada solo para legibilidad del blockout.
- Ríos: bancos y cauce esquemáticos, sin hidrología simulada.

## Si se incorpora un DEM

La opción preferida sería **híbrida**:

1. DEM de 30 m (Copernicus GLO-30 o ALOS AW3D30) solo para valle y montañas.
2. Explanada, terrazas y núcleo arqueológico modelados aparte.
3. El DEM no reemplaza la huella PE-330 ni las plataformas.
4. Documentar fuente, licencia, resolución, fecha de descarga y transformación.
5. Evaluar el resultado antes de materiales finales.

Criterio para cambiar: que el valle procedural no sostenga el encuadre hero o que el cliente pida contexto topográfico verificable. No se cambia por defecto en el look-dev.

## Límites

- No hay curvas de nivel locales ni levantamiento propio.
- El terreno no debe citarse como reconstrucción topográfica.
- La decisión DEM queda abierta para la fase de detalle; no bloquea el texturizado UV v0.2. Si se incorpora, debe documentarse con fuente, licencia, resolución y transformación, y no reemplaza la huella PE-330 ni las plataformas.
