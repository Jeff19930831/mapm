# Multi-Agent Project Manager (MAPM)

## What This Is

A lightweight, file-based coordination system for developers who work across multiple devices with multiple AI coding agents (Claude Code, Kimi Code, Codex CLI). It replaces scattered project records with a centralized status registry and event log, synchronized across devices via Git.

## Core Value

Never lose track of which agent is running on which device doing what — a single `status/` directory gives you the full picture.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Per-device status files (`status/{device}.yaml`) with zero Git conflicts
- [ ] Append-only event logs (`events/{device}.log`) for audit trail
- [ ] One-command global status viewer (`status/view.sh`)
- [ ] Git auto-sync script (`auto-sync.sh`) for cross-device state consistency
- [ ] Agent start/end protocols for Claude Code, Kimi Code, and Codex CLI
- [ ] Shared API spec file (`specs/api.yaml`) to prevent logical conflicts between agents
- [ ] Device name hardcoding in per-device context files (CLAUDE.md / AGENTS.md)

### Out of Scope

- Team collaboration (3+ people) — single-developer multi-device only for v1
- Real-time sync (sub-second) — Git-based, minutes-level sync acceptable
- Web dashboard — terminal/obsidian view sufficient
- Automated agent scheduling — manual switching only
- MCP server integration for Kimi Code — file-system direct access only

## Context

- Developer has 2-3 devices (Windows desktop, Mac laptop, Linux server)
- Each device runs a different CLI agent: Claude Code (architecture/backend), Kimi Code (frontend/full-stack), Codex CLI (DevOps/scripts)
- Current pain point: project records scattered across devices, no visibility into what's happening where
- Prior research: 3 rounds of multi-agent review identified sequential isolation, per-device files, and append-only logs as the correct architecture

## Constraints

- **Tech stack**: Shell scripts + Git + YAML/MD — no database, no server, no dependencies
- **Sync mechanism**: Git push/pull with 5-minute cron interval
- **Agent compatibility**: Must work with Claude Code (full hooks), Kimi Code (shell commands), Codex CLI (CLI args)
- **File format**: YAML for machine-readable state, Markdown for human-readable notes
- **Cost**: Zero infrastructure cost, minimal token overhead

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Per-device files instead of single STATUS.md | Eliminates Git merge conflicts entirely | — Pending |
| Sequential isolation (one agent at a time) | Avoids file-lock and concurrent-write complexity | — Pending |
| Git auto-sync with `--no-rebase` merge | Safer than rebase for concurrent edits | — Pending |
| Obsidian as optional visualization layer | Core system works in terminal alone | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-24 after initialization*
