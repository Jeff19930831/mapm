# CLAUDE.md — Claude Code 全局项目规范

> 所有项目必须遵守本规范。每次启动新项目前，先阅读本文件。
> **完整规范**: `C:\Users\lk\Documents\Jeff1993\项目规范.md`

---

## 零、我是谁

- **Agent**: win-claude-work（Claude on Win_Work）
- **层 YAML**: `C:\Users\lk\Documents\Jeff1993\Win_Claude_Work\.project-status.yaml`
- **General YAML**: `C:\Users\lk\Documents\Jeff1993\.project-status.yaml`

### 写入规则

- **状态变更** → 同时写入层 YAML + General YAML
- **日常推进** → 只更新项目的 README.md / PROGRESS.md / HANDOFF.md（3 个必备文件）
- **YAML 变更后** → `python "C:\Users\lk\.claude\scripts\update-dashboard.py" && python "C:\Users\lk\.claude\scripts\update-overview.py"`

---

## 一、核心分层与路径映射

### 三层事实源

| 事实源 | 文件 | 记录什么 |
|--------|------|---------|
| 项目生命周期 | `.project-status.yaml` | 项目处于规划中/运行中/已完成/维护中/已归档 |
| 项目进展 | `PROGRESS.md` | 每轮工作完成了什么、还剩什么、哪里阻塞 |
| 接力状态 | `HANDOFF.md` | 下一个 Agent 做什么、如何验证 |

### 多设备路径映射

```yaml
roots:
  mac_codex: /Users/apple/Documents/Jeff1993/MacCodex
  mac_claude: /Users/apple/Documents/Jeff1993/MacClaude
  win_claude_work: C:\Users\lk\Documents\Jeff1993\Win_Claude_Work
  win_codex_work: C:\Users\lk\Documents\Jeff1993\Win_Codex_Work
  win_code: D:\ClaudeCode
```

- **Claude 文档库**：`C:\Users\lk\Documents\Jeff1993\Win_Claude_Work`
- **Claude 代码库**：`D:\ClaudeCode`
- **Mac Codex**：`/Users/apple/Documents/Jeff1993/MacCodex`

---

## 二、新项目初始化流程

### Step 0：检查是否已有同名项目

启动新项目前先检查：

- `项目总览.md`
- 当前设备的 `.project-status.yaml`
- 各设备目录中是否已有同名代码目录

如果已有项目，优先接续，不重复创建。

### Step 1：创建文档项目

```bash
mkdir -p "C:\Users\lk\Documents\Jeff1993\Win_Claude_Work\<项目名>"
```

生成文档（3 个必备文件）：
```
Win_Claude_Work/<项目名>/
├── README.md      ← 项目概述（按模板填写）
├── PROGRESS.md    ← 进展记录（按模板填写）
└── HANDOFF.md     ← 当前接力状态（按模板填写）
```

### Step 2：创建代码仓库（GitHub）

```bash
cd D:\ClaudeCode
mkdir <项目名> && cd <项目名>
git init -b main
gh repo create Jeff19930831/<项目名> --private --source=. --remote=origin --push
```

### Step 3：填写 README.md + PROGRESS.md + HANDOFF.md

### Step 4：注册项目到状态系统

**必须写入两处**：你的层 YAML + General YAML

```yaml
项目名:
  status: 规划中
  archive: keep
  owner: claude
  type: 项目类型
  repo: "[仓库名](https://github.com/...)"
  docs: "`Win_Claude_Work/<项目名>/`"
  code_path: "D:\\ClaudeCode\\<项目名>\\"
  last_handoff: "HANDOFF.md"
  last_update: "2026-04-29"
```

### Step 5：同步 Dashboard（状态质变时）

```bash
python "C:\Users\lk\.claude\scripts\update-dashboard.py"
python "C:\Users\lk\.claude\scripts\update-overview.py"
```

---

## 三、目录结构规范

### 代码仓库（`D:\ClaudeCode\`）

