# Ciudades Sagradas

Atlas interactivo de ciudades y centros ceremoniales del Perú antiguo. Proyecto independiente: no depende de `edades-del-peru` ni de ningún juego.

## Comandos

```bash
npm install
npm run dev          # desarrollo en 127.0.0.1:5173
npm run validate     # valida cities/index.json, city.json y assets
npm run build        # build en dist/
npm run serve        # preview de producción en 127.0.0.1:4173
```

Kiosco: abrir `http://127.0.0.1:4173/?kiosk=1`.

## Blender MCP

- Blender 5.2.2 LTS debe estar abierto.
- El servidor del add-on debe estar iniciado: panel `N` → **MCP for Blender** → **Start MCP Server** (puerto 9876).
- Si el MCP no responde, pide al usuario que arranque ese servidor; no lo lances desde la terminal.
- Safe mode activo (`BLENDER_MCP_SAFE_MODE=1`): modelado, materiales, render, guardado e import/export funcionan; no hacer lectura/escritura arbitraria de archivos, red ni subprocess.
- La configuración está en `opencode.json`. Si `uvx` no está en el PATH, instala `uv` o ajusta el comando en tu copia local; no commitees rutas absolutas.

## Skills

Están en `.agents/skills/` y su procedencia en `skills-lock.json`. Para trabajo 3D carga primero `text-to-blender`; después encadena `blender-modeling`, `blender-materials`, `blender-lighting`, `blender-cameras`, `blender-rendering` y `blender-export` según la tarea.

Las recetas usan nombres de herramientas de versiones antiguas. Traduce siempre a las herramientas reales de OpenCode:

| Receta antigua | Herramienta real |
|---|---|
| `mcp__blender__execute_blender_code`, `execute_python`, `execute_code` | `blender_execute_blender_code` |
| `get_scene_info` | `blender_get_scene_info` |
| `get_object_info`, `get_objects_summary`, `get_object_detail_summary` | `blender_get_scene_info` con `query`/`root`, o Python vía `blender_execute_blender_code` |
| `get_viewport_screenshot`, `screenshot`, `render_viewport_to_path` | `blender_look` o render real vía Python |
| `get_addon_status` | `blender_get_addon_status` |
| `search_polyhaven_assets`, `download_polyhaven_asset`, Sketchfab, Hyper3D/Hunyuan | `blender_search_assets`, `blender_import_asset`, `blender_generate_3d` |
| `search_api_docs` | No existe; usa `help()`, `dir()` o la documentación local de Blender 5.2 |

## Estructura

```text
public/cities/<slug>/     city.json, model.glb, hero.jpg
src/                      visor, UI, audio, datos
blender/caral/            escena editable y export.py
blender/textures/         texturas de la escena Caral
docs/fuentes/             dossier por ciudad
docs/capturas/            capturas de referencia
scripts/validate.mjs      validación de datos y assets
```

## Pipeline Blender

1. Abrir `blender/caral/caral_art.blend` (texturas relativas en `blender/textures/`).
2. Modelar y guardar la escena.
3. Exportar:
   ```bash
   blender --background blender/caral/caral_art.blend \
     --python blender/caral/export.py -- \
     --out public/cities/caral/model.glb
   ```
4. Actualizar `public/cities/caral/city.json` si cambian cámaras, escala o recorrido.
5. Ejecutar `npm run validate` y `npm run build`.
6. Probar en navegador y kiosco.

## Remaster de Caral

- Rama de trabajo: `feat/caral-remaster`.
- No reemplazar el GLB de `main` hasta que el remaster pase QA.
- Alcance inicial: Pirámide Mayor, Plaza Mayor, Plaza Circular, Anfiteatro, terraza y valle.
- Plan y auditoría: `docs/remaster/caral/`.
- Texturas nuevas: CC0 o procedurales; no nuevas texturas de IA.

## Convenciones

- Nombres: `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras, `COL-` colecciones.
- Usa `bpy.data.objects['nombre']`; cada llamada a `blender_execute_blender_code` tiene un namespace nuevo.
- Escala de escena: metros; el visor aplica la escala indicada en `city.json`.
- Y-up en el GLB; el exportador usa `export_yup=True`.
- Guarda un `.blend` antes de operaciones destructivas.
- Verifica con `ls` que los archivos existan antes de reportar éxito.

## Reglas de contenido

- Caral es un **piloto** y está en remasterización. No presentarlo como reconstrucción final.
- No usar cerámica, metales, rueda, llamas, caballos ni imaginería inca en Caral.
- Cada dato dudoso se marca como documentado, inferido o interpretativo.
- No copiar imágenes de UNESCO/Mincul/ICOMOS sin permiso.
- Las texturas de IA de Caral están documentadas y pendientes de auditoría; las próximas ciudades deben usar CC0/procedurales.
- No añadir dependencias del juego `edades-del-peru`.
