# Writing multiple-choice questions for learn.json packs

Design rules for Part A (Learn) scenario questions, distilled from Cheng, Xu & Jin (2024),
*TreeQuestion: Assessing Conceptual Learning Outcomes with LLM-Generated Multiple-Choice
Questions* (CSCW 2024, https://doi.org/10.1145/3686970), adapted for SAIL Studio /go packs.

## 1. Anchor every question in a scenario

Scenario-based stems (a named student in a concrete situation) move the question up
Bloom's taxonomy — from *Remember* to *Apply/Analyze*. Prefer "Ming did X; what should he
do?" over "What is a display name?". LLMs are good at generating realistic scenarios;
teachers should supply the concept list and check accuracy (the paper's
Explore–Validate–Generate split).

## 2. Distractor rules (the paper's three-rule pattern)

Generate distractors deliberately, one per rule, instead of asking for "3 wrong answers":

1. **Same-category confusion** — another plausible action/object from the same category as
   the key (e.g. another greeting pattern, another email habit).
2. **Common misconception** — the belief a student who half-understands actually holds
   ("the address already shows who I am", "unread counts are cosmetic").
3. **Plausible-but-wrong fix** — a real action that addresses the wrong root cause
   ("put your student number in every subject line").

Every distractor must be *falsifiable* — a student who fully understands the concept can
rule it out with confidence. Avoid ambiguous options that are arguably half-right.

## 3. No surface cues

- **Length parity**: the correct option must NOT be the longest. Keep all options within
  ±30% of each other's length. Move the explanation/justification into `feedback`, not
  into the correct option's text.
- **No joke options** ("You are popular") — they reduce a 3-option item to a coin flip.
- **Position carries no signal**: the /go player shuffles option order at render time,
  but still vary the position of `"correct": true` in the JSON (defence in depth, and
  other harnesses may not shuffle).
- Avoid "all/none of the above", absolutes ("always", "never") only in wrong options,
  and grammatical mismatches between stem and options.

## 4. Probe questions (the "tree" in TreeQuestion)

Each scenario should carry a `probe`: a *simpler, lower-Bloom-level* question on the same
concept, shown only when the student answers the main question wrongly. The probe locates
the actual gap — did they fail the application, or do they lack the underlying concept?

```json
"probe": {
  "question": "Quick check: what is an email alias?",
  "options": [ { "text": "...", "correct": true, "feedback": "..." }, ... ]
}
```

Probe stems should test *Remember/Understand* ("what is X?", "which part does Y?") while
the main question tests *Apply/Analyze*. Every probe option needs feedback too.

## 5. Feedback discipline

- Correct-option feedback: confirm *why*, restating the principle in one sentence.
- Distractor feedback: name the misconception and correct it — never just "wrong".
- Feedback is where the teaching happens; options are where the diagnosis happens.

## 6. Validate before shipping (human-in-the-loop)

LLM-generated items are prone to: wrong answer annotations, multiple defensible answers,
ambiguous distractors, and out-of-scope concepts. Before committing a learn.json:

- [ ] Exactly one option per item has `"correct": true`, and it is defensibly the only one.
- [ ] Correct option is not the longest; no option is a throwaway.
- [ ] Each distractor maps to rule 1, 2 or 3 above.
- [ ] Probe present and one Bloom level below the main stem.
- [ ] Feedback present on every option (scenarios and probes).
