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
const ENV_NAME = 'QL_TEMPLATE_TOKEN';
const { splitAccounts, maskSecret, sendNotification } = require('../utils/ql_common');

async function runAccount(account, index) {
  // 替换这里的示例逻辑，所有外部请求必须设置 timeout。
  const safeAccount = maskSecret(account);
  return {
    index,
    ok: true,
    message: `账号${index}执行完成: ${safeAccount}`,
  };
}

async function main() {
  const accounts = splitAccounts(process.env[ENV_NAME]);
  if (accounts.length === 0) {
    const message = `未配置环境变量 ${ENV_NAME}`;
    console.log(message);
    await sendNotification(SCRIPT_NAME, message);
    process.exitCode = 1;
    return;
  }

  const results = [];
  for (let index = 0; index < accounts.length; index += 1) {
    const accountNo = index + 1;
    try {
      results.push(await runAccount(accounts[index], accountNo));
    } catch (error) {
      console.error(error);
      results.push({
        index: accountNo,
        ok: false,
        message: `账号${accountNo}失败: ${error.message || error}`,
      });
    }
  }

  const content = results
    .map(result => `${result.ok ? '成功' : '失败'} | 账号${result.index}: ${result.message}`)
    .join('\n');

  await sendNotification(SCRIPT_NAME, content);

  if (results.some(result => !result.ok)) {
    process.exitCode = 1;
  }
}

main().catch(error => {
  console.error(`${SCRIPT_NAME}运行失败:`, error);
  process.exitCode = 1;
});
