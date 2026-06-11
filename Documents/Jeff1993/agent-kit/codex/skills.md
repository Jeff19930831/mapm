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
- CodeGraph 是本地开发雷达（`.codegraph/` 不入 Git）；CODEMAP 是 durable onboarding 地图，checkpoint/refresh-onboarding 刷新。
- 三流程边界：`session-handoff` 同机短续接；`con-dev` 冷启动接手；`checkpoint` durable 收口与 commit，push/deploy 需授权。

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

> 若 Codex 会话已能扫描 `agent-kit/claude/skills/*` 同步出的完整 `checkpoint` / `con-dev` / `session-handoff`，优先使用完整 skill；`*-onboarding-ext` 保留为旧 Codex/通用 prompt 的轻量扩展源。

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

Claude 源目录仍是完整治理 skill 的 canonical source。Codex 若能读取通用目录，也可直接使用完整 `checkpoint` / `con-dev` / `session-handoff`；若运行时只支持项目 prompt 或轻量注入，则使用 `-onboarding-ext` 扩展模式。

- `init-agent` 仅限 Claude：它安装 Claude 专用插件和 MCP 服务器，Codex 用 `AGENTS.md` + `collab-entry.md` 作为自己的初始化路径。
- `checkpoint-onboarding-ext` / `con-dev-onboarding-ext` 是轻量 delta，不重复完整 skill 的全部逻辑。

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
