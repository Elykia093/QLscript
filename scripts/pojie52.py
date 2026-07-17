#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 5 9 * * *
new Env('吾爱破解')

环境变量:
  POJIE52_COOKIE 必填，吾爱破解论坛 Cookie。多账号建议用换行分隔，兼容 & 或 #。

依赖:
  Python: requests
  青龙通知: notify.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, cookie_name, run_accounts

SCRIPT_NAME = "吾爱破解"
ACCOUNT_ENV_NAME = "POJIE52_COOKIE"
TIMEOUT = 15

BASE_URL = "https://www.52pojie.cn"
SIGN_PAGE_URL = f"{BASE_URL}/plugin.php?id=dsu_paulsign:sign"
SIGN_POST_URL = f"{BASE_URL}/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1"
CREDIT_URL = f"{BASE_URL}/home.php?mod=spacecp&ac=credit&showcredit=1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
}


def extract_formhash(html: str) -> str:
    patterns = (
        r'name="formhash"\s+value="([^"]+)"',
        r"formhash=([a-zA-Z0-9]+)",
        r"'formhash'\s*:\s*'([^']+)'",
    )
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    raise RuntimeError("未找到 formhash，Cookie 可能失效或页面结构已变更")


def extract_credit(html: str) -> str:
    items = re.findall(r"<em>([^<:：]+)[:：]\s*</em>\s*([^<\s]+)", html)
    if not items:
        return "未获取到积分信息"
    wanted = []
    for name, value in items:
        if any(keyword in name for keyword in ("吾爱币", "积分", "热心值", "技术成就")):
            wanted.append(f"{name.strip()} {value.strip()}")
    return "，".join(wanted[:4]) if wanted else "，".join(f"{name.strip()} {value.strip()}" for name, value in items[:4])


def run_account(cookie: str, account_index: int) -> AccountResult:
    title = cookie_name(cookie, account_index)
    headers = {**HEADERS, "Cookie": cookie, "Referer": BASE_URL}
    with requests.Session() as session:
        page = session.get(SIGN_PAGE_URL, headers=headers, timeout=TIMEOUT)
        page.raise_for_status()

        if "您今天已经签到过了" in page.text or "今日已签" in page.text:
            credit = session.get(CREDIT_URL, headers=headers, timeout=TIMEOUT)
            credit.raise_for_status()
            return AccountResult(
                index=account_index,
                ok=True,
                title=title,
                message=f"今日已签到，{extract_credit(credit.text)}",
            )

        formhash = extract_formhash(page.text)
        payload = {
            "formhash": formhash,
            "qdxq": "kx",
            "qdmode": "1",
            "todaysay": "每日签到",
            "fastreply": "0",
        }
        response = session.post(SIGN_POST_URL, headers=headers, data=payload, timeout=TIMEOUT)
        response.raise_for_status()
        text = response.text
        if any(keyword in text for keyword in ("签到成功", "您今天已经签到过了", "今日已签")):
            credit = session.get(CREDIT_URL, headers=headers, timeout=TIMEOUT)
            credit.raise_for_status()
            return AccountResult(
                index=account_index,
                ok=True,
                title=title,
                message=f"签到完成，{extract_credit(credit.text)}",
            )

        clean_text = re.sub(r"<[^>]+>", "", text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        raise RuntimeError(clean_text[:80] or "签到失败")


def main() -> int:
    return run_accounts(SCRIPT_NAME, ACCOUNT_ENV_NAME, run_account, cookie_name)


if __name__ == "__main__":
    raise SystemExit(main())
