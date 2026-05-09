# Claude Code 多 Provider Wrapper — 执行框架

> 基于 2026-04-28 三轮评审结论
> 性质：旁路执行框架，不修改原方案正文

---

## 一、当前状态快照

| 检查项 | 状态 |
|--------|------|
| `~/.claude/settings.json` 含 provider env | 是（ANTHROPIC_BASE_URL + ANTHROPIC_AUTH_TOKEN） |
| `~/.claude/.env.providers` | 不存在 |
| `~/.local/bin/claude-anthropic` | 不存在 |
| `~/.local/bin/claude-kimi` | 不存在 |
| `~/.local/bin/claude-glm` | 不存在 |
| `~/.local/bin` 在 PATH | 是 |

---

## 二、执行阶段总览

```
Phase 0: 紧急安全处置（P0-1, P0-2）
    │
Phase 1: 备份与清理（P0-3, P0-4）
    │
Phase 2: 创建 Secrets 文件（P1-3）
    │
Phase 3: 创建 Wrapper 脚本（P1-1, P1-2, P1-4）
    │
Phase 4: 验证与并行测试（P0-5, P1-5）
    │
Phase 5: 回归与收尾
```

---

## 三、Phase 0 — 紧急安全处置

### 步骤 0.1：轮换已暴露 Token

**动作**：在对应 provider 控制台撤销或轮换当前 token。

**当前暴露点核查**：
- [ ] `settings.json` 中的 `ANTHROPIC_AUTH_TOKEN`
- [ ] 任何历史 shell history
- [ ] 任何聊天记录或 plan 文件副本

**验收标准**：
- 旧 token 在 provider 控制台已标记为撤销/失效
- 新 token 不进入任何文档、脚本或聊天上下文

### 步骤 0.2：隔离当前 Secrets

**动作**：将当前 token 从 settings.json 中移出，暂存到本地安全位置。

```bash
# 提取当前 token（一次性，后续不再引用）
jq -r '.env.ANTHROPIC_AUTH_TOKEN' ~/.claude/settings.json

# 提取当前 base URL
jq -r '.env.ANTHROPIC_BASE_URL' ~/.claude/settings.json
```

**人工动作**：将提取的值手动填入安全位置（密码管理器），不要写入文件。

---

## 四、Phase 1 — 备份与清理

### 步骤 1.1：备份 settings.json

```bash
BACKUP="$HOME/.claude/settings.json.backup.$(date +%Y%m%d-%H%M%S)"
cp "$HOME/.claude/settings.json" "$BACKUP"
echo "Backup: $BACKUP"
```

**验收标准**：
- `ls ~/.claude/settings.json.backup.*` 存在且大小 > 0

### 步骤 1.2：验证备份可恢复

```bash
# 测试性恢复命令（不实际执行，仅记录）
# cp "$BACKUP" "$HOME/.claude/settings.json"
```

### 步骤 1.3：修剪 settings.json 中的 provider 绑定

**删除的键**（6 个）：
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_AUTH_TOKEN`
- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_MODEL`
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`
- `ANTHROPIC_DEFAULT_SONNET_MODEL`
- `ANTHROPIC_DEFAULT_OPUS_MODEL`
- `ANTHROPIC_SMALL_FAST_MODEL`

**当前实际存在的 provider 键**（从状态快照）：
- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_AUTH_TOKEN`

**操作**：从 settings.json 的 `env` 对象中移除上述键。

保留的通用 env：
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
- `API_TIMEOUT_MS`
- `PROJECTS_DIR`

**操作后验证**：
```bash
jq '.env // {} | keys' ~/.claude/settings.json
# 预期输出：不包含 ANTHROPIC_BASE_URL 和 ANTHROPIC_AUTH_TOKEN
```

---

## 五、Phase 2 — 创建 Secrets 文件

### 步骤 2.1：创建 .env.providers

```bash
cat > "$HOME/.claude/.env.providers" << 'EOF'
# Anthropic Official
ANTHROPIC_OFFICIAL_API_KEY=""

# Kimi (via Anthropic-compatible endpoint)
KIMI_AUTH_TOKEN=""
KIMI_BASE_URL="https://api.kimi.com/coding/"

# GLM (via Anthropic-compatible endpoint)
GLM_AUTH_TOKEN=""
GLM_BASE_URL=""
EOF

chmod 600 "$HOME/.claude/.env.providers"
```

