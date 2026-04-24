# Phase 1: Core Status System - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-24
**Phase:** 1-core-status-system
**Areas discussed:** Status file fields, Event log format, View output format, Directory location

---

## Status File Fields

| Option | Description | Selected |
|--------|-------------|----------|
| 精简版 (6字段) | device, agent, task, status, started, updated | |
| 标准版 (8字段) | device, agent, project, branch, task, status, started, updated | ✓ |
| 扩展版 (10字段) | + git_commit, working_dir, pid | |

**User's choice:** 标准版 (8字段)
**Notes:** User wants complete visibility including project and branch context for cross-project usage

---

## Event Log Format

| Option | Description | Selected |
|--------|-------------|----------|
| 纯文本行 | `[timestamp] [device/agent] message` | ✓ |
| YAML结构化 | Each event as YAML entry | |
| JSON Lines | Each line a JSON object | |

**User's choice:** 纯文本行
**Notes:** Simplicity and human readability prioritized. Append-only guarantee is the key feature.

---

## View Output Format

| Option | Description | Selected |
|--------|-------------|----------|
| 简单文本表格 | Plain text alignment, no colors | ✓ |
| 彩色终端输出 | ANSI color codes | |
| Markdown表格 | Paste-friendly format | |

**User's choice:** 简单文本表格
**Notes:** Maximum terminal compatibility across Windows WSL, Git Bash, Linux, and Mac

---

## Directory Location

| Option | Description | Selected |
|--------|-------------|----------|
| 项目根目录 | Peer to src/, TODO.md | ✓ |
| .planning/子目录 | Hidden in planning folder | |
| ~/.mapm/全局 | Global cross-project storage | |

**User's choice:** 项目根目录
**Notes:** Visibility and intuitiveness — agents see status/ immediately on `ls`

---

## Claude's Discretion

- Status file field ordering
- view.sh column width calculation
- Event message prefix format

## Deferred Ideas

None
