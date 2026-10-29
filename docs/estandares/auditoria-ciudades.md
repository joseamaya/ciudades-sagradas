# Auditoría de ciudades frente al estándar

Fecha: 28 de octubre de 2026.  
Estándar: [`ciudad.md`](./ciudad.md).

| Ciudad | Estado actual | LOD0 / LOD1 | Texturas | Paradas | QA | Cumple | Brecha y siguiente acción |
|---|---|---:|---|---:|---|---|---|
| **Caral** | `available` · v2 | 230.800 / 56.332 | 2K/1K | 6 | Android P2; hardware pendiente | **Técnico/visual sí; QA con excepción** | Cerrar o mantener waiver de `CARAL-ANDROID-GROUND-001`; QA iPhone/desktop. |
| **Chavín** | `available` · preview v0.5 | 249.930 / 27.563 | 2K/1K | 6 | Hardware pendiente; Lanzón CC BY-NC-SA | **Visual/técnico sí; QA pendiente** | Repetir QA v0.5; revisar primer plano del Lanzón y licencia comercial. |
| **Aypate** | `available` · preview v0.4 | 209.560 / 30.663 | 2K/1K | 6 | Sin QA hardware | **Visual/técnico sí; QA pendiente** | QA de hardware; cotas finas y recintos periféricos; cierre de conjunto documentado. |
| **Narihualá** | `available` · preview v0.2 | 162.432 / 29.682 | 2K/1K | 6 | Sin QA hardware | **Parcial; interpretativo** | Montículo este y capilla desde SIGRID; oeste/plaza inferidos; cotas finas pendientes. |
| **Chan Chan** | `research` | — | — | — | — | **No** | Producir desde cero; ciudad de adobe, nueve ciudadelas y relieves. Prioridad posterior. |
| **Wari** | `research` | — | — | — | — | **No** | Producir desde cero; barrios, templos en D y galerías. Prioridad posterior. |

## Lectura

- **Caral** y **Chavín** son las referencias actuales. Caral cumple el estándar técnico con una incidencia P2 aceptada; Chavín cumple la calidad visual y técnica, pero su QA de hardware sigue abierta.
- **Aypate** cumple el gate visual/técnico con el layout macro y la escala corregida de la v0.4; falta la QA de hardware y el detalle de cotas finas; el cierre de conjunto está documentado.
- **Chan Chan y Wari** no tienen modelo; no se marcan `available` hasta completar el proceso. **Narihualá** sí tiene un preview interpretativo, pero no estándar cerrado.

## Orden de trabajo

1. **Aypate:** QA de hardware y cotas finas; el layout, la escala y el cierre de conjunto v0.4 ya siguen el plano de 2013.
2. **Narihualá:** cerrar cotas finas con plano arqueológico o levantamiento propio; el preview interpretativo ya existe.
3. **Chan Chan:** blockout y high-poly por ciudadelas.
4. **Wari:** blockout y high-poly por sectores.
5. **Caral/Chavín:** cerrar QA y excepciones; no reconstruir.

## Criterio de actualización

Esta tabla se actualiza en el mismo PR que cambie el estado, las métricas o la QA de una ciudad. Una fila no puede decir “cumple” si falta un gate del estándar.
