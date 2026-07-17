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

import sys
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.ql_common import AccountResult, error_message, mask_secret, run_accounts

SCRIPT_NAME = "阿里云盘"
ACCOUNT_ENV_NAME = "ALIYUNDRIVE_TOKEN"
TIMEOUT = 15

TOKEN_URL = "https://auth.aliyundrive.com/v2/account/token"
SIGN_URL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
REWARD_URL = "https://member.aliyundrive.com/v1/activity/sign_in_reward"


def account_title(refresh_token: str, _account_index: int) -> str:
    return mask_secret(refresh_token)


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

    reward_text = "奖励：今日未获得奖励"
    try:
        reward_response = session.post(
            REWARD_URL,
            headers=headers,
            json={"signInDay": sign_days},
            timeout=TIMEOUT,
        )
    except requests.RequestException as error:
        reward_text = f"奖励领取失败：{error_message(error)}"
    else:
        if not reward_response.ok:
            reward_text = f"奖励领取失败：HTTP {reward_response.status_code}"
        else:
            try:
                reward_data = reward_response.json().get("result") or {}
            except ValueError:
                reward_text = "奖励领取失败：响应不是有效 JSON"
            else:
                reward = reward_data.get("name") or reward_data.get("rewardName")
                reward_description = reward_data.get("description") or reward_data.get("notice")
                if reward:
                    reward_text = f"奖励：{reward} - {reward_description}" if reward_description else f"奖励：{reward}"

    return f"累计签到 {sign_days} 天，{reward_text}"


def run_account(refresh_token: str, account_index: int) -> AccountResult:
    with requests.Session() as session:
        access_token = refresh_access_token(session, refresh_token)
        message = sign_in(session, access_token)
    return AccountResult(
        index=account_index,
        ok=True,
        title=account_title(refresh_token, account_index),
        message=message,
    )


def main() -> int:
    return run_accounts(SCRIPT_NAME, ACCOUNT_ENV_NAME, run_account, account_title)


if __name__ == "__main__":
    raise SystemExit(main())
