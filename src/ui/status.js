import { escapeHtml } from './escape.js';

const MATURITY_LABELS = {
  research: 'Investigación',
  blockout: 'Blockout',
  preview: 'Preview',
  released: 'Publicada',
};

const EVIDENCE_LABELS = {
  documented: 'Documentado',
  mixed: 'Evidencia mixta',
  interpretive: 'Interpretativo',
  'not-applicable': 'Ficha documental',
};

const EVIDENCE_HINTS = {
  documented: 'La forma principal se apoya en planos, excavaciones o levantamientos publicados.',
  mixed: 'Combina elementos documentados, inferidos e interpretativos; cada parada lo indica.',
  interpretive: 'Propuesta visual para facilitar la lectura; no es una reconstrucción arqueológica cerrada.',
  'not-applicable': 'Ficha documental sin modelo 3D publicado.',
};

const QA_LABELS = {
  passed: 'QA aprobada',
  partial: 'QA parcial',
  pending: 'QA pendiente',
  waived: 'Excepción P2 aceptada',
};

const QA_HINTS = {
  passed: 'Contrastada en hardware real dentro del alcance documentado.',
  partial: 'Hay pruebas parciales o de producto, pero falta la matriz completa de hardware.',
  pending: 'Todavía no se ha probado en hardware real.',
  waived: 'Incidencia P2 conocida y aceptada; no equivale a cierre de QA.',
};

const STOP_EVIDENCE_LABELS = {
  documented: 'Documentado',
  inferred: 'Inferido',
  interpretive: 'Interpretativo',
};

const STOP_EVIDENCE_HINTS = {
  documented: 'La parada se apoya en evidencia publicada.',
  inferred: 'La parada deriva de evidencia parcial; los vacíos no se presentan como hechos.',
  interpretive: 'La parada es una propuesta visual para comprender el conjunto.',
};

export function maturityLabel(city) {
  const label = MATURITY_LABELS[city.maturity] || 'Estado';
  return city.version ? `${label} · ${city.version}` : label;
}

export function evidenceBadge(value, stop = false) {
  const labels = stop ? STOP_EVIDENCE_LABELS : EVIDENCE_LABELS;
  const hints = stop ? STOP_EVIDENCE_HINTS : EVIDENCE_HINTS;
  const label = labels[value] || 'Sin clasificar';
  return `<span class="status-badge status-badge--${escapeHtml(value)}" title="${escapeHtml(hints[value] || '')}">${escapeHtml(label)}</span>`;
}

export function qaBadge(value) {
  if (!value || value === 'not-applicable') return '';
  return `<span class="status-badge status-badge--qa-${escapeHtml(value)}" title="${escapeHtml(QA_HINTS[value] || '')}">${escapeHtml(QA_LABELS[value] || value)}</span>`;
}

export function statusBadges(city, { includeMaturity = false } = {}) {
  const badges = [];
  if (includeMaturity) {
    badges.push(`<span class="status-badge status-badge--maturity">${escapeHtml(maturityLabel(city))}</span>`);
  }
  badges.push(evidenceBadge(city.evidence));
  const qa = qaBadge(city.qa);
  if (qa) badges.push(qa);
  return badges.join('');
}
