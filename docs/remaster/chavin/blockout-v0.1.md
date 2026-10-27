# Chavín — blockout v0.1

Fecha: 27 de octubre de 2026.
Estado: **generado y guardado; revisión pendiente**. Actualizado por `blockout-v0.2.md` (pase de terreno).
Fuente: `blender/chavin/chavin_blockout_v0.1.blend` (168 KB).

## Vistas

### Hero — sureste, fachada este del Edificio A

![Hero del blockout](blockout-v0.1-hero.jpg)

### Planta — comparación con PE-330

![Planta del blockout](blockout-v0.1-plan.jpg)

### Núcleo — Edificio A, Edificio B y Plaza Circular

![Núcleo del blockout](blockout-v0.1-core.jpg)

### Galería — acceso hacia el Edificio B

![Galería del blockout](blockout-v0.1-gallery.jpg)

### Lanzón — volumen de blockout

![Lanzón del blockout](blockout-v0.1-lanzon.jpg)

## Comparación con el plano

- La explanada usa los cuatro puntos del plano PE-330: **295,9 × 313,7 m**.
- El orden del núcleo coincide con el plano: **Edificio A / Castillo al suroeste**, **Edificio B / Templo del Lanzón al norte**, **Plaza Circular al este de B**, **Plataforma Norte al noreste** y **Plaza Cuadrada al sureste**.
- El acceso principal se representa desde el norte.
- Las huellas de los edificios no están acotadas en el plano de trabajo: son **inferidas** y se ajustarán en la revisión.

## Qué contiene

| Elemento | Blockout | Evidencia |
|---|---|---|
| Explanada del sitio | 295,9 × 313,7 m; 3 m de espesor | Cuatro puntos del plano PE-330 |
| Terrazas | 210 × 170 / 145 × 120 / 95 × 75 m | Inferido a partir del plano |
| Edificio A / Pirámide Mayor / “Castillo” | 70 × 80 m; 4 terrazas + cima; ~22,5 m + 2 m | Altura documentada; huella inferida |
| Portada de las Falcónidas | Pórtico y puerta oscura en fachada este | Documentado; simplificado |
| Edificio B / Templo del Lanzón | Base en U de 50 × 40 m; tres niveles | Huella y altura inferidas |
| Galería del Lanzón | Nicho abierto al este, dinteles, ducto y portal | Documentado; solo una secuencia |
| Lanzón | Monolito ahusado de 4,5 m | Presencia documentada; forma simplificada |
| Plaza Circular / Atrio | Radio 12,5 m; muro anular hueco de 2 m; altar | Presencia documentada; diámetro inferido |
| Plataforma Norte / Edificio D | 60 × 35 m; dos niveles | Documentado; huella inferida |
| Plaza Cuadrada / Plaza Mayor | 60 × 60 m; muros laterales | Documentado; dimensiones inferidas |
| Edificios C/E/F | Plataformas de fondo | Contexto del plano; sin detalle |
| Caminos, ríos y valle | Eje norte, Mosna/Wacheqsa, laderas | Aproximación al plano; sin DEM |
| Escala humana | Cinco referencias de 1,7 m | Interpretativo |

## Métricas

- 76 mallas, 1.798 vértices y **3.258 tris**.
- 8 colecciones: terreno, arquitectura, plazas, detalles, referencia, luces y cámaras.
- Cámaras: `CAM-Chavin_Hero`, `CAM-Chavin_Plan`, `CAM-Chavin_Core`, `CAM-Chavin_Gallery`, `CAM-Chavin_Lanzon`.
- Luces: `LGT-Chavin_Sun`, `LGT-Chavin_Fill`, `LGT-Chavin_GalleryFill`.
- Render: EEVEE, 1280×720, 32 muestras.
- Sin texturas, sin imágenes oficiales y sin geometría de IA.

## Evidencia e inferencia

**Documentado o verificado en fuentes:**

- Huella del sitio y orientación general, a partir de los puntos PE-330.
- Edificio A como Pirámide Mayor / “Castillo”, con fachada este y Portada de las Falcónidas.
- Edificio B / Templo del Lanzón y la Galería del Lanzón.
- Plaza Circular/Atrio del Lanzón, Plataforma Norte y Plaza Cuadrada.
- Altura del Edificio A: ~22,5 m + ~2 m de recintos de cima.
- Existencia de una secuencia de galerías, ductos y dinteles.

**Inferido o interpretativo:**

- Huellas de B, D, C, E y F; alturas de B y D.
- Diámetro de la Plaza Circular y dimensiones de la Plaza Cuadrada.
- Trazado exacto de terrazas, caminos, ríos y laderas.
- Distribución de vanos, dinteles, escaleras y muros.
- Forma, proporción y posición del volumen del Lanzón.
- Figuras humanas y vegetación.

## Límites de esta versión

- No hay galerías interiores completas: solo el nicho/portal de la Galería del Lanzón y un ducto.
- El Lanzón es un volumen de blockout, sin talla, rostro, relieves ni textura.
- No hay Estela Raimondi, Obelisco Tello, cabezas clavas ni otros relieves.
- No hay techos, cubiertas ni hipótesis de altura interior.
- No hay DEM fino; el terreno es una explanada con terrazas y laderas aproximadas.
- Los materiales son colores planos de blockout, no look-dev.
- La Plaza Circular es un anillo de blockout, no una reconstrucción métrica.
- No se ha comparado todavía con fotografías autorizadas ni con secciones de detalle.

## Revisión recomendada

1. Ajustar huellas y ejes de Edificio A/B contra el plano y una sección de detalle.
2. Revisar la relación Edificio B/Plaza Circular y la orientación de la galería.
3. Decidir si el terreno se modela con DEM o con laderas procedurales marcadas como inferidas.
4. Desarrollar la secuencia de galería y el Lanzón con una fuente autorizada.
5. Solo después: materiales, detalle, LOD y export.
