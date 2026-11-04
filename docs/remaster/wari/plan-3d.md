# Wari — plan 3D v0.1

Fecha: 4 de noviembre de 2026.
Estado: **preview del núcleo monumental construido; QA de hardware pendiente**.
Alcance: Vegachayoc Moqo, Capillapata, Monqachayoc y Cheqo Huasi; no las 2.000 ha del sitio.

## Objetivo

Publicar un preview navegable del núcleo monumental con seis paradas, LOD0/LOD1, cuatro capas y evidencia explícita. La pieza debe leerse como una lectura de conjunto documentada, no como una reconstrucción final.

## Fuentes y evidencia

- Templos en D: documentados en Vegachayoc Moqo, Capillapata, Monqachayoc y Cheqo Huasi.
- Capillapata: muros dobles de 8–12 m, base ~3 m, coronamiento 0,8–1,2 m y ~400 m de longitud; se modela un segmento de 360 m.
- Monqachayoc: mausoleo, galerías subterráneas, patio hundido y estructura en D; profundidad publicada ~8 m.
- Muros de piedra con mortero y revoques blancos/rojos; murales y policromía parcial.
- Trazado urbano completo, alturas, techos y población: discutidos, inferidos o interpretativos.

## Fases

1. **Fuentes y alcance:** dossier, cobertura y límites; sin copiar planos ni imágenes oficiales.
2. **Blockout:** terrazas, plaza, D-temples, Capillapata, Monqachayoc y Cheqo Huasi.
3. **High-poly:** muros de piedra, nichos, galerías, revoques, terreno y vegetación andina.
4. **Cámaras y datos:** seis paradas, cuatro capas, cámara hero y `city.json`.
5. **LOD y export:** LOD1 + Draco, WebP 80, fallback y `hero.jpg`.
6. **QA:** `validate`, `test`, `build`, `bench`; desktop 1600×900; móvil/1080p pendiente por #71.

## Límites

- No se modelan las 2.000 ha, los barrios completos ni el trazado urbano cerrado.
- No se reconstruyen techos, alturas perdidas, policromía completa ni el interior de las galerías.
- Monqachayoc se representa como corte interpretativo; no cierra la profundidad real.
- No se usan imágenes oficiales ni texturas de IA.
- La QA de hardware real no está cerrada: `qa: partial`, no `released`.

## Criterios de aceptación

- [x] Dossier, cobertura y plan 3D.
- [x] GLB LOD0/LOD1 con `extras.layer`.
- [x] Seis paradas y cuatro capas.
- [x] `hero.jpg` propio y `city.json` coherente con el índice.
- [x] `npm run validate`, `npm run build` y `npm run bench`.
- [x] QA desktop 1600×900.
- [ ] QA móvil/1080p/kiosco.
