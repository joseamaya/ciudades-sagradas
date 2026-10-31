# Auditoría de ciudades frente al estándar

Fecha: 31 de octubre de 2026.
Estándar: [`ciudad.md`](./ciudad.md).
QA: [`qa-hardware.md`](./qa-hardware.md).

## Estado

| Ciudad | Disponibilidad | Madurez | Evidencia | QA | LOD0 / LOD1 | Draw calls | Paradas | Cumple | Brecha y siguiente acción |
|---|---|---|---|---|---|---:|---|---|---|
| **Caral** | `available` | `released` · v2 | Mixta | `waived` (P2 Android) | 230.800 / 56.332 | 44 / 31 | 6 | **Técnico/visual sí; QA con excepción** | Desktop integrado 1600×900 completo: LOD0/LOD1, flags, offline, standalone y 10 min. Faltan 1080p y móvil. Cerrar o mantener `CARAL-ANDROID-GROUND-001`. |
| **Chavín** | `available` | `preview` · v0.3 | Mixta | `partial` | 249.942 / 42.842 | 19 / 16 | 6 | **Visual/técnico sí; QA móvil pendiente** | Desktop integrado 1600×900 LOD0/LOD1 OK a 60 fps; faltan 1080p y móvil. Decidir dintel/escalera; licencia CC BY-NC-SA. |
| **Aypate** | `available` | `preview` · v0.4 | Mixta | `partial` | 209.560 / 30.663 | 17 / 15 | 6 | **Visual/técnico sí; QA pendiente** | Desktop integrado 1600×900 LOD0/LOD1 OK; faltan 1080p y móvil. Cotas finas y recintos periféricos. |
| **Narihualá** | `available` | `preview` · v0.2 | Interpretativa | `partial` | 162.432 / 29.682 | 14 / 13 | 6 | **Parcial; interpretativo** | Desktop integrado 1600×900 LOD0/LOD1 OK; faltan 1080p y móvil. Plano arqueológico de sectores y cotas finas. |
| **Chan Chan** | `research` | `research` | No aplica | No aplica | — | — | — | **No** | Piloto solo-datos completado; ficha y cobertura cerradas sin modelo. |
| **Wari** | `research` | `research` | No aplica | No aplica | — | — | — | **No** | Siguiente piloto solo-datos; barrios, templos en D y galerías. |

## Métricas y condiciones

| Ciudad | LOD0 tris / bytes | LOD1 tris / bytes | Texturas | Caché | Fuente |
|---|---|---|---|---|---|
| Caral | 230.800 / 3.277.080 B | 56.332 / 1.345.092 B | 2K/1K; 373/208 MB VRAM estimada | v38 | `npm run validate` + release v2 |
| Chavín | 249.942 / 1.741.708 B | 42.842 / 746.544 B | 2K/1K | v38 | `npm run validate` + informe high-poly v0.7 |
| Aypate | 209.560 / 2.139.720 B | 30.663 / 443.372 B | 1K/1K; 160/80 MB | v38 | `npm run validate` + preview v0.4 |
| Narihualá | 162.432 / 1.599.008 B | 29.682 / 441.800 B | 1K/1K; 96/48 MB | v38 | `npm run validate` + preview v0.2 |

- Triángulos y bytes se miden de los accessors del GLB en `npm run validate`. Los informes de Blender pueden diferir en ±1 triángulo por degenerados o triangulación; no mezclar ambas fuentes en una misma tabla.
- Draw calls: cámara inicial, 1600×900, Chrome headless/SwiftShader. No son FPS de hardware real.
- Caral usa atlas horneado en LOD1; las demás no. No generalizar esa cifra de VRAM.
- La caché es global (`ciudades-sagradas-v38`), no por ciudad.

## Lectura

- **Caral** es la referencia técnica y de cierre. Cumple el estándar con una excepción P2 aceptada; su contenido no se reabre.
- **Chavín** cumple calidad visual y técnica para preview, pero su QA de hardware sigue abierta y el Lanzón tiene licencia CC BY-NC-SA.
- **Aypate** cumple el gate visual/técnico con el layout y la escala de la v0.4; el desktop integrado 1600×900 ya pasó LOD0/LOD1. Faltan QA móvil/1080p y cotas finas. No se reabre geometría.
- **Narihualá** es un preview interpretativo; el desktop integrado 1600×900 ya pasó LOD0/LOD1. No se eleva artificialmente al nivel de Caral ni se inventan sectores, rampas o alturas.
- **Chan Chan** tiene ficha documental y cobertura, pero no modelo; no se marca `available`.
- **Wari** no tiene modelo; no se marca `available` hasta completar el proceso.

## Orden de trabajo

1. **QA de hardware:** desktop 1600×900 ya auditado; móvil/1080p/kiosco siguen pendientes. No hay dispositivo móvil disponible, así que no se certifican por emulación.
2. **Caral:** cerrar o mantener la excepción Android con evidencia.
3. **Chavín:** decidir dintel/escalera y revisar la licencia comercial.
4. **Aypate:** cotas finas y recintos periféricos, sin rehacer el layout.
5. **Narihualá:** plano arqueológico de sectores y cotas finas.
6. **Chan Chan:** piloto solo-datos completado; no se abre geometría.
7. **Wari:** siguiente piloto solo-datos; después se decide si alguna ciudad pasa a 3D.

## Criterio de actualización

Esta tabla se actualiza en el mismo PR que cambie el estado, la evidencia, las métricas o la QA de una ciudad. Una fila no puede decir “cumple” si falta un gate del estándar. Un preview no se presenta como reconstrucción final.
