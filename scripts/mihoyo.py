#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 0 9 * * *
new Env('米游社')

环境变量:
  MIHOYO_COOKIE 必填，米游社 Cookie。多账号建议用换行分隔，兼容 & 或 #。
  MIHOYO_GIDS 可选，签到分区 id，默认 2,6,8。

依赖:
  Python: requests
  青龙通知: notify.py
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys
import time
import uuid
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, mask_secret, run_accounts

SCRIPT_NAME = "米游社"
ACCOUNT_ENV_NAME = "MIHOYO_COOKIE"
FORUM_IDS_ENV_NAME = "MIHOYO_GIDS"
TIMEOUT = 15

SIGN_URL = "https://bbs-api.miyoushe.com/apihub/app/api/signIn"
APP_VERSION = "2.109.0"
CLIENT_TYPE = "2"
DS_SALT = "t0qEgfub6cvueAPgR5m9aQWWVciEer7v"

FORUMS = {
    "1": "崩坏3",
    "2": "原神",
    "3": "崩坏2",
    "4": "未定事件簿",
    "5": "大别野",
    "6": "崩坏：星穹铁道",
    "8": "绝区零",
    "9": "崩坏：因缘精灵",
}


def md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def make_ds(body: str, query: str = "") -> str:
    timestamp = str(int(time.time()))
    random_value = str(random.randint(100001, 200000))
    checksum = md5(f"salt={DS_SALT}&t={timestamp}&r={random_value}&b={body}&q={query}")
    return f"{timestamp},{random_value},{checksum}"


def extract_cookie_value(cookie: str, key: str) -> str:
    match = re.search(rf"(?:^|;\s*){re.escape(key)}=([^;]+)", cookie)
    return match.group(1).strip() if match else ""


def account_title(cookie: str, account_index: int) -> str:
    uid = (
        extract_cookie_value(cookie, "account_id_v2")
        or extract_cookie_value(cookie, "ltuid_v2")
        or extract_cookie_value(cookie, "account_id")
        or extract_cookie_value(cookie, "ltuid")
    )
    return f"账号{account_index}" if not uid else mask_secret(uid)


def selected_gids() -> list[str]:
    raw = os.getenv(FORUM_IDS_ENV_NAME, "2,6,8")
    gids = [item.strip() for item in re.split(r"[,，\s]+", raw) if item.strip()]
    return list(dict.fromkeys(gid for gid in gids if gid in FORUMS))


def build_headers(cookie: str, body: str) -> dict[str, str]:
    return {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "DS": make_ds(body),
        "Origin": "https://webstatic.mihoyo.com",
        "Referer": "https://webstatic.mihoyo.com/",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 12; Unspecified Device) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36 miHoYoBBS/{APP_VERSION}"
        ),
        "X-Requested-With": "com.mihoyo.hyperion",
        "x-rpc-app_version": APP_VERSION,
        "x-rpc-channel": "miyousheluodi",
        "x-rpc-client_type": CLIENT_TYPE,
        "x-rpc-device_id": str(uuid.uuid3(uuid.NAMESPACE_URL, cookie)),
        "x-rpc-sys_version": "12",
    }


def sign_forum(session: requests.Session, cookie: str, gid: str) -> str:
    body = json.dumps({"gids": gid}, separators=(",", ":"))
    response = session.post(SIGN_URL, headers=build_headers(cookie, body), data=body, timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    retcode = payload.get("retcode")
    message = payload.get("message") or "未知响应"
    name = FORUMS.get(gid, gid)
    success_messages = ("OK", "成功", "已签到", "已经签到", "已完成")
    if retcode == 0 or any(item in message for item in success_messages):
        return f"{name}: {message}"
    if retcode == 1034:
        raise RuntimeError(f"{name}: 触发验证码")
    if retcode == -100:
        raise RuntimeError(f"{name}: Cookie 失效")
    raise RuntimeError(f"{name}: {message}")


def run_account(cookie: str, account_index: int) -> AccountResult:
    gids = selected_gids()
    if not gids:
        raise RuntimeError(f"{FORUM_IDS_ENV_NAME} 未配置有效分区")

    messages: list[str] = []
    with requests.Session() as session:
        for gid in gids:
            messages.append(sign_forum(session, cookie, gid))
            time.sleep(random.uniform(1.0, 2.0))

    return AccountResult(
        index=account_index,
        ok=True,
        title=account_title(cookie, account_index),
        message="；".join(messages),
    )


def main() -> int:
    return run_accounts(SCRIPT_NAME, ACCOUNT_ENV_NAME, run_account, account_title)


if __name__ == "__main__":
    raise SystemExit(main())
