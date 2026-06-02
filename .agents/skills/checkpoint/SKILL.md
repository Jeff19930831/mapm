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
0. **Onboarding 刷新** (若启用大型附加层) — refresh_codemap.py
1. 冲突检查 — Git 冲突标记、Obsidian 冲突副本
2. **Memory Recall** — 从云端 agentmemory 拉取项目相关记忆，为后续步骤提供上下文
3. 文档解析 — 按 resolver 规则定位 handoff / plan / progress / README
4. Doc Lifecycle Gate — 入口短、历史归档、重复问题 runbook 化
5. Plan ↔ Progress 同步 — 已完成任务从 plan 归档到 progress/YYYY-MM.md
6. 刷新 handoff.md — Persistent / Current Takeover / Index
5.1. **collab-entry 同步** (MAPM 项目专用) — 版本头、改动记录、受影响段落
6. 长期运行知识同步 — 配置/服务器/secret 引用写入 runbook, payload 不入 Git
7. **Memory Store** — 将项目状态和 secret 引用写入云端 agentmemory，供跨设备/跨 session 使用
8. **dev-log 写入** — 全局 dev-log，合并规则
9. Secret gate — 检查候选 secret payload 是否被 Git tracked
10. **Governance lint** — relations / contracts 一致性校验
11. **Onboarding 健康检查** (若启用大型附加层) — check_onboarding.py + FAIL 项自动起草
12. Git commit — `[CHECKPOINT]` 前缀
13. **Git push** — 项目代码仓 + Jeff1993 文档仓双仓 push (若各自有 origin)
</objective>

<process>
### Step 0: Onboarding 刷新 (新增, 条件)

若项目根存在 `docs/onboarding/` (大型附加层启用):

```bash
python3 scripts/refresh_codemap.py
```

此步只刷新 CODEMAP 表格 + 元数据, 不阻断任何后续步骤。失败时记录 stderr 并继续。

若不存在 `docs/onboarding/` → 跳过此步, 直接进 Step 1。

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

### Step 2.5: Memory Recall (云端记忆拉取)

从云端 agentmemory 搜索与当前项目相关的记忆，为后续 handoff 刷新提供跨设备上下文。

**API 地址**: `http://43.133.86.33:3111`（即 `cloud-memory` 项目的 agentmemory 服务）

```bash
curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<project-name> status goal blocker","limit":5}'
```

**处理规则**:
- 搜索结果中的关键事实（项目状态、目标变更、偏好）纳入 handoff.md 刷新的参考输入。
- 若搜索返回空或服务不可达 → 不阻断 checkpoint，仅记录 "memory recall: no results / service unreachable"。
- 不在 handoff 中逐条引用 memory，只吸收有价值的信息作为上下文。

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
- 标记为 `[x]` 或 "已完成" 的条目 → 移入 `progress/YYYY-MM.md`（若项目未启用月度 progress, 则移入 `progress.md`）
- 仍在进行中的条目 → 保留在 `plan.md` 的 Active
- 近期但未开始的条目 → 保留在 Next
- 旧计划/长评审/checkpoint 原文 → 移入 `archive/YYYY-MM-DD-<slug>.md`
- `plan.md` 最终只保留 Active / Next / Archived Plans, Archived Plans 只放链接和一句话结论

### Step 4.5: Doc Lifecycle Gate

写入入口文档前先检查:

- `handoff.md` 是否超过 150 行或 Current Takeover 过长。
- `plan.md` 是否 Completed/History 长于 Active/Next。
- 同一部署、配置、secret、环境或常驻服务问题是否重复出现两次以上。

处理规则:

1. `handoff.md` 只保留 Persistent Context、常驻问题雷达、Current Takeover、Next、Blockers、Verification、Index。
2. 已完成事实和验证证据写入 `progress/YYYY-MM.md` / `progress.md`。
3. 旧计划、旧评审、历史 checkpoint 原文写入 `archive/**`。
4. 重复问题写入 `docs/runbooks/**`; handoff 只留问题名、风险、链接。
5. 若项目提供 `scripts/md_health.py` 或 `scripts/archive_md_sections.py`, 先跑 dry-run/health check 再落盘:

```bash
test -f scripts/md_health.py && python3 scripts/md_health.py
test -f scripts/archive_md_sections.py && python3 scripts/archive_md_sections.py --dry-run
```

### Step 5: 刷新 handoff.md

基于最新状态重写 `handoff.md`：
- Persistent Context（半永久约束和常驻问题雷达）
- Current Takeover（当前目标 1 句话、下一步、阻塞、验证命令）
- Index（progress/archive/runbook/ADR 链接）
- 当前工作区（分支、最近提交、未提交改动）

