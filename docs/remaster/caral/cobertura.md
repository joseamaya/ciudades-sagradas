# Cobertura de Caral v2 — estándar de ciudad representativa

Fecha: 27 de octubre de 2026.
Estado: **cierre de contenido de Caral v2.0.1**.
Estándar: **ciudad representativa**, no inventario 1:1 de los 32 edificios públicos.

## Definición

Caral se considera completa cuando:

- Están representados los volúmenes y sectores principales respaldados por fuentes.
- Las zonas hero tienen detalle high-poly y las demás un LOD de fondo legible.
- Los huecos de evidencia están documentados y no se rellenan con invención.
- El conjunto se lee como ciudad en el visor, aunque no cada edificio tenga un modelo individual.

Queda fuera de este estándar:

- Modelar los 32 edificios públicos uno por uno.
- Repetir el high-poly del hero en las cinco pirámides secundarias y todos los sectores.
- Inventar los 20 cubículos del Anfiteatro o el perfil norte/sur del Mayor sin planos o sección.

## Cobertura por elemento

| Elemento | Evidencia | En el GLB | Nivel | Render high-poly | Nota |
|---|---|---|---|---|---|
| Pirámide Mayor | Documentado | Sí | High-poly | `v2-after-mayor.jpg` | Núcleo 170,80 × 149,69 m; perfil N/S pendiente |
| Pirámide Galería | Documentado | Sí | V1 | No | Presencia y volumen simplificados |
| Pirámide Cantera | Documentado | Sí | V1 | No | Presencia y volumen simplificados |
| Pirámide Central | Documentado | Sí | V1 | No | Presencia y volumen simplificados |
| Pirámide Huanca | Documentado | Sí | V1 | No | Incluye Plazuela Huanca |
| Pirámide Menor | Documentado | Sí | V1 | No | Presencia y volumen simplificados |
| Plaza Mayor | Documentado | Sí | High-poly | `v2-after-plaza.jpg` | 36,5 m externos / 21,5 m internos |
| Anfiteatro | Documentado | Sí | High-poly | `v2-after-anfiteatro.jpg` | 20 cubículos ausentes por falta de planta |
| Altar Circular | Documentado | Sí | High-poly | `v2-after-altar.jpg` | Altar de 2,7 m; pared modelada de 1,5 m |
| Plaza Central | Documentado | Sí | V1 | No | Piso y fogón simplificados |
| Plazuela Huanca | Documentado | Sí | V1 | No | Huanca y piso |
| Edificios E2/E3 | Documentado | Sí | V1 | No | Agrupados por sector |
| Templo Banqueta | Documentado | Sí | V1 | No | Volumen simplificado |
| Residencial Mayor | Documentado | Sí | V1 | No | Muros, fogones y techos inferidos |
| Residencial Menor | Documentado | Sí | V1 | No | Muros, fogones y techos inferidos |
| Residencia B1/B2/B5/Q | Documentado | Sí | V1 | No | Agrupadas por sector |
| Elite I2 | Documentado | Sí | V1 | No | Agrupada por sector |
| Taller Especializado | Documentado | Sí | V1 | No | Volumen simplificado |
| Periferia | Documentado | Sí | V1 | No | Cierre del conjunto |
| Terreno, valle, río, campos y caminos | Documentado/inferido | Sí | Infraestructura | No | Base del diorama |
| Rocas, grava, shicras, totora, algodón, árboles y figuras | Documentado/inferido/interpretativo | Sí | Props/referencia | No | No son edificios |
| 20 cubículos del Anfiteatro | Documentado | No | Ausente | No | Sin planta publicada suficiente |
| Perfil norte/sur del Mayor | Documentado | No | Ausente | No | Sin sección o DEM |
| 32 edificios públicos individuales | Documentado | Parcial | Sectorizado | No | No hay correspondencia 1:1 verificada |

## Lectura de los LOD

- **LOD0:** 230.800 tris; high-poly fusionado de Mayor, Plaza Mayor, Anfiteatro y Altar Circular + infraestructura v1.
- **LOD1:** 56.332 tris; las mismas cuatro zonas con atlas horneado 1K + infraestructura v1.
- **Fallback v1:** 55.944 tris; modelo completo simplificado, sin Draco.

El high-poly no reemplaza a los otros cinco edificios piramidales: estos siguen en la geometría v1. En el visor se leen como parte del conjunto, pero no tienen el detalle de fachada, escaleras y shicras del hero.

## Huecos y decisión

| Hueco | Motivo | Decisión |
|---|---|---|
| 20 cubículos del Anfiteatro | Falta planta publicada suficiente | Diferido hasta nueva fuente |
| Perfil norte/sur del Mayor | Falta sección o DEM | Diferido hasta nueva fuente |
| High-poly de las otras cinco pirámides | Fuera del alcance hero de v2 | Solo v3 si el producto lo pide |
| 32/32 edificios individuales | No es el estándar elegido | Fuera de alcance |
| QA Android del suelo | Incidencia P2 de render | Documentada en `incidencias.md` |

**Decisión:** Caral v2 queda cerrada como ciudad representativa. No se planifica un v3 por ahora; cualquier ampliación de cobertura requiere una decisión de producto y fuentes nuevas.

## Criterio de aceptación

- [x] Seis pirámides presentes en el GLB.
- [x] Plazas, altar, anfiteatro y sectores residenciales representados.
- [x] Cuatro zonas hero con high-poly y renders propios.
- [x] Huecos de fuente documentados sin invención.
- [x] Estándar y cobertura explícitos.
- **32/32 edificios individuales:** no requerido por el estándar.
- **Perfil N/S y 20 cubículos:** diferidos por fuente.
- **QA Android:** incidencia P2 abierta, no bloqueante para el cierre de contenido.
