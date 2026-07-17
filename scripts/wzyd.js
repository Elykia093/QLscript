/*
cron: 40 8 * * *
new Env('王者营地')

环境变量:
  WZYD_HEADERS 必填，请求头 JSON 对象。多账号建议用换行分隔，兼容 & 或 #。
  WZYD_BODY 必填，请求体 JSON 对象。多账号数量和 WZYD_HEADERS 保持一致。
  WZYD_TOKEN 兼容旧变量名，建议迁移到 WZYD_HEADERS。

依赖:
  Node.js >= 18
  青龙通知: sendNotify.js
*/

'use strict';

const {
  errorMessage,
  formatResults,
  maskSecret,
  requestJson,
  sendNotification,
  splitJsonAccounts,
} = require('../utils/ql_common');

const SCRIPT_NAME = '王者营地';
const HEADERS_ENV_NAME = 'WZYD_HEADERS';
const LEGACY_HEADERS_ENV_NAME = 'WZYD_TOKEN';
const BODY_ENV_NAME = 'WZYD_BODY';
const SIGN_URL = 'https://kohcamp.qq.com/operation/action/signin';

function parseJsonObject(value, label, accountIndex) {
  let parsed;
  try {
    parsed = JSON.parse(value);
  } catch (error) {
    throw new Error(`账号${accountIndex}${label}不是合法 JSON: ${error.message}`);
  }

  if (parsed === null || Array.isArray(parsed) || typeof parsed !== 'object') {
    throw new Error(`账号${accountIndex}${label}必须是 JSON 对象`);
  }
  return parsed;
}

async function runAccount(headerText, bodyText, accountIndex) {
  const headers = parseJsonObject(headerText, '请求头', accountIndex);
  const payload = parseJsonObject(bodyText, '请求体', accountIndex);
  const data = await requestJson(SIGN_URL, {
    method: 'POST',
    headers: {
      ...headers,
      'content-type': 'application/json',
    },
    body: JSON.stringify(payload),
    timeout: 15000,
  });

  const roleId = payload.roleId ? maskSecret(String(payload.roleId), 2) : `账号${accountIndex}`;
  return {
    index: accountIndex,
    ok: true,
    title: roleId,
    message: JSON.stringify(data),
  };
}

async function main() {
  const headerTexts = splitJsonAccounts(
    process.env[HEADERS_ENV_NAME] || process.env[LEGACY_HEADERS_ENV_NAME],
  );
  const bodyTexts = splitJsonAccounts(process.env[BODY_ENV_NAME]);

  if (headerTexts.length === 0 || bodyTexts.length === 0) {
    await sendNotification(SCRIPT_NAME, `未配置环境变量 ${HEADERS_ENV_NAME} 或 ${BODY_ENV_NAME}`);
    process.exitCode = 1;
    return;
  }

  if (headerTexts.length !== bodyTexts.length) {
    await sendNotification(SCRIPT_NAME, `${HEADERS_ENV_NAME} 和 ${BODY_ENV_NAME} 账号数量不一致`);
    process.exitCode = 1;
    return;
  }

  const results = [];
  for (const [accountOffset, headerText] of headerTexts.entries()) {
    const accountIndex = accountOffset + 1;
    try {
      results.push(await runAccount(headerText, bodyTexts[accountOffset], accountIndex));
    } catch (error) {
      results.push({
        index: accountIndex,
        ok: false,
        title: `账号${accountIndex}`,
        message: errorMessage(error),
      });
    }
  }

  await sendNotification(SCRIPT_NAME, formatResults(results));
  if (!results.some(result => result.ok)) {
    process.exitCode = 1;
  }
}

main().catch(error => {
  console.error(`${SCRIPT_NAME}运行失败: ${errorMessage(error)}`);
  process.exitCode = 1;
});
