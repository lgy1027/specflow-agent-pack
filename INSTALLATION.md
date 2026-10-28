# 安装到不同 Agent

SpecFlow 的每个 `skills/<name>/` 目录都是一个独立 Skill。安装时复制整个 Skill 目录，保留其中的 `SKILL.md`、`references/` 和 `templates/`；只复制 `SKILL.md` 会丢失按需参考和模板文件。

以下命令默认在完整源码仓库根目录执行。

## Claude Code、Codex、Hermes Agent

在项目根目录使用 Vercel `skills` CLI，可以把五个 Skills 安装到这三个 Agent 的项目级目录。CLI 需要 Node.js 22.20 或更新版本：

```powershell
npx skills add . --skill "*" -a claude-code -a codex -a hermes-agent --copy -y
```

`--copy` 会复制文件而不是创建符号链接，适合 Windows 项目。要安装单个 Skill，把 `"*"` 替换成 `probe`、`align`、`proto`、`pilot` 或 `init`。该命令安装到当前项目；Agent 应从这个项目目录启动。

Vercel `skills` CLI 当前的 Agent 列表包含 Claude Code、Codex 和 Hermes Agent；不包含 DeepSeek Harness 或 WorkBuddy，后两者请按下面的原生方式安装。参见 [CLI 支持列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。

也可以手动复制：

| Agent | 项目级目录 | 使用方式 |
|---|---|---|
| Claude Code | `.claude/skills/<name>/` | 启动 Claude Code 后用 `/probe` 等名称调用，或让它按任务自动选择。 |
| Codex | `.agents/skills/<name>/` | 从项目目录启动 Codex；可通过 `$probe` 显式选择，也可按描述自动触发。 |
| Hermes Agent | `.hermes/skills/<name>/` 或 `.agents/skills/<name>/` | 如果 Hermes 提示项目 Skills 尚未信任，在项目根目录运行 `hermes skills trust .`。 |

## DeepSeek Harness

DeepSeek Harness 的本地发现支持 `.dsh/skills/<name>/` 和共享的 `.agents/skills/<name>/`。推荐使用后者，便于与 Codex、Hermes 共用文件。它要求每个 Skill 直接位于该目录下一层，例如 `.agents/skills/probe/SKILL.md`；不要把整个 `skills/` 文件夹再嵌套复制成 `.agents/skills/skills/probe/`。

Windows PowerShell 手动复制示例：

```powershell
$skillsSource = (Resolve-Path .\skills).Path
$skillsTarget = Join-Path (Get-Location) '.agents\skills'
New-Item -ItemType Directory -Force $skillsTarget | Out-Null
Get-ChildItem $skillsSource -Directory | ForEach-Object {
    Copy-Item $_.FullName -Destination $skillsTarget -Recurse -Force
}
```

## WorkBuddy

WorkBuddy 通过 Open Platform 的 Skill Marketplace 管理 Skills：进入 **Experts → Skills → Connectors → Skills**，再使用 **Add Skill / Create Skill** 流程。平台文档描述了 `SKILL.md`、ZIP 解析和参考/模板目录，但没有证明当前这套源文件已经在你的 WorkBuddy 租户中导入成功。

**现有文件不能原样当作 WorkBuddy 成品包。**WorkBuddy 文档要求额外的展示元数据，包括 `display_name`、`display_name_en`、`description_zh`、`description_en`、`version` 和 `author`；参考资料按它的格式通过 `@references/...` 引用。当前核心 Skill 保持通用 Agent Skills 格式，因此应制作独立的 WorkBuddy 兼容副本并保留原始目录，不要为平台元数据或引用语法改写通用源文件。原型起始模板现位于 `templates/`，但导入后仍需按平台实际行为验证模板和参考文件能否加载。

WorkBuddy 适配完成后，每个 Skill 单独打包或通过平台创建流程导入，确保其 `SKILL.md` 与对应的参考/资源文件保持同一目录结构。导入后在 Skill Marketplace 安装，再在对话中用对应场景验证是否能加载引用文件。官方说明：[WorkBuddy Skill 文档](https://open.workbuddy.cn/en/docs/skill)。

### 更新适配副本

适配副本与通用源文件分开维护。更新时先记录上游提交号/版本，再把对应 Skill 的源文件与 WorkBuddy 副本逐项比较；保留 WorkBuddy 元数据和路径改动，将上游逻辑更新合并到副本后重新导入并验证 `@references/...` 与模板资源能加载。不要直接用上游目录覆盖已适配副本。当前仓库不提供自动同步脚本，避免把平台专用转换规则固化进通用 Skill；若团队开始重复执行这一流程，再考虑增加可复现的打包脚本。

## 验证安装

在新会话中分别确认：

1. Skill 出现在 Agent 的 Skills 列表中，或能通过名称显式调用；
2. 运行 `/probe` 时可读取 `references/interrogation-library.md` 等被引用的文件；
3. 运行 `/proto` 时能访问 `templates/` 中的模板（仅在原型问题需要时）。

不同 Agent 的安装目录和打包要求可能变化，导入后请在新会话验证 Skill 与参考文件是否能加载。提交客户材料前，先完成脱敏并确认授权。

各 Agent 官方说明： [Claude Code](https://code.claude.com/docs/en/skills)、[Codex](https://developers.openai.com/codex/skills)、[Hermes Agent](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)、[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)。
