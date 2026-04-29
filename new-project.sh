#!/bin/bash
# new-project.sh — MacCodex 新建项目
# 用法: bash ~/.claude/scripts/new-project.sh <项目名> [代码目录]
# 示例: bash ~/.claude/scripts/new-project.sh my-project ~/Documents/Jeff1993/MacCodex
# 规范: /Users/apple/Documents/Jeff1993/项目规范.md

set -e

PROJECT="$1"
CODE_DIR="${2:-$HOME/Documents/Jeff1993/MacCodex}"
DOCS_DIR="$CODE_DIR"
YAML_FILE="$DOCS_DIR/.project-status.yaml"
GENERAL_YAML_FILE="$HOME/Documents/Jeff1993/.project-status.yaml"

if [ -z "$PROJECT" ]; then
    echo "用法: bash ~/.claude/scripts/new-project.sh <项目名> [代码目录]"
    exit 1
fi

# 验证项目名格式 (小写、短横线)
if ! echo "$PROJECT" | grep -qE '^[a-z][a-z0-9-]+$'; then
    echo "错误: 项目名必须小写，用短横线连接，如 my-project"
    exit 1
fi

# Step 0: 检查同名项目
echo "Step 0: 检查同名项目..."
FOUND=0
if [ -d "$DOCS_DIR/$PROJECT" ]; then
    echo "  ⚠️  文档目录已存在: $DOCS_DIR/$PROJECT"
    FOUND=1
fi
if [ -d "$CODE_DIR/$PROJECT" ]; then
    echo "  ⚠️  代码目录已存在: $CODE_DIR/$PROJECT"
    FOUND=1
fi
if grep -q "^  ${PROJECT}:" "$YAML_FILE" 2>/dev/null; then
    echo "  ⚠️  YAML 中已有注册: $PROJECT"
    FOUND=1
fi
if [ "$FOUND" -eq 1 ]; then
    echo "  → 同名项目已存在，优先接续，不重复创建"
    echo ""
fi

# Step 1: 创建项目目录与文档
DOCS_PATH="$DOCS_DIR/$PROJECT"
if [ ! -d "$DOCS_PATH" ]; then
    mkdir -p "$DOCS_PATH"
    echo "✅ Step 1: 文档目录已创建: $DOCS_PATH"
else
    echo "✅ Step 1: 文档目录已存在，跳过"
fi

TODAY=$(date +%Y-%m-%d)

# 生成 README.md
if [ ! -f "$DOCS_PATH/README.md" ]; then
cat > "$DOCS_PATH/README.md" << HEREDOC
# ${PROJECT}

## 项目概述

一句话描述项目做什么。

## 功能表

| 功能 | 状态 | 说明 |
|------|------|------|
| 功能 A | ✅ 已完成 | 描述 |
| 功能 B | 🚧 进行中 | 描述 |
| 功能 C | ⏳ 待开始 | 描述 |

## 技术栈

- 语言：
- 框架：
- 关键依赖：

## 关联项目

| 项目 | 关系 | 链接 |
|------|------|------|
| xxx | 上游依赖 | [repo](url) |
| yyy | 下游消费 | [repo](url) |

## 代码仓库

