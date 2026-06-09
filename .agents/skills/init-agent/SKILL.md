---
name: init-agent
description: "Initialize a new Claude Agent or device into the Jeff1993 collaboration system. Use this skill whenever the user says 'init agent', 'onboard', 'new device setup', 'setup this machine', 'agent onboarding', or when a new Agent session starts and needs to confirm identity, read rules, and sync project-approved skills/plugins. Also use when the user wants to install the everything-claude-code plugin or add its marketplace."
argument-hint: "[--dry-run|--apply]"
allowed-tools:
  - Read
  - Bash
  - Write
  - AskUserQuestion
  - Glob
  - Grep
---

<objective>
One-command onboarding for a new Agent/device into Jeff1993.

**What it does:**
1. Confirm identity (device, user, Agent type, Jeff1993 root)
2. Read global rules (collab-entry.md, onboarding.md)
3. Discover local projects from .project-status.yaml
4. Install/sync project-approved skills and plugins (including everything-claude-code)
5. Check/sync cloud-memory agentmemory MCP access
6. Generate an onboarding report

**What it does NOT do:**
- Secret payload restoration (use `--include-secrets` flag for a future v2, or handle manually)
- Overwrite system/built-in configs
- Modify code repositories (that's what /checkpoint is for)
</objective>

<process>
## Step 1: Identity Confirmation

Confirm and record:
1. **Device & OS**: `uname -s` or `systeminfo | findstr /B /C:"OS"`
2. **Username**: `whoami`
3. **Agent type**: Claude Code CLI / Codex / Other (ask if unclear)
4. **Jeff1993 root**: Check in order:
   - `JEFF1993_ROOT` env var
   - `C:\Users\<user>\Documents\Jeff1993` (Windows)
   - `/Users/<user>/Documents/Jeff1993` (macOS)
   - `/home/<user>/Documents/Jeff1993` (Linux)
   - Ask user if not found

Verify it looks like Jeff1993 (has `collab-entry.md`, `agent-kit/`, `.project-status.yaml`).

If this is a NEW Agent (no memory of previous work), also check:
- Current working directory
- Whether `.project-status.yaml` is readable

## Step 2: Read Global Rules

Read in order:
1. `{JEFF1993_ROOT}/collab-entry.md` — global rules and doc map
2. `{JEFF1993_ROOT}/onboarding.md` — identity rules, write rules, checkpoint, init, secret boundaries

Key takeaways to confirm with user:
- Checkpoint protocol (when and how to run /checkpoint)
- Secret policy (default deny, no payload in Git, dry-run first)
- Document hierarchy (README stable; plan Active/Next; progress/archive history; handoff Persistent/Current; runbooks recurring problems)
- Doc Lifecycle Gate: entry docs stay short; historical reasons live in progress/archive/decisions; recurring issues live in runbooks

## Step 3: Discover Projects

Read `{JEFF1993_ROOT}/.project-status.yaml`.

List projects associated with this device (match by `code_path` containing current OS paths, or `docs` path matching).

Show user a summary:
```
This device has N projects:
- project-a (运行中) → D:\ClaudeCode\project-a
- project-b (维护中) → D:\ClaudeCode\project-b
```

If no projects matched, ask user which project to work on.

## Step 4: Check/Install Skills

Check if project-approved skills are present in the universal skill directory first: `~/.agents/skills/`.

If the target client does not scan `~/.agents/skills/`, fall back to its own user-level skill directory (for example `~/.claude/skills/` or `~/.gemini/skills/`).

### Required skills
| Skill | Source | Status |
|-------|--------|--------|
| checkpoint | Jeff1993 agent-kit | check/install |

**If checkpoint skill missing:**
- Copy from `{JEFF1993_ROOT}/agent-kit/claude/skills/checkpoint/` if exists
- Or create from Jeff1993 onboarding spec

**If init-agent skill itself is outdated:**
- Warn user that this skill may need updating from agent-kit

### Optional skills (from agent-kit manifest)
Read `{JEFF1993_ROOT}/agent-kit/manifest.yaml` if it exists.
For each listed skill:
 - Check if installed in `~/.agents/skills/` first, then client-specific user skill directory if needed
 - If missing and user confirmed `--apply`, install the universal skill link or copy
- If `--dry-run`, report "would install X"

## Step 5: Check/Install Plugins

### everything-claude-code (ecc)

Check if installed:
```bash
claude plugin list 2>/dev/null | grep -i everything || echo "NOT_INSTALLED"
```

If not installed:
1. **Dry-run** (default): Report "Would add marketplace + install everything-claude-code"
2. **Apply** (with `--apply` or user confirmation):
   ```bash
   claude plugin marketplace add https://github.com/affaan-m/everything-claude-code
   claude plugin install everything-claude-code@everything-claude-code
   ```

### Other plugins from agent-kit manifest
Read manifest for plugin entries. For each:
- Check if installed
- If missing, add marketplace (if needed) + install

### Plugin sync rules
- Never uninstall user-existing plugins
- Only ADD project-approved plugins that are missing
- Report skipped/already-installed counts

## Step 6: Sync Claude Code Settings (conditional)

Check if `{JEFF1993_ROOT}/agent-kit/claude/settings.json` exists.

If it exists, compare with local `~/.claude/settings.json`:
- Report differences (env vars, hooks, plugins)
- If `--dry-run`: show diff, do not write
- If `--apply`: ask user which sections to merge, backup before write

**Never overwrite without backup.**

## Step 6.5: Check/Install Cloud Memory MCP (agentmemory)

All Jeff1993 agents should be able to reach the shared cloud-memory service unless the target client has no MCP support.

**Service source of truth**: `{JEFF1993_ROOT}/cloud-memory/README.md`

**Expected endpoint**: `http://43.133.86.33:3111`

**Expected MCP server**: `agentmemory`

Check common client config surfaces for an `agentmemory` MCP entry:

| Client | Config path | Expected shape |
|--------|-------------|----------------|
| Claude Code / ZCode | `~/.claude.json` | `mcpServers.agentmemory` |
| Codex | `~/.codex/config.toml` | `[mcp_servers.agentmemory]` |
| Gemini CLI | `~/.gemini/settings.json` | `mcpServers.agentmemory` |
| OpenCode | `~/.config/opencode/opencode.json` | `mcp.agentmemory` |

Expected MCP command/env:

```json
{
  "command": "npx",
  "args": ["-y", "@agentmemory/mcp"],
  "env": {
    "AGENTMEMORY_URL": "http://43.133.86.33:3111",
    "AGENTMEMORY_FORCE_PROXY": "1"
  }
}
```

Windows Claude/ZCode may need `"command": "cmd"` and `"args": ["/c", "npx", "-y", "@agentmemory/mcp"]`.

Rules:
- Dry-run by default: report missing/mismatched entries without writing.
- `--apply`: backup each target config before merge; preserve unrelated user config.
- Prefer the client's own user-level config file as the default MCP install target; there is no single universal MCP config that all clients share.
- Never store `AGENTMEMORY_SECRET` or other secret payloads in Git-tracked files.
- Verify service reachability with `curl http://43.133.86.33:3111/agentmemory/livez`; unreachable does not block onboarding, but must appear in the report.

## Step 7: Onboarding Report

Generate report: `~/.claude/init-agent-report-<timestamp>.md`

```markdown
# Agent Onboarding Report

| Field | Value |
|-------|-------|
| run_id | <uuid> |
| mode | dry-run / apply |
| device | <os>-<hostname> |
| user | <username> |
| agent_type | claude / codex / other |
| jeff1993_root | <path> |
| timestamp | ISO8601 |

## Identity Checklist

- [x] Device/OS confirmed
- [x] Username confirmed
- [x] Agent type confirmed
- [x] Jeff1993 root located

## Rules Acknowledged

- [x] collab-entry.md read
- [x] onboarding.md read
- [x] Checkpoint protocol understood
- [x] Secret policy understood

## Projects on This Device

| Project | Status | Code Path |
|---------|--------|-----------|
| ... | ... | ... |

## Skills Sync

| Skill | Action |
|-------|--------|
| checkpoint | installed / already present / skipped |
| init-agent | current / outdated |

## Plugins Sync

| Plugin | Marketplace | Action |
|--------|-------------|--------|
| everything-claude-code | affaan-m/everything-claude-code | installed / already present / dry-run |

## Settings Sync

| Section | Action |
|---------|--------|
| env vars | merged / skipped / dry-run |
| hooks | merged / skipped / dry-run |
| plugins | merged / skipped / dry-run |

## Cloud Memory MCP

| Client | Action | Status |
|--------|--------|--------|
| Claude Code / ZCode | installed / already present / dry-run / skipped | reachable / unreachable / not checked |
| Codex | installed / already present / dry-run / skipped | reachable / unreachable / not checked |
| Gemini CLI | installed / already present / dry-run / skipped | reachable / unreachable / not checked |
| OpenCode | installed / already present / dry-run / skipped | reachable / unreachable / not checked |

## Next Steps

- [ ] Review report above
- [ ] If dry-run: re-run with `--apply` to actually install
- [ ] Pick a project and read handoff Persistent/Current → plan Active → README positioning/architecture/run sections
- [ ] Confirm agentmemory MCP tools appear after restarting the target AI client
- [ ] Run /checkpoint when work ends
```

Show user the report path and key findings.
</process>

<notes>
**Jeff1993 secret policy (hard boundary):**
- agent-kit/secrets/ holds policy and allowlist ONLY
- Real secret payloads live outside Git (password manager, env vars)
- init-agent NEVER copies secret payloads unless explicitly directed
- Any config file containing secrets must be in .gitignore

**When NOT to use this skill:**
- User just wants to read a single project doc → use Read
- User wants to checkpoint a project → use /checkpoint
- User wants to update a specific skill → use direct Edit/Write
- User is already onboarded and just switching projects → use Read on handoff.md

**Windows notes:**
- Use `claude` CLI directly (it handles paths internally)
- For bash checks: `uname -s` in Git Bash returns `MINGW64_NT` or similar
- Home dir: `$HOME` works in Git Bash, `%USERPROFILE%` in cmd/PowerShell
</notes>
