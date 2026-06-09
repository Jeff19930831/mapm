---
name: adr
description: >
  起草 ADR (架构决策记录) 到 docs/onboarding/decisions/。用法: /adr [<slug>]。
  模型基于当前对话上下文自动抽取候选决策, 用户确认后写入。也支持用户指定 slug 强制起草。
  当用户说"记一下这个决定"、"把刚才讨论的写成 ADR"、"adr <主题>"时触发。
argument-hint: "[<slug>]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# adr — 起草架构决策记录

把对话中讨论出的决策沉淀为可检索的 ADR 文件。

## 前置

- 当前项目根有 `docs/onboarding/decisions/` 目录 (即已启用大型项目附加层)
- 若无, 提示用户先跑 `/init-onboarding`

## Doc Lifecycle Gate

ADR 是历史原因, 不属于入口正文:

- 决策正文只写入 `docs/onboarding/decisions/NNNN-<slug>.md`。
- `handoff.md` 只保留当前影响、风险和 ADR 链接, 不复制上下文/否决方案/后果全文。
- 若决策替代旧计划或长评审, 把旧材料放到 `archive/**`, ADR 中引用。
- 若决策形成重复操作流程, 把步骤写到 `docs/runbooks/**`, ADR 只解释为什么。

## 流程

### Step 1 — 抽取候选决策

读最近 ~50 轮对话, 找符合以下任一条件的内容:

1. **关键词触发**:
   - 决定 / 确定 / 就这么做 / 选这个
   - 否决 / 改用 / 不要 X 改 Y
   - 全量做 / 不做 MVP / 最终用 X

2. **结构触发**:
   - 给出了多个候选方案 + 选择了其中一个
   - 关闭了某条之前讨论过的路径
   - 改变了一处已落地的设计

3. **若用户提供了 slug 参数**: 跳过抽取, 让用户用一两句话描述决策, 直接进 Step 2。

### Step 2 — 询问用户确认

输出格式:

```
📝 候选 ADR (NNNN — auto):
   标题: <slug>
   决定: <一句话>
   否决: <一两条>
   影响模块: [<list>]
   状态: proposed

确认? [y/改/不写]
```

NNNN 自动取 `decisions/` 中最大 ID + 1, 不足 4 位补 0。

### Step 3 — 写文件

用户 y → 按 [`templates/ADR.md.tmpl`](../../../../MAPM/onboarding-suite/templates/ADR.md.tmpl) 5 段填写:

```yaml
---
id: NNNN
date: YYYY-MM-DD              # 今日
status: proposed
modules: [foo.py, bar.py]     # 受影响文件
supersedes: []
superseded_by: null
---
```

5 段:
1. **上下文**: 当时面对的问题/约束 (从对话抽 2-3 段)
2. **决定**: 一句话结论 + 必要的范围限定
3. **否决了什么**: 列出考虑过但没选的方案 + 理由
4. **后果**: 对代码/流程/性能/兼容性的影响
5. **触发新决策的条件**: 什么情况下应该重新审视

文件名: `docs/onboarding/decisions/<NNNN>-<slug>.md`

slug 规则: 小写 kebab-case, ≤ 6 词, 去除虚词。例: `kg-tier-system`, `unify-yaml-as-sot`。

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

如需修改, 直接编辑该文件。下次 /checkpoint 会一并 commit。
```

## 多决策一次性起草

若用户说 "把刚才讨论的 3 件事都记成 ADR":
- 抽取候选返回数组
- 用 AskUserQuestion 批量确认 (3 个问题)
- 每条独立写文件, ID 递增
- 末尾批量报告

## 边界

- 不修改已有 ADR (若用户想改, 提示直接编辑文件)
- 不自动设 status=accepted, 起手都是 proposed (用户可手改)
- 若识别到决策是对旧 ADR 的覆盖 → 在新 ADR 的 frontmatter 填 supersedes: [旧 ID]
- 若用户 nack → 不写文件, 但记在 dev-log/ 当日条目 (避免下次重复识别)

## 模型行为提示

- 对话中**自然提及**决策时 (不是用户主动 `/adr`) → 主动询问 "起草 ADR 吗?"
- 用户回复"先不"→ 等用户主动叫 `/adr` 再起
- 用户回复"y"→ 进入 Step 2 流程
