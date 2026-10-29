# Auditoría de ciudades frente al estándar

Fecha: 28 de octubre de 2026.  
Estándar: [`ciudad.md`](./ciudad.md).

| Ciudad | Estado actual | LOD0 / LOD1 | Texturas | Paradas | QA | Cumple | Brecha y siguiente acción |
|---|---|---:|---|---:|---|---|---|
| **Caral** | `available` · v2 | 230.800 / 56.332 | 2K/1K | 6 | Android P2; hardware pendiente | **Técnico/visual sí; QA con excepción** | Cerrar o mantener waiver de `CARAL-ANDROID-GROUND-001`; QA iPhone/desktop. |
| **Chavín** | `available` · preview v0.4 | 249.906 / 27.539 | 2K/1K | 6 | Hardware pendiente; Lanzón CC BY-NC-SA | **Visual/técnico sí; QA pendiente** | Repetir QA v0.4; revisar primer plano del Lanzón y licencia comercial. |
| **Aypate** | `available` · preview v0.3 | 226.408 / 28.735 | 2K/1K | 6 | Sin QA hardware | **Visual/técnico sí; QA pendiente** | QA de hardware; cotas finas y recintos periféricos. |
| **Narihualá** | `research` | — | — | — | — | **No** | Cerrar ficha, plan y cobertura; construir blockout y high-poly hasta el estándar. |
| **Chan Chan** | `research` | — | — | — | — | **No** | Producir desde cero; ciudad de adobe, nueve ciudadelas y relieves. Prioridad posterior. |
| **Wari** | `research` | — | — | — | — | **No** | Producir desde cero; barrios, templos en D y galerías. Prioridad posterior. |

## Lectura

- **Caral** y **Chavín** son las referencias actuales. Caral cumple el estándar técnico con una incidencia P2 aceptada; Chavín cumple la calidad visual y técnica, pero su QA de hardware sigue abierta.
- **Aypate** cumple el gate visual/técnico con el layout macro de la v0.3 basado en el plano de 2013; falta la QA de hardware y el detalle de cotas finas.
- **Narihualá, Chan Chan y Wari** no tienen modelo; no se marcan `available` hasta completar el proceso.

## Orden de trabajo

1. **Aypate:** QA de hardware y cierre de cotas finas; el layout macro v0.3 ya sigue el plano de 2013.
2. **Narihualá:** de ficha a preview completo.
3. **Chan Chan:** blockout y high-poly por ciudadelas.
4. **Wari:** blockout y high-poly por sectores.
5. **Caral/Chavín:** cerrar QA y excepciones; no reconstruir.

## Criterio de actualización

Esta tabla se actualiza en el mismo PR que cambie el estado, las métricas o la QA de una ciudad. Una fila no puede decir “cumple” si falta un gate del estándar.
