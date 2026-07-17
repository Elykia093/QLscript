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

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, mask_secret, run_accounts

SCRIPT_NAME = "示例任务"
ACCOUNT_ENV_NAME = "QL_TEMPLATE_TOKEN"


def account_title(account: str, account_index: int) -> str:
    return f"账号{account_index}-{mask_secret(account)}"


def run_account(account: str, account_index: int) -> AccountResult:
    """替换这里的示例逻辑，所有外部请求必须设置 timeout。"""
    return AccountResult(
        index=account_index,
        ok=True,
        title=account_title(account, account_index),
        message="执行完成",
    )


def main() -> int:
    return run_accounts(SCRIPT_NAME, ACCOUNT_ENV_NAME, run_account, account_title)


if __name__ == "__main__":
    raise SystemExit(main())
