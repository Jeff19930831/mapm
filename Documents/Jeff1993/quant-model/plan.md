# quant-model — plan

> 管未来和当前任务；完成后在 checkpoint 中同步到 `progress.md`。

## 当前目标

把本地 Qwen 喂成专业策略生成器：稳定输出可被 `tradingcenter.StrategySpec` 校验通过的 DSL YAML，并能解释 Brooks Price Action / Elliott Wave 概念。

## Active

- [ ] 完成 ASR 转写 16 集波浪理论 `.flv`（faster-whisper large-v3，后台进行中）；验收：`data/corpus/transcripts/elliott_wave_zh/*.txt` 16 份齐全。
- [ ] ASR 完成后蒸馏 wave_principle 类 SFT 卡 → `training_data/asr_wave_sft.jsonl`；并训一轮 v5。
- [ ] 修补 DSL 生成里 `metadata.tag_taxonomy.*` 字段类型（应为字符串）— 通过 schema-aware system prompt 或后处理修正。
- [ ] 写 `scripts/eval_strategy_dsl.py`：把模型输出 YAML 跑 `StrategySpec.model_validate`，计算合规率与节点覆盖率。

## Next

- [ ] 接 tradingcenter `backtest.engine.run`：给模型生成的 DSL 跑回测，把 sharpe / max_dd 写入 reward，做 DPO 负样本回流。
- [ ] 加入 R0-R9 角色蒸馏（hypothesizer / mutator / reviewer / distiller）覆盖更全 prompt 模式。
- [ ] 探索 14B 重训：先把 Windows 页面文件提到 64GB+ 或迁移到 WSL2，再试 Qwen2.5-Coder-14B QLoRA 长跑。
- [ ] 写 `serve/agent_gateway` 的 stream + tool_use 端点版本，配合下游 Agent 调用。

## Deferred

- [ ] 加入付费/版权材料的对外分发能力 — 仅本地推理；任何二次分发需先确认授权。
- [ ] 替换底座到 Qwen3-Coder（待 14B / 32B Instruct 官方发布）。
- [ ] 接入大型 onboarding 附加层（`docs/onboarding/BOOTSTRAP.md` + CODEMAP + module-cards）— 当本工程规模再扩 2x 时再开。

## Completed / Archived by checkpoint

- 2026-05-23：CUDA 训练全链路打通 + tradingcenter DSL 接入 + 本地价格行为蒸馏；证据见 `progress.md`。
- 2026-05-15：llama.cpp-first 部署与 QLoRA 冒烟链路落地；证据见 `progress.md`。
- 2026-05-10：项目初始化与首个 checkpoint；证据见 `progress.md`。