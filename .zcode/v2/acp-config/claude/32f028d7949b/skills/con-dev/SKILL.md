---
name: con-dev
description: "Jeff1993 连续开发 - 自动化项目初始化和跨设备协作，支持快速加入项目"
argument-hint: "+<项目名>"
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Glob
  - Grep
---

# Con-Dev - 连续开发自动化

<objective>
自动化完成新设备/新 Agent 加入项目的流程，实现一键协作。
</objective>

<process>
## 使用方式

```
/con-dev +<项目名>
```

示例：
- `/con-dev +MAPM`
- `/con-dev +采购数据处理`
- `/con-dev +招标信息处理`
</process>

<process>
## 自动化流程

### Step 1: Git Pull 更新 Jeff1993 文档
```bash
cd "C:/Users/lk/Documents/Jeff1993" || cd "/Users/lk/Documents/Jeff1993"
git pull origin master
```

### Step 2: 解析项目状态
读取 `.project-status.yaml`，找到指定项目：
- 提取项目 `code_path`
- 提取项目 `repo` 地址
- 提取项目 `last_handoff` 文件
- 验证项目状态是否活跃

### Step 3: Clone 代码仓库
根据项目信息 clone 代码仓库：
```bash
cd "C:/Users/lk/Documents/Jeff1993" || cd "/Users/lk/Documents/Jeff1993"
git clone <repo_url> <项目名>
cd <项目名>
```

### Step 4: 读取项目文档
按优先级读取：
1. `handoff.md` → `plan.md` → `README.md`
2. 如不存在小写文件，则读取 `HANDOFF.md` / `PROGRESS.md`

### Step 5: 环境检测
检查项目环境：
- Python 依赖（requirements.txt）
- Node.js 依赖（package.json）
- 数据库连接
- 测试环境

### Step 6: 输出就绪报告
生成项目就绪状态报告，包含：
- 当前目标
- 下一步行动
- 验证命令
- 环境状态
</process>

<notes>
- 必须先安装 Claude Code 和确保 GitHub CLI 登录
- 自动处理兼容期的大写文件（HANDOFF.md / PROGRESS.md）
- 支持所有项目状态枚举（规划中、进行中、运行中、维护中）
- 错误时会提供明确的修复指导
</notes>