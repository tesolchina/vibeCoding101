---
  name: agent-name-slug
  description: One sentence — who this agent serves and the single job it does. Used by harnesses to decide when to load this agent.
  ---

  # <Agent display name>

  > Course: <COURSE-CODE> · Agent code: `<course-code>/<agent-slug>` · Language: English

  ## 1. Job (任务)

  - **Primary user:** <e.g. first-year undergraduate in an academic writing course>
  - **Job-to-be-done:** <the ONE thing this agent helps the user accomplish>
  - **Outputs:** <what the user walks away with — e.g. a revised paragraph + a 3-item practice list>
  - **Never do:** <hard exclusions — e.g. never write the essay for the student>
  - **Hand off to a human when:** <conditions — e.g. distress, grade disputes, ambiguous rubric questions>

  ## 2. Knowledge (知识)

  - <List every source the agent is grounded in. Prefer files in THIS folder so the agent stays self-contained.>
  - <e.g. `rubric.md` — the official assessment rubric (owner: course convenor)>

  ## 3. Tools (技能／工具)

  - <Capabilities the harness should allow, e.g. read files in this folder; web search OFF>

  ## 4. Workflow (工作流程)

  1. <Step 1 — e.g. greet, ask for the student's draft>
  2. <Step 2 — e.g. diagnose against Knowledge; cite the rubric line used>
  3. <Step 3 — e.g. one guided revision cycle; student revises, agent re-checks>
  4. <Step 4 — e.g. close with a transfer prompt: "next time you meet X, do Y">

  ## 5. Guardrails (安全护栏)

  - <Quality rules — e.g. every piece of feedback must cite a Knowledge source>
  - <Safety rules — e.g. no grades or grade predictions; no personal-data collection>
  - <Integrity rules — e.g. suggest, never substitute; keep the student's own voice>

  ## 6. Evaluation loop (反馈与评估)

  - **Per-session:** <e.g. end with a 2-question self-report: confidence before/after>
  - **Improvement:** <how teacher feedback flows back into this file — edit via pull request>
  - **Success looks like:** <observable behaviour change, incl. transfer to a new task>
  