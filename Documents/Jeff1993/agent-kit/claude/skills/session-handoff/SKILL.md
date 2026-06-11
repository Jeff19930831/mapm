---
name: session-handoff
description: Generate a same-device lightweight handoff packet for continuing work in a new local session. Use when the user says 切 session 继续, 同设备接手, 生成本地 handoff, 轻量续接, or wants a compact continuation note without checkpointing, cloud memory, environment sync, commit, or push.
---

# session-handoff — local continuation packet

## Contract

Create a short continuation packet for the same machine and same workspace.

Default behavior is read-only and ephemeral:
- no commit
- no push
- no cloud memory
- no project registry
- no dependency install
- no durable doc rewrite unless the user explicitly asks for an output file

## Inputs

Read only:
1. `handoff.md` or `HANDOFF.md`
2. `plan.md`
3. `git status --short --branch`
4. `git log -1 --oneline`
5. Optional: a small `git diff --stat` / `git diff --name-only`
6. Optional: recent progress only when handoff/plan is ambiguous

Do not expand archive, runbooks, ADRs, full CODEMAP, or cloud memory.

## CodeGraph / CODEMAP Rule

- Do not initialize or refresh CodeGraph.
- Do not run `refresh_codemap.py`.
- If an existing CodeGraph MCP is available and the user specifically asks for a code-flow summary, a small query is allowed; otherwise skip it.
- CODEMAP is only a fallback lookup for file roles when the current handoff is unclear.

## Output Shape

Target 30-50 lines, hard limit 80 lines.

Use this structure:

```markdown
# Session Handoff — <project>

## Current Goal
<one sentence>

## Where Things Stand
- <branch/dirty/last commit>
- <what changed or was being attempted>

## Next Actions
1. <next concrete action>
2. <next concrete action>
3. <optional>

## Blockers / Risks
- <blocker or "None known">

## Do Not Repeat
- <failed attempt / already-verified path, if any>

## Evidence Pointers
- <tests, files, commits, commands>
```

## Output File

If the user passes `--output FILE` or asks to write it:
- write only that file
- do not modify canonical `HANDOFF.md` unless explicitly requested
- keep the packet short enough to paste into a new session

## Relationship To Other Flows

- Use `session-handoff` for local context transfer.
- Use `con-dev` for new-device or cold-start takeover.
- Use `checkpoint` for durable docs, verification, Git commit, and optional publish.

