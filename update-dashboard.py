#!/usr/bin/env python3
"""
update-dashboard.py — 双层项目仪表盘同步

同步两套入口：
1. Jeff1993 general 入口：根目录 README + 现有全局管理页
2. MacCodex 入口：MacCodex/README.md

用法: python3 ~/.claude/scripts/update-dashboard.py
"""

import os
import re
import yaml
from datetime import datetime

ROOT_DIR = os.path.expanduser("~/Documents/Jeff1993")
GENERAL_YAML_FILE = os.path.join(ROOT_DIR, ".project-status.yaml")
CODEX_YAML_FILE = os.path.join(ROOT_DIR, "MacCodex", ".project-status.yaml")

GENERAL_DASHBOARD_FILES = [
    os.path.join(ROOT_DIR, "README.md"),
    os.path.join(ROOT_DIR, "MacClaude", "README.md"),
    os.path.join(ROOT_DIR, "MacClaude", "项目管理", "README.md"),
    os.path.join(ROOT_DIR, "Win_Claude_Work", "项目管理.md"),
]

CODEX_DASHBOARD_FILES = [
    os.path.join(ROOT_DIR, "MacCodex", "README.md"),
]

STATUS_ORDER = {
    "运行中": 0,
    "维护中": 1,
    "规划中": 2,
    "已完成": 3,
    "已归档": 4,
}

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


def generate_table(projects):
    sorted_projects = sorted(
        projects.items(),
        key=lambda x: (
            STATUS_ORDER.get(x[1].get("status", "规划中"), 99),
            x[0].lower(),
        ),
    )

    lines = [
        "| 项目 | 类型 | 代码仓库 | 文档位置 | 状态 | Archive | 负责人 |",
        "|------|------|---------|---------|------|---------|--------|",
    ]

    for name, info in sorted_projects:
        status = info.get("status", "规划中")
        emoji = STATUS_EMOJI.get(status, "")
        owner = info.get("owner", "") or ""
        ptype = info.get("type", "")
        repo = info.get("repo", "—")
        docs = info.get("docs", "—")
        archive = ARCHIVE_LABEL.get(info.get("archive", "keep"), "保留")

        lines.append(
            f"| **{name}** | {ptype} | {repo} | {docs} | {emoji} {status} | {archive} | {owner} |"
        )

    return "\n".join(lines)


def generate_owner_table(projects):
    sorted_projects = sorted(
        projects.items(),
        key=lambda x: ((x[1].get("owner", "") or "zzzz"), x[0].lower()),
    )

    lines = [
        "| 项目 | Owner | 状态 | Archive | 文档位置 |",
        "|------|-------|------|---------|----------|",
    ]

    for name, info in sorted_projects:
        owner = info.get("owner", "") or "unassigned"
        status = info.get("status", "规划中")
        archive = ARCHIVE_LABEL.get(info.get("archive", "keep"), "保留")
        docs = info.get("docs", "—")
        lines.append(f"| **{name}** | {owner} | {status} | {archive} | {docs} |")

    return "\n".join(lines)


def generate_archive_table(projects):
    lines = [
        "| 项目 | 状态 | Archive | Owner | 文档位置 |",
        "|------|------|---------|-------|----------|",
    ]

    selected = []
    for name, info in sorted(projects.items(), key=lambda x: x[0].lower()):
        archive = info.get("archive", "keep")
        if archive != "keep":
            selected.append((name, info))

    if not selected:
        lines.append("| — | — | — | — | 当前没有待整理/已归档项目 |")
        return "\n".join(lines)

    for name, info in selected:
        status = info.get("status", "规划中")
        archive = ARCHIVE_LABEL.get(info.get("archive", "keep"), "保留")
        owner = info.get("owner", "") or "unassigned"
        docs = info.get("docs", "—")
        lines.append(f"| **{name}** | {status} | {archive} | {owner} | {docs} |")

    return "\n".join(lines)


def parse_date(value):
    if not value:
        return datetime.min

    text = str(value).strip().strip("'\"")
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(text, fmt)
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)
            return parsed
        except ValueError:
            pass
    return datetime.min


def clean_docs_value(value):
    if not value:
        return ""

    text = str(value)
    match = re.search(r"`([^`]+)`", text)
    if match:
        return match.group(1)
    return text.strip()


def resolve_docs_dir(docs):
    path_text = clean_docs_value(docs)
    if not path_text:
        return None

    if " + " in path_text:
        path_text = path_text.split(" + ", 1)[0].strip()

    if path_text.startswith("~"):
        return os.path.expanduser(path_text)

    if os.path.isabs(path_text):
        return path_text

    # Windows paths are kept in the table but cannot be read from macOS.
    if re.match(r"^[A-Za-z]:\\", path_text):
        return None

    return os.path.join(ROOT_DIR, path_text)


def latest_progress_heading(info):
    docs_dir = resolve_docs_dir(info.get("docs", ""))
    if not docs_dir:
        return ""

    progress_file = os.path.join(docs_dir, "PROGRESS.md")
    if not os.path.exists(progress_file):
        return ""

    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"^##\s+(.+?)\s*$", line)
                if match:
                    heading = match.group(1).strip()
                    if heading and "按时间倒序" not in heading:
                        return heading
    except OSError:
        return ""

    return ""


def activity_date_from_heading(heading):
    if not heading:
        return datetime.min

    match = re.search(r"(\d{4}-\d{2}-\d{2})", heading)
    if match:
        return parse_date(match.group(1))

    match = re.search(r"(\d{4}-\d{2})", heading)
    if match:
        return parse_date(f"{match.group(1)}-01")

    return datetime.min


