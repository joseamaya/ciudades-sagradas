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
blender blender/caral/caral_art.blend
```

Las texturas se resuelven desde `blender/textures/` con rutas relativas. La escena es un piloto en remasterización.

## Exportar Caral

```bash
blender --background blender/caral/caral_art.blend \
  --python blender/caral/export.py -- \
  --out public/cities/caral/model.glb
```

Después:

```bash
npm run validate
npm run build
```

El GLB publicado se reproduce con `export.py` (excluye las colecciones de juego). Valida el resultado antes de reemplazarlo. Si cambia el modelo, actualiza su hash/tamaño en `public/cities/caral/README.md`, `docs/fuentes/registro-assets.csv` y la versión de caché de `public/sw.js`.

## Kiosco

```bash
npm run build
npm run serve
```

Abre `http://127.0.0.1:4173/?kiosk=1` o usa `scripts/kiosk.sh`.

## Verificación rápida

- `npm run validate` → OK.
- `npm run build` → OK.
- Caral carga en el navegador.
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