**验收标准**：
```bash
ls -l "$HOME/.claude/.env.providers"
# 权限应为：-rw-------
```

### 步骤 2.2：人工填充 Token

**动作**：使用密码管理器或 provider 控制台，将新 token 填入对应变量。

**禁止**：
- 不要把 token 粘贴到聊天记录
- 不要把 token 写入任何 .md 文件
- 不要把 token 写入 wrapper 脚本

**填充后验证**：
```bash
# 确认文件不为空
test -s "$HOME/.claude/.env.providers" && echo "OK: file not empty"

# 确认不包含占位符
grep -c '<fill locally>\|YOUR_TOKEN\|REPLACE_ME' "$HOME/.claude/.env.providers" || echo "OK: no placeholders"
```

---

## 六、Phase 3 — 创建 Wrapper 脚本

### 6.1 Wrapper 设计规范

每个 wrapper 必须满足：
1. `set -euo pipefail`
2. 启动前清理所有相关 env
3. source .env.providers 前检查文件权限
4. 只注入当前 provider 需要的 env
5. 不输出 token 内容
6. 失败时给出明确错误信息

### 6.2 claude-anthropic

```bash
#!/usr/bin/env bash
set -euo pipefail

SECRETS="$HOME/.claude/.env.providers"

# 清理所有 provider 相关 env
unset ANTHROPIC_API_KEY 2>/dev/null || true
unset ANTHROPIC_AUTH_TOKEN 2>/dev/null || true
unset ANTHROPIC_BASE_URL 2>/dev/null || true
unset ANTHROPIC_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_HAIKU_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_SONNET_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_OPUS_MODEL 2>/dev/null || true
unset ANTHROPIC_SMALL_FAST_MODEL 2>/dev/null || true

# 检查 secrets 文件
if [[ ! -f "$SECRETS" ]]; then
    echo "Error: $SECRETS not found" >&2
    exit 1
fi

# 检查权限（Windows Git Bash 可能不支持 stat -c，做降级）
if command -v stat &>/dev/null; then
    PERM=$(stat -c "%a" "$SECRETS" 2>/dev/null || echo "644")
    if [[ "$PERM" != "600" ]]; then
        echo "Warning: $SECRETS permissions are $PERM, expected 600" >&2
    fi
fi

# source secrets
# shellcheck source=/dev/null
source "$SECRETS"

# 设置 Anthropic Official
if [[ -z "${ANTHROPIC_OFFICIAL_API_KEY:-}" ]]; then
    echo "Error: ANTHROPIC_OFFICIAL_API_KEY not set in $SECRETS" >&2
    exit 1
fi

export ANTHROPIC_API_KEY="$ANTHROPIC_OFFICIAL_API_KEY"

# 不设置 ANTHROPIC_BASE_URL，使用官方端点

# 启动 claude
echo "[Provider: Anthropic Official]"
claude "$@"
```

### 6.3 claude-kimi

```bash
#!/usr/bin/env bash
set -euo pipefail

SECRETS="$HOME/.claude/.env.providers"

# 清理所有 provider 相关 env
unset ANTHROPIC_API_KEY 2>/dev/null || true
unset ANTHROPIC_AUTH_TOKEN 2>/dev/null || true
unset ANTHROPIC_BASE_URL 2>/dev/null || true
unset ANTHROPIC_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_HAIKU_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_SONNET_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_OPUS_MODEL 2>/dev/null || true
unset ANTHROPIC_SMALL_FAST_MODEL 2>/dev/null || true

# 检查 secrets 文件
if [[ ! -f "$SECRETS" ]]; then
    echo "Error: $SECRETS not found" >&2
    exit 1
fi

# 检查权限
if command -v stat &>/dev/null; then
    PERM=$(stat -c "%a" "$SECRETS" 2>/dev/null || echo "644")
    if [[ "$PERM" != "600" ]]; then
        echo "Warning: $SECRETS permissions are $PERM, expected 600" >&2
    fi
fi

# source secrets
# shellcheck source=/dev/null
source "$SECRETS"

# 设置 Kimi
if [[ -z "${KIMI_AUTH_TOKEN:-}" ]]; then
    echo "Error: KIMI_AUTH_TOKEN not set in $SECRETS" >&2
    exit 1
fi

if [[ -z "${KIMI_BASE_URL:-}" ]]; then
    echo "Error: KIMI_BASE_URL not set in $SECRETS" >&2
    exit 1
fi

export ANTHROPIC_AUTH_TOKEN="$KIMI_AUTH_TOKEN"
export ANTHROPIC_BASE_URL="$KIMI_BASE_URL"

# 启动 claude
echo "[Provider: Kimi]"
claude "$@"
```

