---
name: init-onboarding
description: >
  一次性初始化项目的 onboarding 文档体系。自动判定 small/large 项目, 大项目时生成 docs/onboarding/ 全套
  (BOOTSTRAP/CODEMAP/module-cards/decisions), 模型起草后批量交给用户审。用法: /init-onboarding [--small|--large|--upgrade]
  当用户说"初始化 onboarding"、"接入大型项目附加层"、"给项目搭骨架"时触发。
argument-hint: "[--small|--large|--upgrade|--threshold-loc=N --threshold-files=N]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# init-onboarding — 项目接力骨架一次性初始化

按"大型项目附加层"规约 (见 [MAPM/onboarding-suite/docs/design.md](../../../../MAPM/onboarding-suite/docs/design.md)) 给当前项目搭骨架。

## 前置

- 当前工作目录是项目代码根 (含 git)
- 项目已注册在 `~/Documents/Jeff1993/.project-status.yaml`

## Doc Lifecycle Gate

初始化或升级时必须把文档职责立住:

- `handoff.md`: Persistent Context / 常驻问题雷达 / Current Takeover / Index, 只回答"现在怎么接手"。
- `plan.md`: Active / Next / Archived Plans, 不保留长 Completed 历史。
- `progress.md` 或 `progress/YYYY-MM.md`: 已完成事实和验证证据。
- `archive/**`: 旧计划、长评审、历史 checkpoint 原文。
- `docs/runbooks/**`: 反复出现的部署、配置、secret 引用、恢复步骤。

BOOTSTRAP 只做场景跳转和静态入口, 不复制 progress/archive/ADR 正文。

## 流程

### Step 1 — 模式判定

读 flag 或自动判定:

```bash
# 收集规模数据
LOC=$(find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) \
      -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/var/*" \
      | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')

SRC_FILES=$(find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) \
            -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/var/*" \
            | wc -l)
```

判定规则:
- `--small` → 强制 small
- `--large` → 强制 large
- `--upgrade` → 从 small 升级 (保留四文档, 新增 onboarding/)
- 自动:
  - `LOC >= 10000 OR SRC_FILES >= 20` → large
  - `7000 <= LOC < 10000 OR 15 <= SRC_FILES < 20` → 用 AskUserQuestion 弹问
  - 否则 → small

阈值可通过 `--threshold-loc=N --threshold-files=N` 覆盖。

### Step 2 — Small 模式

只做四文档基线检查:
1. 检查 README.md / plan.md / progress.md / handoff.md 是否齐全
2. 缺什么从 `~/Documents/Jeff1993/docs/templates/project/` 复制
3. 模型基于 README + 已有代码 起草:
   - README 一句话定位
   - handoff.md Persistent / Current Takeover / Index 初稿
   - plan.md Active / Next / Archived Plans 初稿
4. 输出 "✓ Small 模式初始化完成" + 一句"如项目规模长起来, 用 `/init-onboarding --upgrade` 升级"
5. 结束

### Step 3 — Large 模式

#### 3.1 拷模板与脚本
```bash
SUITE=~/Documents/Jeff1993/MAPM/onboarding-suite

mkdir -p docs/onboarding/module-cards docs/onboarding/decisions scripts

# 拷脚本 (若已存在则跳过)
[ ! -f scripts/refresh_codemap.py ] && cp "$SUITE/scripts/refresh_codemap.py" scripts/
[ ! -f scripts/check_onboarding.py ] && cp "$SUITE/scripts/check_onboarding.py" scripts/
chmod +x scripts/refresh_codemap.py scripts/check_onboarding.py

# 拷 codemap 配置 (若已存在则跳过)
[ ! -f docs/onboarding/codemap.yaml ] && cp "$SUITE/templates/codemap.yaml.tmpl" docs/onboarding/codemap.yaml
```

#### 3.2 跑 refresh_codemap 生成首版 CODEMAP
```bash
python3 scripts/refresh_codemap.py
```
此时 CODEMAP.md 的"一行职责"列全是 `<待填>`。

#### 3.3 模型填职责行 (核心一步)
对每个待填文件:
- Read 文件首 50 行 + 末 30 行
- 抽取主要 class / def + docstring
- 用一句话 (≤ 30 字) 写"对外做什么"

填完后写回 CODEMAP.md 表格 (替换 `<待填>` 为实际职责)。

**批量策略**: 每填完 10 个文件给用户一次预览, 用户 y/改/skip。

#### 3.4 起草大模块 module-cards
读 CODEMAP "大模块详情" 列出的 LOC > 1000 文件清单。对每个文件:
- Read 完整文件 (若 > 2000 行, 分多次读取关键段)
- 按 `templates/module-card.md.tmpl` 5 段填空:
  - 责任 / 不负责什么 / 核心数据流 / 已知陷阱 / 相关 ADR
