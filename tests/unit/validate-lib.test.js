import assert from 'node:assert/strict';
import { test } from 'node:test';
import { isNumberTriplet, parseCsv } from '../../scripts/validate-lib.mjs';

test('isNumberTriplet exige tres números finitos', () => {
  assert.equal(isNumberTriplet([1, 2.5, -3]), true);
  assert.equal(isNumberTriplet([1, 2]), false);
  assert.equal(isNumberTriplet([1, 2, 3, 4]), false);
  assert.equal(isNumberTriplet([1, Number.NaN, 3]), false);
  assert.equal(isNumberTriplet('1,2,3'), false);
});

test('parseCsv separa campos, comas y comillas escapadas', () => {
  assert.deepEqual(parseCsv('a,b\n1,2\n'), [
    ['a', 'b'],
    ['1', '2'],
  ]);
  assert.deepEqual(parseCsv('a,"b,c",d\n'), [['a', 'b,c', 'd']]);
  assert.deepEqual(parseCsv('a,"b""c"\n'), [['a', 'b"c']]);
  assert.deepEqual(parseCsv('a,b\r\n1,2'), [
    ['a', 'b'],
    ['1', '2'],
  ]);
  assert.deepEqual(parseCsv('a,,\n'), [['a', '', '']]);
});

test('parseCsv devuelve vacío para texto vacío', () => {
  assert.deepEqual(parseCsv(''), []);
});
