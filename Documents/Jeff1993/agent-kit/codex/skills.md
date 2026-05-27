# Codex Skills / Agents / Prompts

本目录存放 Codex 的自定义 skills、agents 和 prompts 配置说明。

## 配置位置

- AGENTS.md：Codex 项目级指令
- ~/.codex/：用户级配置
- ~/.codex/skills/：用户级 skills 目录；当前 Codex 自动识别 `~/.codex/skills/<name>/SKILL.md` 目录式 skill

## 规则

- 首读入口：`collab-entry.md` → `onboarding.md`
- 四文档模型：README + plan + progress + handoff
- 兼容旧项目 PROGRESS.md / HANDOFF.md
- 大项目附加层 (LOC ≥ 10K 或源文件 ≥ 20)：启用 `docs/onboarding/`
- Doc Lifecycle Gate：handoff/BOOTSTRAP 只回答"现在怎么接手"；历史写 `progress/YYYY-MM.md` / `archive/**` / `decisions/**`；重复问题写 `docs/runbooks/**`

## Skills 清单 (skills/ 源文件 → 安装为目录式)

> `agent-kit/codex/skills/*.md` 是同步源/通用 Markdown。安装到本机 Codex 时必须转成 `~/.codex/skills/<name>/SKILL.md`；不要只复制为 `~/.codex/skills/<name>.md`。

| 源文件 | 本机目录式 skill | 作用 | 触发 prompt |
|---|---|---|---|
| `init-onboarding.md` | `~/.codex/skills/init-onboarding/SKILL.md` | 一次性给项目搭骨架 | "初始化 onboarding" / "接入大型项目附加层" |
| `adr.md` | `~/.codex/skills/adr/SKILL.md` | 起草 ADR | "记一下这个决定" / "把刚才的写成 ADR" |
| `refresh-onboarding.md` | `~/.codex/skills/refresh-onboarding/SKILL.md` | 中途轻量刷新 onboarding 文档 | "刷新 onboarding" / "看下 onboarding 健康" |
| `checkpoint-onboarding-ext.md` | `~/.codex/skills/checkpoint-onboarding-ext/SKILL.md` | checkpoint 时追加 onboarding 自检 | (随 checkpoint 自动触发) |
| `con-dev-onboarding-ext.md` | `~/.codex/skills/con-dev-onboarding-ext/SKILL.md` | con-dev 时优先读 BOOTSTRAP.md | (随 con-dev 自动触发) |

## 安装步骤

```bash
SRC=~/Documents/Jeff1993/agent-kit/codex/skills
DST=~/.codex/skills

for s in init-onboarding adr refresh-onboarding checkpoint-onboarding-ext con-dev-onboarding-ext; do
  mkdir -p "$DST/$s"
  cp "$SRC/$s.md" "$DST/$s/SKILL.md"
done
```

若源文件没有 YAML frontmatter，安装脚本必须在 `SKILL.md` 顶部补齐：

```yaml
---
name: <skill-name>
description: "<一句话说明触发场景和作用>"
---
```

验证方式：重启 Codex 后，确认会话启动提示的 Skills 列表中出现对应 skill 名称。

## AGENTS.md 注入 (大项目根目录)

在大项目根 `AGENTS.md` 末尾追加:
```markdown
## Onboarding Suite

本项目启用了 Jeff1993 onboarding suite (docs/onboarding/)。

启动协议:
1. 读 handoff.md 的 Persistent / Current Takeover / Index
2. 读 docs/onboarding/BOOTSTRAP.md (静态入口)
3. 按 BOOTSTRAP § 3 场景跳转表按需展开 module-cards/ 或 decisions/
4. 只有入口明确指向时才展开 progress/archive/runbooks
5. 不读全 CODEMAP / 不读全 ADR
6. 启动 token 预算 ≤ 5KB
```

详细设计见 [`MAPM/onboarding-suite/docs/design.md`](../../MAPM/onboarding-suite/docs/design.md)。
