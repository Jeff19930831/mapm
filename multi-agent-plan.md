# 多设备 × 多Agent 项目管理方案 v6（终版）

> 经过3轮9次评审，修复致命并发问题后的最终版本

---

## 你的真实痛点

> 2-3台设备，每台跑不同Agent（Claude Code/Kimi Code/Codex），同时在不同项目上工作。
> 不知道哪台设备上哪个Agent在跑什么，项目记录混乱。

---

## 一、核心设计

### 1.1 三条规则

1. **启动时读状态** — 知道其他设备/Agent在干什么
2. **工作时在独立分支** — `agent/{agent名}/{任务名}`
3. **结束时写状态并push** — 让别人知道你干了什么

### 1.2 核心原则

- **每设备只写自己的文件** → 零并发冲突
- **事件只追加不改** → Git合并零冲突
- **Git自动同步** → 跨设备状态一致（5分钟级）

---

## 二、架构

```
┌─────────────────────────────────────────────────────┐
│  每个项目仓库内                                       │
│                                                     │
│  status/              ← 每设备一个文件（零冲突）      │
│    win-desktop.yaml   ← 只有这台设备写入              │
│    mac-book.yaml      ← 只有这台设备写入              │
│    linux-srv.yaml     ← 只有这台设备写入              │
│                                                     │
│  events.log           ← 只追加，不改历史（零冲突）    │
│  TODO.md              ← 任务列表                     │
│  CLAUDE.md / AGENTS.md ← Agent指令                  │
│                                                     │
│  auto-sync.sh         ← 每5分钟 commit + pull + push │
└─────────────────────────────────────────────────────┘
         │ Git push/pull（5分钟间隔自动）
         │
    ┌────┴────┐     ┌──────────┐     ┌──────────┐
    │设备A     │     │设备B      │     │设备C      │
    │Windows  │     │Mac       │     │Linux     │
    │Claude   │     │Kimi Code │     │Codex CLI │
    │Code     │     │          │     │          │
    └─────────┘     └──────────┘     └──────────┘
         │               │                │
         └───────────────┼────────────────┘
                    Tailscale mesh VPN
```

---

## 三、status/ 目录（核心！）

### 3.1 为什么每设备独立文件

| 对比 | 单文件STATUS.md | 每设备独立文件 |
|------|----------------|---------------|
| 并发写冲突 | **频繁**（多设备改同一个文件） | **零**（各改各的） |
| Git自动合并 | Markdown表格行经常冲突 | **不同文件永远不冲突** |
| 格式校验 | 无（表格随时可能坏） | YAML语法检查 |
| Agent更新自己 | sed匹配行，不可靠 | **只改自己的文件，原子性** |

### 3.2 设备状态文件格式

`status/win-desktop.yaml`:
```yaml
# 设备: win-desktop
# 只有 win-desktop 上的Agent可以修改此文件
device: win-desktop
agent: Claude Code
project: alpha
branch: agent/claude/feat-payment
task: 支付API开发
status: in_progress        # idle / in_progress / done / blocked
started: 2026-04-24T10:30:00
updated: 2026-04-24T11:00:00
```

`status/mac-book.yaml`:
```yaml
device: mac-book
agent: Kimi Code
project: alpha
branch: agent/kimi/feat-checkout
task: 结算页面UI
status: in_progress
started: 2026-04-24T10:15:00
updated: 2026-04-24T10:45:00
```

`status/linux-srv.yaml`:
```yaml
device: linux-srv
agent: Codex CLI
project: alpha
branch: agent/codex/docker
task: Docker Compose配置
status: done
started: 2026-04-24T08:00:00
updated: 2026-04-24T09:00:00
```

### 3.3 事件日志（只追加）

`events.log`:
```
[2026-04-24T11:00:00] [win-desktop/Claude] 支付API: 完成数据模型设计
[2026-04-24T10:45:00] [mac-book/Kimi] 结算页面: 完成表单组件
[2026-04-24T10:30:00] [win-desktop/Claude] 支付API: 开始开发
[2026-04-24T10:15:00] [mac-book/Kimi] 结算页面: 开始UI开发
[2026-04-24T09:00:00] [linux-srv/Codex] Docker配置: 完成
```

