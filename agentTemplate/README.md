# Agent Library — Conventions (vibecoding101)

  This repo hosts **portable teaching agents**: each agent is a public folder of plain text files that any AI harness (SAIL Studio, Claude Code, Cursor, or any agent-capable IDE) can load and run.

  ## How it is organised
  - **One top-level folder per course**, named by course code (same pattern as GCAP3056/ and LANG0036/). Example: `uni101/` = first-year undergraduate pack.
  - **One subfolder per agent** inside its course folder, named with a short slug (e.g. `uni101/collocation-tutor/`).
  - The student's "agent code" = `<course-code>/<agent-slug>` — typing it into SAIL Studio, or pasting the folder link into any AI tool, loads the full experience.

  ## File format
  Each agent folder contains a `SKILL.md` following the mainstream agent-skill convention (Claude Code skills): **YAML frontmatter** (`name`, `description`) + a markdown body. The body uses six fixed headings — OpenAI's six building blocks for education agents:

  1. **Job** 任务 — who it serves, the job-to-be-done, outputs, never-do list, when to hand off to a human
  2. **Knowledge** 知识 — the sources it is grounded in (files in the same folder, or links)
  3. **Tools** 技能（工具）— what capabilities it may use
  4. **Workflow** 工作流程 — the step-by-step procedure it follows
  5. **Guardrails** 安全护栏 — quality and safety rules
  6. **Evaluation loop** 反馈与评估 — how success is measured and how the agent improves

  Copy `agentTemplate/SKILL.md` to start a new agent.

  ## Principles
  - **BYOK** — learners bring their own AI API key; the content itself is free and open.
  - **Platform-neutral** — nothing here depends on any single platform; SAIL Studio is one home among many.
  - **Independent** — every agent folder is self-contained (its knowledge files live beside its SKILL.md).
  