import { escapeAttr, escapeHtml } from './escape.js';
import { maturityLabel, statusBadges } from './status.js';

function joinNames(names) {
  if (names.length <= 1) return names[0] || '';
  return `${names.slice(0, -1).join(', ')} y ${names.at(-1)}`;
}

function catalogNotice(cities) {
  const released = cities.filter((city) => city.maturity === 'released');
  const preview = cities.filter((city) => city.maturity === 'preview');
  const research = cities.filter((city) => city.maturity === 'research');
  const parts = ['Preview público.'];

  if (released.length) {
    const references = released
      .map((city) => `${city.name}${city.version ? ` ${city.version}` : ''}`)
      .join(' y ');
    parts.push(`${references} ${released.length === 1 ? 'es' : 'son'} la referencia;`);
  }
  if (preview.length) {
    parts.push(
      `${joinNames(preview.map((city) => city.name))} ${preview.length === 1 ? 'sigue' : 'siguen'} en revisión.`,
    );
  }
  if (research.length) {
    parts.push(
      `${joinNames(research.map((city) => city.name))} ${research.length === 1 ? 'es ficha documental' : 'son fichas documentales'}.`,
    );
  }
  parts.push('La QA de hardware está en curso.');
  return parts.join(' ');
}

export function renderCatalog(root, cities) {
  const withModel = cities.filter((city) => city.availability === 'available').length;
  const oldestYears = Math.max(
    0,
    ...cities.map((city) => (Number.isFinite(city.yearsAgo) ? city.yearsAgo : 0)),
  );
  const cards = cities
    .map((city) => {
      const isAvailable = city.availability === 'available';
      const maturity = escapeHtml(maturityLabel(city));
      const accent = escapeAttr(city.accent || '#d9a441');
      const monogram = escapeHtml(city.monogram || city.name.slice(0, 1));
      const media = city.thumb
        ? `<div class="city-card__media" style="background-image:url('${escapeAttr(city.thumb)}')"></div>`
        : `<div class="city-card__media city-card__media--empty" style="--accent:${accent}">
             <span>${monogram}</span>
             <small>Ficha documental</small>
           </div>`;
      return `
        <a class="city-card${isAvailable ? ' city-card--available' : ''}" href="#/ciudad/${escapeAttr(city.id)}" aria-label="${escapeAttr(`${city.name}: ${city.subtitle}`)}">
          ${media}
          <div class="city-card__body">
            <div class="city-card__kicker">
              <span>${escapeHtml(city.culture)}</span>
              <span class="badge ${isAvailable ? 'badge--live' : ''}">${maturity}</span>
            </div>
            <h2>${escapeHtml(city.name)}</h2>
            <p class="city-card__subtitle">${escapeHtml(city.subtitle)}</p>
            <p class="city-card__summary">${escapeHtml(city.summary)}</p>
            <div class="city-card__status">${statusBadges(city)}</div>
            <div class="city-card__meta">
              <span>${escapeHtml(city.period)}</span>
              <span>${escapeHtml(city.region)}</span>
            </div>
          </div>
        </a>`;
    })
    .join('');

  const stats = [
    `<span><strong>${cities.length}</strong> ciudades</span>`,
    `<span><strong>${withModel}</strong> con modelo 3D</span>`,
    oldestYears
      ? `<span><strong>${oldestYears.toLocaleString('es')}</strong> años</span>`
      : '',
  ]
    .filter(Boolean)
    .join('');

  root.innerHTML = `
    <section class="catalog">
      <header class="catalog__header">
        <div class="catalog__brand">
          <span class="eyebrow">Atlas del Perú antiguo</span>
          <h1>Ciudades<br /><em>Sagradas</em></h1>
        </div>
        <div class="catalog__intro">
          <p class="lede">Reconstrucciones 3D de los grandes centros ceremoniales y ciudades del Perú prehispánico.</p>
          <p>Un atlas para mirar de cerca la arquitectura, el paisaje y la memoria de sociedades que transformaron los Andes. Cada ficha distingue lo documentado de lo interpretado.</p>
          <div class="catalog__stats">${stats}</div>
          <p class="catalog__notice">${escapeHtml(catalogNotice(cities))}</p>
        </div>
      </header>

      <div class="city-grid">${cards}</div>

      <footer class="catalog__footer">
        <p>Reconstrucciones artísticas basadas en fuentes arqueológicas públicas. No son fotografías históricas.</p>
        <p>Hecho para museos, aulas y curiosos. <span class="dot">·</span> Español</p>
      </footer>
    </section>`;
}