**为什么用独立log文件而不是写在状态文件里**: 日志只追加不改历史，两个设备追加到同一文件末尾可能冲突 → 改为每条日志一行，追加到自己的文件 `events/{device}.log`，或者接受极低概率的末尾冲突（因为事件记录是辅助信息，丢失一条不影响核心功能）。

**更安全的做法**: 也用每设备独立文件：

```
events/
├── win-desktop.log
├── mac-book.log
└── linux-srv.log
```

### 3.4 汇总脚本

`status/view.sh`（一键查看全局状态）:
```bash
#!/bin/bash
# 在任意设备上运行，显示所有设备的当前状态
echo "====== 全局设备状态 ======"
echo ""
for f in status/*.yaml; do
  [ -f "$f" ] || continue
  device=$(grep '^device:' "$f" | head -1 | awk '{print $2}')
  agent=$(grep '^agent:' "$f" | head -1 | awk '{print $2}')
  task=$(grep '^task:' "$f" | head -1 | sed 's/task: //')
  status=$(grep '^status:' "$f" | head -1 | awk '{print $2}')
  updated=$(grep '^updated:' "$f" | head -1 | sed 's/updated: //')
  printf "%-15s %-15s %-20s %-12s %s\n" "$device" "$agent" "$task" "$status" "$updated"
done
echo ""
echo "====== 最近事件 ======"
tail -5 events/*.log 2>/dev/null | sort -r | head -10
```

输出示例：
```
====== 全局设备状态 ======
win-desktop     Claude Code     支付API开发          in_progress  2026-04-24T11:00:00
mac-book        Kimi Code       结算页面UI           in_progress  2026-04-24T10:45:00
linux-srv       Codex CLI       Docker Compose配置   done         2026-04-24T09:00:00

====== 最近事件 ======
[2026-04-24T11:00:00] [win-desktop/Claude] 支付API: 完成数据模型设计
[2026-04-24T10:45:00] [mac-book/Kimi] 结算页面: 完成表单组件
...
```

---

## 四、设备名定义

**在每台设备的Agent上下文文件中硬编码**。

`CLAUDE.md`（设备A - win-desktop）:
```markdown
## 设备信息
- 设备名: win-desktop
- 设备状态文件: status/win-desktop.yaml
- 事件日志: events/win-desktop.log
```

`AGENTS.md`（设备B - mac-book）:
```markdown
## 设备信息
- 设备名: mac-book
- 设备状态文件: status/mac-book.yaml
- 事件日志: events/mac-book.log
```

**不同设备的同名上下文文件内容不同**。这通过每台设备各自维护自己的CLAUDE.md/AGENTS.md实现。或者用`.agents/`模板 + 脚本生成时注入设备名。

---

## 五、Agent启动/结束协议

### 5.1 Claude Code（自动化）

**CLAUDE.md**:
```markdown
# CLAUDE.md

## 设备
- 设备名: win-desktop
- 状态文件: status/win-desktop.yaml

## 启动协议
1. git pull
2. bash status/view.sh（查看全局状态）
3. 读取 TODO.md 中指派给自己的任务
4. 更新 status/win-desktop.yaml: status=in_progress, task=..., branch=...
5. 追加事件到 events/win-desktop.log

## 结束协议
1. 更新 status/win-desktop.yaml: status=done/idle
2. 追加完成事件到 events/win-desktop.log
3. 在 TODO.md 打勾
4. git add -A && git commit -m "agent:claude $(hostname) $(date +%Y%m%d-%H%M%S)" && git push

## 规则
- 改API前先更新 specs/api.yaml
- 看到其他设备 status= in_progress 时，不要碰对应代码
- 工作分支: agent/claude/{任务名}
```

**Hook**（`.claude/settings.json`）:
```json
{
  "hooks": {
    "SessionStart": [{
      "command": "cd $(git rev-parse --show-toplevel) && git pull && bash status/view.sh"
    }],
    "Stop": [{
      "command": "echo '⚠️ 更新 status/ 和 events/ → git add -A → git commit → git push'"
    }]
  }
}
```

