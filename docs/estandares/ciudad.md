# Estándar de ciudad publicada

Versión: **1.1**, 30 de octubre de 2026.
Ámbito: **todas las ciudades del atlas**, desde su publicación como `available` y durante cualquier preview público.
Referencia visual: **Chavín de Huántar high-poly v0.7**. Referencia técnica y de cierre: **Caral Remaster v2**.

## 1. Principio

Una ciudad no es un experimento aislado: es una pieza del atlas. El estándar garantiza que cualquier ciudad publicada tenga el mismo nivel de lectura, rendimiento, evidencia y QA. Un blockout puede existir como escena de trabajo, pero **no se presenta como preview final ni se deja indefinidamente como `available`**.

La norma se aplica a Caral, Chavín, Aypate, Narihualá, Chan Chan y Wari, y a toda ciudad futura.

## 2. Estado, madurez y evidencia

Cada entrada de `public/cities/index.json` y cada `city.json` usa cuatro ejes independientes:

| Campo | Valores | Uso |
|---|---|---|
| `availability` | `available`, `research` | `available` = modelo navegable; `research` = ficha documental sin modelo. |
| `maturity` | `research`, `blockout`, `preview`, `released` | Grado de cierre. `version` indica la entrega publicada. |
| `evidence` | `documented`, `mixed`, `interpretive`, `not-applicable` | Nivel general de la reconstrucción. |
| `qa` | `passed`, `partial`, `pending`, `waived`, `not-applicable` | Estado de QA en hardware real. |

Una ciudad `available` no equivale a ciudad terminada. `preview` puede publicarse con QA pendiente documentada; `released` exige contenido y QA cerrados, o una excepción P2 explícita.

Cada parada del recorrido declara `evidence`: `documented`, `inferred` o `interpretive`. La UI debe mostrar esa distinción sin convertir la ficha en un ensayo.

## 3. Gate visual

### Modelo

- **LOD0:** 150.000–250.000 triángulos.
- **LOD1:** 25.000–80.000 triángulos.
- La silueta, las zonas hero y las seis paradas deben leerse en ambos LOD.
- No se aceptan cajas planas como arquitectura final: muros, vanos, escalinatas, portadas, terrazas y detalles constructivos deben tener geometría suficiente.
- Los techos, alturas y recintos no conservados se omiten o se modelan como vacíos señalizados; no se inventan.
- La vegetación, el terreno y la atmósfera forman parte del modelo, no son un fondo plano.
- Cada nodo con mesh de LOD0/LOD1 debe traer `extras.layer` (`city`, `terrain`, `props`, `reference` o una capa adicional justificada).

### Texturas y materiales

- Hero: hasta **2K**; móvil: **1K**.
- PBR con difusa, rugosidad y normal; WebP 80.
- Sin texturas de IA. Materiales propios, procedurales o CC0 con registro.
- Sin `KHR_materials_transmission` salvo justificación medida.
- Culling en superficies sólidas; doble cara solo en vegetación, textiles, agua y fuego.

### Experiencia

- **Seis paradas** con cámara propia y texto que distinga documentado, inferido e interpretativo.
- Cuatro capas mínimas: arquitectura, terreno, detalles y escala humana. Se permiten capas adicionales justificadas.
- Cuatro presets de luz: amanecer, mediodía, atardecer y noche.
- Cámara hero y portada propia, sin imágenes oficiales.
- Suelo y niebla configurables por ciudad (`ground`, `fog`); no se impone una paleta de desierto a un valle andino.
- Ninguna parada puede quedar dentro de un muro, recortada o sin lectura del elemento protagonista.

## 4. Gate técnico

| Elemento | Objetivo |
|---|---|
| GLB LOD0/LOD1 | <25 MB cada uno |
| Draw calls | <100 en régimen estable |
| Compresión | Draco en LOD0/LOD1 |
| Texturas móviles | 1K |
| Fallback | LOD1 o fallback explícito |
| Sombreado | Sombras estáticas cacheadas |
| Caché | Versión global actualizada si cambian assets |
| Validación | `npm run validate`, `npm run build`, `npm run bench` |
| Consola | Sin errores ni warnings nuevos en las cargas medidas |

