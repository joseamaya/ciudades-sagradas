# Auditoría de ciudades frente al estándar

Fecha: 4 de noviembre de 2026.
Estándar: [`ciudad.md`](./ciudad.md).
QA: [`qa-hardware.md`](./qa-hardware.md).

## Estado

Las cifras de LOD, draw calls y paradas se generan en `docs/metricas.json`; esta tabla conserva solo el veredicto editorial.

| Ciudad | Disponibilidad | Madurez | Evidencia | QA | Cumple | Brecha y siguiente acción |
|---|---|---|---|---|---|---|
| **Caral** | `available` | `released` · v2 | Mixta | `waived` (P2 Android) | **Técnico/visual sí; QA con excepción** | Desktop integrado 1600×900 completo: LOD0/LOD1, flags, offline, standalone y 10 min. Faltan 1080p y móvil. Cerrar o mantener `CARAL-ANDROID-GROUND-001`. |
| **Chavín** | `available` | `preview` · v0.3 | Mixta | `partial` | **Visual/técnico sí; QA móvil pendiente** | Desktop integrado 1600×900 LOD0/LOD1 OK a 60 fps; faltan 1080p y móvil. Dintel/escalera y licencia documentados en `decisiones.md`; kiosco comercial bloqueado por CC BY-NC-SA. |
| **Aypate** | `available` | `preview` · v0.4 | Mixta | `partial` | **Visual/técnico sí; QA pendiente** | Desktop integrado 1600×900 LOD0/LOD1 OK; faltan 1080p y móvil. Cotas finas cerradas como no alcanzables; recintos periféricos diferidos. |
| **Narihualá** | `available` | `preview` · v0.2 | Interpretativa | `partial` | **Parcial; interpretativo** | Desktop integrado 1600×900 LOD0/LOD1 OK; faltan 1080p y móvil. Plano de sectores bloqueado: sin fuente pública y sectorización 3/4/8 en conflicto. |
| **Chan Chan** | `available` | `preview` · v0.1 | Mixta | `partial` | **Visual/técnico sí; QA pendiente** | Preview de Nik An; LOD0/LOD1, seis paradas y QA desktop 1600×900. Faltan móvil/1080p y no se amplía a las nueve ciudadelas. |
| **Wari** | `research` | `research` | No aplica | No aplica | **No** | Piloto solo-datos completado; ficha y cobertura cerradas sin modelo. |

## Métricas y condiciones

<!-- metrics:auditoria-metricas:start -->
| Ciudad | LOD0 tris / bytes | LOD1 tris / bytes | Texturas | Caché | Fuente |
|---|---|---|---|---|---|
| Caral | 230.800 / 3.277.080 B | 56.332 / 799.260 B | 373,3 / 40 MB VRAM estimada | hash | `npm run validate` + QA |
| Chavín de Huántar | 249.942 / 1.741.708 B | 42.842 / 746.544 B | 136 / 72 MB VRAM estimada | hash | `npm run validate` + QA |
| Chan Chan | 156.624 / 1.904.164 B | 27.192 / 533.140 B | 208 / 64 MB VRAM estimada | hash | `npm run validate` + QA |
| Aypate | 209.560 / 2.139.720 B | 30.663 / 443.372 B | 160 / 80 MB VRAM estimada | hash | `npm run validate` + QA |
| Narihualá | 162.432 / 1.599.008 B | 29.682 / 441.800 B | 96 / 48 MB VRAM estimada | hash | `npm run validate` + QA |
<!-- metrics:auditoria-metricas:end -->

- Triángulos, bytes y tablas: `npm run docs:metrics` genera `docs/metricas.json` desde los GLB y los informes QA. No editar las tablas a mano.
- Draw calls y VRAM: cámara inicial, 1600×900, Chrome headless/SwiftShader. No son FPS de hardware real.
- Caral usa atlas horneado en LOD1; las demás no. No generalizar esa cifra de VRAM.
- La caché es global y se genera en build a partir del hash de assets, no por ciudad.

## Lectura

- **Caral** es la referencia técnica y de cierre. Cumple el estándar con una excepción P2 aceptada; su contenido no se reabre.
- **Chavín** cumple calidad visual y técnica para preview, pero su QA de hardware sigue abierta y el Lanzón tiene licencia CC BY-NC-SA.
- **Aypate** cumple el gate visual/técnico con el layout y la escala de la v0.4; el desktop integrado 1600×900 ya pasó LOD0/LOD1. Faltan QA móvil/1080p. Cotas finas cerradas como no alcanzables; recintos periféricos diferidos. No se reabre geometría.
- **Narihualá** es un preview interpretativo; el desktop integrado 1600×900 ya pasó LOD0/LOD1. No se eleva artificialmente al nivel de Caral ni se inventan sectores, rampas o alturas.
- **Chan Chan** abre el preview de Nik An: arquitectura de adobe, plaza, audiencias, depósitos y reservorio. Es una lectura de conjunto; no representa las nueve ciudadelas.
- **Wari** sigue como ficha documental y es el siguiente preview 3D, limitado a su núcleo monumental.

## Orden de trabajo

1. **QA de hardware:** desktop 1600×900 ya auditado; móvil/1080p/kiosco siguen pendientes. No hay dispositivo móvil disponible, así que no se certifican por emulación.
2. **Caral:** cerrar o mantener la excepción Android con evidencia.
3. **Chavín:** QA móvil/1080p; dintel/escalera y licencia documentados en `decisiones.md`; no abrir kiosco comercial con el GLB actual.
4. **Aypate:** cotas finas cerradas como no alcanzables con fuente pública; recintos periféricos diferidos, sin rehacer el layout.
5. **Narihualá:** plano arqueológico de sectores y cotas finas. Búsqueda 2026 sin plano público; la RVM solo aprueba el plano perimétrico y la sectorización 3/4/8 está en conflicto. No etiquetar sectores; solicitar el expediente técnico.
6. **Chan Chan:** preview v0.1 de Nik An construido; QA móvil/1080p pendiente. No ampliar a las nueve ciudadelas sin fuentes y presupuesto.
7. **Wari:** siguiente preview 3D, limitado al núcleo monumental; no modelar los 2.000 ha completos.

## Criterio de actualización

Esta tabla se actualiza en el mismo PR que cambie el estado, la evidencia, las métricas o la QA de una ciudad. Una fila no puede decir “cumple” si falta un gate del estándar. Un preview no se presenta como reconstrucción final.
