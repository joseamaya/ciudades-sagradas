# Remasterizaciones

El estándar de calidad es [`../estandares/ciudad.md`](../estandares/ciudad.md). Toda ciudad publicada debe cumplirlo; la auditoría está en [`../estandares/auditoria-ciudades.md`](../estandares/auditoria-ciudades.md). La caché vigente se genera por hash en build; las menciones a `v7`, `v22`, `v27`, `v34`, `v38` o `v39` en documentos de release son históricas.

- [Caral](./caral/README.md): remaster v2 desplegado y contenido cerrado como ciudad representativa; LOD0/LOD1 con Draco y fallback v1. Es la plantilla técnica del proyecto. Incidencia Android P2 documentada.
- [Chavín de Huántar](./chavin/README.md): preview web v0.3 con pase de valle v0.7; Mosna ~30 m abajo, Wacheqsa al norte, Lanzón derivado del escaneo CyArk (CC BY-NC-SA 4.0) y Portada con fustes acanalados. Dintel y escalera cerrados en `chavin/decisiones.md`; QA móvil/1080p pendiente y kiosco comercial bloqueado por la licencia del Lanzón.
- [Aypate](./aypate/README.md): preview web v0.4 con high-poly navegable; núcleo inca, Qhapaq Ñan y bosque de neblina, con layout macro y escala contrastados con el plano de 2013. Cotas de conjunto cerradas en `aypate/cotas.md`; cotas finas cerradas como no alcanzables con fuente pública. QA móvil/1080p pendiente.
- [Narihualá](./narihuala/README.md): preview web v0.2 interpretativo; montículo este y capilla desde SIGRID 2018; montículo oeste, plaza y accesos inferidos; rampas documentadas no modeladas. Capilla en capa `later`; plano de sectores y QA móvil/1080p pendientes.
- [Chan Chan](./chan-chan/README.md): preview web v0.1 de Nik An; LOD0/LOD1, seis paradas, cuatro capas y QA desktop headless. No representa las nueve ciudadelas; QA de hardware real pendiente.
- [Wari](./wari/README.md): preview web v0.1 del núcleo monumental; LOD0/LOD1, seis paradas, cuatro capas y QA desktop headless. No representa las 2.000 ha; QA de hardware real pendiente.

<!-- metrics:remaster-status:start -->
| Ciudad | Disponibilidad | Madurez | Evidencia | QA | LOD0 tris / bytes | LOD1 tris / bytes | Draw calls LOD0/LOD1 |
|---|---|---|---|---|---|---|---|
| Caral | `available` | `released` · v2 | Mixta | `waived` (P2 Android) | 230.800 / 3.277.080 B | 56.332 / 799.260 B | 45 / 31 |
| Chavín de Huántar | `available` | `preview` · v0.3 | Mixta | `partial` | 249.942 / 1.741.708 B | 42.842 / 746.544 B | 19 / 16 |
| Chan Chan | `available` | `preview` · v0.1 | Mixta | `partial` | 156.624 / 1.904.164 B | 27.192 / 533.140 B | 14 / 13 |
| Wari | `available` | `preview` · v0.1 | Mixta | `partial` | 158.216 / 1.794.588 B | 26.224 / 677.480 B | 15 / 13 |
| Aypate | `available` | `preview` · v0.4 | Mixta | `partial` | 209.560 / 2.139.720 B | 30.663 / 443.372 B | 15 / 15 |
| Narihualá | `available` | `preview` · v0.2 | Interpretativa | `partial` | 162.432 / 1.599.008 B | 29.682 / 441.800 B | 14 / 13 |
<!-- metrics:remaster-status:end -->
