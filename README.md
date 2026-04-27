# MAPM — Multi-Agent Project Manager

## 项目概述

MAPM 是一个轻量级的基于文件的多设备、多 Agent 协调系统。解决开发者在多台设备上使用多个 AI 编码助手（Claude / Kimi / Codex）时的状态同步和可见性问题。

## 功能表

| 功能 | 状态 | 说明 |
|------|------|------|
| 每设备独立 YAML 状态 | ✅ 已完成 | `status/{device}.yaml`，零 Git 冲突 |
| 追加式事件日志 | ✅ 已完成 | `events/{device}.log`，合并零冲突 |
| 全局状态查看器 | ✅ 已完成 | `status/view.sh`，文本表格输出 |
| 任务跟踪 | ✅ 已完成 | `TODO.md`，Markdown 格式 |
| Agent 协议文档 | ✅ 已完成 | `AGENTS.md`，Kimi + Codex 规范 |
| 自动同步脚本 | ✅ 已完成 | `auto-sync.sh`，commit/pull/push |
| API 规范模板 | ✅ 已完成 | `specs/api.yaml`，OpenAPI 3.0 |
| Claude Code Hooks | ✅ 已完成 | SessionStart / Stop / PostToolUse |
| Phase 2: Auto-Sync 测试 | ⏳ 待开始 | 双克隆验证 |
| Phase 3: Agent 协议落地 | ⏳ 待开始 | Kimi + Codex 实际接入 |
| Phase 4: Shared Spec | ⏳ 待开始 | API 变更规范 |

## 技术栈

- Shell (bash)
- YAML（状态文件）
- Git（同步机制）
- Python（Hook JSON 解析）

## 关联项目

| 项目 | 关系 | 链接 |
|------|------|------|
| wechat-ai-daily | 管理对象 | [GitHub](https://github.com/Jeff19930831/wechat-ai-daily) |
| procurement-charts | 管理对象 | [GitHub](https://github.com/Jeff19930831/procurement-charts) |
| wechat-chat-history | 管理对象 | 规划中 |

## 代码仓库

- GitHub：[github.com/Jeff19930831/mapm](https://github.com/Jeff19930831/mapm)
- 本地：`C:\Users\lk`（用户主目录，通过 `.gitignore` 精确控制跟踪范围）

## 文档位置

- 知识库：`Win_Claude_Work\`
- 规范文档：`Win_Claude_Work\项目规范.md`
- 管理总览：`Win_Claude_Work\项目管理.md`

## 核心文件

| 文件 | 作用 |
|------|------|
| `status/view.sh` | 扫描所有设备状态，输出表格 |
| `auto-sync.sh` | 自动 commit、pull（rebase）、push，处理冲突 |
| `AGENTS.md` | Kimi + Codex 的 Agent 协议 |
| `specs/api.yaml` | OpenAPI 3.0 规范模板 |
| `TODO.md` | 全局任务跟踪 |
| `CLAUDE.md` | Claude 专属指令 |

## 目录结构

```
C:\Users\lk\
├── status\              # 设备状态文件
│   ├── win-desktop.yaml
│   └── view.sh          # 状态查看器
├── events\              # 事件日志
│   └── win-desktop.log
├── specs\               # API 规范
│   └── api.yaml
├── .planning\           # GSD 规划
│   ├── PROJECT.md
│   ├── REQUIREMENTS.md
│   ├── ROADMAP.md
│   └── STATE.md
├── AGENTS.md            # Agent 协议
├── auto-sync.sh         # 自动同步脚本
├── TODO.md              # 任务跟踪
├── CLAUDE.md            # Claude 指令
└── .gitignore           # 仅跟踪 MAPM 文件
```

## 使用方式

```bash
# 查看全局状态
bash status/view.sh

# 手动同步
bash auto-sync.sh

# 查看任务
cat TODO.md
```

## 配置

| 配置项 | 位置 | 说明 |
|--------|------|------|
| Claude Code Settings | `C:\Users\lk\.claude\settings.json` | Hooks、环境变量 |
| Git Identity | 全局 | `lk@example.com` / `lk` |
| GitHub CLI | `C:\Program Files\GitHub CLI\gh.exe` | 脚本自动检测路径 |

## 维护者

- 创建者：lk
- 创建日期：2026-04-24
- 当前阶段：Phase 1 完成
- 负责人：claude（win-desktop）
