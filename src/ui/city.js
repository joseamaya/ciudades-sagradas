import { evidenceBadge, statusBadges } from './status.js';

function facts(city) {
  const rows = [
    ['Cultura', city.culture],
    ['Período', city.period],
    ['Región', city.region],
    ['Altitud', city.elevation],
  ];
  if (city.coordinates) {
    rows.push([
      'Coordenadas',
      `${city.coordinates.lat.toFixed(3)}°, ${city.coordinates.lon.toFixed(3)}°`,
    ]);
  }
  return rows.map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`).join('');
}

function sources(city) {
  return (city.sources || [])
    .map(
      (source) =>
        `<li><a href="${source.url}" target="_blank" rel="noreferrer">${source.label}<span aria-hidden="true">↗</span></a></li>`,
    )
    .join('');
}

export function renderCity(root, city) {
  const isAvailable = city.availability === 'available';
  const tour = city.tour || [];
  const layers = city.layers || [];

  if (!isAvailable) {
    root.innerHTML = `
      <section class="city-view city-view--research" style="--accent:${city.accent || '#d9a441'}">
        <div class="research-hero">
          <a class="back-link" href="#/">← Volver al atlas</a>
          <div class="research-hero__content">
            <span class="eyebrow">${city.culture} · ${city.period}</span>
            <h1>${city.name}</h1>
            <p class="research-hero__subtitle">${city.subtitle}</p>
            <div class="research-status">${statusBadges(city, { includeMaturity: true })}</div>
          </div>
        </div>
        <div class="research-body">
          <div class="research-main">
            <p class="lede">${city.summary}</p>
            <div class="research-note">
              <h2>La reconstrucción 3D está en preparación</h2>
              <p>Esta ficha documental reúne el estado de las fuentes y la cobertura. El modelo 3D se publicará cuando haya evidencia, licencias y revisión suficientes.</p>
            </div>
            <dl class="facts">${facts(city)}</dl>
            <p class="disclaimer">${city.disclaimer || ''}</p>
          </div>
          <aside class="research-sources">
            <h2>Fuentes públicas</h2>
            <ul class="source-list">${sources(city)}</ul>
            <p class="credits">${city.credits || ''}</p>
          </aside>
        </div>
      </section>`;
    return { available: false };
  }

  root.innerHTML = `
    <section class="city-view" style="--accent:${city.accent || '#d9a441'}">
      <div
        id="city-canvas"
        class="city-canvas"
        role="img"
        aria-label="Vista 3D de ${city.name}"
        aria-describedby="city-canvas-help"
      ></div>
      <p id="city-canvas-help" class="sr-only">
        Escena 3D de ${city.name}. El recorrido, las capas y la hora del día se controlan con los botones de la ficha.
      </p>

      <header class="city-topbar">
        <a class="back-link" href="#/">← Atlas</a>
        <div class="city-heading">
          <span class="eyebrow">${city.culture}</span>
          <h1>${city.name}</h1>
          <p>${city.subtitle}</p>
          <div class="city-status">${statusBadges(city, { includeMaturity: true })}</div>
        </div>
        <div class="city-tools">
          <button id="sound" class="tool" type="button" aria-pressed="false">Sonido <span class="tool__dot"></span></button>
          <button
            id="info-toggle"
            class="tool tool--icon"
            type="button"
            aria-label="Mostrar u ocultar la ficha"
            aria-controls="city-panel"
            aria-expanded="true"
          >
            Ficha
          </button>
        </div>
      </header>

      <aside id="city-panel" class="city-panel" aria-label="Ficha de la ciudad">
        <button id="panel-close" class="panel-close" type="button" aria-label="Cerrar ficha">×</button>
        <div class="panel-scroll">
          <p class="lede">${city.summary}</p>
          <dl class="facts">${facts(city)}</dl>

          <section>
            <h2>Recorrido</h2>
            <ol class="tour-list" id="tour-list">
              ${tour
                .map(
                  (stop, index) => `
                    <li>
                      <button
                        type="button"
                        data-tour="${index}"
                        class="${index === 0 ? 'is-active' : ''}"
                        aria-current="${index === 0 ? 'true' : 'false'}"
                      >
                        <span class="tour-list__index">${String(index + 1).padStart(2, '0')}</span>
                        <span class="tour-list__title">${stop.title}</span>
                        ${evidenceBadge(stop.evidence, true)}
                      </button>
                    </li>`,
                )
                .join('')}
            </ol>
            <div class="evidence-legend">
              <span>Nivel de evidencia</span>
              ${evidenceBadge('documented', true)}
              ${evidenceBadge('inferred', true)}
              ${evidenceBadge('interpretive', true)}
            </div>
          </section>

          <section>
            <h2>Capas</h2>
            <div class="layer-list">
              ${layers
                .map(
                  (layer) => `
                    <label class="layer">
                      <input type="checkbox" data-layer="${layer.id}" ${layer.default !== false ? 'checked' : ''} />
                      <span>${layer.label}</span>
                    </label>`,
                )
                .join('')}
            </div>
          </section>

          <section>
            <h2>Luz</h2>
            <div class="time-list" role="group" aria-label="Hora del día">
              <button type="button" data-time="morning" class="is-active" aria-pressed="true">Amanecer</button>
              <button type="button" data-time="noon" aria-pressed="false">Mediodía</button>
              <button type="button" data-time="dusk" aria-pressed="false">Atardecer</button>
              <button type="button" data-time="night" aria-pressed="false">Noche</button>
            </div>
          </section>

          <section>
            <h2>Fuentes públicas</h2>
            <ul class="source-list">${sources(city)}</ul>
          </section>

          <p class="disclaimer">${city.disclaimer || ''}</p>
          <p class="credits">${city.credits || ''}</p>
        </div>
      </aside>

      <div class="tour-bar" id="tour-bar">
        <button id="tour-prev" class="tour-arrow" type="button" aria-label="Parada anterior">←</button>
        <div class="tour-copy" aria-live="polite">
          <span class="eyebrow" id="tour-count">01 / ${String(tour.length).padStart(2, '0')}</span>
          <div class="tour-heading">
            <h2 id="tour-title">${tour[0]?.title || city.name}</h2>
            <span id="tour-evidence">${evidenceBadge(tour[0]?.evidence, true)}</span>
          </div>
          <p id="tour-text">${tour[0]?.text || city.summary}</p>
        </div>
        <button id="tour-next" class="tour-arrow" type="button" aria-label="Parada siguiente">→</button>
      </div>

      <div class="city-hint">Arrastra para orbitar · rueda para acercarte · H oculta la interfaz</div>
    </section>`;

  return {
    available: true,
    canvas: root.querySelector('#city-canvas'),
    panel: root.querySelector('#city-panel'),
    panelClose: root.querySelector('#panel-close'),
    infoToggle: root.querySelector('#info-toggle'),
    sound: root.querySelector('#sound'),
    tourBar: root.querySelector('#tour-bar'),
    tourPrev: root.querySelector('#tour-prev'),
    tourNext: root.querySelector('#tour-next'),
    tourCount: root.querySelector('#tour-count'),
    tourTitle: root.querySelector('#tour-title'),
    tourText: root.querySelector('#tour-text'),
    tourEvidence: root.querySelector('#tour-evidence'),
    tourList: root.querySelector('#tour-list'),
    timeButtons: [...root.querySelectorAll('[data-time]')],
    layerInputs: [...root.querySelectorAll('[data-layer]')],
  };
}
