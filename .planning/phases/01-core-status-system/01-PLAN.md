# Phase 1: Core Status System — Execution Plan

**Phase:** 1
**Name:** Core Status System
**Wave:** 1
**Depends on:** (none — first phase)
**Files Modified:**
  - `status/`
  - `events/`
  - `status/view.sh`
  - `TODO.md`
**Autonomous:** true

---

## Objective

Create the per-device status tracking and event logging infrastructure:
- `status/` directory with YAML status files
- `events/` directory with append-only log files
- `status/view.sh` for global status display
- `TODO.md` for task tracking

---

## Must-Haves

1. Each device can create and update its own YAML status file without Git conflicts
2. Events are append-only and never lose data
3. `view.sh` displays all device statuses in a readable table
4. `TODO.md` exists and follows a simple format agents can parse

---

## Task 01: Create Directory Structure and Sample Files

<read_first>
- `.planning/phases/01-core-status-system/01-CONTEXT.md` (decisions from discuss-phase)
- `.planning/REQUIREMENTS.md` (STAT-01 through STAT-04, EVNT-01 through EVNT-04)
</read_first>

<action>
Create the directory structure at project root:

1. Create `status/` directory
2. Create `events/` directory
3. Create a sample status file `status/win-desktop.yaml`:
   ```yaml
   device: win-desktop
   agent: none
   project: ""
   branch: ""
   task: ""
   status: idle
   started: ""
   updated: ""
   ```
4. Create a sample event log `events/win-desktop.log`:
   ```
   # Events for win-desktop
   # Format: [ISO timestamp] [device/agent] message
   ```
5. Create `status/TEMPLATE.yaml` as a copyable template for new devices:
   ```yaml
   # Copy this to status/{your-device-name}.yaml
   # Only the named device should write to this file
   device: YOUR_DEVICE_NAME
   agent: none
   project: ""
   branch: ""
   task: ""
   status: idle
   started: ""
   updated: ""
   ```
</action>

<acceptance_criteria>
- `status/` directory exists and contains `win-desktop.yaml` and `TEMPLATE.yaml`
- `events/` directory exists and contains `win-desktop.log`
- `status/win-desktop.yaml` contains all 8 fields: device, agent, project, branch, task, status, started, updated
- `status/win-desktop.yaml` has `status: idle` and empty strings for optional fields
- `events/win-desktop.log` contains the header comment lines
</acceptance_criteria>

---

## Task 02: Implement status/view.sh

<read_first>
- `status/win-desktop.yaml` (sample file from Task 01)
- `.planning/phases/01-core-status-system/01-CONTEXT.md` § "View Script" decisions
</read_first>

<action>
Create `status/view.sh` that:

1. Scans `status/*.yaml` for all device status files
2. Parses each YAML file to extract: device, agent, task, status, updated
3. Prints a formatted text table:
   ```
   ====== Device Status ======
   
   DEVICE          AGENT           TASK                STATUS       UPDATED
   --------------  --------------  ------------------  -----------  -------------------
   win-desktop     none            -                   idle         -
   ```
4. After the table, prints last 5 events from all `events/*.log` files:
   ```
   ====== Recent Events ======
   
   [2026-04-24T10:30:00] [win-desktop/none] placeholder
   ```
5. Handles edge cases gracefully:
   - No status files found → print "No devices registered"
   - Missing YAML fields → print "-" for missing values
   - Empty events directory → print "No events yet"

Implementation notes:
- Use `grep` + `awk` for YAML parsing (no external dependencies)
- Column widths: device=15, agent=15, task=20, status=12, updated=20
- Sort devices alphabetically
- Exit code 0 on success
</action>

<acceptance_criteria>
- `status/view.sh` exists and is executable (`chmod +x`)
- Running `bash status/view.sh` outputs a table with headers: DEVICE, AGENT, TASK, STATUS, UPDATED
- The table displays the sample `win-desktop.yaml` data correctly
- The "Recent Events" section shows the placeholder event from `win-desktop.log`
- Script exits with code 0
- Script handles missing files gracefully (no crash)
</acceptance_criteria>

---

## Task 03: Create TODO.md

<read_first>
- `.planning/REQUIREMENTS.md` (TASK-01, TASK-02)
</read_first>

<action>
Create `TODO.md` at project root with this format:

```markdown
# TODO

## P1 — High Priority
- [ ] Task description → agent-name

## P2 — Medium Priority
- [ ] Task description → agent-name

## P3 — Low Priority
- [ ] Task description → agent-name

## Done
- [x] Completed task → agent-name ✅ YYYY-MM-DD
```

Add one sample task:
```markdown
## P1 — High Priority
- [ ] Implement auto-sync script → codex
```
</action>

<acceptance_criteria>
- `TODO.md` exists at project root
- File contains sections: P1, P2, P3, Done
- Each task line follows format: `- [ ] description → agent-name`
- Contains at least one sample task
- Markdown checkbox syntax is correct (`- [ ]` and `- [x]`)
</acceptance_criteria>

---

## Task 04: Create .gitignore Entries

<read_first>
- `.planning/config.json` (commit_docs setting)
</read_first>

<action>
If `.gitignore` exists, append these entries if not present:
```
# MAPM status files — device-specific, auto-generated
# Note: We DO track status/ and events/ in git for sync
# Only ignore patterns that shouldn't sync

# Ignore temp/backup files
*.yaml.bak
*.log.bak
status/.*
events/.*
```

If `.gitignore` does not exist, create it with the above content.
</action>

<acceptance_criteria>
- `.gitignore` exists at project root
- `.gitignore` contains entries for `*.yaml.bak`, `*.log.bak`, `status/.*`, `events/.*`
- `status/` and `events/` directories themselves are NOT ignored (we want to sync them)
</acceptance_criteria>

---

## Verification

After all tasks complete, run:

```bash
bash status/view.sh
cat TODO.md
ls -la status/ events/
```

Expected:
- `view.sh` shows the device status table
- `TODO.md` has the sample task
- Both directories exist with correct files

---

*Plan: 01-core-status-system*
*Created: 2026-04-24*
*Requirements: STAT-01..04, EVNT-01..04, TASK-01..02*
