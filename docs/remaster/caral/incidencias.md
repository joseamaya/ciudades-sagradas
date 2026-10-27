# Incidencias conocidas — Caral v2

Fecha: 27 de octubre de 2026.
Versión afectada: **v2.0.1**.
Estado: **P2 abierta y aceptada para el cierre de contenido**.

## CARAL-ANDROID-GROUND-001 — parpadeo continuo del suelo

| Campo | Valor |
|---|---|
| Severidad | P2 — visual, no bloquea navegación |
| Plataforma | Android, navegador móvil |
| Datos del dispositivo | No disponibles; se completarán más adelante |
| Versión | v2.0.0 y v2.0.1 |
| URL | <https://joseamaya.github.io/ciudades-sagradas/?debug=1#/ciudad/caral> |
| Reproducción | Continua, sin mover la cámara |
| LOD | Ocurre también con `?lod=0`; no es específico de LOD1/1K/Draco |
| Escritorio | No reproducido en Chrome headless/SwiftShader ni en el preview local |
| Issue | [#10](https://github.com/joseamaya/ciudades-sagradas/issues/10) |

### Descripción

En Android, el suelo/terreno parpadea de forma continua. El usuario lo reportó primero en v2.0.0 y volvió a confirmar que persistía tras el parche v2.0.1. El parpadeo no impide navegar, abrir la ficha ni cambiar de parada, pero afecta la lectura visual del conjunto.

### Matriz de aislamiento

| Prueba | Resultado | Confianza |
|---|---|---|
| `?lod=0` | Sigue | Reportado |
| `?lod=1` | Sigue | Reportado |
| `?noshadows=1` | No confirmado | Se facilitó la URL; falta confirmación explícita |
| `?noground=1` | No confirmado | Pendiente |
| `?noground=1&noshadows=1` | No confirmado | Pendiente |
| PWA instalada vs. navegador | No confirmado | Pendiente |
| Escritorio | No se reproduce | Verificado en emulación |

No declarar la incidencia como resuelta ni como “shadow acne” hasta completar esta matriz.

### Hipótesis, en orden

1. **Capas internas del terreno coplanares.** `Terrain`, `SiteApron` y superficies de piso del GLB pueden compartir altura y competir por profundidad. Es la hipótesis principal porque el parpadeo sigue con LOD0 y no se reproduce en escritorio.
2. **Precisión de profundidad en GPU Android.** La combinación de cámara, escala 0,08 y superficies grandes puede amplificar el artefacto en drivers móviles.
3. **Sombras.** Menos probable si `?noshadows=1` también lo elimina o no; falta confirmarlo.
4. **Plano de arena del visor.** Ya se bajó a `-0.36` y se le aplicó `polygonOffset`, pero no se ha confirmado con `?noground=1` en el dispositivo.

### Impacto y decisión

- Impacto: visual; no hay crash, pérdida de datos ni bloqueo de navegación.
- No se hace rollback de v2.0.1.
- Se acepta para el cierre de contenido de Caral y **no bloquea Chavín Fase 0**.
- Si aparece en más dispositivos o afecta una presentación pública, sube a P1 y se prioriza.

### Workaround

No hay workaround confirmado. Para demos en hardware desconocido, usar escritorio o el preview local; no prometer que `?noshadows=1` lo resuelve hasta verificarlo.

### Próxima acción

1. Registrar modelo, versión de Android/Chrome, GPU (`chrome://gpu`), si es PWA o navegador, y vídeo de 10 s.
2. Probar la matriz completa de flags.
3. Si se confirma, aislar las capas del terreno en Blender y revisar alturas/duplicados; después reexportar LOD0/LOD1 con hashes y caché actualizados.
4. Si no se puede reproducir, dejar la incidencia abierta con la evidencia disponible y revisar cuando haya un equipo equivalente.

### Evidencia

- Captura/vídeo: pendiente.
- Métricas `?debug=1`: pendiente.
- Conversación: reporte en Android; persistencia tras v2.0.1.
