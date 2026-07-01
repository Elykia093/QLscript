#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static repository checks for ql-scripts.

This script only performs local static checks. It never imports task modules as
programs and never calls their real sign-in APIs.
"""

from __future__ import annotations

import shutil
import subprocess
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_REQUIRED_MARKERS = ("cron:", "new Env(", "环境变量:", "依赖:")


def relative(path: Path) -> str:
    return path.relative_to(ROOT_DIR).as_posix()


def collect_files(pattern: str, *directories: str) -> list[Path]:
    files: list[Path] = []
    for directory in directories:
        base = ROOT_DIR / directory
        if base.exists():
            files.extend(sorted(base.glob(pattern)))
    return files


def check_task_headers() -> list[str]:
    errors: list[str] = []
    for path in collect_files("*.*", "scripts"):
        if path.suffix not in {".py", ".js"}:
            continue

        text = path.read_text(encoding="utf-8")
        head = text[:1200]
        missing = [marker for marker in SCRIPT_REQUIRED_MARKERS if marker not in head]
        if missing:
            errors.append(f"{relative(path)} 缺少文件头字段: {', '.join(missing)}")

        if path.name != path.name.lower():
            errors.append(f"{relative(path)} 文件名应使用小写短命名")

    return errors


def check_readme_script_list() -> list[str]:
    readme_path = ROOT_DIR / "README.md"
    if not readme_path.exists():
        return ["README.md 不存在"]

    actual_scripts = {
        relative(path)
        for path in collect_files("*.*", "scripts")
        if path.suffix in {".py", ".js"}
    }
    readme_text = readme_path.read_text(encoding="utf-8")
    documented_scripts = set(re.findall(r"`(scripts/[^`]+)`", readme_text))

    errors: list[str] = []
    for path in sorted(actual_scripts - documented_scripts):
        errors.append(f"README.md 脚本列表缺少 {path}")
    for path in sorted(documented_scripts - actual_scripts):
        errors.append(f"README.md 引用了不存在的脚本 {path}")
    return errors


def run_command(command: list[str]) -> tuple[bool, str]:
    result = subprocess.run(
        command,
        cwd=ROOT_DIR,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    output = result.stdout.strip()
    return result.returncode == 0, output


def check_python() -> list[str]:
    files = collect_files("*.py", "scripts", "templates", "utils", "tools")

    errors: list[str] = []
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except SyntaxError as error:
            errors.append(f"{relative(path)}:{error.lineno}: {error.msg}")
    return errors


def check_javascript() -> list[str]:
    files = collect_files("*.js", "scripts", "templates", "utils")
    if not files:
        return []

    node = shutil.which("node")
    if not node:
        return ["未找到 node，无法执行 JS 静态检查"]

    errors: list[str] = []
    for path in files:
        ok, output = run_command([node, "--check", str(path)])
        if not ok:
            errors.append(output or f"node --check {relative(path)} failed")
    return errors


def main() -> int:
    checks = (
        ("文件头", check_task_headers),
        ("README 脚本列表", check_readme_script_list),
        ("Python 语法", check_python),
        ("JavaScript 语法", check_javascript),
    )

    failed = False
    for label, check in checks:
        errors = check()
        if errors:
            failed = True
            print(f"[失败] {label}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[通过] {label}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