def latest_project_doc_mtime(info):
    docs_dir = resolve_docs_dir(info.get("docs", ""))
    if not docs_dir or not os.path.isdir(docs_dir):
        return datetime.min

    latest = datetime.min
    for filename in ("PROGRESS.md", "HANDOFF.md", "README.md"):
        path = os.path.join(docs_dir, filename)
        if not os.path.exists(path):
            continue
        try:
            modified = datetime.fromtimestamp(os.path.getmtime(path))
        except OSError:
            continue
        latest = max(latest, modified)
    return latest


def display_activity_time(activity_date, fallback):
    if activity_date == datetime.min:
        return fallback or "—"
    return activity_date.strftime("%Y-%m-%d %H:%M")


def generate_activity_table(projects):
    rows = []
    for name, info in projects.items():
        last_update = str(info.get("last_update", "") or "")
        recent_note = latest_progress_heading(info)
        sort_date = max(
            parse_date(last_update),
            activity_date_from_heading(recent_note),
            latest_project_doc_mtime(info),
        )
        rows.append(
            (
                sort_date,
                name.lower(),
                name,
                info,
                recent_note,
            )
        )

    rows.sort(key=lambda item: (item[0], item[1]), reverse=True)

    lines = [
        "| 更新时间 | 项目 | Owner | 状态 | Archive | 最近记录 | 文档位置 |",
        "|----------|------|-------|------|---------|----------|----------|",
    ]

    for activity_date, _, name, info, recent_note in rows:
        last_update = info.get("last_update", "") or "—"
        activity_time = display_activity_time(activity_date, last_update)
        owner = info.get("owner", "") or "unassigned"
        status = info.get("status", "规划中")
        archive = ARCHIVE_LABEL.get(info.get("archive", "keep"), "保留")
        docs = info.get("docs", "—")
        recent_note = recent_note or "—"
        lines.append(
            f"| {activity_time} | **{name}** | {owner} | {status} | {archive} | {recent_note} | {docs} |"
        )

    return "\n".join(lines)


def generate_stats(projects):
    status_counts = {}
    for info in projects.values():
        s = info.get("status", "规划中")
        status_counts[s] = status_counts.get(s, 0) + 1

    parts = []
    for status in ["运行中", "维护中", "规划中", "已完成", "已归档"]:
        if status in status_counts:
            emoji = STATUS_EMOJI.get(status, "")
            parts.append(f"{emoji} {status}: {status_counts[status]}")

    return " | ".join(parts)


def update_dashboard_file(
    dashboard_file,
    table,
    stats,
    now,
    owner_table=None,
    archive_table=None,
    activity_table=None,
):
    if not os.path.exists(dashboard_file):
        print(f"警告: Dashboard 文件不存在 {dashboard_file}")
        return

    with open(dashboard_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- AUTO-STATUS-START -->\n)(.*?)(<!-- AUTO-STATUS-END -->)"
    replacement = f"\\1{table}\n\\3"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    stats_pattern = r"(<!-- AUTO-STATS-START -->\n)(.*?)(<!-- AUTO-STATS-END -->)"
    stats_replacement = f"\\1{stats}\n\\3"
    new_content = re.sub(stats_pattern, stats_replacement, new_content, flags=re.DOTALL)

    if owner_table is not None:
        owner_pattern = r"(<!-- AUTO-OWNER-START -->\n)(.*?)(<!-- AUTO-OWNER-END -->)"
        owner_replacement = f"\\1{owner_table}\n\\3"
        new_content = re.sub(owner_pattern, owner_replacement, new_content, flags=re.DOTALL)

    if archive_table is not None:
        archive_pattern = r"(<!-- AUTO-ARCHIVE-START -->\n)(.*?)(<!-- AUTO-ARCHIVE-END -->)"
        archive_replacement = f"\\1{archive_table}\n\\3"
        new_content = re.sub(archive_pattern, archive_replacement, new_content, flags=re.DOTALL)

    if activity_table is not None:
        activity_pattern = r"(<!-- AUTO-ACTIVITY-START -->\n)(.*?)(<!-- AUTO-ACTIVITY-END -->)"
        activity_replacement = f"\\1{activity_table}\n\\3"
        new_content = re.sub(activity_pattern, activity_replacement, new_content, flags=re.DOTALL)

    new_content = re.sub(
        r"> 最后更新：.*",
        f"> 最后更新：{now}",
        new_content,
    )

    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.write(new_content)


def update_scope(yaml_file, dashboard_files, scope_name):
    if not os.path.exists(yaml_file):
        print(f"警告: {scope_name} YAML 不存在 {yaml_file}")
        return 0

    data = load_yaml(yaml_file)
    projects = data.get("projects", {})
    table = generate_table(projects)
    stats = generate_stats(projects)
    owner_table = generate_owner_table(projects)
    archive_table = generate_archive_table(projects)
    activity_table = generate_activity_table(projects)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for dashboard_file in dashboard_files:
        update_dashboard_file(
            dashboard_file,
            table,
            stats,
            now,
            owner_table=owner_table,
            archive_table=archive_table,
            activity_table=activity_table,
        )

    print(f"✅ {scope_name} dashboard 已同步 ({len(projects)} 个项目, {now})")
    print(f"   {stats}")
    return len(projects)


def main():
    update_scope(GENERAL_YAML_FILE, GENERAL_DASHBOARD_FILES, "general")
    update_scope(CODEX_YAML_FILE, CODEX_DASHBOARD_FILES, "codex")


if __name__ == "__main__":
    main()
