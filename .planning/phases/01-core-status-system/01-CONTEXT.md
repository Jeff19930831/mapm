# Phase 1: Core Status System - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Create the per-device status tracking and event logging infrastructure:
- `status/` directory with one YAML file per device
- `events/` directory with one append-only log file per device
- `status/view.sh` script to display global status table
- `TODO.md` task tracking file

</domain>

<decisions>
## Implementation Decisions

### Status File Format
- **D-01:** Standard 8-field YAML format: `device`, `agent`, `project`, `branch`, `task`, `status` (idle/in_progress/done/blocked), `started`, `updated`
- **D-02:** One file per device: `status/{device-name}.yaml`
- **D-03:** Only the named device writes its own file (zero conflict principle)

### Event Log Format
- **D-04:** Plain text lines: `[ISO timestamp] [device/agent] message`
- **D-05:** Append-only — never modify existing lines
- **D-06:** One file per device: `events/{device-name}.log`

### View Script
- **D-07:** Simple text table output (no colors, maximum terminal compatibility)
- **D-08:** Displays: device name, agent, task, status, last updated time
- **D-09:** Includes last 5 events from all devices

### Directory Location
- **D-10:** `status/` and `events/` at project root (peer to src/, TODO.md)
- **D-11:** Visible and intuitive — agents see them immediately on `ls`

### Device Name Management
- **D-12:** Hardcoded in per-device CLAUDE.md / AGENTS.md (not dynamically detected)
- **D-13:** Device creates its own status file on first run if missing

### Claude's Discretion
- Status file field ordering (YAML keys)
- view.sh column width calculation approach
- Event message prefix format (e.g., "Task:" vs emoji markers)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Definition
- `.planning/PROJECT.md` — Project vision, core value, constraints
- `.planning/REQUIREMENTS.md` — Phase 1 requirements (STAT-01 through TASK-02)
- `.planning/ROADMAP.md` — Phase 1 goal, success criteria, build order

### Prior Decisions
- `multi-agent-plan.md` — Full v6 architecture document with 3-round review rationale

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None (greenfield infrastructure project)

### Established Patterns
- Shell script + YAML + Git workflow (from multi-agent-plan.md v6)
- Per-device file isolation pattern (zero-conflict architecture)

### Integration Points
- Will integrate with `.claude/settings.json` hooks (Phase 3)
- Will integrate with `auto-sync.sh` cron job (Phase 2)

</code_context>

<specifics>
## Specific Ideas

- Status enum values: `idle`, `in_progress`, `done`, `blocked`
- view.sh should sort devices alphabetically for consistent output
- Sample status file should be created as template for new devices

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-core-status-system*
*Context gathered: 2026-04-24*
