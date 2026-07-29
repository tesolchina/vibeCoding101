# Lesson & Agent Builder — knowledge base

## A. The lesson framework (Part 1 template)

Every lesson built from user materials follows six steps. For EACH step, produce: goal (one line), the ONE question students answer, expected answer, one hint, and a suggested visual (graphic or a 30-second video beat, simple language).

1. **Go over the question** — restate the task in plain words; students identify what is asked and what data they have.
2. **Specify and explain the required principles** — name each concept/principle, explain it in one or two sentences, and say explicitly WHY it applies to THIS question (the connection, not just the definition).
3. **Map out the timeline** — put the events/transactions in date order; timing often decides which rule applies.
4. **Choose the format** — decide the working format: journal entries, T-accounts, schedules, comparison tables, or step lists.
5. **Execute calculations** — show the formula BEFORE substituting numbers; one calculation per step; students compute, the lesson checks.
6. **Review** — verify the logic, highlight common mistakes, summarise the key learning points, and give one similar practice question.

## B. One-step-at-a-time scaffolding rules (anti-wall-of-text)

Derived from a real failure case: a tutor LLM answered a "guide me, don't give answers" request with a 90-line document covering every part at once. Correct pedagogy, wrong delivery. Rules:

- One small question card at a time: a short prompt plus one to three input fields.
- Instant, specific checking ("your quantities total 390 — they must add to 400"), not generic "try again".
- Escalating hints; a Reveal only after hints are exhausted.
- After a correct answer, show the consequence (the computed number and what it means), THEN move on.
- A visible progress indicator (e.g. 3/9) so students feel motion.
- Reflection at the end: one open question that asks students to argue a choice, not recall a number.

## C. The six building blocks (Part 2 template)

1. **Job** — role, primary user, job-to-be-done, outputs, never-do list, human-handoff conditions.
2. **Knowledge** — user-provided materials (slides, notes, chapters, questions, solutions) plus built-in domain knowledge; uploaded course materials take priority over general knowledge, with conflicts noted.
3. **Tools** — document reader, OCR for screenshots, calculator, the lesson framework from Part 1, practice-question generator, feedback module (hints before answers).
4. **Workflow** — mirror the six lesson steps: understand the question → identify principles → map timeline → select format → guide the solution step by step → review → reinforce with a practice question.
5. **Guardrails** — teach, don't answer; never fabricate standards or course content; state assumptions; encourage thinking before revealing; no dishonest completion of graded work; simple language; supportive tone.
6. **Evaluation loop** — accuracy (principles, calculations), teaching quality (concepts before calculations), engagement (questions and hints, not answer dumps), consistency across topics, and learning outcomes (students solve similar problems with less help and can explain their reasoning).

## D. Worked example — accounting tutor from P6.6 (Greco Diamonds)

Input materials: textbook problem P6.6 (periodic inventory, specific identification vs FIFO vs average cost), plus lecture notes on inventory costing.

Part 1 lesson framework produced nine step cards: warm-up unit counts → revenue → maximize-profit allocation (two sales) → minimize-profit allocation (two sales) → FIFO layers → weighted-average unit cost → reflection on method choice. Each card: one question, check, hints, reveal, then the computed consequence (e.g. "Mar 5 COGS = €57,000").

Part 2 agent spec: an expert Accounting Professor tutor whose workflow mirrors those lesson steps, guardrailed to guide rather than answer, defaulting to IFRS, with uploaded course materials taking priority. Evaluation: students should afterwards solve a similar inventory-costing problem unaided and explain WHY rising prices make FIFO show the highest profit.

## E. Output style

- Markdown headings, short paragraphs, simple language (end users may be first-year students).
- For each lesson step, suggest one visual: a bar chart, a timeline graphic, a filled table, or a 30-second narrated video beat ("show the three purchase batches as three stacked boxes with prices").
- English by default.
