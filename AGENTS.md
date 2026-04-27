# AGENTS.md — Multi-Agent Project Manager (MAPM)

## Agent Roles

| Agent | Tool | Primary Device | Status File | Focus |
|-------|------|---------------|-------------|-------|
| Claude | Claude Code | win-desktop | `status/win-desktop.yaml` | Infrastructure + backend |
| Kimi | Kimi CLI / Kimi Code | (user's other devices) | `status/{device}.yaml` | Frontend + docs |
| Codex | Codex CLI | (user's other devices) | `status/{device}.yaml` | Scripts + automation |

## Universal Rules (All Agents)

1. **Only modify your own status file** — `status/{your-device}.yaml`
2. **Events are append-only** — never edit existing log lines
3. **Work on agent branches** — `agent/{name}/{task-name}`
4. **Commit at session end** — `git add -A && git commit -m "agent:{name} $(date +%Y%m%d-%H%M%S)" && git push`
5. **Git pull before start** — get latest state from other devices

## Agent Start Protocol

1. `git pull`
2. `bash status/view.sh` — see what other agents are doing
3. `cat TODO.md` — check assigned tasks
4. Update your status file: `status=in_progress`, `task=...`
5. Append start event to your event log

## Agent End Protocol

1. Update status file: `status=done/idle`
2. Append completion event to your event log
3. Update `TODO.md` checkbox if task complete
4. `git add -A && git commit -m "..." && git push`

---

## Kimi Protocol

### Status File Format

```yaml
device: YOUR_DEVICE_NAME
agent: kimi
project: ""
branch: ""
task: ""
status: idle
started: ""
updated: ""
```

### How to Update Status (Shell Commands)

```bash
# Read current status
cat status/YOUR_DEVICE.yaml

# Update status (replace fields)
echo 'device: YOUR_DEVICE
agent: kimi
project: "project-name"
branch: "agent/kimi/task-name"
task: "Doing something"
status: in_progress
started: "2026-04-27T10:00:00"
updated: "2026-04-27T10:00:00"
' > status/YOUR_DEVICE.yaml

# Append event
echo "[$(date -Iseconds)] [YOUR_DEVICE/kimi] Started task: something" >> events/YOUR_DEVICE.log
```

### Kimi-Specific Rules

- Use `Win_Kimi` (Obsidian Vault) for all documentation
- Read `specs/api.yaml` before implementing any API-related code
- Markdown output preferred for documentation tasks

---

## Codex Protocol

### Status File Format

Same as Kimi, but `agent: codex`.

### How to Update Status

Same shell commands as Kimi.

### Codex-Specific Rules

- Use `codex-done.sh` wrapper after completing tasks (see below)
- Focus on automation scripts and CLI tools
- Test scripts before committing

### codex-done.sh

```bash
#!/bin/bash
# Run this after Codex completes a task
# Usage: bash codex-done.sh "task description"

TASK="$1"
DEVICE="YOUR_DEVICE_NAME"

# Update status
cat > "status/${DEVICE}.yaml" << EOF
device: ${DEVICE}
agent: codex
project: ""
branch: ""
task: ""
status: idle
started: ""
updated: "$(date -Iseconds)"
EOF

# Append event
echo "[$(date -Iseconds)] [${DEVICE}/codex] Completed: ${TASK}" >> "events/${DEVICE}.log"

# Commit
git add -A
git commit -m "agent:codex $(date +%Y%m%d-%H%M%S) - ${TASK}"
git push

echo "Status updated and committed."
```

---

## Shared Resources

| Resource | Location | Who Writes | Who Reads |
|----------|----------|-----------|----------|
| Status files | `status/*.yaml` | Each device | Everyone |
| Event logs | `events/*.log` | Each device | Everyone |
| Task list | `TODO.md` | Everyone | Everyone |
| API spec | `specs/api.yaml` | Claude (backend) | Kimi (frontend) |
| View script | `status/view.sh` | Claude | Everyone |
| Auto-sync | `auto-sync.sh` | Claude | System |
