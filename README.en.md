# SpecFlow Agent Pack

[English](README.en.md) | [简体中文](README.md)

**Clarify the problem before deciding what to build and how to validate it.**

SpecFlow is a set of composable Agent Skills for forward-deployed engineers, product managers, and development teams. It helps teams clarify goals, evidence, critical unknowns, and the next validation step before committing to implementation or a field pilot.

Use it for software, internal tools, customer projects, AI applications, and intelligent hardware. It does not assume a specific industry, product shape, or technology stack. AI, hardware, and embodied systems are key focus areas, but are not prerequisites.

## How It Works

Start with a real question, such as: “A customer wants a sleep-monitoring demo in two weeks. Should we take the project?” SpecFlow does not automatically turn the proposed solution into a development task. It helps the team answer:

1. **What decision are we making?** Clarify the decision, goal, and constraints.
2. **What do we know?** Separate confirmed facts, reported claims, inferences, and unknowns. Ask follow-up questions when the answers could change the recommendation.
3. **Where are the risks and gaps?** Assess feasible paths, dependencies, authorization, safety, and acceptance boundaries based on the available evidence.
4. **What is the smallest credible next step?** It may be further alignment, a focused assumption check, a lightweight prototype, or a bounded pilot. If key information is missing, the right next step may be to clarify it first.

These are user-invoked Skills that can be combined as needed. SpecFlow is not a background platform that makes decisions for a team, runs an end-to-end delivery process, or controls production systems.

## Skills

| Skill | Use it when | Typical output |
|---|---|---|
| [`probe`](skills/probe/SKILL.md) | The goal, scope, feasibility, or next step is unclear | Decision brief, critical unknowns, validation options |
| [`align`](skills/align/SKILL.md) | Roles or systems need to agree on observable behavior | Minimal behavior contract, acceptance evidence |
| [`proto`](skills/proto/SKILL.md) | A key assumption can be tested with a low-cost prototype | Disposable prototype, validation findings |
| [`pilot`](skills/pilot/SKILL.md) | A bounded validation with real users, customers, or a physical site is needed | Pilot plan with scope, owners, and stop conditions |
| [`init`](skills/init/SKILL.md) | Engineering decisions depend on repository context | Project profile with evidence, confidence, and unknowns |

Each Skill can be used on its own. A common path starts with `/probe`, then selects a follow-up Skill based on the problem. You do not need to run the entire sequence for every request.

```text
Unclear request ──> /probe ──> Decision and smallest next step
                                  ├── /align  Align cross-role behavior
                                  ├── /proto  Validate a key assumption
                                  └── /pilot  Plan a bounded field pilot

Use /init when repository context affects the decision.
```

## Quick Start

### Install

Each `skills/<name>/` directory is a standalone Skill. Keep the whole directory when installing, including `SKILL.md`, `references/`, `templates/`, and any optional `scripts/`. Copying only `SKILL.md` will omit supporting resources.

#### Claude Code, Codex, and Hermes Agent

