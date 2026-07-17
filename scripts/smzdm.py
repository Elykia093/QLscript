#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 55 8 * * *
new Env('什么值得买')

环境变量:
  SMZDM_COOKIE 必填，什么值得买 Cookie。多账号建议用换行分隔，兼容 & 或 #。

依赖:
  Python: requests
  青龙通知: notify.py
"""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, cookie_name, run_accounts

SCRIPT_NAME = "什么值得买"
ACCOUNT_ENV_NAME = "SMZDM_COOKIE"
TIMEOUT = 15

CHECKIN_URL = "https://user-api.smzdm.com/checkin"
USER_AGENT = "smzdm_android_V10.8.40 rv:838 (Redmi Note 3;Android10.0;zh)smzdmapp"


def extract_cookie_value(cookie: str, key: str) -> str:
    match = re.search(rf"(?:^|;\s*){re.escape(key)}=([^;]+)", cookie)
    return match.group(1).strip() if match else ""


def random_request_key(length: int = 18) -> str:
    return "".join(random.choice("0123456789") for _ in range(length))


def build_headers(cookie: str) -> dict[str, str]:
    return {
        "Accept": "*/*",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "application/x-www-form-urlencoded",
        "request_key": random_request_key(),
        "User-Agent": USER_AGENT,
        "Cookie": cookie,
    }


def run_account(cookie: str, account_index: int) -> AccountResult:
    token = extract_cookie_value(cookie, "sess")
    if not token:
        raise RuntimeError("Cookie 缺少 sess")

    payload = {
        "touchstone_event": "",
        "sk": "1",
        "token": token,
        "captcha": "",
    }
    response = requests.post(CHECKIN_URL, headers=build_headers(cookie), data=payload, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()

    if str(data.get("error_code")) != "0":
        raise RuntimeError(data.get("error_msg") or data.get("message") or "签到失败")

    result = data.get("data") or {}
    message = (
        f"连续签到 {result.get('daily_num', '-')} 天，"
        f"金币 {result.get('cgold', '-')}，"
        f"碎银 {result.get('pre_re_silver', '-')}，"
        f"补签卡 {result.get('cards', '-')}"
    )
    return AccountResult(
        index=account_index,
        ok=True,
        title=cookie_name(cookie, account_index),
        message=message,
    )


def main() -> int:
    return run_accounts(SCRIPT_NAME, ACCOUNT_ENV_NAME, run_account, cookie_name)


if __name__ == "__main__":
    raise SystemExit(main())
