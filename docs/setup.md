# Setup del proyecto

## Requisitos

- Node.js 22 y npm.
- Blender 5.2.2 LTS.
- Add-on **MCP for Blender** instalado y activo en Blender.
- `uv` / `uvx` en el PATH.
- OpenCode con el proyecto abierto en la raíz.

## Web

```bash
npm install
npm run dev
```

Abre `http://127.0.0.1:5173/`.

Validación y build:

```bash
npm run validate
npm run build
npm run serve
```

## OpenCode + Blender MCP

`opencode.json` ya incluye el servidor MCP `blender`:

- comando: `uvx --python 3.11 mcp-for-blender`
- host: `localhost`
- puerto: `9876`
- safe mode: activo

Pasos:

1. Abre Blender.
2. En el panel `N`, abre **MCP for Blender**.
3. Pulsa **Start MCP Server** y confirma el puerto `9876`.
4. Desde la raíz del repo, abre una sesión de OpenCode.
5. Verifica el MCP:
   - `blender_get_addon_status`
   - `blender_get_scene_info`
6. Verifica las skills: deben aparecer las de `.agents/skills/`.

Si `uvx` no está en el PATH, instala `uv` o ajusta el comando de `opencode.json` en tu copia local. No commitees rutas absolutas de tu máquina.

## Escena Blender

```bash
blender blender/caral/caral_remaster.blend
```

Caral v2 es el estado actual. La fuente versionada es `blender/caral/caral_remaster.blend`; las escenas v2/LOD y los atlas se regeneran con `scripts/` y no se versionan por tamaño.

## Exportar Caral

```bash
blender --background blender/caral/caral_remaster.blend \
  --python blender/caral/export.py -- \
  --out public/cities/caral/model.glb \
  --image-format WEBP --image-quality 80
```

Después:

```bash
npm run validate
npm run build
```

El GLB v1 se reproduce con `export.py` (excluye las colecciones de juego). Los LOD0/LOD1 se exportan con `scripts/export_caral_lod.py` (WebP 80 + Draco). Valida el resultado antes de reemplazarlo. Si cambia un modelo, actualiza su hash/tamaño en `public/cities/caral/README.md`, `docs/fuentes/registro-assets.csv` y la versión de caché de `public/sw.js`.

## Kiosco

```bash
npm run build
npm run serve
```

Abre `http://127.0.0.1:4173/?kiosk=1` o usa `scripts/kiosk.sh`.

Diagnóstico y benchmark:

```bash
# métricas en vivo
http://127.0.0.1:4173/?debug=1#/ciudad/caral

# benchmark reproducible (Chrome + build)
npm run bench -- --out /tmp/caral-bench
```

## Verificación rápida

- `npm run validate` → OK.
- `npm run build` → OK.
- Caral carga en el navegador con LOD0 en escritorio y LOD1 en móvil.
- `?debug=1` muestra draw calls, triángulos, texturas, FPS y carga.
- `?lod=0` y `?lod=1` fuerzan el LOD; `?nosw=1` desactiva el service worker para QA.
- El MCP responde a `blender_get_addon_status`.
- Las skills de Blender aparecen en la sesión.
- El sitio publicado carga desde GitHub Pages.

## Problemas comunes

| Problema | Solución |
|---|---|
| MCP no responde | Inicia el servidor del add-on en Blender, puerto 9876. |
| `uvx` no encontrado | Instala `uv` y asegúrate de que `~/.local/bin` esté en PATH. |
| Texturas rosas/faltantes | Abre la escena desde `blender/caral/` y verifica `blender/textures/`. |
| El GLB no cambia en kiosco | Sube `CACHE` en `public/sw.js` o limpia la caché del navegador. |
| Pages no actualiza | Revisa el workflow **Deploy GitHub Pages** en Actions. |
