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

from utils.ql_common import AccountResult, cookie_name, error_message, run_accounts

SCRIPT_NAME = "百度贴吧"
ACCOUNT_ENV_NAME = "TIEBA_COOKIE"

TIMEOUT = 15
MAX_WORKERS = 8
MAX_ROUNDS = 5
MAX_FAVORITE_PAGES = 20
MIN_DELAY = 1
MAX_DELAY = 3

TBS_URL = "https://tieba.baidu.com/dc/common/tbs"
LIKE_URL = "https://c.tieba.baidu.com/c/f/forum/like"
SIGN_URL = "https://c.tieba.baidu.com/c/c/forum/sign"

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

SUCCESS_CODES = {"0", "160002"}
CRITICAL_ERRORS = {"340006"}
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
    if not isinstance(data, dict):
        raise RuntimeError("获取 tbs 的响应不是 JSON 对象")
    tbs = data.get("tbs")
    if not tbs:
        raise RuntimeError(data.get("error") or "获取 tbs 失败")
    return tbs


def get_favorites(session: requests.Session, bduss: str) -> list[dict[str, object]]:
    bars: list[dict[str, object]] = []
    seen_ids: set[str] = set()

    for page in range(1, MAX_FAVORITE_PAGES + 1):
        previous_count = len(seen_ids)
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
        if not isinstance(payload, dict):
            raise RuntimeError("关注贴吧响应不是 JSON 对象")
        forum_list = payload.get("forum_list") or {}
        if not forum_list:
            if str(payload.get("has_more")) == "1":
                raise RuntimeError("关注贴吧分页指示继续，但当前页没有数据")
            return bars

        for forum_type in ("non-gconforum", "gconforum"):
            items = forum_list.get(forum_type)
            candidates = items if isinstance(items, list) else [items] if isinstance(items, dict) else []
            for item in candidates:
                if not isinstance(item, dict):
                    raise RuntimeError("关注贴吧条目不是 JSON 对象")
                forum_id = str(item.get("id", ""))
                if forum_id in seen_ids:
                    continue
                seen_ids.add(forum_id)
                bars.append(item)

        if str(payload.get("has_more")) != "1":
            return bars
        if len(seen_ids) == previous_count:
            raise RuntimeError("关注贴吧分页没有新增数据，已停止继续请求")

    raise RuntimeError(f"关注贴吧分页超过 {MAX_FAVORITE_PAGES} 页，已停止继续请求")


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
    if not isinstance(payload, dict):
        raise RuntimeError("贴吧签到响应不是 JSON 对象")
    error_code = str(payload.get("error_code", "unknown")).strip()
    return {
        "id": str(bar["id"]),
        "name": str(bar["name"]),
        "error_code": error_code,
        "status": ERROR_CODES.get(str(error_code), f"未知错误: {error_code}"),
        "ok": error_code in SUCCESS_CODES,
        "retryable": False,
    }


def failed_sign_result(
    bar: dict[str, object],
    error: Exception,
    *,
    retryable: bool,
) -> dict[str, object]:
    forum_id = str(bar.get("id", "unknown"))
    forum_name = str(bar.get("name") or f"贴吧{forum_id}")
    return {
        "id": forum_id,
        "name": forum_name,
        "error_code": "request_error" if retryable else "response_error",
        "status": error_message(error),
        "ok": False,
        "retryable": retryable,
    }


def is_retryable_request_error(error: requests.RequestException) -> bool:
    response = getattr(error, "response", None)
    if response is None:
        return True
    return response.status_code == 429 or response.status_code >= 500


def run_sign_round(
    bduss: str,
    tbs: str,
    bars: list[dict[str, object]],
    workers: int,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(sign_bar, bduss, tbs, bar): bar for bar in bars}
        for future in as_completed(futures):
            bar = futures[future]
            try:
                results.append(future.result())
            except requests.RequestException as error:
                results.append(
                    failed_sign_result(
                        bar,
                        error,
                        retryable=is_retryable_request_error(error),
                    )
                )
            except (KeyError, RuntimeError, TypeError, ValueError) as error:
                results.append(failed_sign_result(bar, error, retryable=False))
    return results


def run_account(cookie: str, account_index: int) -> AccountResult:
    bduss = extract_bduss(cookie)
    cookie_header = build_cookie_header(cookie, bduss)
    title = cookie_name(cookie_header, account_index)

    with requests.Session() as session:
        tbs = get_tbs(session, cookie_header)
        favorites = get_favorites(session, bduss)
        if not favorites:
            return AccountResult(index=account_index, ok=False, title=title, message="未获取到关注贴吧")

        pending = favorites
        latest_results: dict[str, dict[str, object]] = {}
        workers = min(MAX_WORKERS, max(1, os.cpu_count() or 1), len(favorites))

        for _ in range(MAX_ROUNDS):
            if not pending:
                break

            round_results = run_sign_round(bduss, tbs, pending, workers)

            for result in round_results:
                latest_results[str(result["id"])] = result
            if any(result.get("error_code") in CRITICAL_ERRORS for result in round_results):
                break

            retryable_ids = {
                str(item["id"])
                for item in round_results
                if not item.get("ok") and item.get("retryable")
            }
            pending = [bar for bar in pending if str(bar.get("id")) in retryable_ids]

        results = list(latest_results.values())
        success_count = sum(1 for item in results if item.get("ok"))
        failed = [f"{item['name']}({item['status']})" for item in results if not item.get("ok")]
        message = f"成功/已签 {success_count}/{len(favorites)}"
        if failed:
            message += "；失败：" + "、".join(failed[:8])

        return AccountResult(index=account_index, ok=success_count > 0, title=title, message=message)


def main() -> int:
    return run_accounts(SCRIPT_NAME, ACCOUNT_ENV_NAME, run_account, cookie_name)


if __name__ == "__main__":
    raise SystemExit(main())
