> **Nota histórica:** auditoría de la escena piloto `caral_art.blend`, retirada del repositorio. No describe Caral v2; ver `auditoria-v2.md` y `release-v2.md`.

# Auditoría de la escena Caral

Generada desde `blender/caral/caral_art.blend` con `scripts/audit_blender_scene.py`. El JSON completo está en `auditoria.json`.

## Totales

| Métrica | Valor |
|---|---|
| Objetos | 578 |
| Mallas | 557 |
| Triángulos base | 47.322 |
| Materiales | 33 |
| Imágenes | 42 |
| Modificadores | 247 Bevel |
| Cámaras | 4 |
| Luces | 5 |
| Unidades | Métricas, escala 1.0 |
| Render | EEVEE, 1600 × 900, AgX |

## Colecciones

| Colección | Objetos | Lectura |
|---|---:|---|
| `COL-Caral_UpperHalf` | 200 | Núcleo superior; incluye Pirámide Mayor y Plaza Mayor. |
| `COL-Caral_Terrain` | 182 | Terreno, valle, río, campos y colinas. |
| `COL-Caral_Residential` | 45 | Conjuntos residenciales. |
| `COL-Caral_Props` | 44 | Shicras, bloques, textiles y detalles. |
| `COL-Caral_LowerHalf` | 43 | Anfiteatro, altar y sectores bajos. |
| `COL-Caral_Reference` | 40 | Figuras de escala humana. |
| `COL-Caral_Gameplay` | 11 | Spawns/recursos del juego; excluir del preview. |
| `COL-Caral_ScenarioCityExport` | 2 | LOD0/LOD1 del juego; excluir. |
| `COL-Caral_GameExport` | 1 | Plataforma de juego; excluir. |

## Hallazgos

1. **Los LOD de juego no tienen UVs.** Son `GEO-Caral_ScenarioCity_LOD0/LOD1`; no deben entrar al preview.
2. **El exportador ya excluye** `COL-Caral_GameExport`, `COL-Caral_ScenarioCityExport`, `COL-Caral_Gameplay`, cámaras y luces. El GLB resultante coincide con el publicado: 554 mallas, 23 materiales, 44.640 tris.
3. **Texturas relativas:** todas las imágenes resuelven desde `blender/textures/`; se corrigió una ruta que apuntaba al proyecto antiguo.
4. **Texturas pequeñas:** 38 de 512 px y 23 de 1024 px. Para primeros planos hay que subir a 2K en los materiales hero.
5. **Draw calls:** 554 mallas es demasiado para el visor final. Hay que fusionar por capa/material o instanciar.
6. **Bevel:** 247 modificadores; se aplican al exportar. El high-poly debe generarse aparte y hornearse.
7. **Geometría:** 44.640 tris para toda la ciudad es un blockout. El remaster necesita detalle real, no solo bevel.
8. **Materiales:** 33 en la escena, 23 en el GLB. La diferencia viene de materiales no usados o variantes.

## Implicaciones

- Mantener `COL-Caral_Gameplay`, `COL-Caral_GameExport` y `COL-Caral_ScenarioCityExport` fuera del preview.
- Crear una colección `COL-Caral_HighPoly` y otra `COL-Caral_LowPoly` para el bake.
- Definir un set de materiales hero: piedra, piedra cortada, revoque blanco/amarillo/rojo, arcilla, madera, totora, arena, suelo, vegetación.
- Presupuestar 2K para esos materiales y 1K/512 para fondo.
- Fusionar arquitectura por material y usar instancing para vegetación, rocas y figuras.
