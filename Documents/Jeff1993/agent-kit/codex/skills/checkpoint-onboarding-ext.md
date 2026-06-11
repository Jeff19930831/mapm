---
name: checkpoint-onboarding-ext
description: Extend checkpoint with onboarding and Doc Lifecycle Gate checks.
---

# checkpoint — Onboarding Extension (Codex)

> 在 Codex 通用 checkpoint 行为基础上, 追加大型附加层支持。
> 与 Claude `agent-kit/claude/skills/checkpoint/SKILL.md` 的 durable closeout 口径一致。
> CodeGraph 是本地开发雷达；CODEMAP 是可提交 onboarding 地图。

## Step 0 — Onboarding 刷新 (条件)

在跑 checkpoint 开始, 检查项目根是否存在 `docs/onboarding/`:

```bash
if [ -d "docs/onboarding" ]; then
  python3 scripts/refresh_codemap.py
fi
```

失败时记录 stderr 并继续, 不阻断后续步骤。

不要提交 `.codegraph/`。若本机有 CodeGraph，可在验证阶段用它查询调用链/影响面，但 checkpoint 的 durable 地图仍是 `docs/onboarding/CODEMAP.md`。

## Step 0.5 — Doc Lifecycle Gate

在写 handoff / plan 前检查入口文档是否膨胀:

- `handoff.md` 超过 150 行, 或 Current Takeover 需要滚动才能看完。
- `plan.md` 的 Completed/History 长于 Active/Next。
- 同一部署、配置、secret、环境或常驻服务问题重复出现两次以上。

处理规则:

1. handoff 只保留 Persistent Context、常驻问题雷达、Current Takeover、Next、Blockers、Verification、Index。
2. 已完成事实和验证证据写入 `progress/YYYY-MM.md` 或 `progress.md`。
3. 旧计划、长评审、历史 checkpoint 原文写入 `archive/**`。
4. 重复问题写入 `docs/runbooks/**`; handoff 只留问题名、风险和链接。
5. 若项目提供 `scripts/md_health.py` 或 `scripts/archive_md_sections.py`, 先跑:

```bash
test -f scripts/md_health.py && python3 scripts/md_health.py
test -f scripts/archive_md_sections.py && python3 scripts/archive_md_sections.py --dry-run
```

## Step 2.5 — Memory Recall

从 cloud-memory 的 agentmemory 服务拉取项目相关记忆，用作 handoff 刷新的上下文，不阻断 checkpoint。

```bash
curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<project-name> checkpoint deploy","limit":5}'

curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<project-name> blocker decision","limit":3}'
```

处理规则:
- 搜索结果只作为上下文输入，不在 handoff 中逐条复制。
- 服务不可达或无结果时记录 `memory recall: no results / service unreachable`，继续 checkpoint。

## Step 5.1 — collab-entry 同步 (MAPM 专用)

当 checkpoint 的项目是 MAPM，且本次变更影响全局协作规则时，同步更新 `collab-entry.md`:

1. 顶部版本头与 MAPM 规则版本保持一致。
2. 追加 `vX.Y 改动:` 摘要。
3. 更新受影响段落，例如同步模型、文档地图、Checkpoint 要点、Skill 清单。
4. 若 compact 入口引用发生变化，同步更新 `onboarding-compact.md`。

仅归档 MAPM 内部 `plan/progress/handoff` 且不改变全局规则时跳过。

## Step 5.5 — 长期运行知识同步 (条件)

若本次 checkpoint 涉及配置方法、服务器接入、部署、常驻服务、环境变量、secret 引用或恢复步骤:

