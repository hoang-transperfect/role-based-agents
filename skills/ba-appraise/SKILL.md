---
name: ba-appraise
description: >
  Builds the business case before requirements work starts — appraises the options for addressing
  a problem (always including do-nothing), weighs each on cost, benefit, risk, and feasibility, and
  recommends one for the user to decide on. Invoke at the very start of an effort, before ba-plan,
  whenever it isn't yet settled WHETHER to act or WHICH option to take — e.g. "is this worth doing?",
  "should we build or buy?", "what are our options?", a new initiative, or any sizable investment.
  Skip it only when the option is already chosen (often the case for small maintain changes). Run
  after ba-scan-context so the options reflect what already exists.
---

# ba-appraise

The most expensive requirements are the ones gathered for the wrong solution — or for a change that
shouldn't have been made at all. This skill front-loads that judgement: before any requirements
work, it weighs the realistic **options** for solving the problem (including doing nothing) and
helps the user decide which one is worth pursuing. It answers *whether* and *which*, so `ba-plan`
can get on with *how*.

This is where a senior BA earns their title — not by documenting a pre-chosen solution, but by
testing whether the investment is justified and surfacing options the user hadn't considered.

## Where things live

- Read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`).
- Write the deliverable to
  `<real_project_path>/ba-assistant-artifacts/tasks/<task-id>/options-appraisal.md`.
- This runs **before** `ba-plan`, so the `## Plan` checklist may not exist yet — this skill does
  not tick it. It feeds `ba-plan`. Assumptions and risks it surfaces are recorded in the
  project-wide RAID log (`<real_project_path>/ba-assistant-artifacts/raid-log.md`).

---

## The skill contract

### Inputs
- The business **problem or opportunity** (from the user / task description) — the underlying need,
  not a pre-selected solution.
- The `related-context.md` artifact from `ba-scan-context` — what already exists, and the
  constraints any option must live within.
- Known constraints the user can state: budget, time, regulatory, strategic direction.

### Input Acceptance Criteria
- The **problem or opportunity is stated as a need**, not only as a solution request. If the user
  has only named a solution ("build feature X"), surface the underlying problem first — you can't
  appraise options against a solution. Ask; never assume the rationale.
- Enough context exists to identify genuine options. If little is known, run (or hand off to)
  `ba-scan-context` first.

### Outputs
- `options-appraisal.md` — the problem, the options considered (including do-nothing), each
  assessed on cost / benefit / risk / feasibility / strategic fit, a recommendation with rationale,
  and the user's recorded decision.

### Output Quality Criteria
- **Do-nothing (the baseline) is always an option.** Without the cost of inaction, you can't show
  any change is worth its cost. Include it every time.
- There are **at least two or three genuine options**, not strawmen propped up to justify a
  foregone conclusion. Build vs buy vs configure vs change-the-process are common axes.
- Each option is assessed on **cost, benefit, risk, feasibility, and strategic fit** — comparably,
  so they can be weighed against each other.
- **Benefits are stated measurably where possible** and tied to the business objectives. These
  expected benefits set up `ba-plan`'s success criteria and become the yardstick `ba-evaluate`
  measures realised benefits against later — so they must be concrete, not aspirational.
- The **recommendation is justified** — why it best serves the objectives relative to cost and
  risk — and the **trade-offs it accepts** are named.
- The appraisal is **honest**: it never manufactures options or inflates benefits to rationalise a
  decision already made. If the evidence points to do-nothing, say so. (Never invent.)
- **Assumptions and key risks are captured** and recorded in the RAID log, so they're tracked and
  validated rather than forgotten.

## Techniques available
Cost-benefit analysis and feasibility assessment by default; SWOT to interrogate an option's
strengths/weaknesses; MoSCoW-style must-haves to screen options; root-cause analysis to confirm
the problem is real before appraising solutions. Use what the decision needs — not every technique.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If only a solution is stated, draw out the
underlying problem with the user; if context is thin, run `ba-scan-context` first. **Ask, never
assume.** (The working tree is already clean — the before-work guard runs once at session start via
`gather-needs`, not here.)

### Gate 2 — Process
Brainstorm options **with** the user — including the baseline and at least one they may not have
considered. For each, assess cost, benefit (measurable, tied to objectives), risk, feasibility, and
strategic fit. Debate openly; challenge optimistic benefits and hand-wavy costs. Draft:

```markdown
# Options Appraisal — <problem / opportunity>
_Appraised: <date>_

## Problem / opportunity
<the underlying need and for whom — not a pre-chosen solution>

## Options considered
| # | Option | Description | Cost (effort / £) | Benefits (measurable) | Risks | Feasibility | Strategic fit |
|---|--------|-------------|-------------------|------------------------|-------|-------------|---------------|
| 0 | Do nothing (baseline) | <what happens if we don't act> | — | <cost of inaction> | <…> | — | — |
| 1 | <option> | <…> | <…> | <…> | <…> | <…> | <…> |

## Recommendation
**Recommended:** Option <n> — <why it best serves the objectives vs cost / risk>
**Trade-offs accepted:** <what we give up by choosing it>

## Decision
<chosen option> · decided by <name / role> on <date>  (proceed / defer / reject)

## Assumptions & key risks  (→ RAID log)
- <assumption to validate later> / <risk to track>
```

### Gate 3 — Output
Check the draft against the Output Quality Criteria — especially that do-nothing is present,
options are genuine, and benefits are measurable and honest. Improve if short of the bar (ask the
user where you need their input; never assume). When it meets the bar:
1. Present it and ask the user to confirm the appraisal and **record their decision**.
2. **If confirmed** → write `options-appraisal.md`, append the assumptions/risks to the RAID log,
   then hand off to `commit-work` (real project repo).
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill`.

You author the appraisal as the BA assistant, on the user's behalf, for the audit record; the
decision is the user's.

---

## Handoff
- **If the decision is proceed** → `ba-plan` takes the chosen option and frames the problem +
  tailors the requirements-gathering plan for it. The expected benefits become the basis of the
  plan's measurable success criteria.
- **If defer or reject** → the BA effort pauses or stops; the appraisal stands as the audit record
  of why.
- The expected benefits also feed `ba-evaluate` at the end of the lifecycle, which checks whether
  they were actually realised.