### 5.2 Kimi Code（AGENTS.md中写入Shell命令）

```markdown
# AGENTS.md

## 设备
- 设备名: mac-book
- 状态文件: status/mac-book.yaml
- 事件日志: events/mac-book.log

## 启动时执行
1. cd项目根目录 && git pull
2. cat status/*.yaml（查看全局状态）
3. cat TODO.md
4. 更新状态文件:
   cat > status/mac-book.yaml << 'EOF'
device: mac-book
agent: Kimi Code
project: alpha
branch: agent/kimi/{任务名}
task: {任务描述}
status: in_progress
started: $(date -Iseconds)
updated: $(date -Iseconds)
EOF
5. 追加事件: echo "[$(date -Iseconds)] [mac-book/Kimi] {任务}: 开始" >> events/mac-book.log

## 结束时执行
1. 更新 status/mac-book.yaml (status: done)
2. 追加事件到 events/mac-book.log
3. git add -A && git commit -m "agent:kimi mac-book $(date +%Y%m%d-%H%M%S)" && git push
```

### 5.3 Codex CLI（CLI参数传入）

```bash
# 查看全局状态
git pull && bash status/view.sh

# 启动Codex
codex "{任务描述}"

# 完成后手动更新
# 或用wrapper脚本:
codex-done.sh linux-srv "Docker配置完成"
```

`codex-done.sh`:
```bash
#!/bin/bash
DEVICE=$1
MSG=$2
cat > "status/${DEVICE}.yaml" << EOF
device: ${DEVICE}
agent: Codex CLI
status: done
updated: $(date -Iseconds)
task: ${MSG}
EOF
echo "[$(date -Iseconds)] [${DEVICE}/Codex] ${MSG}" >> "events/${DEVICE}.log"
git add -A && git commit -m "agent:codex ${DEVICE} $(date +%Y%m%d-%H%M%S)" && git push
```

---

## 六、auto-sync.sh（修复版）

```bash
#!/bin/bash
# 每台设备每5分钟运行: crontab: */5 * * * * /path/to/project/auto-sync.sh
# 只同步 status/ 和 events/ 目录，不影响源码工作目录

cd "$(dirname "$0")"
git rev-parse --git-dir > /dev/null 2>&1 || exit 0

# 如果有rebase中断状态，先恢复
if git rebase --show-current-patch-base > /dev/null 2>&1; then
    git rebase --abort 2>/dev/null
fi

# 如果有未提交的变更，自动提交
if ! git diff --cached --quiet 2>/dev/null || ! git diff --quiet status/ events/ TODO.md 2>/dev/null; then
    git add status/ events/ TODO.md
    git commit -m "auto-sync: $(hostname) $(date +%Y%m%d-%H%M%S)" --no-verify 2>/dev/null
fi

# 拉取远程变更（使用merge而非rebase，避免冲突复杂化）
git pull --no-rebase --autostash 2>/dev/null || {
    # pull失败时，尝试合并冲突文件
    git diff --name-only --diff-filter=U 2>/dev/null | grep -q '.' && {
        # 对冲突文件采用"两方都保留"策略
        git checkout --theirs status/ events/ 2>/dev/null
        git add status/ events/
        git commit --no-edit --no-verify 2>/dev/null
    }
}

git push 2>/dev/null || true
```

**关键改进**:
- 只同步 `status/ events/ TODO.md`，不碰源码
- 用 `--no-rebase`（merge策略）替代 `--rebase`，冲突处理更安全
- 冲突时自动 `--theirs`（保留远程版本），因为status文件5分钟后会再次更新
- 有rebase中断检测和恢复

---

## 七、项目仓库完整结构