1. 确认项目存在对应 `docs/runbooks/*.md`; 没有则按 `docs/templates/project/runbook.md` 创建。
2. 写入配置方法、服务地址/端口、恢复步骤、验证命令和 secret 引用。
3. secret 引用只允许记录名称、用途、存放位置、恢复步骤; 不得写真实值、私钥正文、token、cookie、auth cache。
4. 若是大项目, 确认 `.project-status.yaml:sync.include` 覆盖 `docs/runbooks/**/*.md` 和 `.env.example` / `config*.example.*`。
5. 在 `progress.md` 追加 `[RUNBOOK]` 或 `[SECRET-REF]` 记录, 包含验证证据和不含值的恢复入口。

此步不得读取或打印真实 secret payload。发现疑似 payload 文件时先用 `git ls-files -- <path>` 判断是否 tracked, 不要打开内容。

## Step 5.7 — Memory Store

将 checkpoint 后的项目状态写入 cloud-memory，供跨设备/跨 session Agent 搜索。

默认安全口径:
- 每次 checkpoint 必写项目状态摘要。
- secret 默认只写引用：名称、用途、存放位置、恢复步骤、runbook 路径，不写真实值。
- 真实 secret payload 只有在服务认证、HTTPS、allowlist 和用户明确授权同时满足时，才允许另行登记。

```bash
curl -s -X POST http://43.133.86.33:3111/agentmemory/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[<project-name>] <当前目标一句话>. 最近完成: <最近完成的3条>. 下一步: <最重要的1-2条>. 阻塞: <有则写, 无则写无>. Checkpoint: <YYYY-MM-DD>.",
    "scope": "project:<project-name>"
  }'
```

若本次涉及凭证或服务器引用变化，只写不含真实值的引用摘要:

```bash
curl -s -X POST http://43.133.86.33:3111/agentmemory/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[<project-name>] Secret reference: <名称/用途>. 存放位置: <路径或系统>. 恢复步骤: <runbook 路径>. 不含真实值.",
    "scope": "credentials:<project-name>"
  }'
```

服务不可达时不阻断 checkpoint，在 handoff 中记录 `memory store: service unreachable`。

## Step 5.7.5 — dev-log 写入 (全局)

dev-log 是全局目录, 位于 Jeff1993 根目录下 (不是项目子目录)。

路径: `<Jeff1993根>/dev-log/YYYY-MM-DD.md`

```markdown
## <项目名>

**<主题>** — 一句话摘要
- 完成: 事项 1
- 完成: 事项 2
- 证据: 测试结果/commit hash/关键输出
```

**合并规则**: 写入前先扫描当天文件是否已有 `## <项目名>` 区块。已有则合并到该区块; 无则在末尾追加。

## Step 5.8 — 自动生命周期 Hook

本机 Claude/Codex 已安装 Stop 生命周期 hook：`agent-kit/hooks/checkpoint-agentmemory-stop.ps1`。

- 触发时机：会话 Stop / turn 结束。
- 写入内容：git root、分支、HEAD、dirty count、upstream ahead/behind、最近提交标题。
- 安全口径：只写 metadata，不读取、不打印、不同步 secret payload。
- 失败策略：服务不可达或非 Git 目录时退出 0，不阻断会话。

## Step 6 — Secret Gate 补充

- `.env.example`、`config*.example.*`、secret-reference / allowlist 文档可以进入 Git, 但必须脱敏。
- 真实 `.env`、`*.key`、私钥、token、cookie、credential、auth cache 默认高风险；按当前私有仓策略可警告放行，但必须只打印路径、不打印值。
- Secret gate 应按路径片段/扩展名匹配, 避免把普通词（如 `Turkey.md`）误判为 `key`。
- 若 `git ls-files` 命中疑似 secret payload, 列清单提醒；是否阻断由项目策略决定。
- 报告只写路径和批准状态, 不读取/打印内容。

## Step 6.1 — Governance lint

在 Jeff1993 根目录执行:

```bash
python3 scripts/governance_lint.py
```

- `ERROR:` → 中止 checkpoint, 先修复 `.project-status.yaml` 的 `relations` 或 `docs/contracts/*`。
- `WARN:` → 可继续, 在 `progress.md` 记录告警原因。

## Step 6.5 — Onboarding 健康检查 (新增, 条件)

