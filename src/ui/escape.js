const ENTITIES = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};

const HEX_COLOR = /^#[0-9a-f]{6}$/i;
const HERO_PATH = /^cities\/[a-z0-9-]+\/hero\.(?:jpe?g|png|webp)$/;

export function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, (character) => ENTITIES[character]);
}

export const escapeAttr = escapeHtml;

export function safeAccent(value, fallback = '#d9a441') {
  return HEX_COLOR.test(value || '') ? value : fallback;
}

export function safeHeroPath(value) {
  return HERO_PATH.test(value || '') ? value : '';
}

export function safeHttpsUrl(value) {
  try {
    const url = new URL(String(value));
    return url.protocol === 'https:' ? url.href : '';
  } catch {
    return '';
  }
}