不要把旧完成历史、长评审或 ADR 正文复制进 handoff。

### Step 5.1: collab-entry 同步 (MAPM 项目专用)

**触发条件**：当 checkpoint 的项目是 MAPM（即 `~/Documents/Jeff1993/MAPM`）且本次变更影响全局协作规则时，必须同步更新 `collab-entry.md`。

MAPM 是基础设施元项目，其版本变更可能意味着全局规则变更。checkpoint MAPM 时：

1. **版本头更新**：`collab-entry.md` 顶部的 `版本: vX.Y` 与本次 MAPM 规则版本保持一致。
2. **改动记录追加**：在版本头下方添加 `vX.Y 改动:` 行，简要说明本次变更内容。
3. **受影响段落更新**：根据本次变更性质，更新同步模型、文档地图、Checkpoint 要点、Skill 清单等段落。
4. **onboarding-compact.md 检查**：若变更涉及 compact 超简版中的引用表，同步更新。

仅修改 MAPM 内部 `plan/progress/handoff` 归档、且不改变基础设施规则时，跳过此步。

### Step 5.5: 长期运行知识同步 (条件)

若本次改动涉及配置方法、服务器接入、部署、常驻服务、环境变量、secret 引用或恢复步骤:

1. 检查项目是否已有对应 `docs/runbooks/*.md`; 没有则按 `docs/templates/project/runbook.md` 创建。
2. 写入配置方法、服务地址/端口、恢复步骤、验证命令和 secret 引用。
3. secret 引用只允许记录名称、用途、存放位置、恢复步骤; 不得写真实值、私钥正文、token、cookie、auth cache。
4. 若是大项目, 确认 `.project-status.yaml:sync.include` 覆盖 `docs/runbooks/**/*.md` 和 `.env.example` / `config*.example.*`。
5. 在 `progress.md` 追加 `[RUNBOOK]` 或 `[SECRET-REF]` 记录, 包含验证证据和不含值的恢复入口。

此步不得读取或打印真实 secret payload。发现疑似 payload 文件时先用 `git ls-files -- <path>` 判断是否 tracked, 不要打开内容。

### Step 5.7: Memory Store (云端记忆写入)

将项目关键状态写入云端 agentmemory，让其他设备/agent/session 能通过记忆搜索获取项目最新上下文。

**写入时机**: handoff.md 刷新完成后、secret gate 之前。

**默认安全口径**:
- 每次 checkpoint 必写项目状态摘要。
- secret 默认只写引用：名称、用途、存放位置、恢复步骤、相关 runbook，不写真实值。
- 真实 secret payload 只有在服务认证、HTTPS、allowlist 和用户明确授权同时满足时，才允许另行登记；否则禁止写入。

```bash
# 写入项目状态摘要（每次 checkpoint 必写）
curl -s -X POST http://43.133.86.33:3111/agentmemory/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[<project-name>] <当前目标一句话>. 最近完成: <最近完成的3条>. 下一步: <最重要的1-2条>. 阻塞: <有则写, 无则写无>. Checkpoint: <YYYY-MM-DD>.",
    "scope": "project:<project-name>"
  }'

# 写入 secret 引用（不含真实值）
curl -s -X POST http://43.133.86.33:3111/agentmemory/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[<project-name>] Secret reference: <名称/用途>. 存放位置: <路径或系统>. 恢复步骤: <runbook 路径>. 不含真实值.",
    "scope": "credentials:<project-name>"
  }'
```

**写入规则**:
1. scope 格式：`project:<name>` / `credentials:<name>` / `decision:<name>` / `troubleshoot:<name>`。
2. 凭证/连接信息仅在项目首次 checkpoint 或引用变化时写入；后续 checkpoint 仅在引用有变化时更新。
3. 若服务不可达 → 不阻断 checkpoint，在 handoff.md 中记录 "memory store: service unreachable"。
4. 写入后打印返回的 memory ID 作为验证。

可选写入重要观察:

```bash
# 架构决策
curl -s -X POST http://43.133.86.33:3111/agentmemory/observe \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<重要发现或决策的描述>",
    "scope": "decision:<project-name>"
  }'

# 排障记录（问题和解法，供其他设备/agent 参考）
curl -s -X POST http://43.133.86.33:3111/agentmemory/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[<project-name>] Troubleshoot: <问题>. 原因: <根因>. 解决: <解法>. 影响: <影响范围>.",
    "scope": "troubleshoot:<project-name>"
  }'
```

### Step 5.8: 写入当日 dev-log（全局）

**dev-log 是全局目录，位于 Jeff1993 根目录下，不是项目目录的子目录。**
- 正确路径：`<Jeff1993根>/dev-log/YYYY-MM-DD.md`

