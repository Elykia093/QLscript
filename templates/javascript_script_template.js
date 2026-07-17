/*
cron: 10 8 * * *
new Env('示例任务')

环境变量:
  QL_TEMPLATE_TOKEN 必填，多账号建议用换行分隔，兼容 & 或 #。

依赖:
  青龙通知: sendNotify.js
*/

'use strict';

const SCRIPT_NAME = '示例任务';
const ACCOUNT_ENV_NAME = 'QL_TEMPLATE_TOKEN';
const {
  errorMessage,
  formatResults,
  maskSecret,
  sendNotification,
  splitAccounts,
} = require('../utils/ql_common');

function accountTitle(account, accountIndex) {
  return `账号${accountIndex}-${maskSecret(account)}`;
}

async function runAccount(account, accountIndex) {
  // 替换这里的示例逻辑，所有外部请求必须设置 timeout。
  return {
    index: accountIndex,
    ok: true,
    title: accountTitle(account, accountIndex),
    message: '执行完成',
  };
}

async function main() {
  const accounts = splitAccounts(process.env[ACCOUNT_ENV_NAME]);
  if (accounts.length === 0) {
    const message = `未配置环境变量 ${ACCOUNT_ENV_NAME}`;
    console.log(message);
    await sendNotification(SCRIPT_NAME, message);
    process.exitCode = 1;
    return;
  }

  const results = [];
  for (const [accountOffset, account] of accounts.entries()) {
    const accountIndex = accountOffset + 1;
    try {
      results.push(await runAccount(account, accountIndex));
    } catch (error) {
      const message = errorMessage(error);
      console.error(`账号${accountIndex}失败: ${message}`);
      results.push({
        index: accountIndex,
        ok: false,
        title: accountTitle(account, accountIndex),
        message,
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
