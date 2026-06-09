# progress

## 2026-06-05

Created this Obsidian-visible pointer folder for `clash-governance`.

Evidence:

- `.project-status.yaml` already pointed to `WinCodex/clash-governance/`, but the folder did not exist.
- The pointer now links back to the code repo at `D:\Workspace\clash-governance`.
- Full checkpoint evidence remains in the code repo `progress.md`.

## 2026-06-05 治理发现：全局 TUN 把基础设施 IP 走了不稳定代理节点

排查 cloud-memory 服务器 (`43.133.86.33`, 腾讯云) 接入抖动时定位到一条 Clash 治理问题（先在 Mac 的 Clash Verge 上发现，规则同样适用于本 Windows 机）：

- **现象**：全局 TUN 把到 `43.133.86.33` 的流量（SSH:22 + HTTP:3111）塞进代理出口节点 → 经代理 HTTP `livez` 5 次 1 次超时、延迟 0.5–3.5s 乱跳；SSH 长会话直接卡死。
- **验证**：改走物理网卡直连（Mac: `route add -host 43.133.86.33 <en0网关>`）后 HTTP `livez` 8/8 成功、稳定 ~0.08s（快 10–40 倍、零失败）。
- **治理规则（建议加入受管 Clash 配置）**：对可直连的国内/基础设施 IP 加 DIRECT 不走代理：
  ```
  IP-CIDR,43.133.86.33/32,DIRECT
  ```
  可扩到其它自有服务器/腾讯云段。临时静态路由重启失效，**DIRECT 规则才是持久解**。
- **落点**：权威修改在代码仓 `D:\Workspace\clash-governance` 的受管 Clash 配置；本 pointer 只记结论。Mac 侧 Clash 也需同样加该 DIRECT 规则。
