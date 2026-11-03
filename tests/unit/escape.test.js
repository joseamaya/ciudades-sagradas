import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  escapeAttr,
  escapeHtml,
  safeAccent,
  safeHeroPath,
  safeHttpsUrl,
} from '../../src/ui/escape.js';

test('escapeHtml y escapeAttr escapan todos los caracteres peligrosos', () => {
  assert.equal(escapeHtml(`<a href="x">'&'</a>`), '&lt;a href=&quot;x&quot;&gt;&#39;&amp;&#39;&lt;/a&gt;');
  assert.equal(escapeAttr('<>&"'), '&lt;&gt;&amp;&quot;');
  assert.equal(escapeHtml(), '');
});

test('safeAccent acepta hex de seis dígitos y aplica fallback', () => {
  assert.equal(safeAccent('#d9a441'), '#d9a441');
  assert.equal(safeAccent('#ABCDEF'), '#ABCDEF');
  assert.equal(safeAccent('red'), '#d9a441');
  assert.equal(safeAccent(null), '#d9a441');
  assert.equal(safeAccent('red', '#000000'), '#000000');
});

test('safeHeroPath solo acepta rutas de portada válidas', () => {
  assert.equal(safeHeroPath('cities/caral/hero.jpg'), 'cities/caral/hero.jpg');
  assert.equal(safeHeroPath('cities/chan-chan/hero.png'), 'cities/chan-chan/hero.png');
  assert.equal(safeHeroPath('cities/caral/hero.webp'), 'cities/caral/hero.webp');
  assert.equal(safeHeroPath('cities/caral/hero.gif'), '');
  assert.equal(safeHeroPath('../cities/caral/hero.jpg'), '');
  assert.equal(safeHeroPath(''), '');
});

test('safeHttpsUrl solo permite https y normaliza la URL', () => {
  assert.equal(safeHttpsUrl('https://example.com/a'), 'https://example.com/a');
  assert.equal(safeHttpsUrl('http://example.com'), '');
  assert.equal(safeHttpsUrl('javascript:alert(1)'), '');
  assert.equal(safeHttpsUrl('no-es-url'), '');
  assert.equal(safeHttpsUrl(null), '');
});
