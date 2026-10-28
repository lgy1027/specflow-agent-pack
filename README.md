# SpecFlow Agent Pack

**把智能硬件和 AI 项目里的模糊需求，变成团队能评估、能验证的下一步。**

SpecFlow 是一组供 FDE、产品经理和研发团队使用的 Agent Skills。它帮助团队在投入算法、设备联调或客户试点之前，先把用户问题、已有证据、关键未知和后续验证说清楚。

它面向软件、AI 应用、智能设备和具身场景，不预设某种产品、模型或技术栈。核心交付通常是一份简洁的决策简报；只有确实需要时，才继续准备契约、原型或试点。

## Skills

| Skill | 适用场景 | 常见产物 |
|---|---|---|
| [`probe`](skills/probe/SKILL.md) | 需求不完整，需要评估选择或决定下一步 | 决策简报、证据与未知项、建议验证 |
| [`align`](skills/align/SKILL.md) | 多个角色或系统需要对齐一个可观察行为 | 最小行为契约和验收证据 |
| [`proto`](skills/proto/SKILL.md) | 一个重要未知可以通过低成本原型回答 | 一次性原型及验证结论 |
| [`pilot`](skills/pilot/SKILL.md) | 需要有限的真实用户、设备或现场验证 | 有范围、负责人和停止条件的试点计划 |
| [`init`](skills/init/SKILL.md) | 仓库事实会影响当前判断或需要跨任务复用 | 带来源和未知项的项目画像 |

每个 Skill 都可以单独使用。需求还不清楚时通常从 `/probe` 开始；`/align`、`/proto` 和 `/pilot` 是按需衔接的能力，不要求每个项目跑完整套流程。

## 快速开始

需要 Node.js 22.20 或更新版本。站在仓库根目录，可把整套 Skills 安装到 Claude Code、Codex 和 Hermes Agent 的当前项目：

```powershell
npx skills add . --skill "*" -a claude-code -a codex -a hermes-agent --copy -y
```

DeepSeek Harness 和 WorkBuddy 使用各自的加载方式；WorkBuddy 还需要平台专用元数据。详见[跨 Agent 安装说明](INSTALLATION.md)。

也可以不安装，先直接阅读 [`probe/SKILL.md`](skills/probe/SKILL.md) 和它引用的按需参考文件。

## 示例

输入：

> 客户想用毫米波做睡眠分析，再用麦克风识别鼾声。我们能不能接这个 POC？

`/probe` 不会据此承诺算法效果或周期，而会先澄清 POC 要验证什么、数据和设备条件是否具备、结果用于什么场景，再给出当前建议和最小下一步。涉及真实客户时，应使用获准并脱敏的材料。

## 使用边界

- Skills 帮助整理问题、证据和交接物，不会自动实现算法、权限控制、设备联锁、部署回滚或生产监控。
- 页面原型可以验证交互，不能代替传感器或模型效果评测；真实硬件测试须遵守项目安全流程。
- 未经授权，不要把客户材料、凭据或个人数据发送给外部模型或服务。
- 当前的安装说明描述各平台的加载方式，不代表所有 Agent 或企业租户都已实际试装通过；WorkBuddy 需要单独适配。

## 参与改进

见[贡献指南](CONTRIBUTING.md)。增加新规则、模板或脚本前，请先确认它解决了反复出现的实际问题；不要把单个客户案例写成所有项目的固定要求。安全问题请看[安全报告说明](SECURITY.md)。

## 发布状态

本仓库按 [Apache License 2.0](LICENSE) 发布。原型页会从公共 CDN 加载 Tailwind CSS 与 Font Awesome；部分交互模板预填 DeepSeek API 端点和模型名作为可编辑示例，不包含 API 密钥。使用实时模式前请自行配置端点并遵守数据授权要求。
