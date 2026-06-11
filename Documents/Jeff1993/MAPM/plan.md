# MAPM — plan

## Active

- [ ] 观察跨设备 Git 同步稳定性
- [ ] Win 端适配去层化后的目录结构和脚本
- [ ] **项目同步清单推广**: 继续为 mysteel-crawl / hermes-agent 等大项目补齐 `code_paths` + `sync`, 并观察 `project_registry.py lint` 的误报率
- [ ] **Onboarding Suite v1.0 推广**: 把 wechat-macro-kb 作为首个适配项目, 跑通完整周期 (init-onboarding → 日常 checkpoint → con-dev 验证 token ≤ 5KB)
- [ ] **con-dev / checkpoint / session-handoff v3.14 验证**: 新会话跑 `/con-dev +wechat-macro-kb` 与一次 docs-only checkpoint dry-run，确认 CodeGraph/CODEMAP 边界和 compact 规则足够
- [ ] **cloud-memory Phase 3 优化**: AGENTMEMORY_SECRET 认证 + HTTPS + 数据库备份
- [ ] **Memory Hooks 验证**: ✅ 已发现搜索策略问题并修复（con-dev/checkpoint skill 多查询并行），继续观察多个项目 checkpoint 验证稳定性
- [ ] **独立 mapm 仓库处置**: 决定 `Jeff19930831/mapm` 是归档、脚本包保留，还是重新迁移为独立 canonical repo

## Completed

- [x] **治理优化 Roadmap 全部落地 (OPT-1..6)** (2026-06-03) — 详见 `progress.md`

## Archived

- Older milestones (v3.4..v3.11, governance, con-dev optimization) recorded in `MAPM/progress.md`.

## Next

- [ ] 根据实际使用反馈继续迭代 onboarding 协议（v3.14 已落地，观察三流程边界稳定性）
- [ ] agent-kit bootstrap 脚本落地（当前只有合同，无可执行脚本）
- [ ] 探索 session/lock 模型替代 status/ 设备状态文件（参考 docs/2026-04-28-mapm-review-optimization.md）
- [ ] Onboarding Suite 推广到其他大项目: mysteel-crawl / hermes-agent
- [ ] Onboarding Suite 收集使用反馈, 优化模板与阈值
- [ ] 探索 Gemini/Kimi 的 skill 适配 (目前仅 Claude/Codex)

## Historical Archive

- Older completed MAPM milestones are recorded in `MAPM/progress.md`; keep `plan.md` to Active / Next / one recent Completed section.
