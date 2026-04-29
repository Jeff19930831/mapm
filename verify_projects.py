#!/usr/bin/env python3
"""
verify-projects.py - Data health check for MAPM project status YAML files.

Checks:
  1. code_path_exists   - Verify local code_path directories exist
  2. cross_yaml_consistency - Cross-check layer YAMLs against General YAML
  3. last_update_stale  - Flag stale last_update on active/maintained projects
  4. docs_dir_exists    - Verify local docs directories exist
  5. layer_assignment   - Verify docs prefix matches the layer YAML membership

Usage:
  python3 verify-projects.py              # Full check, terminal output
  python3 verify-projects.py --json       # JSON output
  python3 verify-projects.py --refresh    # Refresh last_update from PROGRESS.md mtime
  python3 verify-projects.py --stale-days 30  # Custom stale threshold

Exit codes:
  0 - No error-level issues (warnings/info OK)
  1 - One or more error-level issues found
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta

import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT_DIR = os.path.expanduser("~/Documents/Jeff1993")
GENERAL_YAML = os.path.join(ROOT_DIR, ".project-status.yaml")
LAYER_YAMLS = {
    "macclaude": os.path.join(ROOT_DIR, "MacClaude", ".project-status.yaml"),
    "maccodex": os.path.join(ROOT_DIR, "MacCodex", ".project-status.yaml"),
    "win_claude_work": os.path.join(ROOT_DIR, "Win_Claude_Work", ".project-status.yaml"),
    "wincodex": os.path.join(ROOT_DIR, "WinCodex", ".project-status.yaml"),
}

# Statuses that trigger stale checks
ACTIVE_STATUSES = {"\u8fd0\u884c\u4e2d", "\u7ef4\u62a4\u4e2d"}  # 运行中, 维护中

# Windows path pattern: starts with drive letter like C:\ or D:\
WINDOWS_PATH_RE = re.compile(r"^[A-Za-z]:")

# Layer names that correspond to Windows machines (skip local filesystem checks)
WINDOWS_LAYERS = {"win_claude_work", "wincodex"}

# Map docs prefix (e.g. "MacClaude") to layer key
PREFIX_TO_LAYER = {
    "MacClaude": "macclaude",
    "MacCodex": "maccodex",
    "Win_Claude_Work": "win_claude_work",
    "WinCodex": "wincodex",
}


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------

def load_yaml(path):
    """Load and return YAML data from a file path."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_windows_path(path_str):
    """Return True if path looks like a Windows absolute path."""
    return bool(WINDOWS_PATH_RE.match(path_str))


def _is_skip_path(path_str):
    """Return True if this code_path should be skipped (em-dash or Windows)."""
    if not path_str or path_str.strip() == "\u2014":
        return True
    return _is_windows_path(path_str)


def _parse_docs_field(docs_str):
    """
    Parse a docs field and return list of (prefix, raw_path) tuples.

    Handles formats:
      `MacClaude/proj-a/`
      `~/projects/foo/`
      `MacClaude/a/` + `Win_Claude_Work/b/`
    """
    if not docs_str:
        return []
    # Split on ' + ' for multi-layer docs
    parts = re.split(r"\s*\+\s*", docs_str)
    results = []
    for part in parts:
        part = part.strip()
        # Strip backticks
        part = part.strip("`")
        if not part:
            continue
        # Extract prefix (first path component before /)
        if part.startswith("~/"):
            results.append((None, part))
        else:
            segments = part.split("/")
            if segments:
                prefix = segments[0]
                results.append((prefix, part))
    return results


def _resolve_docs_path(raw_path, root_dir):
    """Resolve a docs path to an absolute filesystem path."""
    if raw_path.startswith("~/"):
        return os.path.expanduser(raw_path)
    # Relative to root_dir
    return os.path.join(root_dir, raw_path)


def _is_windows_docs_prefix(prefix):
    """Check if a docs prefix refers to a Windows layer."""
    if prefix is None:
        return False
    layer_key = PREFIX_TO_LAYER.get(prefix)
    return layer_key in WINDOWS_LAYERS


# ---------------------------------------------------------------------------
# Check 1: code_path_exists
# ---------------------------------------------------------------------------

def check_code_path_exists(projects):
    """
    Check that code_path directories exist on the local machine.

    Skips Windows paths and em-dash (\u2014) entries.
    Returns list of issue dicts with keys: project, check, level, message.
    """
    issues = []
    for name, meta in projects.items():
        code_path = meta.get("code_path", "")
        if _is_skip_path(code_path):
            continue
        expanded = os.path.expanduser(code_path)
        if not os.path.isdir(expanded):
            issues.append({
                "project": name,
                "check": "code_path_exists",
                "level": "warning",
                "message": f"code_path directory not found: {code_path}",
            })
    return issues


