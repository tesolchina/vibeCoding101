# vibeCoding101
  For various workshops to run in Fall 2025 and beyond.

  ## Agent packs — run any of these right now

  Each pack is a folder with a `SKILL.md` (the agent's instructions), optional `knowledge.md`, and an optional `learn.json` (interactive scenarios, narration audio and a lesson video).

  | Pack | Code | What's inside | Run it | Run it in YOUR OWN agent |
  |---|---|---|---|---|
  | **Using Email Well at University** | `uni101/email-essentials` | Learn + Act (video + audio) | [Run on SAIL Studio](https://fiteagent.replit.app/go?ref=uni101%2Femail-essentials) | [Open the pack](https://github.com/tesolchina/vibecoding101/tree/main/uni101/email-essentials) |
| **Learning Vocabulary in Networks** | `dse/vocab-networks` | Learn + Act (video + audio) | [Run on SAIL Studio](https://fiteagent.replit.app/go?ref=dse%2Fvocab-networks) | [Open the pack](https://github.com/tesolchina/vibecoding101/tree/main/dse/vocab-networks) |
| **Hong Kong's Digital Commons** | `hk/saanseoi-atlas` | Learn + Act (video + audio) | [Run on SAIL Studio](https://fiteagent.replit.app/go?ref=hk%2Fsaanseoi-atlas) | [Open the pack](https://github.com/tesolchina/vibecoding101/tree/main/hk/saanseoi-atlas) |
| **Collocation Tutor** | `uni101/collocation-tutor` | Agent only | [Run on SAIL Studio](https://fiteagent.replit.app/go?ref=uni101%2Fcollocation-tutor) | [Open the pack](https://github.com/tesolchina/vibecoding101/tree/main/uni101/collocation-tutor) |
| **Thesis Tutor** | `uni101/thesis-tutor` | Agent only | [Run on SAIL Studio](https://fiteagent.replit.app/go?ref=uni101%2Fthesis-tutor) | [Open the pack](https://github.com/tesolchina/vibecoding101/tree/main/uni101/thesis-tutor) |
| **Study Planner** | `uni101/study-planner` | Agent only | [Run on SAIL Studio](https://fiteagent.replit.app/go?ref=uni101%2Fstudy-planner) | [Open the pack](https://github.com/tesolchina/vibecoding101/tree/main/uni101/study-planner) |

  ### Run a pack in your own agent
  You don't need our platform — every pack is plain Markdown:
  1. **Any AI chat (ChatGPT, Claude, Gemini, …):** open the pack folder above, copy the `SKILL.md` (and `knowledge.md` if present) into your chat, and say "act as this agent".
  2. **Replit Agent / Claude Code / coding agents:** paste the pack's GitHub folder link and ask the agent to load the SKILL.md and role-play it.
  3. **SAIL Studio launcher:** paste the folder link (or just the code, e.g. `uni101/thesis-tutor`) at https://fiteagent.replit.app/go — Learn scenarios run free; the practice agent uses your own AI key.

  ### Author your own pack
  Copy `agentTemplate/` — a pack is just `SKILL.md` (+ optional `knowledge.md`, `learn.json`, `audio/`, `video/`). See `AUTHORING-MC.md` for the learn.json format.
  