```markdown
## <项目名>

**<主题>** — 一句话摘要
- 完成: 事项 1
- 完成: 事项 2
- 证据: 测试结果/commit hash/关键输出
```

**合并规则**：写入前先扫描当天文件是否已有 `## <项目名>` 区块。若已有，将新内容合并到该区块（追加子主题或合并摘要）。若无，在文件末尾追加新区块。多个项目在同一天用 `## 项目名` 分隔。

### Step 5.9: 自动生命周期 Hook

本机 Claude/Codex 已安装 Stop 生命周期 hook：`agent-kit/hooks/checkpoint-agentmemory-stop.ps1`。

- 触发时机：会话 Stop / turn 结束。
- 写入内容：git root、分支、HEAD、dirty count、upstream ahead/behind、最近提交标题。
- 安全口径：只写 metadata，不读取、不打印、不同步 secret payload。
- 失败策略：服务不可达或非 Git 目录时退出 0，不阻断会话。

### Step 6: Secret Gate

```bash
git ls-files | grep -iE '(^|[/._-])(\.env|secret|secrets|token|tokens|password|passwd|credential|credentials|auth|api[_-]?key|private[_-]?key|key)([/._-]|$)|\.(key|pem|p12)$|config\.json$' | grep -v -iE "(README|example|template|test|mock|fixture|allowlist|policy|policies|payload-policy|reference)"
```

命中候选 secret payload 时:
- 若路径精确匹配 `agent-kit/secrets/allowlist.yaml` 中 `classification: tracked-exception` 且 `risk_acceptance: user-approved` 的条目 → 允许继续, 但报告只写路径和 "tracked exception approved", 不读取/打印内容。
- 否则 **停止 checkpoint**，提示 remove-from-index / 轮换。
- 若命中的是 policy / allowlist / secret-reference 文档, 必须人工确认它不含真实值后才允许继续。

同时扫描新增文件内容：
```bash
git diff --cached --name-only | xargs git diff --cached | grep -iE "api[_-]?key|token|secret|password|credential" | head -20
```

### Step 6.1: Governance lint

在 `Jeff1993` 根目录执行：

```bash
python3 scripts/governance_lint.py
```

- 若出现 `ERROR:` → 中止 checkpoint，先修复 `.project-status.yaml` 的 `relations` 或 `docs/contracts/*`。
- 若只有 `WARN:` → 可继续 checkpoint，在 `progress.md` 记录告警原因。

### Step 6.5: Onboarding 健康检查 (新增, 条件)

若项目根存在 `docs/onboarding/`:

```bash
python3 scripts/check_onboarding.py
```

处理输出:
- **FAIL** 项 → 模型自动起草修复:
  - `codemap_missing_role`: 读对应文件首末, 写一句话职责, Edit CODEMAP.md 替换 `<待填>`
  - `module_card_missing`: 读对应大文件, 按 module-card 模板起草, 写到 `docs/onboarding/module-cards/<stem>.md`
  - `adr_index_stale`: 跑 `python3 scripts/check_onboarding.py --rebuild-index`
  - `bootstrap_jump_dead`: 不自动改 (BOOTSTRAP 是用户手写), 仅在提交前提示用户
- **WARN** 项 → 仅展示, 不阻断也不自动改

所有自动起草必须 diff 给用户预览, 用户 y 后纳入本次 commit。
用户 n → 不应用, 但 onboarding/ 健康问题保留到下一次 checkpoint。

### Step 7: Git Commit

```bash
git add -A
git commit -m "[CHECKPOINT] <简短描述>

- <改动1>
- <改动2>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 7.1: Jeff1993 文档仓 Commit (条件)

若项目代码仓 ≠ Jeff1993 文档仓（外部项目如 wechat-macro-kb），handoff/plan/progress 写入了
`~/Documents/Jeff1993/<project>/` 但 Step 7 只 commit 了代码仓。此步补提文档仓的变更。

```bash
JEFF_DIR="$HOME/Documents/Jeff1993"
CURR_GIT_ROOT=$(git -C "$(pwd)" rev-parse --show-toplevel 2>/dev/null)

if [ "$CURR_GIT_ROOT" != "$JEFF_DIR" ]; then
    pushd "$JEFF_DIR" > /dev/null
    git add .
    if ! git diff --cached --quiet; then
        git commit -m "[CHECKPOINT] docs: handoff + plan + progress 更新

Co-Authored-By: Claude <noreply@anthropic.com>"
        echo "✓ Jeff1993 文档仓 commit 完成"
    else
        echo "✓ Jeff1993 文档仓无新改动, 跳过 commit"
    fi
    popd > /dev/null
