export function renderCatalog(root, cities) {
  const available = cities.filter((city) => city.status === 'available').length;
  const cards = cities
    .map((city) => {
      const available = city.status === 'available';
      const media = city.thumb
        ? `<div class="city-card__media" style="background-image:url('${city.thumb}')"></div>`
        : `<div class="city-card__media city-card__media--empty" style="--accent:${city.accent}">
             <span>${city.monogram || city.name.slice(0, 1)}</span>
             <small>En investigación</small>
           </div>`;
      return `
        <a class="city-card${available ? ' city-card--available' : ''}" href="#/ciudad/${city.id}" aria-label="${city.name}: ${city.subtitle}">
          ${media}
          <div class="city-card__body">
            <div class="city-card__kicker">
              <span>${city.culture}</span>
              <span class="badge ${available ? 'badge--live' : ''}">${available ? 'Disponible' : 'En investigación'}</span>
            </div>
            <h2>${city.name}</h2>
            <p class="city-card__subtitle">${city.subtitle}</p>
            <p class="city-card__summary">${city.summary}</p>
            <div class="city-card__meta">
              <span>${city.period}</span>
              <span>${city.region}</span>
            </div>
          </div>
        </a>`;
    })
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
          <div class="catalog__stats">
            <span><strong>${cities.length}</strong> ciudades</span>
            <span><strong>${available}</strong> disponible${available === 1 ? '' : 's'}</span>
            <span><strong>5000</strong> años</span>
          </div>
        </div>
      </header>

      <div class="city-grid">${cards}</div>

      <footer class="catalog__footer">
        <p>Reconstrucciones artísticas basadas en fuentes arqueológicas públicas. No son fotografías históricas.</p>
        <p>Hecho para museos, aulas y curiosos. <span class="dot">·</span> Español</p>
      </footer>
    </section>`;
}
