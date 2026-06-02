---
name: session-handoff
description: 同设备切 session 的轻量续接。
---

# session-handoff (Codex)

> 同设备切 session 的轻量续接 skill。只读当前工作区最少上下文: handoff/plan/git 摘要。
> 不做跨设备解析、不查云端记忆、不跑环境检测。

## 触发关键词
- "切 session 继续"
- "同设备接手"
- "生成本地 handoff"
- "轻量续接"
- "session handoff"

## 前置
- 当前工作目录是项目代码根（含 git）

## 读取范围
1. `handoff.md` / `HANDOFF.md`
2. `plan.md`
3. `git status --short`
4. `git log -1 --oneline`
5. 可选 `progress.md`

## 不做什么
- 不查 `.project-status.yaml`
- 不做跨设备路径解析
- 不拉 cloud-memory
- 不展开 runbook / archive / decisions 全文
- 不做环境检测

## 流程
```bash
python3 scripts/session_handoff_draft.py [--project-root .] [--output file]
```

## 输出规则
- 默认 dry-run，不改文件
- 目标 30-50 行，硬上限 80 行
- 只保留：当前目标、下一步、阻塞 / 风险、不要重复、Evidence Pointers

## 与 con-dev 的区别
- `session-handoff`：同设备、轻量续接
- `con-dev`：跨设备、老项目冷启动、注册表/云记忆/环境检测

## 边界
- 不 commit / push
- 不自动改四文档
- 不读取敏感 payload