else
    echo "ℹ️ 项目即 Jeff1993 仓, 文档已在 Step 7 提交"
fi
```

### Step 7.5: Git Push (双仓)

**重要**: checkpoint 涉及两个独立 Git 仓库, 必须都 push, 否则跨设备同步失效。

#### 7.5.1 项目代码仓 push (当前 cwd)

```bash
# 检查是否有 origin
if git remote get-url origin >/dev/null 2>&1; then
    # 检查是否落后远程 (需要先 pull)
    git fetch origin
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/$(git branch --show-current) 2>/dev/null || echo "")
    BASE=$(git merge-base HEAD origin/$(git branch --show-current) 2>/dev/null || echo "")

    if [ -z "$REMOTE" ]; then
        # 新分支无 upstream, 第一次 push
        git push -u origin HEAD
        echo "✓ 项目仓新分支 push 成功 (已设 upstream)"
    elif [ "$LOCAL" = "$REMOTE" ]; then
        echo "✓ 项目仓已与 origin 同步"
    elif [ "$REMOTE" = "$BASE" ]; then
        # 本地领先, 直接 push
        git push origin $(git branch --show-current)
        echo "✓ 项目仓 push 成功"
    elif [ "$LOCAL" = "$BASE" ]; then
        echo "⚠️ 项目仓落后远程, 需要先 pull / rebase, 暂不 push"
    else
        echo "⚠️ 项目仓与远程分叉, 需要手动处理"
    fi
else
    echo "ℹ️ 项目仓无 origin, 跳过 push"
fi
```

#### 7.5.2 Jeff1993 文档仓 push

若项目代码仓与 Jeff1993 文档仓相同（如 MAPM、agent-kit），7.5.1 已经 push，此步跳过，避免重复。

```bash
JEFF_DIR="$HOME/Documents/Jeff1993"
CURR_GIT_ROOT=$(git -C "$(pwd)" rev-parse --show-toplevel 2>/dev/null)

if [ "$CURR_GIT_ROOT" = "$JEFF_DIR" ]; then
    echo "ℹ️ 项目即 Jeff1993 仓, 已在 7.5.1 push, 跳过"
else
    cd ~/Documents/Jeff1993
    if [ -n "$(git log origin/main..HEAD --oneline 2>/dev/null)" ]; then
        git push origin main
        echo "✓ Jeff1993 文档仓 push 成功"
    else
        echo "✓ Jeff1993 文档仓无新提交"
    fi
fi
```

**安全约束**:
- 若 secret gate (Step 6) FAIL → 跳过 Step 7.5, 强制阻断
- 若 push 因 non-fast-forward 失败 → 不强 push, 提示用户手动 pull --rebase
- 不在主分支以外的分支自动 push (除非用户显式 --allow-non-main)

### Step 8: 更新 .project-status.yaml（条件）

仅在以下情况更新：
- 生命周期变化（规划中 → 运行中 → 已完成）
- owner 变化
- path 变化
- status 变化
- 明确迁移 `last_handoff`

否则不碰 YAML。

### Step 9: 结束清单

- [ ] plan.md 已更新
- [ ] progress/YYYY-MM.md 或 progress.md 已归档已完成内容
- [ ] handoff.md 已按 Persistent / Current Takeover / Index 刷新且保持短入口
- [ ] 旧计划/长评审/checkpoint 原文已移入 archive/** 或保留为链接
- [ ] **collab-entry.md 已同步** (MAPM 项目且全局规则变化时：版本头 + 改动记录 + 受影响段落)
- [ ] 配置/服务器/secret 引用变更已写入 `docs/runbooks/*.md`, payload 未入 Git
- [ ] **云端记忆已写入** (Memory Store: 项目状态摘要；secret 仅写引用)
- [ ] **dev-log 已写入**（全局，合并规则）
- [ ] README.md 仅在稳定信息变化时更新
- [ ] secret gate 通过
- [ ] **governance lint 通过**
- [ ] (若启用) onboarding/ 健康检查通过, FAIL 项已起草修复
- [ ] git commit 可追踪
- [ ] **项目代码仓已 push 到 origin** (若配置)
- [ ] **Jeff1993 文档仓已 push 到 origin**
</process>

<notes>
- 旧项目兼容：若存在 `HANDOFF.md` / `PROGRESS.md` 大写文件，保留它们，同时创建小写版本供新模型使用。
- 不回滚其他 Agent 的改动；冲突时先合并意图再写入。
- 高冲突文件：`collab-entry.md`、`onboarding.md`、项目 `plan/progress/handoff`、`.project-status.yaml`。
</notes>
