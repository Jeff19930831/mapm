# CLAUDE.md — Multi-Agent Project Manager (MAPM)

## Project Overview

This is the Multi-Agent Project Manager — a lightweight file-based coordination system for developers working across multiple devices with multiple AI coding agents.

## Your Role

You are the primary development agent for this project. You implement the core infrastructure and agent protocols.

## GSD Workflow

This project uses the GSD (Get Shit Done) workflow:
- `/gsd-discuss-phase N` — Gather context before planning
- `/gsd-plan-phase N` — Create detailed execution plan
- `/gsd-execute-phase N` — Execute the plan
- `/gsd-verify-work N` — Verify deliverables
- `/gsd-ship N` — Create PR and prepare for merge

## Device Info

- **Device name**: win-desktop (update this for your device)
- **Status file**: `status/win-desktop.yaml`
- **Event log**: `events/win-desktop.log`

## Agent Start Protocol

1. `git pull` — Get latest state from other devices
2. `bash status/view.sh` — See what other agents are doing
3. `cat TODO.md` — Check your assigned tasks
4. Update `status/win-desktop.yaml`: status=in_progress, task=...
5. Append start event to `events/win-desktop.log`

## Agent End Protocol

1. Update `status/win-desktop.yaml`: status=done/idle
2. Append completion event to `events/win-desktop.log`
3. Update `TODO.md` checkbox if task complete
4. `git add -A && git commit -m "agent:claude $(date +%Y%m%d-%H%M%S)" && git push`

## Project Structure

```
.
├── status/              # Per-device YAML status files
├── events/              # Per-device append-only event logs
├── specs/               # Shared API specifications
├── status/view.sh       # Global status viewer
├── auto-sync.sh         # Git auto-sync script
├── codex-done.sh        # Codex completion wrapper
├── TODO.md              # Task tracking
├── CLAUDE.md            # This file (Claude Code instructions)
├── AGENTS.md            # Kimi Code + Codex instructions
└── .planning/           # GSD planning artifacts
    ├── PROJECT.md
    ├── REQUIREMENTS.md
    ├── ROADMAP.md
    └── STATE.md
```

## Key Rules

- Only modify `status/{your-device}.yaml` — never touch other devices' files
- Events are append-only — never edit existing log lines
- Work on `agent/claude/{task-name}` branches
- Update specs/api.yaml BEFORE changing any API
- Commit status changes at the end of every session

## Workspace Directories

| Agent | Directory | Purpose |
|-------|-----------|---------|
| Claude | `Win_Claude_Work` (Obsidian Vault) | Docs, knowledge base, notes |
| Kimi | `Win_Kimi` (Obsidian Vault) | Docs, knowledge base, notes |
| Code | GitHub repositories | Actual code, managed via `git` |

## External Tool Management

### GitHub

- All project code is version-controlled and hosted via **GitHub** by default.
- Initialize projects with a GitHub repository (`gh repo create` or web UI).
- Commit changes regularly to keep local and remote in sync.
- Agent handles code-level operations; user manages `gh`/`git` installation and login.

### Obsidian

- All project docs, knowledge bases, and progress notes are managed via **Obsidian**.
- `Win_Claude_Work` is Claude's Obsidian Vault.
- `Win_Kimi` is Kimi's Obsidian Vault.
- Use Markdown format for all docs so Obsidian can parse and link them.

## Current Phase

Phase 1: Core Status System — See `.planning/ROADMAP.md`
