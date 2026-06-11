---
name: con-dev-onboarding-ext
description: Extend con-dev with BOOTSTRAP-aware onboarding reads.
---

# con-dev — Onboarding Extension (Codex)

> 在 Codex 通用 con-dev 行为基础上, Phase 3 引入 BOOTSTRAP-aware 读取。
> 与 Claude `agent-kit/claude/skills/con-dev/SKILL.md` Phase 3a 行为一致。
> con-dev 是冷启动接手：不 checkpoint、不 commit、不 push、不刷新 durable docs。

## Phase 3a — 优先走大型附加层 (BOOTSTRAP-aware)

若 `<code_path>/docs/onboarding/BOOTSTRAP.md` 存在:

1. **完整读 BOOTSTRAP.md** (≤ 3KB)
2. 找到 handoff 文件, 只读 Persistent / Current Takeover / Index
3. 读 plan.md 仅 Active 区
4. **不读全 README**, 仅前 30 行 + "运行方式 / 快速开始" 段
5. **不读 CODEMAP / module-cards / decisions** (按需展开)
6. **不读 progress/archive/runbooks 全量**；仅当 BOOTSTRAP / handoff / plan Active 明确指向时读取必要段落
7. Token 预算: ≤ 5KB

完成后跳过 Phase 3b, 进入 Phase 4。

## Phase 3.5 — CodeGraph 准备（可选）

若本机安装 CodeGraph，可在代码根执行:

```bash
codegraph --version
codegraph init -i
```

规则:
- `.codegraph/` 是本地索引，不进入 Git / sync 清单 / checkpoint payload。
- con-dev 可用 CodeGraph 查入口链路、callers/callees、blast radius。
- con-dev 不运行 `scripts/refresh_codemap.py`; CODEMAP 由 checkpoint / refresh-onboarding 维护。
- 未安装 CodeGraph 不阻断接手，报告写明 fallback 为 `rg` / CODEMAP。

## Phase 3b — 经典流程 (无附加层)

走原 con-dev 流程, 但仍遵守 Doc Lifecycle Gate: handoff 只读 Persistent / Current Takeover / Index, plan 只读 Active, README 只读定位/架构/运行段。

## Doc Lifecycle Gate

- 入口文档只回答"现在怎么接手"。
- 历史原因在 `progress*`、`archive/**`、`decisions/**`, 只有入口链接时才展开。
- 重复问题在 `docs/runbooks/**`, 只读当前任务指向的 runbook。
- con-dev 报告必须指出入口是否过长或是否需要把历史归档。

## Phase 2 补充 — 多设备路径与同步清单

在 Codex 执行 con-dev 时, 先用注册表工具解析当前设备路径, 避免只看到其他设备的 `code_path`:

```bash
python3 scripts/project_registry.py resolve <项目名>
python3 scripts/project_registry.py sync-list <项目名> --summary
```

规则:

1. `code_paths` 优先于旧 `code_path`; 按当前 `device` / `user` / `os` 匹配 active 路径。
2. `status: reference|retired|archived|disabled|remote` 只做历史提示, 不作为当前工作目录。
3. 项目条目若有 `sync`, con-dev 报告必须展示同步清单摘要和缺失的 `required` 文件。
4. 大项目如 `wechat-macro-kb` / `tradingcenter` 不再只看四文档; 以 `sync.include` 作为需要跨设备保持可见的文件集合。
5. 若 `sync` 包含 `docs/runbooks/**/*.md` 或脱敏示例配置, 报告展示 runbook / example config 数量; 但默认不读取正文。

## 长期配置与 Secret 引用

- 功能配置方法、服务器接入、恢复步骤应放项目 `docs/runbooks/*.md`。
- `.env.example` / `config*.example.*` 可以同步; 真实 `.env`、token、私钥、cookie、auth cache 不读、不打印、不提交。
- secret 只读取引用卡片: 名称、用途、存放位置、恢复步骤、验证命令; 不读取 secret payload。

## Phase 2.5 — Memory Recall（云端记忆拉取）

在 Phase 3 之前，从云端 agentmemory 搜索项目相关记忆。

**优先 MCP tool**（`mcp__agentmemory__memory_recall`），不可用时回退 curl：
```bash
curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<项目名> checkpoint deploy","limit":5}'

curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<项目名> blocker decision","limit":3}'

curl -s -X POST http://43.133.86.33:3111/agentmemory/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<项目名> credentials server","limit":3}'
```

**处理规则**：
- 搜索结果中的关键事实（最近状态变更、重要决策、凭证引用位置）纳入就绪报告
- 凭证类记忆（scope 含 credentials）只展示凭证位置、权限范围、恢复方式和 runbook 链接；不得展示真实密码/token
- MCP 和 curl 均不可达 → 不阻断，在报告中注明
- 与 handoff 矛盾时以 handoff 为准

## 与 Claude 版本的差异
无功能差异。Codex 通过 prompt 触发 (例: "继续开发 wechat-macro-kb"), 自动包含本扩展。
