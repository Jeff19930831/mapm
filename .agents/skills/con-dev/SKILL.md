---
name: con-dev
description: >
  继续在新设备上开发一个 Jeff1993 老项目。用法：/con-dev +<项目名>
  自动执行五阶段接力流程：文档同步 → 定位项目 → 读取上下文 → 环境检测 → 就绪报告。
  当用户说"继续开发 X"、"新设备上开始 X"、"接手项目 X"、"con-dev X" 时触发。
argument-hint: "<项目名>"
allowed-tools:
  - Bash
  - Read
  - Glob
---

# con-dev — 新设备继续老项目

接收 `<项目名>`，五阶段接力准备。

## Phase 1 — 文档环境同步

```bash
cd ~/Documents/Jeff1993 && git status && git pull
```

- 非 git repo → 提示 clone，**停止**
- 有未提交改动 → 提示处理，**停止**
- 合并冲突 → 提示解决，**停止**
- 记录 pull 结果供 Phase 5

## Phase 2 — 定位项目

读取 `~/Documents/Jeff1993/.project-status.yaml`，查找 `projects.<项目名>`。

- 不存在 → 列出所有项目（按状态分组），**停止**

提取字段：`status`、`owner`、`repo`、`code_path` / `code_paths`、`sync`、`last_handoff`、`docs`。

优先用注册表解析工具选择当前设备路径：

```bash
python3 scripts/project_registry.py resolve <项目名>
python3 scripts/project_registry.py sync-list <项目名> --summary
```

路径解析规则：

1. 若存在 `code_paths`，优先选 `device` / `user` / `os` 匹配当前设备的 active 记录。
2. 无匹配时选 `device: default` 或已存在的 active 路径。
3. 仍无可用路径时回退旧字段 `code_path`。
4. `status: reference|retired|archived|disabled|remote` 仅用于提示，不作为当前 clone / cd 目标。

代码仓库处理（`repo` 格式为 `[名称](URL)`，提取括号内 URL）：

| repo | code_path | 动作 |
|---|---|---|
| GitHub URL | 存在 | 跳过 |
| GitHub URL | 不存在 | `git clone <url> <code_path>` |
| GitHub URL | 当前设备无 code_path | 先根据 `repo` + 项目名给出建议路径，必要时 clone 到 `~/projects/<repo>` 或用户约定路径，并在 checkpoint 时补 `code_paths` |
| `—` 或空 | 任意 | 纯文档，跳过 |
| `内置 Git` | 存在 | 已就绪 |
| `内置 Git` | 不存在 | 提示手动同步，继续 |

若项目条目有 `sync`，Phase 5 报告中列出同步清单摘要；大型项目接力优先确认 `required` 文件齐全。
若 `sync` 包含 `docs/runbooks/**/*.md` 或脱敏示例配置，Phase 5 报告中列出 runbook / example config 数量；但默认不读取 runbook 正文，除非 handoff / BOOTSTRAP / plan Active 明确指向。

## Phase 2.5 — Memory Recall（云端记忆拉取）

从云端 agentmemory 搜索项目相关记忆，为后续读取提供跨设备上下文。

```bash
curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<项目名> status decision credentials blocker","limit":5}'
```

**处理规则**：
- 搜索结果中的关键事实（最近状态变更、重要决策、凭证引用位置）纳入 Phase 5 就绪报告的参考输入
- 若搜索返回空或服务不可达 → 不阻断 con-dev，在报告中注明 "cloud memory: no results / unreachable"
- 凭证类记忆（scope 含 `credentials`）只展示凭证位置、权限范围、恢复方式和 runbook 链接；不得展示真实密码/token
- 不在报告中逐条引用 memory，只吸收有价值的信息作为上下文补充

**与 Phase 3 的关系**：Memory Recall 是 Phase 3 的前置补充，不替代 handoff/plan 读取。当记忆中的信息与 handoff 矛盾时，以 handoff 为准（文档更新更及时）。

## Phase 3 — 读取项目上下文（精准读取）

