# Codex Skills / Agents / Prompts

本目录存放 Codex 的自定义 skills、agents 和 prompts 配置说明。

## 配置位置

- AGENTS.md：Codex 项目级指令
- ~/.agents/skills/：跨工具通用用户级 skills 目录，默认优先安装到这里
- ~/.codex/：Codex 用户级配置
- ~/.codex/skills/：Codex 专用 fallback skills 目录；仅在当前 Codex 不扫描 `~/.agents/skills` 时同步目录式 skill

## 规则

- 首读入口：`collab-entry.md` → `onboarding.md`
- 四文档模型：README + plan + progress + handoff
- 兼容旧项目 PROGRESS.md / HANDOFF.md
- 大项目附加层 (LOC ≥ 10K 或源文件 ≥ 20)：启用 `docs/onboarding/`
- Doc Lifecycle Gate：handoff/BOOTSTRAP 只回答"现在怎么接手"；历史写 `progress/YYYY-MM.md` / `archive/**` / `decisions/**`；重复问题写 `docs/runbooks/**`

## Skills 清单 (skills/ 源文件 → 安装为目录式)

> `agent-kit/codex/skills/*.md` 是同步源/通用 Markdown。默认安装到 `~/.agents/skills/<name>/SKILL.md`；若当前 Codex 不扫描通用目录，再转成 `~/.codex/skills/<name>/SKILL.md`。不要只复制为 `~/.codex/skills/<name>.md`。

| 源文件 | 默认通用 skill | Codex fallback skill | 作用 | 触发 prompt |
|---|---|---|---|---|
| `init-onboarding.md` | `~/.agents/skills/init-onboarding/SKILL.md` | `~/.codex/skills/init-onboarding/SKILL.md` | 一次性给项目搭骨架 | "初始化 onboarding" / "接入大型项目附加层" |
| `adr.md` | `~/.agents/skills/adr/SKILL.md` | `~/.codex/skills/adr/SKILL.md` | 起草 ADR | "记一下这个决定" / "把刚才的写成 ADR" |
| `refresh-onboarding.md` | `~/.agents/skills/refresh-onboarding/SKILL.md` | `~/.codex/skills/refresh-onboarding/SKILL.md` | 中途轻量刷新 onboarding 文档 | "刷新 onboarding" / "看下 onboarding 健康" |
| `checkpoint-onboarding-ext.md` | `~/.agents/skills/checkpoint-onboarding-ext/SKILL.md` | `~/.codex/skills/checkpoint-onboarding-ext/SKILL.md` | checkpoint 时追加 onboarding 自检 | (随 checkpoint 自动触发) |
| `con-dev-onboarding-ext.md` | `~/.agents/skills/con-dev-onboarding-ext/SKILL.md` | `~/.codex/skills/con-dev-onboarding-ext/SKILL.md` | con-dev 时优先读 BOOTSTRAP.md | (随 con-dev 自动触发) |
| `session-handoff.md` | `~/.agents/skills/session-handoff/SKILL.md` | `~/.codex/skills/session-handoff/SKILL.md` | 同设备切 session 的轻量续接 | "切 session 继续" / "同设备接手" / "轻量续接" |

## 安装步骤

```bash
SRC=~/Documents/Jeff1993/agent-kit/codex/skills
DST=~/.agents/skills

for s in init-onboarding adr refresh-onboarding checkpoint-onboarding-ext con-dev-onboarding-ext session-handoff; do
  mkdir -p "$DST/$s"
  cp "$SRC/$s.md" "$DST/$s/SKILL.md"
done
```

若验证发现当前 Codex 不扫描 `~/.agents/skills`，再使用同一转换流程同步到 `~/.codex/skills`。

若源文件没有 YAML frontmatter，安装脚本必须在 `SKILL.md` 顶部补齐：

```yaml
---
name: <skill-name>
description: "<一句话说明触发场景和作用>"
---
```

验证方式：重启 Codex 后，确认会话启动提示的 Skills 列表中出现对应 skill 名称；若未出现，使用 fallback 目录 `~/.codex/skills` 后再重启验证。

## 与 Claude skills 的分工

Codex 使用 `-onboarding-ext` 扩展模式：Claude 有完整 `checkpoint`/`con-dev`/`init-agent`；Codex 只有追加 onboarding 逻辑的 `*-onboarding-ext` 伴生 skill。这是有意的——两个 Agent 有不同的工具链和插件生态。

- `init-agent` 仅限 Claude：它安装 Claude 专用插件和 MCP 服务器，Codex 用 `AGENTS.md` + `collab-entry.md` 作为自己的初始化路径。
- `checkpoint-onboarding-ext` / `con-dev-onboarding-ext` 是轻量 delta，不重复 Claude 完整 skill 的全部逻辑。

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
