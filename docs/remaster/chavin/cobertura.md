# Cobertura objetivo — Chavín de Huántar

Fecha: 27 de octubre de 2026.
Estado: **blockout v0.5 aceptado; look-dev v0.2 de mampostería en revisión**.
Estándar: **ciudad representativa**.

## Definición

Chavín se considerará completo cuando estén representados los volúmenes y sectores principales con respaldo documental, las zonas hero tengan detalle suficiente y los huecos de evidencia estén señalados. No se modelarán todas las galerías, piedras o piezas de museo una por una.

La marca **Documentado** de la tabla se apoya en la ficha UNESCO 330 y/o en el Ministerio de Cultura. La planta detallada, las secciones y las alturas siguen sujetas a revisión antes del gate.

## Cobertura

| Elemento | Evidencia | Nivel objetivo | Estado | Nota |
|---|---|---|---|---|
| Edificio B / Templo del Lanzón | Documentado | Hero | Blockout | Tradicional “Templo Antiguo”; volumen, acceso y galería |
| Edificio A / Pirámide Mayor / “Castillo” | Documentado | Hero | Blockout | Tradicional “Templo Nuevo”; ~22,5 m + 2 m de cima |
| Plaza Circular Hundida / Atrio del Lanzón | Documentado | Hero | Blockout | Pavimento, gradas y escalinatas este-oeste |
| Plazas rectangulares y atrios | Documentado | Fondo | Pendiente | Lectura de conjunto |
| Galerías internas | Documentado | Hero parcial | Blockout parcial | 22 galerías / 689,70 m; una secuencia modelada en v0.5 |
| Ventilación y drenaje | Documentado | Detalle visible | Blockout parcial | Un ducto esquemático de 0,5 m; sin red completa |
| Lanzón | Documentado | Hero | Blockout | Volumen ahusado de ~4,5 m; sin talla ni textura |
| Mampostería y juntas | Inferido | Base visual | Base procedural | Ashlar 2K propio; no es levantamiento de bloques |
| Portada de las Falcónidas | Documentado | Hero | Blockout | Fachada del Edificio A |
| Estela Raimondi | Documentado | Referencia | Pendiente | Museo; requiere licencia o réplica señalizada |
| Obelisco Tello | Documentado | Referencia | Pendiente | Museo; opcional |
| Cabezas clavas | Documentado | Props/referencia | Pendiente | No todas; selección con fuente |
| Terrazas y plataformas | Documentado/inferido | Fondo | Pendiente | Blockout |
| Techos y cubiertas | Inferido | No reconstruir | Diferido | No conservados |
| Ríos Mosna y Huachecsa | Documentado/inferido | Fondo | Pendiente | Paisaje y encuadre |
| Vegetación de altura | Inferido | Props | Pendiente | Paleta de valle altoandino |
| Figuras humanas | Interpretativo | Referencia | Pendiente | Escala, no retratos |
| Área UNESCO (14,79 ha) | Documentado | Contexto | Fuera de alta fidelidad | No se modela 1:1 |

## Huecos de evidencia

| Hueco | Estado | Decisión |
|---|---|---|
| Planta detallada de todas las galerías | Pendiente de levantamiento de trabajo | Modelar solo secuencia hero |
| Secciones y alturas originales | Parcial | No inventar; usar vacíos o cortes |
| Techos y cubiertas | No conservados | No reconstruir |
| Colores originales | Parcial | Usar restos documentados y paleta sobria |
| Licencias de esculturas y fotos | Pendiente | Tablero de licencias antes de modelar |
| Inventario de cabezas clavas | Pendiente | Selección documentada, no catálogo completo |

## Relación con Caral

- Se reutiliza el pipeline de LOD, Draco, WebP, fallback, sombras cacheadas, capas y benchmark.
- Se reutiliza el estándar de cobertura y el gate de Fase 0.
- No se reutilizan materiales, paleta ni arquitectura de Caral.
- Chavín exige resolver interiores y oscuridad; Caral era principalmente exterior.

## Criterio de aceptación de Fase 0

- [x] Tabla revisada contra fuentes.
- [x] Zonas hero y fondo aprobadas para blockout.
- [x] Huecos marcados como diferidos, no inventados.
- [x] Política de licencias aprobada; permisos de publicación pendientes.
- [x] Presupuesto y recorrido coherentes con la tabla.
- [x] Ningún elemento se declara “completo” sin fuente.
