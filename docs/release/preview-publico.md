# Release — preview público del atlas

Fecha: 30 de octubre de 2026.
Alcance: atlas completo, con Caral v2 como referencia y tres previews en revisión.

## Qué se publica

- **Caral v2:** `released`, contenido cerrado como ciudad representativa. LOD0/LOD1 con Draco y fallback v1.
- **Chavín v0.2:** preview con pase high-poly v0.6, Lanzón derivado de CyArk (CC BY-NC-SA 4.0) y Portada de las Falcónidas.
- **Aypate v0.4:** preview con layout y escala contrastados con el plano de 2013.
- **Narihualá v0.2:** preview interpretativo; montículo este/capilla desde SIGRID 2018 y oeste/plaza inferidos.
- **Chan Chan y Wari:** fichas documentales, sin modelo.

La UI muestra `availability`, `maturity`, `evidence` y `qa` en catálogo, ficha y recorrido. No se presenta ninguna ciudad como reconstrucción final.

## Verificado localmente

- [x] `npm run validate` en verde: 6 ciudades, coherencia índice/ficha, GLB y `extras.layer`.
- [x] `npm run build` en verde (aviso de chunk >500 kB, no bloqueante).
- [x] Caral carga en LOD0/LOD1, fallback v1 y offline.
- [x] Chavín, Aypate y Narihualá cargan en LOD0/LOD1 y fallback LOD1.
- [x] Navegación atlas → ciudad → atlas.
- [x] Fichas de Chan Chan y Wari sin errores de consola.
- [x] Bench de las cuatro ciudades sin errores de consola en cargas normales.
- [x] Informe QA con GPU, WebGL, PWA, flags y captura de errores de ventana.
- [x] Playwright: rutas, LOD0/LOD1, seis paradas, luces, capas, consola y offline en Chromium/Firefox. WebKit bloqueado por dependencias del host.

## Pendiente antes de llamarlo publicación final

- [ ] QA en Android/Chrome, iPhone/Safari y GPU de escritorio.
- [ ] Cerrar o mantener la incidencia `CARAL-ANDROID-GROUND-001`.
- [ ] Repetir QA de Chavín v0.6.
- [ ] Revisar la licencia CC BY-NC-SA 4.0 del Lanzón antes de uso comercial.
- [ ] Cerrar cotas finas de Aypate y Narihualá.
- [ ] Resolver el plano arqueológico de sectores de Narihualá.

Protocolo: [`../estandares/qa-hardware.md`](../estandares/qa-hardware.md). Registro de resultados y secuencia de captura: [`../qa/README.md`](../qa/README.md).

## Publicación

### GitHub Pages

1. Verificar `npm run validate` y `npm run build`.
2. Confirmar que `dist/` contiene los assets actuales.
3. Hacer merge a `main`; el workflow `.github/workflows/pages.yml` valida, construye y despliega.
4. Abrir `https://joseamaya.github.io/ciudades-sagradas/` y ejecutar el smoke post-deploy.

### Cloudflare Pages

- Build command: `npm run build`
- Output directory: `dist`

## Smoke post-deploy

1. Atlas: 6 tarjetas, 4 con modelo, aviso de preview visible.
2. Caral: LOD0/LOD1, seis paradas, cuatro luces y cuatro capas.
3. Chavín: seis paradas; revisar Lanzón y Portada.
4. Aypate: seis paradas; revisar plaza, ushnu, kallanka y fuente.
5. Narihualá: seis paradas; revisar montículos y plaza.
6. Chan Chan y Wari: ficha documental sin canvas.
7. `?debug=1`: LOD, draw calls, GPU/WebGL, PWA y **Copiar informe QA** disponibles.
8. `?lod=0` y `?lod=1`: forzado correcto.
9. Offline: cargar una ciudad, recargar sin red y verificar el LOD cacheado.
10. Consola: sin errores nuevos.

## Rollback

- El código y los datos son reversibles con `git revert` del commit de release.
- No se modificaron GLB ni `public/sw.js`; la caché global sigue en `v36`.
- Caral conserva `model.glb` v1 como fallback y rollback.
