# Estándar de ciudad publicada

Versión: **1.0**, 28 de octubre de 2026.  
Ámbito: **todas las ciudades del atlas**, desde su publicación como `available` y durante cualquier preview público.  
Referencia visual: **Chavín de Huántar v0.4**. Referencia técnica y de cierre: **Caral Remaster v2**.

## 1. Principio

Una ciudad no es un experimento aislado: es una pieza del atlas. El estándar garantiza que cualquier ciudad publicada tenga el mismo nivel de lectura, rendimiento, evidencia y QA. Un blockout puede existir como escena de trabajo, pero **no se presenta como preview final ni se deja indefinidamente como `available`**.

La norma se aplica a Caral, Chavín, Aypate, Narihualá, Chan Chan y Wari, y a toda ciudad futura.

## 2. Niveles de producción

| Nivel | Uso | Puede publicarse |
|---|---|---|
| `research` | Ficha documental, sin modelo | Sí, como ficha de investigación |
| `blockout` | Volúmenes y cámaras de trabajo | No como preview final |
| `preview` | Modelo navegable con calidad visual/técnica del estándar | Sí, con QA pendiente documentada |
| `v1` / `v2` | Remaster cerrado | Sí, con QA y contenido cerrados |

## 3. Gate visual

### Modelo

- **LOD0:** 150.000–250.000 triángulos.
- **LOD1:** 25.000–80.000 triángulos.
- La silueta, las zonas hero y las seis paradas deben leerse en ambos LOD.
- No se aceptan cajas planas como arquitectura final: muros, vanos, escalinatas, portadas, terrazas y detalles constructivos deben tener geometría suficiente.
- Los techos, alturas y recintos no conservados se omiten o se modelan como vacíos señalizados; no se inventan.
- La vegetación, el terreno y la atmósfera forman parte del modelo, no son un fondo plano.

### Texturas y materiales

- Hero: hasta **2K**; móvil: **1K**.
- PBR con difusa, rugosidad y normal; WebP 80.
- Sin texturas de IA. Materiales propios, procedurales o CC0 con registro.
- Sin `KHR_materials_transmission` salvo justificación medida.
- Culling en superficies sólidas; doble cara solo en vegetación, textiles, agua y fuego.

### Experiencia

- **Seis paradas** con cámara propia y texto que distinga documentado, inferido e interpretativo.
- Cuatro capas: arquitectura, terreno, detalles y escala humana.
- Cuatro presets de luz: amanecer, mediodía, atardecer y noche.
- Cámara hero y portada propia, sin imágenes oficiales.
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
| Caché | Versión actualizada si cambian assets |
| Validación | `npm run validate`, `npm run build`, `npm run bench` |
| Consola | Sin errores ni warnings nuevos en las cargas medidas |

Los FPS de SwiftShader no certifican hardware real; sirven para regresiones.

## 5. Gate de evidencia y licencias

Cada ciudad debe tener:

- `docs/fuentes/<id>.md` con ficha, cronología, arquitectura, evidencia y fuentes.
- `docs/remaster/<id>/cobertura.md` con elemento → evidencia → nivel de detalle → estado.
- Etiquetas explícitas: **documentado**, **inferido** o **interpretativo**.
- Política de licencias: imágenes oficiales citadas, no copiadas; assets de terceros con autor, licencia y atribución.
- Registro en `docs/fuentes/registro-assets.csv` para todo GLB, render o asset de terceros.
- Aviso visible de reconstrucción artística y, si aplica, restricción de uso comercial.

## 6. Gate de QA

Antes de cerrar una ciudad como `v1`/`v2`:

- [ ] Escritorio LOD0 y LOD1 sin errores.
- [ ] Móvil real en LOD1; fallback probado.
- [ ] PWA instalada y offline.
- [ ] Seis paradas, cuatro luces y cuatro capas.
- [ ] Capturas de todas las paradas y del hero.
- [ ] Rendimiento en al menos un Android, un iPhone/Safari y una GPU de escritorio.
- [ ] `validate`, `build` y `bench` en verde.
- [ ] Hashes, tamaños, caché y documentación actualizados.

Una incidencia P2 puede aceptarse con responsable, impacto y fecha de revisión; no puede ocultarse.

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

Las excepciones no autorizan a declarar una ciudad terminada ni a omitir el estándar en ciudades nuevas.

## 9. Proceso para una ciudad nueva

1. Dossier y ficha `research`.
2. Plan, cobertura y licencias.
3. Blockout interno, sin publicar como final.
4. High-poly de zonas hero y ambiente.
5. Materiales 2K/1K y look-dev.
6. Cámaras, seis paradas, capas y luces.
7. LOD0/LOD1, export y bench.
8. QA de hardware y correcciones.
9. Docs, registro, caché y PR.
10. Revisión y merge; recién entonces `available` definitivo.

## 10. Referencias

- [Plantilla técnica de Caral](../remaster/caral/plantilla.md)
- [Auditoría de ciudades](./auditoria-ciudades.md)
- [Chavín v0.4](../remaster/chavin/highpoly-v0.4.md)
- [Caral v2](../remaster/caral/release-v2.md)