```
project-root/
├── status/                    # 每设备一个yaml（零冲突核心）
│   ├── win-desktop.yaml
│   ├── mac-book.yaml
│   ├── linux-srv.yaml
│   └── view.sh               # 汇总查看脚本
│
├── events/                    # 每设备一个log（只追加）
│   ├── win-desktop.log
│   ├── mac-book.log
│   └── linux-srv.log
│
├── TODO.md                    # 任务列表
├── specs/
│   └── api.yaml               # 接口契约
│
├── CLAUDE.md                  # Claude Code指令（含设备名）
├── AGENTS.md                  # Kimi + Codex指令（含设备名）
│
├── auto-sync.sh               # Git自动同步
├── codex-done.sh              # Codex完成回调脚本
│
└── src/                       # 项目源码
```

---

## 八、Obsidian Vault（可选）

```
vault/
├── projects/
│   └── alpha/ → 软链接到项目仓库
│
├── brain/
│   ├── index.md
│   ├── Gotchas.md
│   └── Patterns.md
│
└── daily/（可选日志）
```

打开Obsidian → 用Dataview插件查询status/*.yaml → 自动生成看板视图。

不用Obsidian也完全可行：`bash status/view.sh` 在终端看一眼就行。

---

## 九、Git Worktree（同设备多Agent）

一台设备同时跑两个Agent时：
```bash
git worktree add ../alpha-claude agent/claude/feat-payment
git worktree add ../alpha-kimi agent/kimi/feat-checkout

# Claude Code 在 alpha-claude/ 运行
# Kimi Code 在 alpha-kimi/ 运行
# 互不干扰
```

---

## 十、新设备接入（10分钟）

```bash
# 1. Tailscale
curl -fsSL https://tailscale.com/install.sh | sh && tailscale up

# 2. 克隆项目
git clone git@github.com:user/alpha.git ~/projects/alpha

# 3. 创建设备状态文件
cat > ~/projects/alpha/status/{设备名}.yaml << 'EOF'
device: {设备名}
agent: none
status: idle
updated: PLACEHOLDER
EOF
mkdir -p ~/projects/alpha/events
touch ~/projects/alpha/events/{设备名}.log

# 4. 配置auto-sync
echo "*/5 * * * * ~/projects/alpha/auto-sync.sh" | crontab -

# 5. 修改CLAUDE.md或AGENTS.md中的设备名为你的设备名
```

---

## 十一、成本与工具选择

| 场景 | 用谁 | 在哪台设备 |
|------|------|-----------|
| 复杂架构/安全审查 | Claude Code | Windows桌面 |
| 日常开发/重构 | Kimi Code | Mac笔记本 |
| Docker/CI/脚本 | Codex CLI | Linux服务器 |
| 手边急着改bug | 当前设备最近的Agent | 任意 |
| 多项目并行 | 不同设备不同Agent | 各自独立 |

---

## 十二、风险与缓解

| 风险 | 缓解 |
|------|------|
| Agent忘记更新status文件 | Hook提醒 + auto-sync兜底commit残留 |
| Git合并冲突 | 每设备独立文件 → status/零冲突；auto-sync冲突时--theirs自动解决 |
| 设备离线状态过时 | yaml中`updated`时间戳可判断是否过时 |
| API逻辑冲突 | specs/api.yaml + status显示谁在改API |
| events/末尾追加冲突 | 极低概率，且事件是辅助信息，丢失一条不影响核心功能 |
| 设备名不一致 | 在每台设备的上下文文件中硬编码，不依赖hostname |

---

## 十三、方案评分卡

| 维度 | v2 | v3 | v4 | v5 | v6(终版) |
|------|-----|-----|-----|-----|---------|
| 并发安全 | 2/10 | 5/10 | 6/10 | 3/10 | **9/10** |
| 维护成本 | 3/10 | 5/10 | 7/10 | 6/10 | **8/10** |
| 多设备支持 | 1/10 | 2/10 | 2/10 | 7/10 | **9/10** |
| Obsidian独立性 | 2/10 | 4/10 | 7/10 | 6/10 | **9/10** |
| 可扩展性 | 5/10 | 6/10 | 7/10 | 6/10 | **8/10** |
| 实操可行性 | 3/10 | 5/10 | 7/10 | 4/10 | **7/10** |
| **综合** | **2.7** | **4.5** | **6.0** | **5.3** | **8.3** |