- GitHub：[github.com/Jeff19930831/${PROJECT}](https://github.com/Jeff19930831/${PROJECT})
- 本地：\`${CODE_DIR}/${PROJECT}\`

## 使用方式

\`\`\`bash
# 安装依赖

# 运行

# 测试
\`\`\`

## 配置

| 配置项 | 位置 | 说明 |
|--------|------|------|

## 维护者

- 创建者：
- 当前负责人：
HEREDOC
    echo "  ✅ README.md 已生成"
else
    echo "  ⚠️  README.md 已存在，跳过"
fi

# 生成 PROGRESS.md
if [ ! -f "$DOCS_PATH/PROGRESS.md" ]; then
cat > "$DOCS_PATH/PROGRESS.md" << HEREDOC
# ${PROJECT} — 进展记录

> 按时间倒序排列，最新的在最上面

---

## ${TODAY} — 项目启动

### 已完成
- [x] 项目初始化

### 进行中
- [ ] 核心功能开发

### 待办
- [ ] 功能完善
- [ ] 测试

### 阻塞
- 无
HEREDOC
    echo "  ✅ PROGRESS.md 已生成"
else
    echo "  ⚠️  PROGRESS.md 已存在，跳过"
fi

# 生成 HANDOFF.md
if [ ! -f "$DOCS_PATH/HANDOFF.md" ]; then
cat > "$DOCS_PATH/HANDOFF.md" << HEREDOC
# ${PROJECT} — 当前交接

> 给下一个 Agent / 下一台设备快速接手用。保持短、准、最新。

## 当前目标

- 项目初始化，尚未开始开发

## 最近完成

- 项目初始化

## 下一步

1. 填写 README.md 项目信息
2. 开始核心功能开发
3. 编写测试

## 阻塞点

- 无

## 关键文件

| 文件 | 作用 | 注意事项 |
|------|------|----------|
| \`README.md\` | 项目总览 | 功能状态变化时同步 |
| \`PROGRESS.md\` | 进展记录 | 每轮工作结束更新 |
| \`HANDOFF.md\` | 当前交接 | 每轮工作结束更新 |

## 验证命令

\`\`\`bash
# lint / test / run
\`\`\`

## 当前工作区

- 分支：main
- 最近提交：初始化
- 未提交改动：无
HEREDOC
    echo "  ✅ HANDOFF.md 已生成"
else
    echo "  ⚠️  HANDOFF.md 已存在，跳过"
fi

# Step 2: 创建代码仓库（默认分支 main）
CODE_PATH="$CODE_DIR/$PROJECT"
if [ ! -d "$CODE_PATH" ]; then
    mkdir -p "$CODE_PATH"
    cd "$CODE_PATH"
    git init -b main

    cat > .gitignore << 'GITIGNORE'
__pycache__/
*.pyc
.env
.venv/
node_modules/
*.log
.DS_Store
*.egg-info/
dist/
build/
GITIGNORE

    echo "✅ Step 2: 代码仓库已初始化: $CODE_PATH (分支: main)"
else
    echo "✅ Step 2: 代码目录已存在，跳过"
fi

# Step 3: 创建首个提交
cd "$CODE_PATH"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if [ -z "$(git log --oneline 2>/dev/null)" ]; then
        git add -A
        git commit -m "chore: initialize project"
        echo "✅ Step 3: 首个提交已创建"
    else
        echo "✅ Step 3: 已有提交，跳过"
    fi
fi

# Step 4: 创建 GitHub 私有仓库并推送（默认 --private）
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if [ -z "$(git remote get-url origin 2>/dev/null)" ]; then
        if command -v gh >/dev/null 2>&1; then
            cd "$CODE_PATH"
            gh repo create "Jeff19930831/${PROJECT}" --private --source=. --remote=origin --push
            echo "✅ Step 4: GitHub 私有仓库已创建并推送"
        else
            echo "⚠️  Step 4: gh CLI 未安装，跳过 GitHub 创建"
            echo "  手动执行: cd $CODE_PATH && gh repo create Jeff19930831/${PROJECT} --private --source=. --remote=origin --push"
        fi
    else
        echo "✅ Step 4: origin 已配置，跳过"
    fi
fi

# Step 5: 注册到 .project-status.yaml
if ! grep -q "^  ${PROJECT}:" "$YAML_FILE" 2>/dev/null; then
    python3 -c "
import yaml
with open('$YAML_FILE') as f:
    data = yaml.safe_load(f)
data['projects']['$PROJECT'] = {
    'status': '规划中',
    'archive': 'keep',
    'owner': 'codex',
    'type': '',
    'repo': '—',
    'docs': '\`MacCodex/$PROJECT/\`',
    'code_path': '$CODE_PATH/',
    'last_handoff': 'HANDOFF.md',
    'last_update': '$TODAY'
}
with open('$YAML_FILE', 'w') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
"
    echo "✅ Step 5: 已注册到 codex .project-status.yaml"
else
    echo "✅ Step 5: codex YAML 中已有注册，跳过"
fi

# Step 5b: 同步注册到 general .project-status.yaml
if [ -f "$GENERAL_YAML_FILE" ] && ! grep -q "^  ${PROJECT}:" "$GENERAL_YAML_FILE" 2>/dev/null; then
    python3 -c "
import yaml
with open('$GENERAL_YAML_FILE') as f:
    data = yaml.safe_load(f)
data['projects']['$PROJECT'] = {
    'status': '规划中',
    'archive': 'keep',
    'owner': 'codex',
    'type': '',
    'repo': '—',
    'docs': '\`MacCodex/$PROJECT/\`',
    'code_path': '$CODE_PATH/',
    'last_handoff': 'HANDOFF.md',
    'last_update': '$TODAY'
}
with open('$GENERAL_YAML_FILE', 'w') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
"
    echo "✅ Step 5b: 已同步注册到 general .project-status.yaml"
else
    echo "✅ Step 5b: general YAML 已有注册或不存在，跳过"
fi

# Step 6: 同步双层入口
echo "✅ Step 6: 同步 general + codex 双层入口..."
python3 ~/.claude/scripts/update-dashboard.py
python3 ~/.claude/scripts/update-overview.py

echo ""
echo "========================================="
echo "  项目 ${PROJECT} 初始化完成"
echo "========================================="
echo "  文档: ${DOCS_PATH}"
echo "  代码: ${CODE_PATH}"
echo ""
echo "创建完成标准:"
echo "  ✅ 本地目录已 git init"
echo "  ✅ 默认分支为 main"
echo "  ✅ 至少有一个初始化提交"
echo "  ✅ GitHub 私有远程仓库已创建"
echo "  ✅ origin 已绑定"
echo "  ✅ main 已成功推送"
echo "  ✅ codex 台账已登记"
echo "  ✅ general 台账已联动"