# ---------------------------------------------------------------------------
# Check 2: cross_yaml_consistency
# ---------------------------------------------------------------------------

def check_cross_yaml_consistency(general_yaml_path, layer_yamls):
    """
    Cross-check layer YAMLs against General YAML.

    - Any project in a layer must also exist in General (error if not)
    - Status must match between layer and General (warning if not)
    """
    issues = []
    general_data = load_yaml(general_yaml_path)
    general_projects = general_data.get("projects", {})

    for layer_name, layer_path in layer_yamls.items():
        if not os.path.exists(layer_path):
            continue
        layer_data = load_yaml(layer_path)
        layer_projects = layer_data.get("projects", {})

        for proj_name, proj_meta in layer_projects.items():
            if proj_name not in general_projects:
                issues.append({
                    "project": proj_name,
                    "check": "cross_yaml_consistency",
                    "level": "error",
                    "message": f"Project in {layer_name} layer but not found in General YAML",
                })
                continue
            layer_status = proj_meta.get("status", "")
            general_status = general_projects[proj_name].get("status", "")
            if layer_status != general_status:
                issues.append({
                    "project": proj_name,
                    "check": "cross_yaml_consistency",
                    "level": "warning",
                    "message": (
                        f"Status mismatch in {layer_name}: "
                        f"layer={layer_status}, general={general_status}"
                    ),
                })
    return issues


# ---------------------------------------------------------------------------
# Check 3: last_update_stale
# ---------------------------------------------------------------------------

def check_last_update_stale(projects, stale_days=14):
    """
    Check if active/maintained projects have stale last_update dates.

    Only checks projects with status in ACTIVE_STATUSES.
    Returns info-level issues for stale entries.
    """
    issues = []
    threshold = datetime.now() - timedelta(days=stale_days)

    for name, meta in projects.items():
        status = meta.get("status", "")
        if status not in ACTIVE_STATUSES:
            continue
        last_update_str = meta.get("last_update", "")
        if not last_update_str:
            issues.append({
                "project": name,
                "check": "last_update_stale",
                "level": "info",
                "message": f"No last_update date (status: {status})",
            })
            continue
        try:
            last_update = datetime.strptime(last_update_str, "%Y-%m-%d")
        except ValueError:
            issues.append({
                "project": name,
                "check": "last_update_stale",
                "level": "info",
                "message": f"Invalid last_update format: {last_update_str}",
            })
            continue
        if last_update < threshold:
            days_old = (datetime.now() - last_update).days
            issues.append({
                "project": name,
                "check": "last_update_stale",
                "level": "info",
                "message": f"last_update is {days_old} days old (threshold: {stale_days}d)",
            })
    return issues


# ---------------------------------------------------------------------------
# Check 4: docs_dir_exists
# ---------------------------------------------------------------------------

def check_docs_dir_exists(projects, root_dir=None):
    """
    Check that docs directories exist on the local machine.

    For multi-part docs (a + b), checks only the first part.
    Skips Windows-layer docs paths.
    """
    if root_dir is None:
        root_dir = ROOT_DIR
    issues = []

    for name, meta in projects.items():
        docs_str = meta.get("docs", "")
        parsed = _parse_docs_field(docs_str)
        if not parsed:
            continue

        prefix, raw_path = parsed[0]  # Check only first part

        # Skip Windows-layer paths
        if _is_windows_docs_prefix(prefix):
            continue

        abs_path = _resolve_docs_path(raw_path, root_dir)
        if not os.path.isdir(abs_path):
            issues.append({
                "project": name,
                "check": "docs_dir_exists",
                "level": "warning",
                "message": f"docs directory not found: {raw_path}",
            })
    return issues


# ---------------------------------------------------------------------------
# Check 5: layer_assignment
# ---------------------------------------------------------------------------

def check_layer_assignment(projects, layer_yamls):
    """
    Check that each project's docs prefix matches the layer it appears in.

    E.g., a project with docs: "MacClaude/..." should be in the MacClaude YAML.
    """
    issues = []

    # Load all layer project sets
    layer_project_sets = {}
    for layer_name, layer_path in layer_yamls.items():
        if not os.path.exists(layer_path):
            layer_project_sets[layer_name] = set()
            continue
        layer_data = load_yaml(layer_path)
        layer_project_sets[layer_name] = set(layer_data.get("projects", {}).keys())

    for name, meta in projects.items():
        docs_str = meta.get("docs", "")
        parsed = _parse_docs_field(docs_str)
        if not parsed:
            continue

        prefix, _ = parsed[0]
        if prefix is None:
            # ~/ paths don't map to a specific layer
            continue

        expected_layer = PREFIX_TO_LAYER.get(prefix)
        if expected_layer is None:
            # Unknown prefix, skip
            continue

        if expected_layer in WINDOWS_LAYERS:
            # Windows layers can't be verified locally
            continue

        if name not in layer_project_sets.get(expected_layer, set()):
            issues.append({
                "project": name,
                "check": "layer_assignment",
                "level": "warning",
                "message": (
                    f"docs prefix is {prefix}/ but project not in "
                    f"{expected_layer} layer YAML"
                ),
            })
    return issues


