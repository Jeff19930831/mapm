---
name: init-onboarding
description: 一次性初始化项目的 onboarding 文档体系。
---

# init-onboarding (Codex)

> 等同 Claude `/init-onboarding` skill。Codex 没有 slash 命令, 通过 prompt 触发: "跑 init-onboarding"。
> 完整设计见 `agent-kit/claude/skills/init-onboarding/SKILL.md`。

## 触发关键词
- "初始化 onboarding"
- "接入大型项目附加层"
- "给项目搭骨架"
- "init onboarding"

## 前置
- 当前工作目录是项目代码根 (含 git)
- 项目已注册在 `~/Documents/Jeff1993/.project-status.yaml`

## Doc Lifecycle Gate

初始化/升级必须建立文档边界:

- `handoff.md`: Persistent / Current Takeover / Index, 只回答"现在怎么接手"。
- `plan.md`: Active / Next / Archived Plans, 不写长 Completed 历史。
- `progress.md` 或 `progress/YYYY-MM.md`: 已完成事实和验证证据。
- `archive/**`: 旧计划、长评审、历史 checkpoint 原文。
- `docs/runbooks/**`: 重复出现的部署、配置、secret 引用、恢复步骤。
- BOOTSTRAP 只做静态入口和跳转表, 不复制历史正文。

## 流程

### Step 1 — 模式判定

```bash
LOC=$(find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) \
      -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/var/*" \
      | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')

SRC_FILES=$(find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) \
            -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/var/*" \
            | wc -l)
```

| 条件 | 模式 |
|---|---|
| LOC >= 10000 OR SRC_FILES >= 20 | large |
| 7000 <= LOC < 10000 OR 15 <= SRC_FILES < 20 | 问用户 |
| 其他 | small |

用户用 flag (`--small / --large / --upgrade / --threshold-loc=N --threshold-files=N`) 时优先 flag。

### Step 2 — Small 模式
检查/补齐四文档 (README/plan/progress/handoff), 不创建 onboarding/。同时把 handoff 初始化为 Persistent / Current Takeover / Index, 把 plan 初始化为 Active / Next / Archived Plans。

### Step 3 — Large 模式

```bash
SUITE=~/Documents/Jeff1993/MAPM/onboarding-suite

mkdir -p docs/onboarding/module-cards docs/onboarding/decisions scripts
[ ! -f scripts/refresh_codemap.py ] && cp "$SUITE/scripts/refresh_codemap.py" scripts/
[ ! -f scripts/check_onboarding.py ] && cp "$SUITE/scripts/check_onboarding.py" scripts/
chmod +x scripts/refresh_codemap.py scripts/check_onboarding.py
[ ! -f docs/onboarding/codemap.yaml ] && cp "$SUITE/templates/codemap.yaml.tmpl" docs/onboarding/codemap.yaml

python3 scripts/refresh_codemap.py
```

然后:
1. 对 CODEMAP `<待填>` 文件填一行职责 (读首末 50/30 行)
2. 对 LOC > 1000 文件起草 module-card (5 段模板)
3. 读 plan/progress/dev-log 起草 3-10 条初始 ADR
4. 基于以上产物起草 BOOTSTRAP.md (强提醒用户审 + 改场景跳转表 + Doc Lifecycle Gate)
5. `python3 scripts/check_onboarding.py --rebuild-index`
6. `python3 scripts/check_onboarding.py` 最后体检, FAIL 项立即修

### Step 4 — Upgrade
仅在四文档存在但 `docs/onboarding/` 不存在时跑 large 流程, BOOTSTRAP 加"升级自 small"提示。

### Step 5 — 报告
列出所有新增文件 (含 ⚠️ 全部 untracked 标记) + 持久化风险警告 + 下一步建议:
1. 审 BOOTSTRAP 并改场景跳转表
2. **立即跑 checkpoint** 把产物纳入 Git + push (不可跳过)
3. 下次 con-dev 验证 token ≤ 5KB

### Step 6 — 主动提示 commit (强制)
报告后必须显式追问: "这些文件还未进 Git, 切换分支或 git clean 会丢失。要现在立即 checkpoint 吗？(强烈建议 y)"
- 用户 y → **模型直接继续执行 checkpoint 步骤**（git add → secret gate → git commit → git push 双仓），无需用户重新输入命令
- 用户 n → 输出红色警告标明风险窗口持续到下次手动 commit

## 边界
- 不直接 commit (用户决定时机, 但必须显式追问一次)
- 不安装系统级 hook
- 批量交付, 不逐文件 review
