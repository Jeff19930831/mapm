---
name: checkpoint
description: "执行 Jeff1993 项目 checkpoint：检查冲突、归档已完成任务、刷新 handoff、secret gate、git commit"
argument-hint: "[project-name]"
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Glob
  - Grep
---

<objective>
对指定项目（或当前项目）执行 Jeff1993 checkpoint 协议，确保工作状态的文档归档和 Git 追踪。

**流程：**
1. 冲突检查 — Git 冲突标记、Obsidian 冲突副本
2. 文档解析 — 按 resolver 规则定位 handoff / plan / progress / README
3. Plan ↔ Progress 同步 — 已完成任务从 plan 归档到 progress
4. 刷新 handoff.md — 当前目标、下一步、阻塞、关键文件、验证命令
5. Secret gate — 检查候选 secret payload 是否被 Git tracked
6. Git commit — `[CHECKPOINT]` 前缀
7. GitHub 推送 — 检查并推送到远程仓库（如已配置）
</objective>

<process>
### Step 1: 定位项目

若用户提供了 project-name：
- 读取 `$PROJECTS_DIR/.project-status.yaml` 找到对应项目的 `code_path`
- 进入代码目录

若未提供：
- 从当前工作目录向上查找 `.project-status.yaml` 或 Git 仓库根
- 若找不到，提示用户提供项目名

### Step 2: 冲突检查

```bash
grep -r "<<<<<<< HEAD" . --include="*.md" --include="*.py" --include="*.yaml" --include="*.json" 2>/dev/null
grep -r "=======" . --include="*.md" --include="*.py" 2>/dev/null | head -5
```

发现冲突标记 → **停止 checkpoint**，写入 handoff.md 阻塞项，提示用户手动合并。

### Step 3: 文档解析（resolver）

**handoff:**
1. `.project-status.yaml:last_handoff` 指向的文件存在？用该文件。
2. 否则 `handoff.md` 存在？用 `handoff.md`。
3. 否则 `HANDOFF.md` 存在？用 `HANDOFF.md`。
4. 都不存在 → 按模板创建小写 `handoff.md`。

**progress:**
1. `progress.md` 存在？用 `progress.md`。
2. 否则 `PROGRESS.md` 存在？用 `PROGRESS.md`。
3. 都不存在 → 创建 `progress.md`。

**plan:**
1. `plan.md` 存在？用 `plan.md`。
2. 不存在 → 从 README / PROGRESS / HANDOFF 提取当前未完成事项，创建轻量 `plan.md`。

### Step 4: Plan ↔ Progress 同步

读取 `plan.md`：
- 标记为 `[x]` 或 "已完成" 的条目 → 移入 `progress.md`（含验证证据）
- 仍在进行中的条目 → 保留在 `plan.md`
- 更新 `plan.md` 移除已归档条目

### Step 5: 刷新 handoff.md

基于最新状态重写 `handoff.md`：
- 当前目标（1 句话）
- 最近完成（3-5 条）
- 下一步（有序列表）
- 阻塞点（无则写"无"）
- 关键文件表格
- 验证命令（bash 块）
- 当前工作区（分支、最近提交、未提交改动）

### Step 6: Secret Gate

```bash
git ls-files | grep -iE "config\.json|\.env|secret|key|token|password|credential|auth" | grep -v -iE "example|template|test|mock|fixture"
```

命中任何候选 secret payload → **停止 checkpoint**，提示 remove-from-index / 轮换。

同时扫描新增文件内容：
```bash
git diff --cached --name-only | xargs git diff --cached | grep -iE "api[_-]?key|token|secret|password|credential" | head -20
```

### Step 7: Git Commit

```bash
git add -A
git commit -m "[CHECKPOINT] <简短描述>

- <改动1>
- <改动2>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 8: GitHub 推送

检查是否配置了远程仓库，如已配置则推送到 GitHub：
```bash
git remote -v
git push origin master
```

如未配置，提示用户可以通过以下命令创建并推送：
```bash
gh repo create <repo-name> --public --source=. --remote=origin --push
```

### Step 9: 更新 .project-status.yaml（条件）

仅在以下情况更新：
- 生命周期变化（规划中 → 运行中 → 已完成）
- owner 变化
- path 变化
- status 变化
- 明确迁移 `last_handoff`

否则不碰 YAML。

### Step 10: 结束清单

- [ ] plan.md 已更新
- [ ] progress.md 已归档已完成内容
- [ ] handoff.md 已刷新
- [ ] README.md 仅在稳定信息变化时更新
- [ ] secret gate 通过
- [ ] git commit 可追踪
- [ ] GitHub 推送（如已配置远程仓库）
</process>

<notes>
- 旧项目兼容：若存在 `HANDOFF.md` / `PROGRESS.md` 大写文件，保留它们，同时创建小写版本供新模型使用。
- 不回滚其他 Agent 的改动；冲突时先合并意图再写入。
- 高冲突文件：`collab-entry.md`、`onboarding.md`、项目 `plan/progress/handoff`、`.project-status.yaml`。
- GitHub 推送：远程仓库已配置时自动推送，未配置时提示用户手动创建并推送。
</notes>
