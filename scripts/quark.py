#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 50 8 * * *
new Env('夸克网盘')

环境变量:
  QUARK_COOKIE 必填，夸克网盘 Cookie。多账号建议用换行分隔，兼容 & 或 #。

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

from utils.ql_common import AccountResult, format_results, mask_secret, send_notify, split_accounts

SCRIPT_NAME = "夸克网盘"
ENV_NAME = "QUARK_COOKIE"
TIMEOUT = 15

BASE_URL = "https://drive-m.quark.cn"
GROWTH_INFO_URL = f"{BASE_URL}/1/clouddrive/capacity/growth/info"
GROWTH_SIGN_URL = f"{BASE_URL}/1/clouddrive/capacity/growth/sign"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 12; M2012K11AC) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Version/4.0 Chrome/103.0.0.0 Mobile Safari/537.36"
    ),
}


def extract_cookie_value(cookie: str, key: str) -> str:
    match = re.search(rf"(?:^|;\s*){re.escape(key)}=([^;]+)", cookie)
    return match.group(1).strip() if match else ""


def account_title(cookie: str, index: int) -> str:
    uid = extract_cookie_value(cookie, "__uid") or extract_cookie_value(cookie, "kps")
    return f"账号{index}" if not uid else mask_secret(uid)


def format_bytes(size_bytes: int | float) -> str:
    size = float(size_bytes)
    units = ("B", "KB", "MB", "GB", "TB")
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f}{units[index]}"


def build_params(cookie: str) -> dict[str, str]:
    params = {"pr": "ucpro", "fr": "android"}
    for key in ("kps", "sign", "vcode"):
        value = extract_cookie_value(cookie, key)
        if value:
            params[key] = value
    return params


def get_growth_info(session: requests.Session, cookie: str) -> dict[str, object]:
    response = session.get(
        GROWTH_INFO_URL,
        params=build_params(cookie),
        headers={**HEADERS, "Cookie": cookie},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(payload.get("message") or "获取成长信息失败，Cookie 可能失效")
    return data


def sign_growth(session: requests.Session, cookie: str) -> int:
    response = session.post(
        GROWTH_SIGN_URL,
        params=build_params(cookie),
        headers={**HEADERS, "Cookie": cookie},
        json={"sign_cyclic": True},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(payload.get("message") or "签到失败")
    return int(data.get("sign_daily_reward") or 0)


def run_account(cookie: str, index: int) -> AccountResult:
    required = ("kps", "sign", "vcode")
    missing = [key for key in required if not extract_cookie_value(cookie, key)]
    if missing:
        raise RuntimeError("Cookie 缺少移动端参数：" + ", ".join(missing))

    title = account_title(cookie, index)
    with requests.Session() as session:
        info = get_growth_info(session, cookie)
        cap_sign = info.get("cap_sign") or {}
        signed = bool(cap_sign.get("sign_daily"))
        reward = int(cap_sign.get("sign_daily_reward") or 0)

        if signed:
            sign_text = f"今日已签到 +{format_bytes(reward)}"
        else:
            reward = sign_growth(session, cookie)
            sign_text = f"签到成功 +{format_bytes(reward)}"

        progress = f"{cap_sign.get('sign_progress', 0)}/{cap_sign.get('sign_target', 0)}"
        total_capacity = format_bytes(int(info.get("total_capacity") or 0))
        sign_reward = format_bytes(int((info.get("cap_composition") or {}).get("sign_reward") or 0))
        message = f"{sign_text}，连签进度 {progress}，总空间 {total_capacity}，签到累计获得 {sign_reward}"
        return AccountResult(index=index, ok=True, title=title, message=message)


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
                AccountResult(index=index, ok=False, title=account_title(account, index), message=str(error))
            )

    content = format_results(results)
    send_notify(SCRIPT_NAME, content)
    return 0 if any(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
