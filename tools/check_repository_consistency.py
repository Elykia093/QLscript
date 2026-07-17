#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT_DIR / "scripts"
DETAILS_DIR = ROOT_DIR / "docs" / "content" / "docs" / "scripts"

INDEX_FILES = (
    ROOT_DIR / "README.md",
    ROOT_DIR / "scripts" / "README.md",
    ROOT_DIR / "docs" / "content" / "docs" / "guide" / "scripts.mdx",
)
ENVIRONMENT_PAGE = ROOT_DIR / "docs" / "content" / "docs" / "guide" / "environment.mdx"

CRON_PATTERN = re.compile(r"^cron:\s*([^\r\n]+)", re.MULTILINE)
TASK_NAME_PATTERN = re.compile(r"new Env\(['\"]([^'\"]+)['\"]\)")
SCRIPT_NAME_PATTERN = re.compile(
    r"^(?:const\s+)?SCRIPT_NAME\s*=\s*['\"]([^'\"]+)['\"]", re.MULTILINE
)
ENV_NAME_PATTERN = re.compile(
    r"\b([A-Z][A-Z0-9_]*_ENV_NAME)\s*=\s*['\"]([A-Z][A-Z0-9_]*)['\"]"
)


def script_files() -> list[Path]:
    return sorted(
        [*SCRIPTS_DIR.glob("*.py"), *SCRIPTS_DIR.glob("*.js")],
        key=lambda path: path.stem,
    )


def require_match(pattern: re.Pattern[str], text: str, label: str) -> str:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"{label} 缺少必需元数据")
    return match.group(1).strip()


def validate_script(path: Path, index_texts: dict[Path, str], errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    detail_path = DETAILS_DIR / f"{path.stem}.mdx"
    if not detail_path.exists():
        errors.append(f"缺少脚本详情页: {detail_path.relative_to(ROOT_DIR)}")
        return

    detail_text = detail_path.read_text(encoding="utf-8")
    try:
        cron = require_match(CRON_PATTERN, text, str(path.relative_to(ROOT_DIR)))
        task_name = require_match(TASK_NAME_PATTERN, text, str(path.relative_to(ROOT_DIR)))
        script_name = require_match(SCRIPT_NAME_PATTERN, text, str(path.relative_to(ROOT_DIR)))
    except ValueError as error:
        errors.append(str(error))
        return

    if task_name != script_name:
        errors.append(f"任务名不一致: {path.name}: new Env={task_name}, SCRIPT_NAME={script_name}")

    for index_path, index_text in index_texts.items():
        if path.name not in index_text:
            errors.append(f"{index_path.relative_to(ROOT_DIR)} 缺少 {path.name}")

    for target_path, target_text in (
        (ROOT_DIR / "scripts" / "README.md", index_texts[ROOT_DIR / "scripts" / "README.md"]),
        (
            ROOT_DIR / "docs" / "content" / "docs" / "guide" / "scripts.mdx",
            index_texts[ROOT_DIR / "docs" / "content" / "docs" / "guide" / "scripts.mdx"],
        ),
        (detail_path, detail_text),
    ):
        if cron not in target_text:
            errors.append(f"{target_path.relative_to(ROOT_DIR)} 缺少 cron {cron}")

    environment_text = ENVIRONMENT_PAGE.read_text(encoding="utf-8")
    for constant_name, env_name in ENV_NAME_PATTERN.findall(text):
        documentation_targets = [
            *index_texts.items(),
            (ENVIRONMENT_PAGE, environment_text),
            (detail_path, detail_text),
        ]
        if constant_name.startswith("LEGACY_"):
            documentation_targets = [
                (ROOT_DIR / "README.md", index_texts[ROOT_DIR / "README.md"]),
                (
                    ROOT_DIR / "scripts" / "README.md",
                    index_texts[ROOT_DIR / "scripts" / "README.md"],
                ),
                (ENVIRONMENT_PAGE, environment_text),
                (detail_path, detail_text),
            ]
        for target_path, target_text in documentation_targets:
            if env_name not in target_text:
                errors.append(f"{target_path.relative_to(ROOT_DIR)} 缺少环境变量 {env_name}")


def main() -> int:
    scripts = script_files()
    index_texts = {path: path.read_text(encoding="utf-8") for path in INDEX_FILES}
    errors: list[str] = []

    for path in scripts:
        validate_script(path, index_texts, errors)

    script_stems = {path.stem for path in scripts}
    detail_stems = {path.stem for path in DETAILS_DIR.glob("*.mdx")}
    for orphan in sorted(detail_stems - script_stems):
        errors.append(f"详情页没有对应脚本: docs/content/docs/scripts/{orphan}.mdx")

    if errors:
        print("仓库元数据一致性检查失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"仓库元数据一致性检查通过: {len(scripts)} 个脚本")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