```
<项目名>/
├── README.md          # 项目概述（必须）
├── .gitignore         # Git 忽略规则
├── src/               # 源代码（必须）
├── config/            # 配置文件
├── tests/             # 测试数据/脚本
├── docs/              # 项目内部文档（可选）
└── pyproject.toml     # 依赖清单（Python 项目）
```

### 文档知识库（`Win_Claude_Work\`）

```
<项目名>/
├── README.md          # 项目概述（与代码仓库同步）
├── PROGRESS.md        # 进展记录（必须）
└── HANDOFF.md         # 当前接力状态（必须）
```

---

## 四、文档模板

### README.md 模板

```markdown
# <项目名>

## 项目概述

一句话描述项目做什么。

## 功能表

| 功能 | 状态 | 说明 |
|------|------|------|
| 功能 A | 已完成 | 描述 |
| 功能 B | 进行中 | 描述 |
| 功能 C | 待开始 | 描述 |

## 技术栈

- 语言：
- 框架：
- 关键依赖：

## 代码仓库

- GitHub：[github.com/Jeff19930831/<项目名>](url)
- 本地：`D:\ClaudeCode\<项目名>`

## 文档位置

- 知识库：`Win_Claude_Work\<项目名>`
```

### PROGRESS.md 模板

```markdown
# <项目名> — 进展记录

> 按时间倒序排列，最新的在最上面

---

## 2026-04-29 — 当前状态

### 已完成
- [x] 事项 1

### 进行中
- [ ] 事项 2

### 待办
- [ ] 事项 3

### 阻塞
- 问题 X，解决方案：
```

### HANDOFF.md 模板

```markdown
# <项目名> — 当前交接

> 给下一个 Agent / 下一台设备快速接手用。保持短、准、最新。

## 当前目标

-

## 最近完成

-

## 下一步

1.
2.
3.

## 阻塞点

- 无 / 说明阻塞、已尝试方案、需要谁决定

## 关键文件

| 文件 | 作用 | 注意事项 |
|------|------|----------|
| README.md | 项目总览 | 功能状态变化时同步 |
| PROGRESS.md | 进展记录 | 每轮工作结束更新 |

## 验证命令

```bash
# lint / test / run
```

## 当前工作区

- 分支：
- 最近提交：
- 未提交改动：
```

---

## 五、GitHub 使用规范

1. **仓库命名**：小写，短横线连接，如 `wechat-ai-daily`
2. **默认可见性**：所有新项目创建 **私有仓库** `--private`
3. **提交规范**：
   - `feat:` 新功能
   - `fix:` 修复
   - `docs:` 文档
   - `chore:` 杂项
   - `refactor:` 重构
4. **不提交**：大数据文件（>10MB）、密钥/密码/token、运行时日志/缓存

---

## 六、Agent 协作规范

### 并发编辑规则

- `README.md`、`PROGRESS.md`、`HANDOFF.md`、`.project-status.yaml` 属于高冲突文件，收尾时统一更新
- 不回滚其他 Agent 的改动；冲突时先读懂再合并

### 状态文件模板

```yaml
agent: claude
device: win-desktop
project: <项目名>
status: working | blocked | done | idle
branch: main
current_task: ""
touched_files:
  - README.md
last_update: "2026-04-29T10:30:00+08:00"
next_step: ""
blocker: ""
```

---

## 七、会话结束清单

- [ ] 代码保存
- [ ] 测试 / 验证运行
- [ ] README.md 功能表更新（如有变化）
- [ ] 更新 `PROGRESS.md`
- [ ] 更新 `HANDOFF.md`
- [ ] 如项目状态质变，更新层 YAML + General YAML + 同步 Dashboard
- [ ] `git add -A && git commit -m "..." && git push`

---

## 八、设备信息

- **Device name**: win-desktop
- **Agent**: claude
- **Status file**: `status/win-desktop.yaml`
- **文档根目录**: `C:\Users\lk\Documents\Jeff1993\Win_Claude_Work`
- **代码根目录**: `D:\ClaudeCode`

---

*Last updated: 2026-04-29 after agent-onboarding*
