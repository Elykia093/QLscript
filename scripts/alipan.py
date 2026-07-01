#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 10 8 * * *
new Env('阿里云盘')

环境变量:
  ALIYUNDRIVE_TOKEN 必填，阿里云盘 refresh_token。多账号建议用换行分隔，兼容 & 或 #。

依赖:
  Python: requests
  青龙通知: notify.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, format_results, mask_secret, send_notify, split_accounts

SCRIPT_NAME = "阿里云盘"
ENV_NAME = "ALIYUNDRIVE_TOKEN"
TIMEOUT = 15

TOKEN_URL = "https://auth.aliyundrive.com/v2/account/token"
SIGN_URL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
REWARD_URL = "https://member.aliyundrive.com/v1/activity/sign_in_reward"


def refresh_access_token(session: requests.Session, refresh_token: str) -> str:
    response = session.post(
        TOKEN_URL,
        json={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError(data.get("message") or "刷新 access_token 失败")
    return access_token


def sign_in(session: requests.Session, access_token: str) -> str:
    headers = {"Authorization": access_token, "Content-Type": "application/json"}
    response = session.post(SIGN_URL, headers=headers, json={}, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()

    result = data.get("result") or {}
    sign_days = result.get("signInCount")
    if sign_days is None:
        raise RuntimeError(data.get("message") or "签到响应缺少 signInCount")

    reward_name = "今日未获得奖励"
    reward_response = session.post(
        REWARD_URL,
        headers=headers,
        json={"signInDay": sign_days},
        timeout=TIMEOUT,
    )
    if reward_response.ok:
        reward_data = reward_response.json().get("result") or {}
        reward = reward_data.get("name") or reward_data.get("rewardName")
        reward_description = reward_data.get("description") or reward_data.get("notice")
        if reward:
            reward_name = f"{reward} - {reward_description}" if reward_description else reward

    return f"累计签到 {sign_days} 天，奖励：{reward_name}"


def run_account(refresh_token: str, index: int) -> AccountResult:
    with requests.Session() as session:
        access_token = refresh_access_token(session, refresh_token)
        message = sign_in(session, access_token)
    return AccountResult(index=index, ok=True, title=mask_secret(refresh_token), message=message)


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
                AccountResult(index=index, ok=False, title=mask_secret(account), message=str(error))
            )

    content = format_results(results)
    send_notify(SCRIPT_NAME, content)
    return 0 if any(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