- 写到 `docs/onboarding/module-cards/<filename>.md`

每张 card 起草后单独 diff 给用户审。

#### 3.5 起草初始 ADR
- 读 plan.md / progress.md 找出近期"决策类"陈述 (例: "决定用 X 不用 Y")
- 读 dev-log/ 近 1 个月文件找决策痕迹
- 起草 3-10 条 ADR, 编号从 0001 开始
- 每条按 `templates/ADR.md.tmpl` 5 段写
- 批量交用户审

#### 3.6 起草 BOOTSTRAP.md
基于以上所有产物 + 当前 handoff/plan:
- 一句话定位 (从 README)
- 当前焦点 (从 plan.md Active 区)
- 场景跳转表 (从 module-cards + ADR 反推)
- 全局约束 (从 progress.md / CLAUDE.md / AGENTS.md 提炼)
- 模型行为约定 (从模板复制, 项目特定关键词追加)
- Doc Lifecycle Gate (从模板复制, 强化入口短/历史归档/runbook 化)

按 `templates/BOOTSTRAP.md.tmpl` 模板填, 写到 `docs/onboarding/BOOTSTRAP.md`。

**强提醒用户**: "BOOTSTRAP 是你唯一手写的文件, 请仔细审 + 改场景跳转表"。

#### 3.7 重生 ADR INDEX
```bash
python3 scripts/check_onboarding.py --rebuild-index
```

#### 3.8 最后健康检查
```bash
python3 scripts/check_onboarding.py
```
报告所有项, 若有 FAIL 项, 立即起草修复再让用户确认。

#### 3.9 (可选) 安装 pre-commit hook
弹问用户是否启用 pre-commit hook。若同意:
```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
python3 scripts/check_onboarding.py
EOF
chmod +x .git/hooks/pre-commit
```

### Step 4 — Upgrade 模式

仅在已存在四文档但无 `docs/onboarding/` 时跑:
- 跳过 Step 2 的四文档复制
- 走 Step 3 全部, 但 BOOTSTRAP 起草时多注入 "升级自 small 模式" 的提示

### Step 5 — 收尾报告

```
╔══════════════════════════════════════╗
║  /init-onboarding 完成 — <项目名>
╚══════════════════════════════════════╝

模式: <small | large | upgrade>
规模: <LOC> LOC / <N> src 文件

新增文件 (⚠️ 全部 untracked, 未进 Git):
  ✓ docs/onboarding/BOOTSTRAP.md (you must review)
  ✓ docs/onboarding/CODEMAP.md (<N> entries)
  ✓ docs/onboarding/module-cards/ (<M> cards)
  ✓ docs/onboarding/decisions/ (<K> ADRs + INDEX.md)
  ✓ scripts/refresh_codemap.py
  ✓ scripts/check_onboarding.py

⚠️ 持久化风险警告 ⚠️
这些文件当前是 untracked 状态。以下情况会导致全部丢失:
  - 切换分支 + `git clean -fd` (worktree 工作流常见)
  - 跨设备同步 (代码仓不被 Obsidian Sync 覆盖)
  - 任何清理 untracked 的脚本

下一步 (强烈推荐立即按顺序执行):
  1. 审 docs/onboarding/BOOTSTRAP.md 并按需修改场景跳转表
  2. **立即跑 /checkpoint** 把全部产物纳入 Git + push 到 origin
     (这一步不可跳过 — 否则风险窗口持续到下次手动 commit)
  3. 下次新 session 用 /con-dev +<项目> 验证启动 token ≤ 5KB
```

### Step 6 — 主动提示 commit (新增, 强制)

报告输出后, 必须主动询问用户:

> "这些文件还未进 Git。要现在立即跑 `/checkpoint` 把它们纳入版本控制并 push 到 origin 吗？(强烈建议 y)"

- 用户 y → **模型直接继续执行 checkpoint 步骤**（git add → secret gate → git commit → git push 双仓），无需用户重新输入命令
- 用户 n → 在末尾输出红色警告: "⚠️ Onboarding 文件未进 Git, 切换分支或 git clean 会丢失。请尽快手动跑 /checkpoint。"

不要默默退出, 必须显式追问一次。

## 异常处理

- 项目不在 git 仓库 → 提示用户 `git init` 后重跑
- 已存在 `docs/onboarding/` → 用 AskUserQuestion 弹问是否覆盖
- 用户中途 nack 某个起草 → 跳过, 在末尾汇总未完成项
- check_onboarding 在 step 3.8 仍有 FAIL → 不阻断, 但报告中明确列出

## 注意事项

- **不直接 commit**: skill 跑完后所有产物只是落盘, 由用户决定何时 commit (或下次 `/checkpoint`)
- **不安装系统级 hook**: pre-commit 是本项目级
- **批量过审**: 模型一次性出 10 个起草项, 用户批量 y/改, 不强求逐条 review
