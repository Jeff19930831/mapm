---
name: session-handoff
description: >
  同设备切换 session 时生成轻量续接包。用在同一台机器、同一项目、需要从当前 handoff/plan/git 状态快速续上时。
  只读当前工作区最少上下文: handoff.md、plan.md、git diff/commit 摘要, 不做跨设备解析、不查云端记忆、不跑环境检测。
  当用户说“切 session 继续”“同设备接手”“生成本地 handoff”“轻量续接”时触发。
argument-hint: "[--project-root PATH] [--output FILE]"
allowed-tools:
  - Read
  - Bash
---

# session-handoff — 同设备轻量续接

适用于同设备、同项目、从当前 session 切到新 session 的轻量 handoff。

## 目标

输出一个短续接包，只保留：
- 当前目标
- 下一步 1-3 条
- 阻塞 / 风险
- 不要重复 1-3 条
- Evidence Pointers

## 读取范围

默认只看当前工作区：
1. `handoff.md` 或 `HANDOFF.md`
2. `plan.md`
3. `git status --short`
4. `git log -1 --oneline`
5. 可选：`progress.md`

## 不做什么

- 不查 `.project-status.yaml`
- 不做跨设备路径解析
- 不拉 cloud-memory
- 不展开 runbook / archive / decisions 全文
- 不做环境检测或 bootstrap

## 流程

```bash
python3 scripts/session_handoff_draft.py [--project-root .] [--output file]
```

### 输出规则

- 默认只生成 dry-run draft，不改文件
- 输出尽量短，目标 30-50 行，硬上限 80 行
- 如果 `handoff.md` 已很长，提醒先做归档，再继续会话切换

## 与 con-dev 的区别

- `session-handoff`：同设备、轻量续接
- `con-dev`：跨设备、老项目冷启动、注册表/云记忆/环境检测

## 边界

- 不 commit
- 不 push
- 不自动改四文档
- 不读取敏感 payload