Requires Node.js 22.20 or later. Use the [skills CLI](https://www.skills.sh/docs/cli) to install one Skill or the full set from GitHub:

```powershell
# Install just the discovery Skill
npx skills add lgy1027/specflow-agent-pack --skill probe -a codex

# Or install all Skills
npx skills add lgy1027/specflow-agent-pack --skill "*" -a claude-code -a codex -a hermes-agent --copy -y
```

Omit `-a` to choose an agent interactively. To install from a local clone, run the command from the repository root and replace the repository name with `.`. `--copy` avoids symlinks and is useful on Windows.

| Agent | Installation method / project-level location |
|---|---|
| Claude Code | Use the `skills` CLI or copy to `.claude/skills/<name>/`. |
| Codex | Use the `skills` CLI or copy to `.agents/skills/<name>/`. Start Codex from the project directory; invoke a Skill explicitly with `$probe`. |
| Hermes Agent | Use the `skills` CLI or copy to `.hermes/skills/<name>/` or `.agents/skills/<name>/`. If prompted to trust project Skills, run `hermes skills trust .` from the repository root. |
| DeepSeek Harness | Copy to `.agents/skills/<name>/` or `.dsh/skills/<name>/`. Place each Skill directly one level below the target directory. |
| WorkBuddy | Import through **Experts → Skills → Connectors → Skills** using **Add Skill / Create Skill**. Preserve each Skill's supporting files and adapt the platform metadata and reference syntax. The source files in this repository are not a ready-to-import WorkBuddy package; verify Skill and reference loading in a new conversation after import. |

#### Plugin support

Claude Code and Codex also support Plugin distribution, but a Plugin is not the same as a portable Agent Skill. **This repository currently contains standalone Agent Skills, not Claude Code or Codex Plugin packages.** It has no Claude Marketplace manifest or Codex `plugin.json` wrapper, so install the Skills using the methods above. Plugin installation will be supported only after the platform-specific packages and manifests are added and verified. See the official [Claude Code Plugins documentation](https://code.claude.com/docs/en/plugins) and [Codex Plugins documentation](https://developers.openai.com/plugins/concepts/plugins).

After installation, open a new session and confirm the Skills are available. When needed, verify that `/probe` can load files from `references/` and `/proto` can load files from `templates/`. The optional `pilot` validation script requires Python in the target environment; if it cannot run, report that it was not mechanically validated. Installation instructions describe supported loading paths, not compatibility testing for every agent version or enterprise environment. See the [WorkBuddy Skill documentation](https://open.workbuddy.cn/en/docs/skill) for platform-specific details.

### Use

In an agent that supports Skills, select `/probe` and describe the decision or problem in natural language:

```text
/probe
A customer wants to use millimeter-wave radar for sleep analysis and a microphone for snore detection. Should we take this POC?
```

SpecFlow asks about information that could change the recommendation, then responds based on the available evidence. It does not promise model performance, delivery dates, or field feasibility based on a one-line request. You can also browse the `skills/` directory or install an individual Skill manually.

## Behavioral Evaluations

The repository includes manually run evaluation cases for information-sparse requests, cross-team alignment, offline prototypes, pilot reviews, and read-only repository discovery. See [`evals/README.md`](evals/README.md). These evaluations are not automated tests and do not certify production safety or platform compatibility.

## Design Principles

- **Understand before recommending:** Clarify an underspecified request instead of treating the proposed solution as settled.
- **State the evidence:** Distinguish confirmed facts, reported claims, inferences, and unknowns.
- **Compose only what is needed:** Use the smallest workflow that can answer the current question.
- **Keep technology open:** Follow the project's tools and conventions; do not mandate a model, framework, protocol, or CI platform.
- **Make validation limits explicit:** A prototype, contract, or plan does not provide production controls or safety assurance.

## Scope and Data Use

- Skills help organize decisions, evidence, and handoff artifacts. They do not implement algorithms, access controls, device interlocks, deployment rollback, or production monitoring by themselves.
- A prototype can validate an interaction or workflow. It does not replace model evaluation, device safety assessment, or production reliability testing.
- For work involving real users, customers, devices, or field sites, follow the project's data authorization, safety, and approval processes.
- Do not send customer materials, credentials, or personal data to an external model or service without authorization.
- In intelligent hardware and embodied-system scenarios, checks are scoped to the actual capabilities and risks. A page prototype cannot replace hardware safeguards.

## Contributing

Issues, improvement suggestions, and contributions are welcome. Start with the [contribution guide](CONTRIBUTING.md); report security concerns according to [SECURITY.md](SECURITY.md). Before adding a rule, template, or script, confirm that it addresses a recurring problem rather than hard-coding a one-off case.

## License

SpecFlow is released under the [Apache License 2.0](LICENSE).

Some HTML prototype templates load Tailwind CSS and Font Awesome from public CDNs, so those templates require network access unless their styles and icons are replaced with inline or approved local resources. The live-model examples use editable endpoint and model settings and do not include API keys. Before using live mode, verify data flows and authorization requirements.
