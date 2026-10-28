# Auditoría de ciudades frente al estándar

Fecha: 28 de octubre de 2026.  
Estándar: [`ciudad.md`](./ciudad.md).

| Ciudad | Estado actual | LOD0 / LOD1 | Texturas | Paradas | QA | Cumple | Brecha y siguiente acción |
|---|---|---:|---|---:|---|---|---|
| **Caral** | `available` · v2 | 230.800 / 56.332 | 2K/1K | 6 | Android P2; hardware pendiente | **Técnico/visual sí; QA con excepción** | Cerrar o mantener waiver de `CARAL-ANDROID-GROUND-001`; QA iPhone/desktop. |
| **Chavín** | `available` · preview v0.4 | 249.906 / 27.539 | 2K/1K | 6 | Hardware pendiente; Lanzón CC BY-NC-SA | **Visual/técnico sí; QA pendiente** | Repetir QA v0.4; revisar primer plano del Lanzón y licencia comercial. |
| **Aypate** | `available` · preview v0.1 | 43.420 / 14.252 | 512 | 6 | Sin QA hardware | **No** | Subir a high-poly v0.2: muros, portada, Ushnu, Kallanka, vegetación, 2K y LOD1 40k–60k. Excepción temporal. |
| **Narihualá** | `research` | — | — | — | — | **No** | Cerrar ficha, plan y cobertura; construir blockout y high-poly hasta el estándar. |
| **Chan Chan** | `research` | — | — | — | — | **No** | Producir desde cero; ciudad de adobe, nueve ciudadelas y relieves. Prioridad posterior. |
| **Wari** | `research` | — | — | — | — | **No** | Producir desde cero; barrios, templos en D y galerías. Prioridad posterior. |

## Lectura

- **Caral** y **Chavín** son las referencias actuales. Caral cumple el estándar técnico con una incidencia P2 aceptada; Chavín cumple la calidad visual y técnica, pero su QA de hardware sigue abierta.
- **Aypate** es la deuda inmediata: el blockout v0.1 no llega al estándar visual (43k tris y texturas de 512 px). Se mantiene publicado de forma temporal y debe pasar a v0.2.
- **Narihualá, Chan Chan y Wari** no tienen modelo; no se marcan `available` hasta completar el proceso.

## Orden de trabajo

1. **Aypate v0.2:** high-poly, materiales 2K, vegetación/niebla, LOD1 y QA.
2. **Narihualá:** de ficha a preview completo.
3. **Chan Chan:** blockout y high-poly por ciudadelas.
4. **Wari:** blockout y high-poly por sectores.
5. **Caral/Chavín:** cerrar QA y excepciones; no reconstruir.

## Criterio de actualización

Esta tabla se actualiza en el mismo PR que cambie el estado, las métricas o la QA de una ciudad. Una fila no puede decir “cumple” si falta un gate del estándar.
