from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

DEFAULT_SEPARATORS = ("\n", "&", "#")
QUERY_VALUE_PATTERN = re.compile(r"([?&][^=\s&]+)=([^&\s]+)")


@dataclass
class AccountResult:
    index: int
    ok: bool
    title: str
    message: str


def split_accounts(raw_value: str | None, separators: Sequence[str] = DEFAULT_SEPARATORS) -> list[str]:
    if not raw_value:
        return []

    normalized = raw_value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []

    for separator in separators:
        if separator in normalized:
            return [item.strip() for item in normalized.split(separator) if item.strip()]

    return [normalized]


def mask_secret(value: str, keep: int = 4) -> str:
    value = value.strip()
    if len(value) <= keep * 2:
        return "***"
    return f"{value[:keep]}***{value[-keep:]}"


def error_message(error: Exception) -> str:
    return QUERY_VALUE_PATTERN.sub(lambda match: f"{match.group(1)}=***", str(error))


def cookie_name(cookie: str, account_index: int) -> str:
    for key in ("pt_pin", "un", "BDUSS", "smzdm_id", "uid"):
        match = re.search(rf"(?:^|;\s*){re.escape(key)}=([^;]+)", cookie)
        if match:
            return f"{key}={mask_secret(match.group(1))}"
    return f"账号{account_index}"


def format_results(results: Iterable[AccountResult]) -> str:
    lines = []
    for result in results:
        status = "成功" if result.ok else "失败"
        lines.append(f"{status} | 账号{result.index} | {result.title}: {result.message}")
    return "\n".join(lines)


def send_notify(title: str, content: str) -> None:
    print(f"\n{title}\n{content}")
    try:
        from notify import send
    except ImportError:
        print("未检测到青龙 notify.py，已降级为控制台输出。")
        return

    try:
        send(title, content)
    except Exception as error:
        print(f"通知发送失败: {error}")


def run_accounts(
    script_name: str,
    account_env_name: str,
    runner: Callable[[str, int], AccountResult],
    error_title: Callable[[str, int], str] | None = None,
) -> int:
    accounts = split_accounts(os.getenv(account_env_name))
    if not accounts:
        send_notify(script_name, f"未配置环境变量 {account_env_name}")
        return 1

    results: list[AccountResult] = []
    for account_index, account in enumerate(accounts, start=1):
        try:
            results.append(runner(account, account_index))
        except Exception as error:
            title = error_title(account, account_index) if error_title else f"账号{account_index}"
            results.append(AccountResult(index=account_index, ok=False, title=title, message=error_message(error)))

    send_notify(script_name, format_results(results))
    return 0 if any(result.ok for result in results) else 1
