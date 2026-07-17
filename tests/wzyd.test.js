'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');

const { parseJsonObject, parseSignResponse } = require('../scripts/wzyd');

test('parseJsonObject accepts objects and rejects arrays', () => {
  assert.deepEqual(parseJsonObject('{"roleId":"1"}', '请求体', 1), { roleId: '1' });
  assert.throws(() => parseJsonObject('[]', '请求体', 1), /必须是 JSON 对象/);
});

test('parseSignResponse accepts explicit root and nested success codes', () => {
  assert.equal(parseSignResponse({ code: 0, message: '签到成功' }), '签到成功');
  assert.equal(parseSignResponse({ data: { retcode: '0', msg: '已签到' } }), '已签到');
  assert.equal(parseSignResponse({ result: 0 }), '签到成功（业务码 0）');
  assert.equal(parseSignResponse({ result: true }), '签到成功（业务码 true）');
  assert.equal(parseSignResponse({ success: true, message: 'done' }), 'done');
});

test('parseSignResponse rejects business failures even when text contains success', () => {
  assert.throws(
    () => parseSignResponse({ code: 999, message: '签到不成功' }),
    /业务码 999: 签到不成功/,
  );
  assert.throws(() => parseSignResponse({ success: false, message: 'failed' }), /业务码 unknown/);
});

test('parseSignResponse rejects missing or conflicting status', () => {
  assert.throws(() => parseSignResponse({ message: 'unknown' }), /缺少可识别的业务状态/);
  assert.throws(
    () => parseSignResponse({ success: true, code: 500 }),
    /success 与业务码相互冲突/,
  );
  assert.throws(() => parseSignResponse([]), /必须是 JSON 对象/);
});

test('parseSignResponse limits notification message length', () => {
  assert.equal(parseSignResponse({ code: 0, message: 'x'.repeat(500) }).length, 300);
});
