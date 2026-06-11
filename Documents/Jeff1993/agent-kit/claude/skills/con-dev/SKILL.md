---
name: con-dev
description: >
  Continue development on an existing Jeff1993 project from a new device or fresh
  session: sync project metadata, locate the repo, pull safe updates, recall
  cloud memory, read only takeover docs, prepare CodeGraph if available, check
  the local environment, and produce a compact readiness report. Use when the
  user says 继续开发, 接手项目, 新设备继续, con-dev, or asks to resume an old project.
---

# con-dev — cold-start takeover

## Contract

Prepare to start work on an existing project. Prefer read-only inspection and safe sync. Do not checkpoint, commit, push, deploy, or rewrite durable docs.

Use maps like this:
- **BOOTSTRAP / handoff / plan**: takeover source of truth.
- **CODEMAP**: durable file-role map; grep it only when needed, do not refresh during con-dev.
- **CodeGraph**: optional local code intelligence. Initialize or refresh local `.codegraph/` if installed and useful for immediate development.

## Stop Conditions

Stop and ask for user action when:
- The project registry cannot identify the requested project.
- The target repo has unresolved merge conflicts.
- Pull/rebase would be required while the workspace has uncommitted changes.
- Required code path does not exist and clone destination is ambiguous.

Warnings do not block: missing venv, missing `node_modules`, missing CodeGraph, unavailable cloud memory.

## Workflow

### 1. Sync Jeff1993 Metadata

If a Jeff1993 docs/registry repo exists:
- Check `git status`.
- Pull only if clean.
- If dirty, report and continue with local docs when safe; do not stash.

### 2. Locate Project

Use registry data when available:
- `.project-status.yaml`
- `scripts/project_registry.py resolve <project>`
- `scripts/project_registry.py sync-list <project> --summary`

Resolve:
- project status/owner
- repo URL
- active `code_path` / `code_paths`
- `last_handoff`
- sync/runbook hints

If no registry exists, use the current Git root as the project.

### 3. Sync Code Repo

If the code path exists:
- Run `git status --short --branch`.
- Pull only when clean and fast-forward safe.
- If dirty, do not pull; report dirty state and continue reading local context.

If the code path is missing and repo URL is known:
- Clone only when the destination is clear.
- Otherwise report the suggested path.

### 4. Recall Cloud Memory

Use 2-3 focused queries when memory tools/service are available:
- `<project> checkpoint deploy`
- `<project> blocker decision`
- `<project> credentials server`

Merge and summarize only useful facts. Never output secret payloads. If memory conflicts with handoff, trust handoff.

### 5. Read Takeover Context

Read the smallest useful set:

When `docs/onboarding/BOOTSTRAP.md` exists:
1. `BOOTSTRAP.md`
2. handoff current sections only: Persistent Context, Current Takeover, Next, Blockers, Verification, Index
3. `plan.md` Active section only
4. Do not read full CODEMAP, ADRs, archive, runbooks, or progress unless pointed there.

Without BOOTSTRAP:
1. handoff current sections
2. `plan.md` Active section or first 40 lines
3. README only for goal/architecture/run commands
4. runbooks only if current task touches deployment, credentials, or services

### 6. Prepare CodeGraph

Check for CodeGraph:

```bash
codegraph --version
```

If installed:
- If `.codegraph/` is absent, stale, or user explicitly wants codegraph readiness, run `codegraph init -i`.
- Use CodeGraph only for immediate questions such as “where is this flow?” or “what callers matter?”
- Keep `.codegraph/` local and untracked.

If not installed:
- Report “CodeGraph unavailable; using rg/CODEMAP fallback.”
- Do not block readiness.

### 7. Environment Check

Detect common project runtimes:

```bash
test -f pyproject.toml
test -d .venv
test -f package.json
test -d node_modules
test -f go.mod
test -f Cargo.toml
```

For Windows PowerShell, use equivalent `Test-Path` checks.

Do not install dependencies unless the user asks.

### 8. Readiness Report

Return a compact report:
- project and path
- git branch/ahead/behind/dirty state
- docs read
- cloud memory summary or unavailable
- CodeGraph status
- environment status
- current goal
- next 1-3 actions
- blockers/risks

End by saying work should continue from `plan.md` Active and future durable closeout should use `checkpoint`.
