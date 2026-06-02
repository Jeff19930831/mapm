---
name: adr
description: 起草 ADR 架构决策记录。
---

# adr (Codex)

> 等同 Claude `/adr [<slug>]` skill。完整设计见 `agent-kit/claude/skills/adr/SKILL.md`。
> Codex 通过 prompt 触发: "把刚才的决定记成 ADR" / "adr <主题>"。

## 触发关键词
- "记一下这个决定"
- "把刚才讨论的写成 ADR"
- "adr <slug>"
- "记决策"

## 前置
- 项目根有 `docs/onboarding/decisions/` (大型附加层已启用)
- 否则提示先跑 init-onboarding

## Doc Lifecycle Gate

- ADR 是历史原因, 决策正文只写 `docs/onboarding/decisions/`。
- handoff 只保留当前影响、风险和 ADR 链接, 不复制 ADR 正文。
- 旧计划/长评审若作为背景材料, 放 `archive/**` 并由 ADR 链接。
- 决策产生的重复操作步骤写 `docs/runbooks/**`, ADR 只解释为什么。

## 流程

### Step 1 — 抽取候选决策

读最近 ~50 轮对话, 抓符合以下任一的内容:

**关键词触发**:
- 决定 / 确定 / 就这么做 / 选这个
- 否决 / 改用 / 不要 X 改 Y
- 全量做 / 不做 MVP / 最终用 X

**结构触发**:
- 给出了多个候选方案 + 选择了其中一个
- 关闭了某条之前讨论过的路径
- 改变了一处已落地的设计

### Step 2 — 询问确认

输出:
```
📝 候选 ADR (NNNN — auto):
   标题: <slug>
   决定: <一句话>
   否决: <一两条>
   影响模块: [<list>]
   状态: proposed

确认? [y/改/不写]
```

NNNN = `decisions/` 中最大 ID + 1, 补 0 到 4 位。

### Step 3 — 写文件

按 `~/Documents/Jeff1993/MAPM/onboarding-suite/templates/ADR.md.tmpl` 5 段填写:
1. 上下文 — 当时的问题/约束
2. 决定 — 一句话结论
3. 否决了什么 — 列出考虑过但没选的 + 理由
4. 后果 — 对代码/流程/性能/兼容性的影响
5. 触发新决策的条件 — 什么情况下重新审视

frontmatter:
```yaml
---
id: NNNN
date: YYYY-MM-DD
status: proposed
modules: [foo.py, bar.py]
supersedes: []
superseded_by: null
---
```

文件名: `docs/onboarding/decisions/<NNNN>-<slug>.md`
slug: 小写 kebab-case, ≤ 6 词

### Step 4 — 重生 INDEX
```bash
python3 scripts/check_onboarding.py --rebuild-index
```

### Step 5 — 报告

```
✓ ADR-NNNN 已写入 docs/onboarding/decisions/NNNN-<slug>.md
  影响模块: [...]
  INDEX 已重生
  handoff 如需更新, 只加当前影响和 ADR 链接
```

## 边界
- 不修改已有 ADR (提示用户直接编辑)
- status 起手都是 proposed
- 若是覆盖旧 ADR, 填 supersedes: [旧 ID]
- 用户 nack → 不写文件, 但在 dev-log 当日条目留痕

## 模型行为
- 对话中自然提及决策时主动询问 (不必等用户 `/adr`)
- 用户"先不"→ 等下次主动叫
