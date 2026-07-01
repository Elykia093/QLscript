from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Sequence

DEFAULT_SEPARATORS = ("\n", "&", "#")


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
    for separator in separators:
        if separator in normalized:
            return [item.strip() for item in normalized.split(separator) if item.strip()]

    return [normalized]


def mask_secret(value: str, keep: int = 4) -> str:
    value = value.strip()
    if len(value) <= keep * 2:
        return "***"
    return f"{value[:keep]}***{value[-keep:]}"


def cookie_name(cookie: str, index: int) -> str:
    for key in ("pt_pin", "un", "BDUSS", "smzdm_id", "uid"):
        match = re.search(rf"(?:^|;\s*){re.escape(key)}=([^;]+)", cookie)
        if match:
            return f"{key}={mask_secret(match.group(1))}"
    return f"账号{index}"


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
