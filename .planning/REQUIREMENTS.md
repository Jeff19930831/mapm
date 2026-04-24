# Requirements: Multi-Agent Project Manager (MAPM)

**Defined:** 2026-04-24
**Core Value:** Never lose track of which agent is running on which device doing what

## v1 Requirements

### Status Tracking

- [ ] **STAT-01**: Each device has its own YAML status file (`status/{device}.yaml`) that only that device writes to
- [ ] **STAT-02**: Status file contains: device name, agent type, project, branch, task, status (idle/in_progress/done/blocked), start time, update time
- [ ] **STAT-03**: Running `status/view.sh` displays a formatted table of all devices' current states
- [ ] **STAT-04**: Device names are hardcoded in per-device context files, not dynamically detected

### Event Logging

- [ ] **EVNT-01**: Each device has its own append-only event log (`events/{device}.log`)
- [ ] **EVNT-02**: Events are timestamped with ISO 8601 format
- [ ] **EVNT-03**: Event format: `[timestamp] [device/agent] message`
- [ ] **EVNT-04**: Events are never modified or deleted (append-only)

### Git Auto-Sync

- [ ] **SYNC-01**: `auto-sync.sh` runs via cron every 5 minutes
- [ ] **SYNC-02**: Script auto-commits changes to status/ and events/ directories
- [ ] **SYNC-03**: Script pulls remote changes with `--no-rebase --autostash` merge strategy
- [ ] **SYNC-04**: Script handles rebase interruption recovery (auto-abort if stuck)
- [ ] **SYNC-05**: Script resolves merge conflicts on status/ and events/ by keeping remote version
- [ ] **SYNC-06**: Script pushes local commits to remote

### Agent Protocols

- [ ] **AGNT-01**: Claude Code has SessionStart Hook that reads all status files and runs `view.sh`
- [ ] **AGNT-02**: Claude Code has Stop Hook that reminds to update status and commit
- [ ] **AGNT-03**: Kimi Code AGENTS.md contains shell commands to read/write status files
- [ ] **AGNT-04**: Codex CLI has a wrapper script (`codex-done.sh`) to update status after task completion
- [ ] **AGNT-05**: All agents work on `agent/{agent-name}/{task-name}` Git branches
- [ ] **AGNT-06**: All agents commit and push status changes at end of session

### Shared Spec

- [ ] **SPEC-01**: `specs/api.yaml` exists for projects with backend/frontend split
- [ ] **SPEC-02**: Only the backend agent (Claude Code) can modify specs/api.yaml
- [ ] **SPEC-03**: Frontend agent (Kimi Code) reads but never writes specs/api.yaml
- [ ] **SPEC-04**: API changes require spec update before code change

### Task Tracking

- [ ] **TASK-01**: `TODO.md` exists at project root with simple task list
- [ ] **TASK-02**: Tasks include assignee (agent name) and priority
- [ ] **TASK-03**: Agents read TODO.md at startup to know their assigned tasks
- [ ] **TASK-04**: Agents update TODO.md checkbox when task completes

## v2 Requirements

### Multi-Project

- **PROJ-01**: Single vault/directory tracks multiple projects' statuses
- **PROJ-02**: Per-project status isolation

### Enhanced Sync

- **SYNC-V2-01**: File watcher triggers sync immediately (instead of 5-min cron)
- **SYNC-V2-02**: Conflict notifications (alert when manual merge needed)

### Validation

- **VALD-01**: YAML schema validation for status files
- **VALD-02**: Pre-commit hook checks spec/api.yaml consistency

## Out of Scope

| Feature | Reason |
|---------|--------|
| Team collaboration (3+ people) | Current design is single-developer multi-device; team scaling requires different architecture |
| Real-time sync (sub-second) | Git-based minutes-level sync is sufficient for this use case |
| Web dashboard | Terminal `view.sh` + optional Obsidian is sufficient |
| Automated agent scheduling | Manual agent switching is deliberate and safe |
| MCP server for Kimi Code | File-system direct access is more reliable given Kimi MCP support is unconfirmed |
| Windows batch/PowerShell scripts | v1 targets bash; Windows users use WSL or Git Bash |
| Conflict resolution UI | Conflicts resolved by auto-sync script or manual git commands |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| STAT-01 | Phase 1 | Pending |
| STAT-02 | Phase 1 | Pending |
| STAT-03 | Phase 1 | Pending |
| STAT-04 | Phase 1 | Pending |
| EVNT-01 | Phase 1 | Pending |
| EVNT-02 | Phase 1 | Pending |
| EVNT-03 | Phase 1 | Pending |
| EVNT-04 | Phase 1 | Pending |
| SYNC-01 | Phase 2 | Pending |
| SYNC-02 | Phase 2 | Pending |
| SYNC-03 | Phase 2 | Pending |
| SYNC-04 | Phase 2 | Pending |
| SYNC-05 | Phase 2 | Pending |
| SYNC-06 | Phase 2 | Pending |
| AGNT-01 | Phase 3 | Pending |
| AGNT-02 | Phase 3 | Pending |
| AGNT-03 | Phase 3 | Pending |
| AGNT-04 | Phase 3 | Pending |
| AGNT-05 | Phase 3 | Pending |
| AGNT-06 | Phase 3 | Pending |
| SPEC-01 | Phase 4 | Pending |
| SPEC-02 | Phase 4 | Pending |
| SPEC-03 | Phase 4 | Pending |
| SPEC-04 | Phase 4 | Pending |
| TASK-01 | Phase 1 | Pending |
| TASK-02 | Phase 1 | Pending |
| TASK-03 | Phase 3 | Pending |
| TASK-04 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-24*
*Last updated: 2026-04-24 after initial definition*
