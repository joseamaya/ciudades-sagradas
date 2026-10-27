# Ciudades Sagradas

Atlas interactivo de ciudades y centros ceremoniales del Perú antiguo. Proyecto independiente: no depende de `edades-del-peru` ni de ningún juego.

## Comandos

```bash
npm install
npm run dev          # desarrollo en 127.0.0.1:5173
npm run validate     # valida cities/index.json, city.json, GLB, hashes y assets
npm run build        # build en dist/
npm run serve        # preview de producción en 127.0.0.1:4173
npm run bench        # benchmark/QA con Chrome headless (SwiftShader)
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

1. La fuente versionada es `blender/caral/caral_remaster.blend`; las escenas v2/LOD y atlas se regeneran con `scripts/` y no se versionan por tamaño.
2. Modelar y guardar la escena.
3. Exportar v1 con `blender/caral/export.py` (WebP 80). Exportar LOD0/LOD1 con `scripts/export_caral_lod.py` (WebP 80 + Draco).
4. Actualizar `public/cities/caral/city.json` si cambian cámaras, escala o recorrido.
5. Actualizar hashes/tamaños en `docs/fuentes/registro-assets.csv` y la caché de `public/sw.js` si cambian assets.
6. Ejecutar `npm run validate`, `npm run build` y `npm run bench`.
7. Probar en navegador y kiosco.

## Remaster de Caral

- Caral Remaster v2 es el estado actual y la plantilla técnica; no presentarlo como reconstrucción final.
- LOD0/LOD1 con Draco, fallback v1 y override `?lod=0/1`.
- Plan, auditoría y release: `docs/remaster/caral/`.
- Texturas nuevas: CC0 o procedurales; no nuevas texturas de IA.
- Cambios en GLB: actualizar hashes, registro, caché y QA visual.

## Convenciones

- Nombres: `GEO-` geometría, `MAT-` materiales, `LGT-` luces, `CAM-` cámaras, `COL-` colecciones.
- Usa `bpy.data.objects['nombre']`; cada llamada a `blender_execute_blender_code` tiene un namespace nuevo.
- Escala de escena: metros; el visor aplica la escala indicada en `city.json`.
- Y-up en el GLB; el exportador usa `export_yup=True`.
- Guarda un `.blend` antes de operaciones destructivas.
- Verifica con `ls` que los archivos existan antes de reportar éxito.

## Reglas de contenido

- Caral v2 está publicado; sigue siendo una reconstrucción artística, no un registro final.
- No usar cerámica, metales, rueda, llamas, caballos ni imaginería inca en Caral.
- Cada dato dudoso se marca como documentado, inferido o interpretativo.
- No copiar imágenes de UNESCO/Mincul/ICOMOS sin permiso.
- Los GLB publicados no contienen texturas de IA; el piloto histórico con IA fue retirado del repositorio. Las próximas ciudades deben usar CC0/procedurales.
- No introducir KTX2/Draco adicional sin medir el beneficio y actualizar el decoder/licencias.
- No añadir dependencias del juego `edades-del-peru`.
