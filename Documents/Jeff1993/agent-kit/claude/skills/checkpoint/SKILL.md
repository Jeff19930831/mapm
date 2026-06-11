---
name: checkpoint
description: >
  Execute a Jeff1993 project checkpoint: close out local work, verify changes,
  refresh durable handoff/onboarding docs, store safe memory, run secret checks,
  and create a traceable Git commit. Use when the user says checkpoint, 收口,
  归档当前进展, 刷新 handoff, or asks to prepare work for cross-device continuation.
---

# checkpoint — durable closeout

## Contract

Turn the current workspace into a durable, reviewable handoff.

Checkpoint writes committed project state. It is different from:
- `session-handoff`: same-device, no commit, no cloud, no durable doc rewrite by default.
- `con-dev`: cold-start/takeover, mostly read-only, prepares the workspace to start work.

Use two maps with different jobs:
- **CodeGraph**: local development radar. Use it for flow/call/impact questions when installed. `.codegraph/` is local artifact and must not be committed.
- **CODEMAP**: durable onboarding map. Refresh `docs/onboarding/CODEMAP.md` when onboarding is enabled; commit it with project docs.

## Safety Defaults

- Never revert user or other-agent changes unless explicitly asked.
- Do not print secret values. Secret checks print paths only.
- Do not push, deploy, or touch production/cloud unless the user explicitly authorizes it in this turn or the project policy clearly allows it.
- If merge conflicts or conflict markers are found, stop before editing checkpoint docs except for a short blocker note if safe.

## Modes

- **default/local**: verify, update docs, commit if appropriate, no push/deploy.
- **draft**: inspect and produce proposed checkpoint notes only; no file writes.
- **publish**: after local checkpoint, push permitted remotes if fast-forward safe and explicitly authorized.
- **no-commit**: update/verify docs but stop before `git add` / `git commit`.

If the user does not specify a mode, assume **default/local**.

## Workflow

### 1. Resolve Project

From the current directory or provided project name:
- Find the Git root.
- Identify branch, upstream/ahead/behind, recent commit, and dirty files.
- Resolve handoff/progress/plan with this priority:
  - `handoff.md`, then `HANDOFF.md`
  - `progress.md`, then `PROGRESS.md`
  - `plan.md`, create only when needed
- If a Jeff1993 registry exists, use it only for project metadata; do not block if absent.

### 2. Preflight

Run targeted checks:

```bash
git status --short --branch
rg -n "<<<<<<<|=======|>>>>>>>" .
```

If conflict markers exist, stop and report paths. Do not proceed to commit.

### 3. CodeGraph Radar

When `codegraph` is installed:
- If `.codegraph/` is missing or the user asked for a fresh structural pass, run `codegraph init -i` from the project root.
- Use CodeGraph/MCP queries for changed entry points, callers/callees, route-to-handler paths, and blast-radius checks when that helps validate the checkpoint.
- Summarize only the relevant findings in handoff/progress; do not commit `.codegraph/`.

When `codegraph` is not installed:
- Continue with `rg`, tests, and CODEMAP.
- Add a short note only if structural verification would materially help the next takeover.

### 4. Verify Work

Choose the smallest useful validation set from project docs (`AGENTS.md`, `BOOTSTRAP.md`, `plan.md`) and the diff:
- Backend: focused pytest, then broader pytest when shared behavior changed.
- Frontend: typecheck/build for UI/API wiring changes.
- Docs-only: run doc/onboarding checks; say tests were not needed.

Record commands and results. Do not invent passing tests.

### 5. Durable Docs

Refresh docs in this order:

1. `plan.md`: keep only Active / External or Authorization Required / Next / Archived links. Move completed facts to progress.
2. `progress.md` or `PROGRESS.md`: append concise completed work and evidence.
3. `handoff.md` or `HANDOFF.md`: keep it short:
   - Persistent Context
   - Current Takeover
   - Next
   - Blockers / Risks
   - Verification
   - Index
4. Runbooks/ADR: create or update only for stable operational knowledge, repeated failure modes, or decisions affecting two or more modules.
5. Onboarding, when `docs/onboarding/` exists:

```bash
python scripts/refresh_codemap.py
python scripts/check_onboarding.py
```

For onboarding failures:
- `codemap_missing_role`: read only the needed files and replace `<待填>` with one-line roles.
- `module_card_missing`: create a concise module card for the large file.
- `adr_index_stale`: run `python scripts/check_onboarding.py --rebuild-index`.
- User-authored bootstrap/routing issues: report before changing.

Re-run `check_onboarding.py` after fixes.

### 6. Memory

Memory is a supplement, not the source of truth.

Before rewriting handoff, optionally recall recent project memory if available and relevant. Handoff wins over memory on conflicts.

After docs are refreshed, store one safe project summary:
- current goal
- recent completed items
- next step
- blocker if any
- verification evidence

For credentials, store only references: name, purpose, storage location, recovery runbook. Never store payloads.

If memory service is unavailable, continue and mention it in the final report.

### 7. Secret Gate

Check tracked paths and staged diff for likely secret payloads. Print paths only.

Private-repo policy may allow payloads, but the checkpoint must still surface likely accidental files before commit.

### 8. Commit

Stage only the checkpoint-relevant files unless the user asked for `git add -A`. Respect unrelated dirty files.

Use a clear message:

```text
[CHECKPOINT] <project>: <short outcome>

- <completed item>
- <verification>
```

Add co-author trailers only if the project convention requires them.

### 9. Optional Push / Deploy

Push only in `publish` mode or after explicit authorization:
- Fetch first.
- Push only fast-forward-safe branches.
- Never force-push unless explicitly instructed.
- Deploy only with explicit operator authorization and the project runbook.

### 10. Final Report

Return:
- what changed
- tests/checks run
- commit hash or “not committed”
- push/deploy status
- remaining blockers/next step

Keep the report short; link local files when useful.
