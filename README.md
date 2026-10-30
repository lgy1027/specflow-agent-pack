# SpecFlow Agent Pack

[English](README.en.md) | 简体中文

**先把问题问对，再决定要不要做、怎么验证。**

SpecFlow 是面向 FDE、产品经理和研发团队的一组可组合 Agent Skills，帮助团队在投入开发或现场试点前，厘清目标、证据、关键未知和下一步验证方式。

它适用于软件、内部工具、客户项目、AI 应用和智能硬件等工作，不绑定行业、产品形态或技术栈。AI、硬件与具身场景是重点支持方向，但不是使用前提。

## 它如何工作

从一个实际问题开始，例如“客户要两周内做睡眠监测演示，我们现在该不该接？”SpecFlow 不会默认把用户提出的方案直接变成开发任务，而是先帮助团队回答：

1. **要做什么决定？** 明确当前要拍板的问题、目标和约束。
2. **我们知道什么？** 区分已确认事实、他人说法、推断和未知；必要时先追问会改变结论的信息。
3. **风险和缺口在哪里？** 结合当前证据评估可行路径、依赖、授权、安全和验收边界。
4. **最小的可信下一步是什么？** 可能是补充对齐、验证一个假设、做有限原型或制定试点；信息不足时也可以停在澄清阶段。

这些是由用户按需调用的 Skills，不是会自动替团队拍板、执行完整交付流程或控制生产系统的后台平台。

## 适合解决的问题

项目早期常见的困难不是缺少实现方案，而是目标不清、关键条件未核实、角色之间对“完成”的理解不一致。SpecFlow 帮助团队：

- 通过少量有针对性的追问，澄清需求和决策目标；
- 区分证据、说法、推断与未知，避免把假设写成事实；
- 在继续开发前比较可行路径和主要风险；
- 只在确有需要时生成契约、原型或试点计划。

## Skills

| Skill | 什么时候使用 | 常见产物 |
|---|---|---|
| [`probe`](skills/probe/SKILL.md) | 目标、范围、可行性或下一步还不清楚 | 决策简报、关键未知、建议验证 |
| [`align`](skills/align/SKILL.md) | 多个角色或系统需要对齐一个可观察行为 | 最小行为契约、验收证据 |
| [`proto`](skills/proto/SKILL.md) | 一个重要假设可以通过低成本原型验证 | 一次性原型、验证结论 |
| [`pilot`](skills/pilot/SKILL.md) | 需要有限的真实用户、客户或现场验证 | 有范围、责任人和停止条件的试点计划 |
| [`init`](skills/init/SKILL.md) | 工程判断依赖仓库事实，或需要复用项目上下文 | 带来源、置信度和未知项的项目画像 |

每个 Skill 都可以单独使用。常见路径是从 `/probe` 开始，再按问题选择后续步骤；并非每个请求都要走完整流程。

```text
模糊需求 ──> /probe ──> 决策与最小下一步
                            ├── /align  对齐跨角色行为
                            ├── /proto  验证关键假设
                            └── /pilot  规划有限现场试点

工程上下文影响判断时，可按需补充 /init
```

## 快速开始

### 安装

每个 `skills/<name>/` 目录都是一个独立 Skill。安装时保留整个目录，包括 `SKILL.md`、`references/`、`templates/` 和可选的 `scripts/`；只复制 `SKILL.md` 会丢失配套资源。

#### Claude Code、Codex、Hermes Agent

