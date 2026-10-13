#!/usr/bin/env python3
"""从确定性模板创建可安装的空白科研项目。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parent.parent / "assets" / "project-template"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="创建空白 AI 科研项目")
    parser.add_argument("--project-name", required=True, help="项目显示名称")
    parser.add_argument("--path", required=True, type=Path, help="项目根目录")
    parser.add_argument("--package-name", help="合法的 ASCII Python 包名；默认从项目名推导")
    parser.add_argument("--dry-run", action="store_true", help="只检查并显示将创建的文件")
    return parser.parse_args()


def resolve_names(project_name: str, package_name: str | None) -> tuple[str, str]:
    if not project_name.strip() or any(ord(char) < 32 for char in project_name):
        raise ValueError("项目名不能为空或包含控制字符")

    distribution_name = re.sub(r"[^a-z0-9]+", "-", project_name.lower()).strip("-")
    if package_name is None:
        package_name = distribution_name.replace("-", "_")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", package_name):
        raise ValueError("无法推导合法包名；请提供 --package-name（ASCII 字母、数字、下划线）")
    if not distribution_name:
        distribution_name = package_name.replace("_", "-").strip("-")
    if not distribution_name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", distribution_name):
        raise ValueError("无法确定合法的 Python 发行包名称")
    return distribution_name, package_name


def render_template(project_name: str, distribution_name: str, package_name: str) -> dict[Path, str]:
    if not TEMPLATE_ROOT.is_dir():
        raise FileNotFoundError(f"找不到项目模板：{TEMPLATE_ROOT}")
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_NAME_JSON}}": json.dumps(project_name, ensure_ascii=False),
        "{{DISTRIBUTION_NAME_JSON}}": json.dumps(distribution_name),
        "{{PACKAGE_NAME}}": package_name,
    }
    rendered = {}
    for source in sorted(TEMPLATE_ROOT.rglob("*")):
        if not source.is_file():
            continue
        relative_name = str(source.relative_to(TEMPLATE_ROOT))
        content = source.read_text(encoding="utf-8")
        for placeholder, value in replacements.items():
            relative_name = relative_name.replace(placeholder, value)
            content = content.replace(placeholder, value)
        rendered[Path(relative_name)] = content
    return rendered


def preflight(destination: Path, rendered: dict[Path, str]) -> list[Path]:
    if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
        raise FileExistsError(f"项目路径不是普通目录：{destination}")

    to_create = []
    for relative_path, expected in rendered.items():
        target = destination / relative_path
        parent = target.parent
        while parent != destination:
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise FileExistsError(f"路径冲突：{parent}")
            parent = parent.parent
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise FileExistsError(f"路径冲突：{target}")
        if target.exists():
            if target.read_text(encoding="utf-8") != expected:
                raise FileExistsError(f"已有文件内容不同，未覆盖：{target}")
        else:
            to_create.append(relative_path)
    return to_create


def main() -> None:
    args = parse_args()
    distribution_name, package_name = resolve_names(args.project_name, args.package_name)
    destination = args.path.expanduser().resolve()
    rendered = render_template(args.project_name, distribution_name, package_name)
    to_create = preflight(destination, rendered)

    if not args.dry_run:
        for relative_path in to_create:
            target = destination / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("x", encoding="utf-8") as output:
                output.write(rendered[relative_path])

    action = "将创建" if args.dry_run else "已创建"
    print(f"{action} {len(to_create)} 个文件；跳过 {len(rendered) - len(to_create)} 个相同文件")
    print(f"项目：{destination}")
    print(f"导入包：{package_name}")


if __name__ == "__main__":
    main()