# ---------------------------------------------------------------------------
# Refresh: update last_update from PROGRESS.md mtime
# ---------------------------------------------------------------------------

def refresh_last_update(projects, root_dir=None):
    """Refresh last_update dates from PROGRESS.md file modification times."""
    if root_dir is None:
        root_dir = ROOT_DIR
    updated = 0

    for name, meta in projects.items():
        docs_str = meta.get("docs", "")
        parsed = _parse_docs_field(docs_str)
        if not parsed:
            continue

        prefix, raw_path = parsed[0]
        if _is_windows_docs_prefix(prefix):
            continue

        abs_docs = _resolve_docs_path(raw_path, root_dir)
        progress_path = os.path.join(abs_docs, "PROGRESS.md")
        if os.path.isfile(progress_path):
            mtime = os.path.getmtime(progress_path)
            new_date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            old_date = meta.get("last_update", "")
            if new_date != old_date:
                meta["last_update"] = new_date
                updated += 1
                print(f"  {name}: {old_date} -> {new_date}")

    return updated


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_all_checks(stale_days=14, root_dir=None, general_path=None, layer_yamls=None):
    """Run all checks and return (issues_list, has_errors)."""
    if root_dir is None:
        root_dir = ROOT_DIR
    if general_path is None:
        general_path = GENERAL_YAML
    if layer_yamls is None:
        layer_yamls = LAYER_YAMLS

    general_data = load_yaml(general_path)
    projects = general_data.get("projects", {})

    issues = []
    issues.extend(check_code_path_exists(projects))
    issues.extend(check_cross_yaml_consistency(general_path, layer_yamls))
    issues.extend(check_last_update_stale(projects, stale_days=stale_days))
    issues.extend(check_docs_dir_exists(projects, root_dir=root_dir))
    issues.extend(check_layer_assignment(projects, layer_yamls))

    has_errors = any(i["level"] == "error" for i in issues)
    return issues, has_errors


def format_terminal(issues):
    """Format issues for terminal output."""
    if not issues:
        return "All checks passed. No issues found."

    level_styles = {
        "error": "\033[91m",   # red
        "warning": "\033[93m", # yellow
        "info": "\033[96m",    # cyan
    }
    reset = "\033[0m"

    lines = []
    # Group by level
    errors = [i for i in issues if i["level"] == "error"]
    warnings = [i for i in issues if i["level"] == "warning"]
    infos = [i for i in issues if i["level"] == "info"]

    if errors:
        lines.append(f"{level_styles['error']}ERRORS ({len(errors)}):{reset}")
        for i in errors:
            lines.append(f"  [{i['check']}] {i['project']}: {i['message']}")
        lines.append("")

    if warnings:
        lines.append(f"{level_styles['warning']}WARNINGS ({len(warnings)}):{reset}")
        for i in warnings:
            lines.append(f"  [{i['check']}] {i['project']}: {i['message']}")
        lines.append("")

    if infos:
        lines.append(f"{level_styles['info']}INFO ({len(infos)}):{reset}")
        for i in infos:
            lines.append(f"  [{i['check']}] {i['project']}: {i['message']}")
        lines.append("")

    lines.append(f"Total: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="MAPM project data health check")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--refresh", action="store_true",
                        help="Refresh last_update from PROGRESS.md mtime")
    parser.add_argument("--stale-days", type=int, default=14,
                        help="Days threshold for stale last_update (default: 14)")
    args = parser.parse_args()

    if not os.path.exists(GENERAL_YAML):
        print(f"Error: General YAML not found at {GENERAL_YAML}", file=sys.stderr)
        sys.exit(1)

    if args.refresh:
        print("Refreshing last_update from PROGRESS.md mtimes...")
        general_data = load_yaml(GENERAL_YAML)
        updated = refresh_last_update(general_data.get("projects", {}))
        if updated > 0:
            with open(GENERAL_YAML, "w", encoding="utf-8") as f:
                yaml.dump(general_data, f, allow_unicode=True, default_flow_style=False)
            print(f"Updated {updated} project(s) in {GENERAL_YAML}")
        else:
            print("No updates needed.")

    issues, has_errors = run_all_checks(stale_days=args.stale_days)

    if args.json:
        print(json.dumps(issues, ensure_ascii=False, indent=2))
    else:
        print(format_terminal(issues))

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
