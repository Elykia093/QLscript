#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 20 8 * * *
new Env('恩山无线论坛')

环境变量:
  ENSHAN_COOKIE 必填，恩山论坛 Cookie。多账号建议用换行分隔，兼容 & 或 #。

依赖:
  Python: requests
  青龙通知: notify.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, cookie_name, format_results, send_notify, split_accounts

SCRIPT_NAME = "恩山无线论坛"
ENV_NAME = "ENSHAN_COOKIE"
TIMEOUT = 15
PROFILE_URL = "https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1"


def extract_credit(html: str) -> tuple[str, str]:
    coin = re.findall(r"恩山币:\s*</em>(.*?)&nbsp;", html)
    point = re.findall(r"<em>积分:\s*</em>(.*?)<span", html)
    if not coin or not point:
        raise RuntimeError("无法提取恩山币或积分，可能页面结构已变更")
    return coin[0].strip(), point[0].strip()


def run_account(cookie: str, index: int) -> AccountResult:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Cookie": cookie,
    }
    response = requests.get(PROFILE_URL, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    coin, point = extract_credit(response.text)
    return AccountResult(
        index=index,
        ok=True,
        title=cookie_name(cookie, index),
        message=f"恩山币：{coin}，积分：{point}",
    )


def main() -> int:
    accounts = split_accounts(os.getenv(ENV_NAME))
    if not accounts:
        message = f"未配置环境变量 {ENV_NAME}"
        send_notify(SCRIPT_NAME, message)
        return 1

    results: list[AccountResult] = []
    for index, account in enumerate(accounts, start=1):
        try:
            results.append(run_account(account, index))
        except Exception as error:
            results.append(
                AccountResult(index=index, ok=False, title=cookie_name(account, index), message=str(error))
            )

    content = format_results(results)
    send_notify(SCRIPT_NAME, content)
    return 0 if any(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