在 Secret gate 之后、Git commit 之前:

```bash
if [ -d "docs/onboarding" ]; then
  python3 scripts/check_onboarding.py
fi
```

处理输出:
- **FAIL** 项 → 模型自动起草修复:
  - codemap_missing_role: 填一行职责
  - module_card_missing: 起草 module-card
  - adr_index_stale: `--rebuild-index`
  - bootstrap_jump_dead: 仅提示用户
- **WARN** 项 → 展示, 不阻断

所有起草必须 diff 给用户预览, 用户 y → 纳入本次 commit。

## Step 7.1 — Jeff1993 文档仓 Commit (条件)

commit 完成后, 若项目代码仓 ≠ Jeff1993 文档仓, 补提文档仓变更（handoff/plan/progress）:

```bash
JEFF_DIR="$HOME/Documents/Jeff1993"
CURR_GIT_ROOT=$(git -C "$(pwd)" rev-parse --show-toplevel 2>/dev/null)

if [ "$CURR_GIT_ROOT" != "$JEFF_DIR" ]; then
  pushd "$JEFF_DIR" > /dev/null
  git add .
  if ! git diff --cached --quiet; then
    git commit -m "[CHECKPOINT] docs: handoff + plan + progress 更新"
    echo "✓ Jeff1993 文档仓 commit 完成"
  else
    echo "✓ Jeff1993 文档仓无新改动, 跳过 commit"
  fi
  popd > /dev/null
else
  echo "ℹ️ 项目即 Jeff1993 仓, 文档已在 Step 7 提交"
fi
```

## Step 7.5 — Git Push (双仓, 新增)

commit 完成后, 必须 push 两个仓库:

```bash
# 7.5.1 当前项目代码仓 push
if git remote get-url origin >/dev/null 2>&1; then
  git fetch origin
  CURR_BRANCH=$(git branch --show-current)
  LOCAL=$(git rev-parse HEAD)
  REMOTE=$(git rev-parse "origin/$CURR_BRANCH" 2>/dev/null || echo "")
  BASE=$(git merge-base HEAD "origin/$CURR_BRANCH" 2>/dev/null || echo "")

  if [ -z "$REMOTE" ]; then
    # 新分支无 upstream, 第一次 push
    git push -u origin HEAD && echo "✓ 项目仓新分支 push 成功 (已设 upstream)"
  elif [ "$LOCAL" = "$REMOTE" ]; then
    echo "✓ 项目仓已同步"
  elif [ "$REMOTE" = "$BASE" ]; then
    git push origin "$CURR_BRANCH" && echo "✓ 项目仓 push 成功"
  else
    echo "⚠️ 项目仓与远程分叉, 暂不 push"
  fi
fi

# 7.5.2 Jeff1993 文档仓 push (若项目即 Jeff1993 仓则跳过, 避免重复)
JEFF_DIR="$HOME/Documents/Jeff1993"
CURR_GIT_ROOT=$(git -C "$(pwd)" rev-parse --show-toplevel 2>/dev/null)

if [ "$CURR_GIT_ROOT" = "$JEFF_DIR" ]; then
  echo "ℹ️ 项目即 Jeff1993 仓, 已在 7.5.1 push, 跳过"
else
  cd ~/Documents/Jeff1993
  if [ -n "$(git log origin/main..HEAD --oneline 2>/dev/null)" ]; then
    git push origin main && echo "✓ Jeff1993 文档仓 push 成功"
  else
    echo "✓ Jeff1993 文档仓无新提交"
  fi
fi
```

安全约束:
- secret gate FAIL → 跳过 push, 阻断
- non-fast-forward → 不强 push, 提示手动 pull --rebase
- 非主分支 → 默认不自动 push (除非用户显式同意)

## 与 Claude 版本的差异
无功能差异。Codex 通过 prompt 触发 checkpoint (例: "做 checkpoint"), 自动包含本扩展。