### 6.4 claude-glm

```bash
#!/usr/bin/env bash
set -euo pipefail

SECRETS="$HOME/.claude/.env.providers"

# 清理所有 provider 相关 env
unset ANTHROPIC_API_KEY 2>/dev/null || true
unset ANTHROPIC_AUTH_TOKEN 2>/dev/null || true
unset ANTHROPIC_BASE_URL 2>/dev/null || true
unset ANTHROPIC_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_HAIKU_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_SONNET_MODEL 2>/dev/null || true
unset ANTHROPIC_DEFAULT_OPUS_MODEL 2>/dev/null || true
unset ANTHROPIC_SMALL_FAST_MODEL 2>/dev/null || true

# 检查 secrets 文件
if [[ ! -f "$SECRETS" ]]; then
    echo "Error: $SECRETS not found" >&2
    exit 1
fi

# 检查权限
if command -v stat &>/dev/null; then
    PERM=$(stat -c "%a" "$SECRETS" 2>/dev/null || echo "644")
    if [[ "$PERM" != "600" ]]; then
        echo "Warning: $SECRETS permissions are $PERM, expected 600" >&2
    fi
fi

# source secrets
# shellcheck source=/dev/null
source "$SECRETS"

# 设置 GLM
if [[ -z "${GLM_AUTH_TOKEN:-}" ]]; then
    echo "Error: GLM_AUTH_TOKEN not set in $SECRETS" >&2
    exit 1
fi

if [[ -z "${GLM_BASE_URL:-}" ]]; then
    echo "Error: GLM_BASE_URL not set in $SECRETS" >&2
    exit 1
fi

export ANTHROPIC_AUTH_TOKEN="$GLM_AUTH_TOKEN"
export ANTHROPIC_BASE_URL="$GLM_BASE_URL"

# 启动 claude
echo "[Provider: GLM]"
claude "$@"
```

### 6.5 安装 Wrapper

```bash
# 创建目录（如果不存在）
mkdir -p "$HOME/.local/bin"

# 写入脚本（上面三个脚本分别写入）
# 然后赋予执行权限
chmod +x "$HOME/.local/bin/claude-anthropic"
chmod +x "$HOME/.local/bin/claude-kimi"
chmod +x "$HOME/.local/bin/claude-glm"

# 验证
command -v claude-anthropic
command -v claude-kimi
command -v claude-glm
```

---

## 七、Phase 4 — 验证与并行测试

### 7.1 单 Provider 验证清单

对每个 wrapper 执行：

```bash
# 1. 确认 wrapper 可调用
which <wrapper-name>

# 2. 确认启动时显示正确的 provider
<wrapper-name> --version 2>&1 | head -5

# 3. 确认不泄露 token
strings <wrapper-script-path> | grep -i "sk-" || echo "OK: no hardcoded token"

# 4. 确认 env 被正确设置
eval "$(<wrapper-name> --dry-run 2>/dev/null || true)"
# 或在新 shell 中检查
bash -c 'source ~/.claude/.env.providers 2>/dev/null; echo "API_KEY set: ${ANTHROPIC_API_KEY:+yes}"'
```

### 7.2 交叉污染测试

```bash
# 测试 1：从 Kimi 切换到 Anthropic
bash -c 'ANTHROPIC_AUTH_TOKEN="old-kimi-token"; ANTHROPIC_BASE_URL="https://api.kimi.com/coding/"; export ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL; claude-anthropic --version 2>&1 | head -3'
# 预期：不应使用 old-kimi-token，应连接官方端点

# 测试 2：从 GLM 切换到 Kimi
bash -c 'ANTHROPIC_AUTH_TOKEN="old-glm-token"; ANTHROPIC_BASE_URL="https://glm.example.com/"; export ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL; claude-kimi --version 2>&1 | head -3'
# 预期：不应使用 old-glm-token，应连接 Kimi 端点
```

### 7.3 三终端并行测试

开三个终端/窗口，同时执行：

```bash
# Terminal 1
claude-anthropic

# Terminal 2
claude-kimi

# Terminal 3
claude-glm
```

每个终端内发送一条短消息（如 "hello"），确认：
- 响应来自正确的 provider
- 互相不干扰
- history 不串线