**核心原则：只读冷启动必需内容，不读参考/历史数据。**

**Doc Lifecycle Gate**:
- 入口文档只回答"现在怎么接手"；历史原因只在入口明确链接时展开。
- handoff 只读 Persistent Context / 常驻问题雷达 / Current Takeover / Index。
- plan 只读 Active；Next 只在安排后续工作时读取；不读 Completed/History。
- progress、archive、decisions、runbooks 只在 handoff / BOOTSTRAP / plan Active 明确指向时读取。

### Phase 3a — BOOTSTRAP 模式

若 `<code_path>/docs/onboarding/BOOTSTRAP.md` 存在：

1. 读 BOOTSTRAP.md（≤ 3KB）
2. 读 handoff.md **仅 Persistent Context + Current Takeover + Index**
3. 读 plan.md **仅 ## Active 区段**（到下一个 `##` 止）
4. **不读 README**（BOOTSTRAP 已含架构）
5. **不读 CODEMAP / module-cards / decisions**（按需展开）
6. **不读所有 runbooks**；只在 BOOTSTRAP 场景跳转表或 handoff 当前任务明确引用时读取对应 `docs/runbooks/<name>.md`
7. Token 预算 ≤ 5KB

跳到 Phase 4。

### Phase 3b — 经典模式

1. **handoff.md**（resolver 优先级：`last_handoff` → `handoff.md` → `HANDOFF.md`）：
   - 读 Persistent Context + Current Takeover + Index
   - **跳过**长历史、旧完成清单、旧 checkpoint 原文

2. **plan.md**：
   - 只读 `## Active` 区段（到下一个 `##` 止）
   - 无 `## Active` → 读前 40 行
   - **不读** Completed / 历史区段；Next 只在需要排后续顺序时读

3. **README.md**：
   - 只读包含"项目目标"/"架构"/"运行"的前 2 个 `##` 段落
   - 无匹配 → 只读前 30 行
   - **不读**数据规模/指标清单/已完成工作/历史记录

4. **runbooks**：
   - 默认不读全量 `docs/runbooks/`
   - 若当前任务涉及配置、服务器、部署、密钥引用，或 handoff/plan 指向具体 runbook，则只读该 runbook 的必要段落

## Phase 4 — 环境检测

`code_path` 为 `—` 或不存在则跳过。

```bash
# 在 code_path 下检测
test -f requirements.txt && echo "HAS_REQUIREMENTS=1"
test -f pyproject.toml && echo "HAS_PYPROJECT=1"
test -d .venv && echo "HAS_VENV=1"
test -f package.json && echo "HAS_PACKAGE=1"
test -d node_modules && echo "HAS_NODE_MODULES=1"
test -f go.mod && echo "HAS_GOMOD=1"
test -f Cargo.toml && echo "HAS_CARGO=1"
```

提示规则：Python+venv ✅ | Python-venv ⚠️ `uv venv && uv pip install -r requirements.txt` | Node+modules ✅ | Node-modules ⚠️ `pnpm install` | Go+go ✅ | Go-go ⚠️ | 无文件 ℹ️

## Phase 5 — 就绪报告

输出简洁报告：项目信息（状态/owner/代码路径）+ 文档同步结果 + 代码仓库状态 + 环境检测结果 + **云端记忆摘要**（Phase 2.5 搜索到的关键事实）+ runbook/配置示例摘要 + 当前目标 + 下一步 + 阻塞。格式自定，保持紧凑。

报告末尾提示：按 plan.md Active 区开始工作，结束后执行 `/checkpoint`。若有 BOOTSTRAP，提示按 § 3 场景跳转表按需展开 module-cards/decisions/runbooks。若任务涉及 secret，只读引用卡片，不读取或打印真实值。

## 错误处理

停止条件（Git 冲突/项目不存在/非 repo）：说明原因 + 修复命令，停止后续阶段。
警告条件（依赖缺失等）：记入报告，继续。
缺失文件（handoff/plan）：提示后继续，不中断。
