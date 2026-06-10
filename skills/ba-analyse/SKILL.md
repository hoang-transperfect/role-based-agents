---
name: ba-analyse
description: >
  Handles Business Analysis steps 5–6 — analysing and validating requirements, then prioritising
  them. Invoke when a BA has elicitation findings to organise, validate, and rank, or when the
  task's ## Plan marks Step 5 or 6 as next. It interprets and confirms requirements with the user,
  applies prioritisation techniques (MoSCoW, Kano, and others as they fit), and produces a
  validated, prioritised requirements list in the task folder under the real project's
  ba-assistant-artifacts, then ticks the
  matching checklist boxes. Run after ba-elicit so it works from documented findings.
---

# ba-analyse

Covers **Step 5 (Analyse & Validate Requirements)** and **Step 6 (Prioritise Requirements)**.
This is where raw findings become a trustworthy, ranked set of requirements. The two risks it
guards against: requirements that were never actually confirmed with stakeholders (so they're
assumptions), and a flat list with no agreed priority (so everything looks equally urgent). The
work is collaborative and often involves healthy debate with the BA.

## Where things live

- Read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`).
- Write the deliverable to
  `<real_project_path>/ba-assistant-artifacts/tasks/<task-id>/prioritised-requirements.md`.
- Tick Steps 5–6 in the task file's `## Plan` checklist when confirmed.

---

## The skill contract

### Inputs
- The `elicitation/findings-log.md` (and its stored raw inputs) from `ba-elicit`.
- The `related-context.md` artifact and the Plan's **Problem framing** (objectives + measurable
  success criteria) — the yardstick for judging each requirement's value and goal-fit.

### Input Acceptance Criteria
- There are documented findings to analyse. If findings are thin or missing, hand back to
  `ba-elicit` — analysis can't manufacture requirements that weren't elicited.
- **Context validation has PASSED** in the elicitation findings-log (no unresolved conflicts with
  the existing backlog). If it's BLOCKED or absent, hand back to `ba-elicit` — never start analysis
  on unvalidated context. This gate holds on a **resumed** session too: re-read the status, don't
  assume a previous chat validated it.

### Outputs
- `prioritised-requirements.md` — the organised, validated, and ranked requirements, each showing
  its priority and the rationale.

### Output Quality Criteria
- Findings are **organised and de-duplicated** into clear, distinct requirements. Conflicts —
  between stakeholders **or with the existing backlog** — are surfaced and resolved; any that can't
  be settled from the requirements are **escalated to the user for a decision**, never averaged
  away or silently chosen. (`ba-elicit` catches most backlog conflicts live; this is the final net.)
- **Terminology is reconciled:** different words for one concept (or one word for two) across
  stakeholders is a conflict like any other — resolve it by picking one term, and note the
  decision so `ba-document` records it in the glossary.
- Each requirement is **validated** — confirmed accurate with the user/stakeholders, not just
  inferred — and the record names **who validated it** (e.g. "yes (PM)"), for the audit trail.
  Mark anything still unconfirmed as provisional.
- Each requirement carries a **priority from an explicit method** — MoSCoW (Must/Should/Could/
  Won't) by default; Kano when satisfaction/delight is the question; note the method used.
- Priority rationale references **value, urgency, feasibility, and alignment with the objectives /
  success criteria** in the Plan's Problem framing — so the ranking can be defended, not just
  asserted. A Must that advances no stated objective is a flag to re-examine.
- Non-functional and transition requirements are analysed and prioritised alongside functional
  ones, not parked.

## Techniques available
MoSCoW and Kano for prioritisation; SWOT and Root-Cause Analysis when you need to interrogate
*why* a requirement matters or whether it addresses a real problem. Use what fits the question —
don't run every technique for its own sake.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If findings are insufficient, hand back to
`ba-elicit` — do not assume. (Tree already clean from the session-start guard.)

### Gate 2 — Process
Adapt to the **work mode** in `## Plan`:
- **from-scratch** — all findings are new; organise into a fresh requirement set and a first MoSCoW
  baseline.
- **develop** — reconcile each finding against the existing `ba-requirement/` backlog (is it new,
  a duplicate, or an extension of an existing story?) and rank it **relative to** what's already
  there. If reconciliation surfaces a conflict that can't be settled, stop and ask the user.
- **maintain** — this is **impact analysis**: trace the change onto the affected story/requirement,
  map the ripple (dependent stories, NFRs), and weigh by urgency + risk rather than a full re-rank.

Then work through the findings **with** the BA: organise, interpret, and challenge. Debate
priorities openly — disagree where the evidence warrants, and ask the user to confirm each
requirement's accuracy (recording who) and rank. Draft:

```markdown
# Prioritised Requirements — <project>
_Prioritisation method: MoSCoW (and Kano where noted)_
| # | Requirement | Type (functional / NFR / service / transition) | Validated? (by whom) | Priority | Rationale (value · urgency · feasibility · goal-fit) |
|---|-------------|------------------------------------------------|----------------------|----------|------|
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that requirements are validated (not
assumed) and priorities are justified. Improve if short of the bar (ask the user to confirm where
needed; never assume). When it meets the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write to the task folder (`ba-assistant-artifacts/tasks/<task-id>/`), tick
   Steps 5–6 in `## Plan` (links + **Next step**), then hand off to `commit-work`.
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill`.

You author the list as the BA assistant, on the user's behalf, for the audit record.

---

## Handoff
The prioritised requirements feed `ba-document` (Step 7), which turns them into the formal agile
backlog — the Epic → Feature → User Story tree in `ba-requirement/`.
