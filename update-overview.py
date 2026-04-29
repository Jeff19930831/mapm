#!/usr/bin/env python3
"""
update-overview.py — 双层项目总览生成

生成两套总览：
1. Jeff1993 general 总览
2. MacCodex codex 总览

用法: python3 ~/.claude/scripts/update-overview.py
"""

import os
import yaml
from datetime import datetime

ROOT_DIR = os.path.expanduser("~/Documents/Jeff1993")
GENERAL_YAML_FILE = os.path.join(ROOT_DIR, ".project-status.yaml")
CODEX_YAML_FILE = os.path.join(ROOT_DIR, "MacCodex", ".project-status.yaml")

GENERAL_OVERVIEW_FILES = [
    os.path.join(ROOT_DIR, "项目总览.md"),
    os.path.join(ROOT_DIR, "MacClaude", "项目总览.md"),
]

CODEX_OVERVIEW_FILES = [
    os.path.join(ROOT_DIR, "MacCodex", "项目总览.md"),
]

STATUS_EMOJI = {
    "运行中": "🟢",
    "维护中": "🟡",
    "规划中": "⚪",
    "已完成": "✅",
    "已归档": "📦",
}

ARCHIVE_LABEL = {
    "keep": "保留",
    "selected": "待整理",
    "archived": "已归档",
}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_overview(data, title, device_label, entry_label, entry_link, state_source, path_rows):
    projects = data.get("projects", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    groups = {}
    for name, info in projects.items():
        status = info.get("status", "规划中")
        groups.setdefault(status, []).append((name, info))

    lines = [
        title,
        "",
        f"> 最后更新：{now}",
        f"> 设备：{device_label}",
        f"> 入口：[{entry_label}]({entry_link})",
        f"> 状态源：`{state_source}`",
        "",
        "---",
        "",
    ]

    stats_parts = []
    for status in ["运行中", "维护中", "规划中", "已完成", "已归档"]:
        count = len(groups.get(status, []))
        if count:
            emoji = STATUS_EMOJI.get(status, "")
            stats_parts.append(f"{emoji} {status}: {count}")
    lines.append(" | ".join(stats_parts))
    lines.append("")
    lines.append("---")
    lines.append("")

    for status in ["运行中", "维护中", "规划中", "已完成", "已归档"]:
        items = groups.get(status, [])
        if not items:
            continue

        emoji = STATUS_EMOJI.get(status, "")
        lines.append(f"## {emoji} {status} ({len(items)})")
        lines.append("")

        for name, info in sorted(items, key=lambda x: x[0]):
            ptype = info.get("type", "")
            repo = info.get("repo", "—")
            code_path = info.get("code_path", "")
            last_update = info.get("last_update", "")
            docs = info.get("docs", "")
            archive = ARCHIVE_LABEL.get(info.get("archive", "keep"), "保留")

            lines.append(f"### {name}")
            lines.append("")
            lines.append(f"- 类型：{ptype}")
            lines.append(f"- 仓库：{repo}")
            if code_path:
                lines.append(f"- 代码：`{code_path}`")
            if docs:
                lines.append(f"- 文档：{docs}")
                # Extract device layer from docs path (e.g. "MacClaude", "MacCodex", "Win_Claude_Work")
                # Strip backticks and take first path segment
                docs_clean = docs.replace("`", "").strip().strip("/").split("/")[0]
                if docs_clean and docs_clean != "~":
                    lines.append(f"- 设备层：{docs_clean}")
            if last_update:
                lines.append(f"- 最近更新：{last_update}")
            lines.append(f"- Archive：{archive}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 路径映射")
    lines.append("")
    lines.append("| 逻辑根 | 物理路径 | 说明 |")
    lines.append("|--------|---------|------|")
    for row in path_rows:
        lines.append(row)
    lines.append("")

    return "\n".join(lines)


def write_files(files, content):
    for path in files:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def update_general():
    if not os.path.exists(GENERAL_YAML_FILE):
        print(f"警告: general YAML 不存在 {GENERAL_YAML_FILE}")
        return 0

    data = load_yaml(GENERAL_YAML_FILE)
    content = generate_overview(
        data=data,
        title="# Jeff1993 General 项目总览",
        device_label="general | Jeff1993 全局快速查阅",
        entry_label="Jeff1993 README",
        entry_link="README.md",
        state_source="/Users/apple/Documents/Jeff1993/.project-status.yaml",
        path_rows=[
            "| `root_docs` | `~/Documents/Jeff1993/` | Jeff1993 总入口 |",
            "| `mac_codex` | `~/Documents/Jeff1993/MacCodex/` | Codex 项目管理根目录 |",
            "| `mac_claude` | `~/Documents/Jeff1993/MacClaude/` | Claude 文档中心 |",
            "| `win_claude_work` | `~/Documents/Jeff1993/Win_Claude_Work/` | Windows Claude 项目文档 |",
            "| `external_code` | `项目各自 code_path` | 允许代码实际位于外部 workspace |",
        ],
    )
    write_files(GENERAL_OVERVIEW_FILES, content)
    count = len(data.get("projects", {}))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"✅ general 项目总览已生成 ({count} 个项目, {now})")
    return count


def update_codex():
    if not os.path.exists(CODEX_YAML_FILE):
        print(f"警告: codex YAML 不存在 {CODEX_YAML_FILE}")
        return 0

    data = load_yaml(CODEX_YAML_FILE)
    content = generate_overview(
        data=data,
        title="# Codex 项目总览",
        device_label="mac-mini | Codex 项目快速查阅",
        entry_label="MacCodex README",
        entry_link="README.md",
        state_source="/Users/apple/Documents/Jeff1993/MacCodex/.project-status.yaml",
        path_rows=[
            "| `mac_codex` | `~/Documents/Jeff1993/MacCodex/` | Codex 项目管理根目录 |",
            "| `external_code` | `项目各自 code_path` | 允许项目代码实际位于外部 workspace |",
        ],
    )
    write_files(CODEX_OVERVIEW_FILES, content)
    count = len(data.get("projects", {}))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"✅ codex 项目总览已生成 ({count} 个项目, {now})")
    return count


def main():
    update_general()
    update_codex()


if __name__ == "__main__":
    main()
