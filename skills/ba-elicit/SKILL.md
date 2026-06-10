---
name: ba-elicit
description: >
  Handles Business Analysis steps 3–4 — conducting elicitation and documenting findings — by
  acting as the BA's live elicitation assistant. The real session is between the BA (human) and a
  stakeholder; the BA relays what the stakeholder says (answers, replies, documents) bite by bite,
  often across several turns or chats. Invoke when a BA is running or processing elicitation, or
  when the task's ## Plan marks Step 3 or 4 as next. It stores each raw stakeholder input in the
  task folder, structures it into traceable findings, tracks coverage against the ba-discover
  gathering guide (what's covered vs still to elicit), and suggests the next questions to close the
  gaps. Run after ba-discover so there's a guide to elicit against.
---

# ba-elicit

Covers **Step 3 (Conduct Elicitation Sessions)** and **Step 4 (Document Observations & Findings)**.
The real session happens between the BA and the stakeholder — this skill is the **BA's assistant
during and after** it. The BA relays what the stakeholder said — an answer, a reply, an attached
document — **bite by bite, not all at once**. The skill's job: help the BA make sense of it,
**structure it into traceable findings, track what's now covered vs still open against the
gathering guide, and suggest the next questions** to close the gaps.

Because all state lives in the task folder, this loop can pause and resume across chats — a later
session reads the stored raw inputs, findings, and coverage and picks up where it left off.

## Where things live

- Read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`).
- `<real_project_path>/ba-assistant-artifacts/tasks/<task-id>/elicitation/`
  - `raw/` — the stakeholder's **actual inputs, stored verbatim** as they arrive (pasted answers,
    replies, transcripts, attached docs). This is the audit source; never paraphrase it away.
  - `findings-log.md` — the structured findings derived from the raw inputs, plus a coverage view.
- Tick Steps 3–4 in the task file's `## Plan` checklist when elicitation is confirmed complete-enough.

---

## The skill contract

### Inputs
- The **gathering guide** (`gathering-plan.md`) and `stakeholder-register.md` from `ba-discover` —
  these define the themes/coverage to elicit against.
- The `related-context.md` artifact (the starting point for Document Analysis).
- The stakeholder's inputs the BA relays — **any format, provided incrementally** across turns.

### Input Acceptance Criteria
- A gathering guide exists, so coverage can be tracked. If not, hand back to `ba-discover`.
- There is at least one piece of stakeholder input to work with — **or** the BA wants help opening
  a session, in which case start from the guide's opening questions. Never invent stakeholder
  answers; if nothing has been relayed yet, ask the BA for it or offer the opening questions.

### Outputs
- `elicitation/raw/…` — the stored stakeholder inputs, verbatim.
- `elicitation/findings-log.md` — structured, traceable findings with a current coverage view.

### Output Quality Criteria
- **Raw inputs are stored faithfully and verbatim** — they are the audit source for every finding.
- Every finding **traces to its raw source** and carries a **type** (functional / NFR / service /
  transition).
- **Coverage is explicit and current:** each theme is marked `covered`, `open`, or `deferred`
  (a TODO for a future task, when the BA stops without it). Open items are never silently dropped —
  they're pursued or explicitly deferred.
- Faithful capture: ambiguity becomes an **open question + a suggested follow-up**, never a guess.
- **Every turn ends with a covered / open / suggested-next report** so the BA always knows where
  the session stands and what to ask next — that running status is the assistant's core value, not
  just the final record.
- The BA's **volunteered input is captured too**, not only answers to suggested questions; new
  topics become new coverage themes.
- **Context is validated against the existing backlog** before elicitation completes: findings are
  checked for conflict/duplication with `ba-requirement/`, every conflict is resolved (or decided
  by the user), and the **Context validation status is PASSED and persisted** in the findings-log.
  This is what stops a resumed session from skipping ahead to analysis on unvalidated context.

---

## The 3-gate flow

### Gate 1 — Input
Check inputs against the Input Acceptance Criteria. No gathering guide → hand back to `ba-discover`.
Nothing relayed yet → ask the BA for stakeholder input or offer the guide's opening questions. Do
not fabricate. (Tree already clean from the session-start guard.)

### Gate 2 — Process (the elicitation loop)
This runs as a **loop across turns** (and can resume in a later chat — state is in the task folder):

1. Establish or refresh the **coverage checklist** from the gathering guide (its themes/questions
   per session).
2. Take **whatever the BA sends** — an answer to a suggested question, *or something new they've
   learned* (a fresh topic, a volunteered detail, a document). Capture all of it, not just replies
   to your questions:
   a. **Store it verbatim** in `elicitation/raw/`.
   b. **Structure it** into findings — trace each to its raw source, set its type, stay faithful.
      If it raises a theme that wasn't in the guide, **add that theme** to the coverage checklist.
   c. **Update coverage** — mark what's now covered; record new open questions the input revealed.
3. **End every turn with a short status report to the BA, then wait for their reply:**
   - ✅ **Covered:** <themes now done>
   - ⬜ **Still open:** <themes remaining>
   - 💡 **Suggested next:** <the questions to take back to the stakeholder>
4. Repeat until **all themes are covered**.

**If the BA wants to stop while themes are still open** (the stakeholder can't give more right
now), don't block them. Mark each remaining theme as **`deferred` — a TODO for a future task**,
with the outstanding question recorded, so it's carried forward rather than lost.

5. **Context-validation checkpoint — before the BA moves to another stakeholder or finishes
   elicitation, run this; it is a hard gate.** Call **`ba-scan-context`** to refresh the existing
   context for the areas just elicited, then check every new finding against the existing
   `ba-requirement/` backlog for **conflict or duplication**. For each conflict:
   - surface it to the BA and **resolve it** — ideally by following up with the stakeholder *while
     they're still in the session*, or by **escalating to the user for a decision** when it can't
     be settled from the requirements alone;
   - record the conflict and its resolution.
   Record the outcome as a **Context validation** status in the findings-log. Elicitation may only
   move on (next stakeholder, or to `ba-analyse`) once the status is **PASSED** — no unresolved
   conflicts. A conflict is never `deferred`; only *coverage* may be deferred.

`findings-log.md` shape:

```markdown
# Findings Log — <task>

## Context validation
**Status:** PASSED / BLOCKED (unresolved conflict)   **Checked against:** ba-requirement/ on <date>
| Conflict / duplicate with existing | Existing item | Resolution (or decision needed) |
|------------------------------------|---------------|---------------------------------|
| <what clashes> | EPIC/FEAT/US-id | <how resolved · who decided> |

## Coverage (against the gathering guide)
| Theme / question | Status | Outstanding follow-up |
|------------------|--------|-----------------------|
| <theme from guide> | covered / open / deferred (TODO → future task) | <what still to ask> |

## Findings
| # | Finding | Raw source | Type (functional / NFR / service / transition) | Open? |
|---|---------|------------|------------------------------------------------|-------|
```

### Gate 3 — Output
Raw inputs are saved as they arrive. Elicitation is **complete-enough** when every theme is either
`covered` or `deferred` (a TODO for a future task) **and Context validation is PASSED** (no
unresolved conflicts with the existing backlog). Then:
1. Present the current `findings-log.md` + coverage + validation status and ask the BA to confirm.
   Call out any `deferred` themes explicitly — they're TODOs to raise as a future task, not silent
   gaps. If validation is still BLOCKED, you are **not** complete — resolve the conflict first.
2. **If confirmed** → the files are written under `elicitation/`; tick Steps 3–4 in `## Plan`
   (links + **Next step**), then hand off to `commit-work` (real project repo).
3. **If not satisfied** → improve with the BA until confirmed, commit, then hand off to
   `improve-skill`.

You author the structured records as the BA assistant, on the user's behalf, for the audit record;
the raw inputs are the stakeholder's own words, kept intact.

---

## Handoff
The `findings-log.md` feeds `ba-analyse` (Steps 5–6), which organises, validates, and prioritises
what elicitation surfaced. Coverage marked still-open is a signal more elicitation is needed before
analysis can be trusted.