需要 Node.js 22.20 或更新版本。使用 [skills CLI](https://www.skills.sh/docs/cli) 从 GitHub 安装单个 Skill 或整套 Skills：

```powershell
# 先试用需求探索
npx skills add lgy1027/specflow-agent-pack --skill probe -a codex

# 或安装整套 Skills
npx skills add lgy1027/specflow-agent-pack --skill "*" -a claude-code -a codex -a hermes-agent --copy -y
```

省略 `-a` 可按提示选择 Agent。从本地克隆目录安装时，在仓库根目录将仓库地址替换为 `.`。`--copy` 适合 Windows 环境，避免创建符号链接。

| Agent | 安装方式 / 项目级目录 |
|---|---|
| Claude Code | `skills` CLI；或复制到 `.claude/skills/<name>/`。 |
| Codex | `skills` CLI；或复制到 `.agents/skills/<name>/`，在项目目录启动 Codex。可用 `$probe` 显式调用。 |
| Hermes Agent | `skills` CLI；或复制到 `.hermes/skills/<name>/` / `.agents/skills/<name>/`。若提示未信任项目 Skills，在仓库根目录运行 `hermes skills trust .`。 |
| DeepSeek Harness | 手动复制到 `.agents/skills/<name>/` 或 `.dsh/skills/<name>/`。每个 Skill 直接放在目标目录下一层。 |
| WorkBuddy | 在 **Experts → Skills → Connectors → Skills** 通过 **Add Skill / Create Skill** 导入。需保留 Skill 配套目录，并按平台要求添加展示元数据、调整引用格式；当前仓库源文件不是可直接导入的 WorkBuddy 成品包。导入后在新对话确认 Skill 和引用资料均能加载。 |

Claude Code 和 Codex 也支持 **Plugin** 分发，但 Plugin 不等同于通用 Skill。当前仓库只有 Agent Skills，**没有** Claude Marketplace 清单或 Codex `plugin.json` 包装，因此请用上面的 Skills 安装方式，不要使用 Plugin 安装命令。以后如提供插件包：Claude Code 从 Marketplace 添加并安装，Codex 从 Plugins 界面或本地 Marketplace 安装；具体命令和清单按发布包提供。官方文档：[Claude Code Plugins](https://code.claude.com/docs/en/plugins)、[Codex Plugins](https://developers.openai.com/plugins/concepts/plugins)。

安装后在新会话确认 Skill 出现在可用列表中；按需验证 `/probe` 可读取 `references/`、`/proto` 可读取 `templates/`。`pilot` 的可选脚本需要目标环境支持 Python；不能运行时标记为未机械校验。不同 Agent 的加载行为可能变化，安装说明不代表每个版本或企业环境都已实测。WorkBuddy 平台参考：[Skill 文档](https://open.workbuddy.cn/en/docs/skill)。

### 使用

在支持 Skill 调用的 Agent 中选择 `/probe`，然后用自然语言描述正在做的决定或遇到的问题。例如：

```text
/probe
客户想用毫米波做睡眠分析，再用麦克风识别鼾声。我们要不要接这个 POC？
```

SpecFlow 会先澄清会影响判断的信息，再基于现有证据给出建议。它不会仅凭一句话承诺算法效果、项目周期或现场可行性。也可以直接打开 [`skills/`](skills/) 下的 `SKILL.md` 阅读或手动安装单个 Skill。

## 行为评测

仓库包含一组人工行为评测案例，用于观察 Skills 在信息稀缺、跨团队对齐、离线原型、试点复盘和只读项目画像等场景中的决策质量。见 [`evals/README.md`](evals/README.md)。该评测集不是自动化测试，也不构成生产安全或平台兼容性认证。

## 设计原则

- **先理解，再建议：** 需求不清时先澄清，不把用户的初始方案当成结论。
- **按证据表达：** 明确区分已确认事实、外部说法、推断和未知。
- **按需组合：** 选择能够回答当前问题的最小工作流，不强制产出一整套文档。
- **技术保持开放：** 遵循项目已有工具和约定，不预设模型、框架、协议或 CI 平台。
- **把验证边界说清：** 原型、契约和计划用于辅助决策，不等于生产控制或安全保障。

## 能力边界与数据使用

- Skills 帮助整理问题、证据和交接物；不会自动实现算法、权限控制、设备联锁、部署回滚或生产监控。
- 原型可以验证交互或工作流，不能代替模型评测、设备安全评估或生产可靠性验证。
- 涉及真实用户、客户、设备或现场时，应遵守项目的数据授权、安全和审批流程。
- 未经授权，不要把客户材料、凭据或个人数据发送给外部模型或服务。
- 智能硬件或具身场景中的专项检查会按实际能力和风险触发；页面原型不能替代硬件保护措施。

## 参与贡献

欢迎提交问题、改进建议和贡献。请从[贡献指南](CONTRIBUTING.md)开始；安全问题请查看[安全报告说明](SECURITY.md)。增加规则、模板或脚本前，优先确认它解决的是可重复出现的问题，避免把单一案例变成所有项目的固定要求。

## 许可证

本项目基于 [Apache License 2.0](LICENSE) 发布。

部分 HTML 原型模板从公共 CDN 加载 Tailwind CSS 与 Font Awesome，因此需要演示环境能够访问 CDN；离线或内网受限时，应改为内联样式/图标或获准的本地资源。实时模型示例中的端点和模型名是可编辑配置，不包含 API 密钥。使用实时模式前，请核实数据流向并遵守相应的数据授权要求。
