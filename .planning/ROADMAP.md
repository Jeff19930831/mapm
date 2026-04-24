# Roadmap: Multi-Agent Project Manager (MAPM)

**Created:** 2026-04-24
**Phases:** 4
**Requirements:** 26 (all v1 mapped)

---

## Phase 1: Core Status System

**Goal:** Create the per-device status tracking and event logging infrastructure

**Requirements:** STAT-01 through STAT-04, EVNT-01 through EVNT-04, TASK-01 through TASK-02

**Success Criteria:**
1. Running `mkdir -p status events && touch status/view.sh` creates the directory structure
2. `status/view.sh` outputs a formatted table when given sample YAML files
3. `events/{device}.log` accepts appended lines without format corruption
4. `TODO.md` exists and is readable by all agents

**Build Order:**
1. Create directory structure (`status/`, `events/`)
2. Implement `status/view.sh` (YAML parsing + table rendering)
3. Create sample `status/{device}.yaml` files
4. Create sample `events/{device}.log` files
5. Create `TODO.md` template

---

## Phase 2: Auto-Sync

**Goal:** Implement reliable Git-based automatic synchronization across devices

**Requirements:** SYNC-01 through SYNC-06

**Success Criteria:**
1. `auto-sync.sh` runs without errors in a test repository
2. Changes to `status/` are auto-committed within 5 minutes
3. Conflicts on `status/` files are automatically resolved (keep remote)
4. Rebase interruption is detected and recovered
5. Local commits are pushed to remote

**Build Order:**
1. Write `auto-sync.sh` with commit/pull/push logic
2. Add rebase interruption detection and recovery
3. Add conflict resolution for status/ and events/
4. Test with two local git clones simulating two devices
5. Document crontab setup

**Depends on:** Phase 1 (needs status/ and events/ to sync)

---

## Phase 3: Agent Protocols

**Goal:** Configure each CLI agent to participate in the status system

**Requirements:** AGNT-01 through AGNT-06, TASK-03 through TASK-04

**Success Criteria:**
1. Claude Code SessionStart Hook displays current device statuses
2. Claude Code Stop Hook reminds to update status
3. Kimi Code can read/write status files via AGENTS.md shell commands
4. `codex-done.sh` wrapper script updates status after Codex completes
5. All agents create and use `agent/{name}/{task}` branches
6. Agents commit status changes at session end

**Build Order:**
1. Write `CLAUDE.md` with device-specific status protocols
2. Write `AGENTS.md` with Kimi + Codex protocols
3. Configure `.claude/settings.json` hooks
4. Write `codex-done.sh` wrapper
5. Test each agent independently

**Depends on:** Phase 1 (needs status files to exist), Phase 2 (needs sync to share updates)

---

## Phase 4: Shared Spec

**Goal:** Add API contract file to prevent logical conflicts between backend and frontend agents

**Requirements:** SPEC-01 through SPEC-04

**Success Criteria:**
1. `specs/api.yaml` exists and documents all API endpoints
2. Backend agent (Claude) updates spec before changing API
3. Frontend agent (Kimi) reads spec and implements accordingly
4. Spec changes are committed and synced like status files

**Build Order:**
1. Create `specs/` directory and `api.yaml` template
2. Add spec update rules to CLAUDE.md
3. Add spec read rules to AGENTS.md
4. Include specs/ in auto-sync.sh

**Depends on:** Phase 3 (needs agent protocols to enforce spec discipline)

---

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
| TASK-01 | Phase 1 | Pending |
| TASK-02 | Phase 1 | Pending |
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
| TASK-03 | Phase 3 | Pending |
| TASK-04 | Phase 3 | Pending |
| SPEC-01 | Phase 4 | Pending |
| SPEC-02 | Phase 4 | Pending |
| SPEC-03 | Phase 4 | Pending |
| SPEC-04 | Phase 4 | Pending |

**Coverage:** 26/26 requirements mapped ✓
