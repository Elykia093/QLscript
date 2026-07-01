#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 10 8 * * *
new Env('示例任务')

环境变量:
  QL_TEMPLATE_TOKEN 必填，多账号建议用换行分隔，兼容 & 或 #。

依赖:
  青龙通知: notify.py
"""

from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, format_results, mask_secret, send_notify, split_accounts

SCRIPT_NAME = "示例任务"
ENV_NAME = "QL_TEMPLATE_TOKEN"


def run_account(account: str, index: int) -> AccountResult:
    """替换这里的示例逻辑，所有外部请求必须设置 timeout。"""
    safe_account = mask_secret(account)
    return AccountResult(index=index, ok=True, title=f"账号{index}", message=f"执行完成: {safe_account}")


def main() -> int:
    accounts = split_accounts(os.getenv(ENV_NAME))
    if not accounts:
        message = f"未配置环境变量 {ENV_NAME}"
        print(message)
        send_notify(SCRIPT_NAME, message)
        return 1

    results: list[AccountResult] = []
    for index, account in enumerate(accounts, start=1):
        try:
            results.append(run_account(account, index))
        except Exception as error:
            traceback.print_exc()
            results.append(AccountResult(index=index, ok=False, title=f"账号{index}", message=str(error)))

    content = format_results(results)
    send_notify(SCRIPT_NAME, content)

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
