#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 30 8 * * *
new Env('百度贴吧')

环境变量:
  TIEBA_COOKIE 必填，百度贴吧 Cookie 或 BDUSS。多账号建议用换行分隔，兼容 & 或 #。

依赖:
  Python: requests
  青龙通知: notify.py
"""

from __future__ import annotations

import hashlib
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, cookie_name, format_results, send_notify, split_accounts

SCRIPT_NAME = "百度贴吧"
ENV_NAME = "TIEBA_COOKIE"

TIMEOUT = 15
MAX_WORKERS = 8
MAX_ROUNDS = 5
MIN_DELAY = 1
MAX_DELAY = 3

TBS_URL = "http://tieba.baidu.com/dc/common/tbs"
LIKE_URL = "http://c.tieba.baidu.com/c/f/forum/like"
SIGN_URL = "http://c.tieba.baidu.com/c/c/forum/sign"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "bdtb for Android 12.0.0.0",
}

BASE_DATA = {
    "_client_type": "2",
    "_client_id": "wappc_1534235498291_488",
    "_client_version": "12.0.0.0",
    "_phone_imei": "000000000000000",
    "model": "MI+5",
    "net_type": "1",
}

SIGN_DATA = {
    **BASE_DATA,
    "from": "1008621y",
}

SUCCESS_CODES = {"0", 0, "160002"}
CRITICAL_ERRORS = {"340006", 340006}
ERROR_CODES = {
    "0": "签到成功",
    "160002": "已经签到",
    "340006": "Cookie 失效或需要验证",
}


def extract_bduss(account: str) -> str:
    match = re.search(r"(?:^|;\s*)BDUSS=([^;]+)", account)
    bduss = match.group(1).strip() if match else account.strip()
    if not bduss:
        raise ValueError("未找到 BDUSS")
    return bduss


def build_cookie_header(account: str, bduss: str) -> str:
    if re.search(r"(?:^|;\s*)BDUSS=", account):
        return account
    return f"BDUSS={bduss}"


def encode_data(data: dict[str, object]) -> dict[str, object]:
    text = "".join(f"{key}={data[key]}" for key in sorted(data.keys()))
    sign = hashlib.md5((text + "tiebaclient!!!").encode("utf-8")).hexdigest().upper()
    return {**data, "sign": sign}


def get_tbs(session: requests.Session, cookie: str) -> str:
    headers = {**HEADERS, "Cookie": cookie}
    response = session.get(TBS_URL, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    tbs = data.get("tbs")
    if not tbs:
        raise RuntimeError(data.get("error") or "获取 tbs 失败")
    return tbs


def get_favorites(session: requests.Session, bduss: str) -> list[dict[str, object]]:
    bars: list[dict[str, object]] = []
    page = 1

    while True:
        data = {
            **BASE_DATA,
            "BDUSS": bduss,
            "from": "1008621y",
            "page_no": str(page),
            "page_size": "200",
            "timestamp": str(int(time.time())),
            "vcode_tag": "11",
        }
        response = session.post(LIKE_URL, data=encode_data(data), timeout=TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        forum_list = payload.get("forum_list") or {}
        if not forum_list:
            break

        for forum_type in ("non-gconforum", "gconforum"):
            items = forum_list.get(forum_type)
            if isinstance(items, list):
                bars.extend(items)
            elif isinstance(items, dict):
                bars.append(items)

        if payload.get("has_more") != "1":
            break
        page += 1

    return bars


def sign_bar(bduss: str, tbs: str, bar: dict[str, object]) -> dict[str, object]:
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY))
    data = {
        **SIGN_DATA,
        "BDUSS": bduss,
        "fid": bar["id"],
        "kw": bar["name"],
        "tbs": tbs,
        "timestamp": str(int(time.time())),
    }
    response = requests.post(SIGN_URL, data=encode_data(data), timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    error_code = payload.get("error_code", "unknown")
    return {
        "name": str(bar["name"]),
        "error_code": error_code,
        "status": ERROR_CODES.get(str(error_code), f"未知错误: {error_code}"),
        "ok": error_code in SUCCESS_CODES,
    }


def run_account(cookie: str, index: int) -> AccountResult:
    bduss = extract_bduss(cookie)
    cookie_header = build_cookie_header(cookie, bduss)
    title = cookie_name(cookie_header, index)

    with requests.Session() as session:
        tbs = get_tbs(session, cookie_header)
        favorites = get_favorites(session, bduss)
        if not favorites:
            return AccountResult(index=index, ok=False, title=title, message="未获取到关注贴吧")

        pending = favorites
        results: list[dict[str, object]] = []
        workers = min(MAX_WORKERS, max(1, os.cpu_count() or 1), len(favorites))

        for _ in range(MAX_ROUNDS):
            if not pending:
                break

            round_results = []
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [executor.submit(sign_bar, bduss, tbs, bar) for bar in pending]
                for future in as_completed(futures):
                    result = future.result()
                    round_results.append(result)
                    if result.get("error_code") in CRITICAL_ERRORS:
                        pending = []
                        break

            results.extend(round_results)
            failed_names = {item["name"] for item in round_results if not item.get("ok")}
            pending = [bar for bar in pending if bar.get("name") in failed_names]

        success_count = sum(1 for item in results if item.get("ok"))
        failed = [f"{item['name']}({item['status']})" for item in results if not item.get("ok")]
        message = f"成功/已签 {success_count}/{len(favorites)}"
        if failed:
            message += "；失败：" + "、".join(failed[:8])

        return AccountResult(index=index, ok=success_count > 0, title=title, message=message)


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