Los FPS de SwiftShader no certifican hardware real; sirven para regresiones.

## 5. Gate de evidencia y licencias

Cada ciudad debe tener:

- `docs/fuentes/<id>.md` con ficha, cronología, arquitectura, evidencia y fuentes.
- `docs/remaster/<id>/cobertura.md` con elemento → evidencia → nivel de detalle → estado.
- Etiquetas explícitas: **documentado**, **inferido** o **interpretativo**, tanto en datos como en UI.
- Política de licencias: imágenes oficiales citadas, no copiadas; assets de terceros con autor, licencia y atribución.
- Registro en `docs/fuentes/registro-assets.csv` para todo GLB, render o asset de terceros.
- Aviso visible de reconstrucción artística y, si aplica, restricción de uso comercial.

## 6. Gate de QA

Antes de cerrar una ciudad como `released`:

- [ ] Escritorio LOD0 y LOD1 sin errores.
- [ ] Móvil real en LOD1; fallback probado.
- [ ] PWA instalada y offline.
- [ ] Seis paradas, cuatro luces y cuatro capas.
- [ ] Capturas de todas las paradas y del hero.
- [ ] Rendimiento en al menos un Android, un iPhone/Safari y una GPU de escritorio.
- [ ] `validate`, `build` y `bench` en verde.
- [ ] Hashes, tamaños, caché y documentación actualizados.

Protocolo y matriz: [`qa-hardware.md`](./qa-hardware.md). Una incidencia P2 puede aceptarse con responsable, impacto y fecha de revisión; no puede ocultarse.

## 7. Definición de terminado

Una ciudad está terminada cuando:

1. Cumple los gates visual, técnico y de evidencia.
2. Tiene seis paradas, capas y luces.
3. Tiene dossier, cobertura, plan, QA y registro de assets.
4. Está revisada en PR, con CI en verde.
5. Está desplegada y verificada en producción.
6. No tiene excepciones sin documentar.

## 8. Excepciones vigentes

| Ciudad | Excepción | Estado |
|---|---|---|
| Caral | Parpadeo de suelo Android `CARAL-ANDROID-GROUND-001` | P2 aceptada; no resuelta |
| Chavín | QA de hardware incompleta; Lanzón CC BY-NC-SA | Documentada; no bloquea preview |
| Aypate | QA de hardware pendiente; cotas finas y recintos periféricos | Layout, escala y cierre de conjunto v0.4 según plano de 2013; no cerrar |
| Narihualá | Preview interpretativo; QA y cotas finas pendientes | Montículo este/capilla SIGRID; oeste/plaza inferidos; no cerrar |

Las excepciones no autorizan a declarar una ciudad terminada ni a omitir el estándar en ciudades nuevas.

## 9. Proceso para una ciudad nueva

1. Dossier y ficha `research`.
2. Plan, cobertura y licencias.
3. Blockout interno, sin publicar como final.
4. High-poly de zonas hero y ambiente.
5. Materiales 2K/1K y look-dev.
6. Cámaras, seis paradas, capas, luces, suelo y niebla.
7. LOD0/LOD1, extras de capa, export y bench.
8. QA de hardware y correcciones.
9. Docs, registro, caché y PR.
10. Revisión y merge; recién entonces `available` definitivo.

La ciudad nueva debe entrar principalmente por datos y assets. Si obliga a añadir un `if (city === ...)` en `src/`, el cambio debe justificarse y, preferentemente, resolverse como configuración reutilizable.

## 10. Referencias

- [Plantilla técnica de Caral](../remaster/caral/plantilla.md)
- [Auditoría de ciudades](./auditoria-ciudades.md)
- [QA de hardware](./qa-hardware.md)
- [Chavín v0.7](../remaster/chavin/highpoly-v0.7.md)
- [Caral v2](../remaster/caral/release-v2.md)
