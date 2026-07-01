/*
cron: 40 8 * * *
new Env('王者营地')

环境变量:
  WZYD_TOKEN 必填，请求头 JSON。多账号建议用换行分隔，兼容 & 或 #。
  WZYD_BODY 必填，请求体 JSON。多账号数量和 WZYD_TOKEN 保持一致。

依赖:
  Node.js >= 18
  青龙通知: sendNotify.js
*/

'use strict';

const {
  maskSecret,
  requestJson,
  sendNotification,
  splitAccounts,
} = require('../utils/ql_common');

const SCRIPT_NAME = '王者营地';
const TOKEN_ENV = 'WZYD_TOKEN';
const BODY_ENV = 'WZYD_BODY';
const SIGN_URL = 'https://kohcamp.qq.com/operation/action/signin';

function parseJson(value, label, index) {
  try {
    return JSON.parse(value);
  } catch (error) {
    throw new Error(`账号${index}${label}不是合法 JSON: ${error.message}`);
  }
}

async function runAccount(headerText, bodyText, index) {
  const headers = parseJson(headerText, '请求头', index);
  const payload = parseJson(bodyText, '请求体', index);
  const data = await requestJson(SIGN_URL, {
    method: 'POST',
    headers: {
      ...headers,
      'content-type': 'application/json',
    },
    body: JSON.stringify(payload),
    timeout: 15000,
  });

  const roleId = payload.roleId ? maskSecret(String(payload.roleId), 2) : `账号${index}`;
  return {
    index,
    ok: true,
    title: roleId,
    message: JSON.stringify(data),
  };
}

async function main() {
  const tokens = splitAccounts(process.env[TOKEN_ENV]);
  const bodies = splitAccounts(process.env[BODY_ENV]);

  if (tokens.length === 0 || bodies.length === 0) {
    await sendNotification(SCRIPT_NAME, `未配置环境变量 ${TOKEN_ENV} 或 ${BODY_ENV}`);
    process.exitCode = 1;
    return;
  }

  if (tokens.length !== bodies.length) {
    await sendNotification(SCRIPT_NAME, `${TOKEN_ENV} 和 ${BODY_ENV} 账号数量不一致`);
    process.exitCode = 1;
    return;
  }

  const results = [];
  for (let index = 0; index < tokens.length; index += 1) {
    const accountNo = index + 1;
    try {
      results.push(await runAccount(tokens[index], bodies[index], accountNo));
    } catch (error) {
      results.push({
        index: accountNo,
        ok: false,
        title: `账号${accountNo}`,
        message: error.message || String(error),
      });
    }
  }

  const content = results
    .map(result => `${result.ok ? '成功' : '失败'} | 账号${result.index} | ${result.title}: ${result.message}`)
    .join('\n');

  await sendNotification(SCRIPT_NAME, content);
  if (!results.some(result => result.ok)) {
    process.exitCode = 1;
  }
}

main().catch(error => {
  console.error(`${SCRIPT_NAME}运行失败:`, error);
  process.exitCode = 1;
});
