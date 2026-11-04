# Chan Chan — plan 3D v0.1

Fecha: 4 de noviembre de 2026.
Estado: **preview de Nik An construido; QA de hardware pendiente**.
Alcance: conjunto amurallado Nik An, no las nueve ciudadelas ni los 20 km² de la ciudad.

## Objetivo

Publicar un preview navegable de Nik An con seis paradas, LOD0/LOD1, cuatro capas y evidencia explícita. La pieza debe leerse como una lectura de conjunto documentada, no como una reconstrucción final.

## Fuentes y evidencia

- Plaza principal: 65 × 75 m; cuatro accesos y rampa; muros de ~4 m de espesor.
- Muralla perimetral: 9–12 m de altura, base de ~5 m y coronamiento de ~1 m; acceso único por el norte.
- Nik An: plaza ceremonial principal, corredor de peces y aves, sala del altarcillo, audiencias, segunda plaza y reservorio.
- Adobe y relieves: técnica documentada; motivos geométricos, antropomorfos y zoomorfos citados en la literatura.
- Techos, alturas originales completas, policromía y posición fina de recintos: inferidos o interpretativos.

## Fases

1. **Fuentes y alcance:** dossier, cobertura y límites; sin copiar planos ni imágenes oficiales.
2. **Blockout:** recinto, plaza, corredor, audiencias, segunda plaza, depósitos, reservorio y plataforma.
3. **High-poly:** cursos de adobe, nichos, banquetas, relieves geométricos, terreno desértico y vegetación dispersa.
4. **Cámaras y datos:** seis paradas, cuatro capas, cámara hero y `city.json`.
5. **LOD y export:** LOD1 + Draco, WebP 80, fallback y `hero.jpg`.
6. **QA:** `validate`, `test`, `build`, `bench`; desktop 1600×900; móvil/1080p pendiente por #71.

## Límites

- No se modelan las nueve ciudadelas, los 32 conjuntos semi-monumentales ni la ciudad completa.
- No se reconstruyen techos, alturas perdidas, policromía completa ni relieves iconográficos cerrados.
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
