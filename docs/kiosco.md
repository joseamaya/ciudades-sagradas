# Modo museo / kiosco

## Objetivo

Una estación táctil de 1080p que funcione sin internet, con una experiencia de 3–8 minutos y retorno automático al atlas.

## Hardware recomendado

- Mini-PC con GPU dedicada de gama media (GTX 1660 / RTX 3060 o equivalente).
- Pantalla táctil 1920 × 1080, 16:9, brillo alto.
- 16 GB de RAM, SSD.
- Sonido estéreo a volumen moderado.
- Chasis con bloqueo físico y arranque automático.

## Software

- Chromium o Chrome en modo kiosco:
  ```bash
  ./scripts/kiosk.sh http://127.0.0.1:8080/?kiosk=1
  ```
- Servidor local estático (`npx serve dist` o Caddy).
- Sin barras del navegador, sin teclado visible.
- El service worker cachea el atlas y el LOD cargado tras la primera visita. No precarga el otro LOD ni el fallback v1.

## Comportamiento

- `?kiosk=1` activa botones grandes y el temporizador de inactividad.
- Tras 90 segundos sin toques, vuelve al atlas.
- El audio ambiental se activa con el primer toque (política de autoplay). La narración grabada queda pendiente.
- La ficha se abre en panel inferior en pantallas táctiles.
- El recorrido avanza con flechas grandes.

## Actualización

1. Copiar el nuevo `dist/` al equipo.
2. Si reemplazaste un modelo en la misma ruta, sube `CACHE` en `public/sw.js` y actualiza `docs/fuentes/registro-assets.csv` para invalidar la copia offline.
3. Limpiar la caché del service worker si cambió la versión.
4. Probar en el equipo antes de abrir al público.

## Accesibilidad

- Contraste alto y texto grande.
- Botones de al menos 44 × 44 px; en kiosco, 52 px.
- No depender del hover.
- Navegación con teclado y flechas.
- Respeto a `prefers-reduced-motion`.

## Pruebas mínimas

- Carga en frío con internet desactivado después de la primera visita (se cachea el LOD elegido, no el fallback).
- 30 minutos de recorrido sin fugas de memoria evidentes.
- Reinicio del equipo y arranque automático.
- Audio y silencio.
- Pantalla táctil: toque, arrastre y doble toque.