### 7.4 状态检查脚本（可选 P1-5）

```bash
#!/usr/bin/env bash
# claude-provider-status

echo "=== Claude Provider Status ==="
echo ""
echo "Active env:"
echo "  ANTHROPIC_API_KEY:        ${ANTHROPIC_API_KEY:+set}"
echo "  ANTHROPIC_AUTH_TOKEN:     ${ANTHROPIC_AUTH_TOKEN:+set}"
echo "  ANTHROPIC_BASE_URL:       ${ANTHROPIC_BASE_URL:-(empty)}"
echo ""

# 判断当前 provider
if [[ -n "${ANTHROPIC_API_KEY:-}" && -z "${ANTHROPIC_BASE_URL:-}" ]]; then
    echo "Provider: Anthropic Official"
elif [[ -n "${ANTHROPIC_AUTH_TOKEN:-}" && "${ANTHROPIC_BASE_URL:-}" == *"kimi"* ]]; then
    echo "Provider: Kimi"
elif [[ -n "${ANTHROPIC_AUTH_TOKEN:-}" && "${ANTHROPIC_BASE_URL:-}" == *"glm"* ]]; then
    echo "Provider: GLM"
else
    echo "Provider: unknown or bare claude"
fi
```

---

## 八、Phase 5 — 回归与收尾

### 8.1 GLM 工作流回归

```bash
# 使用 claude-glm 启动
claude-glm

# 验证：
# - MCP 服务器正常加载
# - Plugins 正常（frontend-design, autoresearch, claude-hud）
# - Skills 正常
# - Hooks 正常触发
# - 项目目录上下文正常
```

### 8.2 回滚验证

```bash
# 测试回滚路径
cp "$HOME/.claude/settings.json.backup.XXXX" "$HOME/.claude/settings.json"
# 然后直接运行 claude，确认恢复原有 GLM 工作流
```

### 8.3 更新项目文档

更新以下文件：
- `README.md`：添加多 provider 使用说明
- `PROGRESS.md`：记录本次变更
- `HANDOFF.md`：记录 wrapper 使用方式

---

## 九、安全检查清单

### 执行前检查
- [ ] 旧 token 已在 provider 控制台撤销
- [ ] settings.json 已备份
- [ ] `.env.providers` 权限为 600
- [ ] wrapper 脚本中无硬编码 token

### 执行后检查
- [ ] `grep -R "sk-" ~/.local/bin/claude-*` 无结果
- [ ] `jq '.env // {} | keys' ~/.claude/settings.json` 无 provider 键
- [ ] `ls -l ~/.claude/.env.providers` 权限为 600
- [ ] 三个 wrapper 均可调用
- [ ] 交叉污染测试通过
- [ ] GLM 回归测试通过
- [ ] 回滚路径验证通过

---

## 十、风险与应对

| 风险 | 可能性 | 影响 | 应对 |
|------|--------|------|------|
| Token 在迁移过程中泄露 | 中 | 高 | 先轮换旧 token，新 token 不写入任何文档 |
| Claude Code 版本不识别 env | 低 | 高 | 先单 provider 测试，确认 /status 正确 |
| Windows Git Bash 权限检查失效 | 中 | 低 | wrapper 降级处理，不阻塞启动 |
| MCP/Plugin 因 env 变化失效 | 低 | 中 | 回归测试覆盖，保留回滚路径 |
| History 串线 | 低 | 低 | 先观察，出现问题再升级到 CLAUDE_CONFIG_DIR 隔离 |

---

## 十一、命令速查

```bash
# 查看当前 settings.json env 键
jq '.env // {} | keys' ~/.claude/settings.json

# 检查 wrapper 是否含硬编码 token
grep -R "sk-" ~/.local/bin/claude-* 2>/dev/null || echo "Clean"

# 检查 .env.providers 权限
ls -l ~/.claude/.env.providers

# 快速测试 wrapper
claude-anthropic --version
claude-kimi --version
claude-glm --version

# 查看当前生效的 provider 相关 env
env | grep -E "ANTHROPIC|KIMI|GLM" | grep -v "^$"

# 回滚
LATEST=$(ls -t ~/.claude/settings.json.backup.* 2>/dev/null | head -1)
cp "$LATEST" ~/.claude/settings.json
```

---

*Framework version: 2026-04-28*
*Based on review: claude-code-provider-fuzzy-quiche-review-2026-04-28*
