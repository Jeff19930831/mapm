# quant-model — plan

> 管未来和当前任务；完成后在 checkpoint 中同步到 \progress.md\。

## 当前目标

建立可接力的本地量化金融模型工程项目，并完成首个 checkpoint。

## Active

- [ ] 修复/替换当前 Qwen3.6 GGUF 运行时：验收：\ollama run <目标模型>\ 能稳定回答 \只回答OK\。
- [ ] 验证 RAG 问答链路：验收：\python .\scripts\chat.py "设计一个A股日频动量轮动策略"\ 成功返回量化金融结构化回答 。
- [ ] 扩展合法公开语料源：验收：\data/corpus/\ 有清单、来源、许可证/公开性说明。

## Next

- [ ] 建立评测集：策略设计、回测偏差、组合优化、衍生品、Python 代码五类问题。
- [ ] 设计 QLoRA 微调路线：明确 HF 基座模型、显存预算、训练环境、数据格式和导出方式。
- [ ] 为本项目建立独立代码仓库或把现有 \C:\Users\Administrator\quant-qwen-finance\ 移入规范位置。

## Deferred

- [ ] 真微调 Qwen3.6-27B — 原因：需要可运行基座、训练数据质量评审和 WSL/Linux 训练环境。
- [ ] 接入付费/版权书籍 — 原因：必须先确认授权，默认不进入语料库。

## Completed / Archived by checkpoint

- 2026-05-10：项目初始化与首个 checkpoint；证据见 \progress.md\。
