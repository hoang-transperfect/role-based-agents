---
name: ba-evaluate
description: >
  Closes the loop after delivery — measures whether the solution actually achieved the objectives
  and success criteria the plan set, and whether the business case's benefits were realised. Invoke
  once a solution (or a meaningful increment) is live and outcomes can be observed, typically as a
  follow-up task after ba-govern. Triggers: "did it work?", "did we get the benefits?", "post-
  implementation review", "evaluate the outcome", "measure success", or the ## Plan's closing
  evaluate step. Produces a benefits-evaluation comparing targets to actuals, with lessons and
  follow-up actions. It is the natural final step of the BA lifecycle.
---

# ba-evaluate

`ba-plan` insists on measurable success criteria; the business case promises benefits. Without this
step, nobody ever checks whether either came true — the lifecycle ends at sign-off and the
organisation never learns. This skill measures the delivered solution against the objectives and
the expected benefits, explains the variance honestly, and turns what's found into follow-up
action or a clean close.

Because outcomes take time to appear, evaluation usually runs **after delivery** — often as its own
later task, once the solution has been live long enough to measure.

## Where things live

- Read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`).
- Write the deliverable to
  `<real_project_path>/ba-assistant-artifacts/tasks/<task-id>/benefits-evaluation.md`.
- Tick the closing evaluate step in the task file's `## Plan` checklist when confirmed (if this
  evaluation is its own follow-up task, that task's plan holds the step).

---

## The skill contract

### Inputs
- The Plan's **Problem framing** — objectives and **measurable success criteria** — the primary
  yardstick.
- The `options-appraisal.md` from `ba-appraise`, if it exists — the **expected benefits** to check
  against what was realised.
- The **actual outcomes**: metrics, usage data, stakeholder feedback on the live solution (from the
  user / stakeholders / data).
- The signed-off backlog (`ba-requirement/`) and RTM — what was actually delivered.

### Input Acceptance Criteria
- **Measurable success criteria exist** (from `ba-plan`). If the original plan set none, evaluation
  can only be qualitative — flag that gap explicitly as a lesson, so future planning sets criteria.
- The solution, or a meaningful increment, is **live and observable**. If nothing is in use yet,
  it's too early — defer and say when to revisit. Never invent outcomes that haven't happened.

### Outputs
- `benefits-evaluation.md` — each objective/success criterion vs its actual outcome (met / partial /
  not met, with evidence), benefits-realisation against the business case, unintended consequences,
  lessons learned, and concrete follow-up actions.

### Output Quality Criteria
- **Every success criterion from the Plan is evaluated** against actual evidence, with the result
  (met / partial / not met) and the **source of the measurement** named. An unmeasured criterion is
  reported as such, not quietly skipped.
- **Benefits from the business case are checked** against what was realised — over- or
  under-delivered, and *why*.
- **Variance is explained honestly.** Where data is missing or inconclusive, say so plainly; never
  claim a success the evidence doesn't support. (Never invent.)
- **Unintended consequences** — positive and negative — are surfaced, not just the planned metrics;
  the most important effects are often the ones nobody set a target for.
- **Lessons learned** are captured for future efforts.
- **Follow-up is concrete:** each shortfall leads to a new requirement / change (→ `ba-plan` or
  `ba-govern`) or to an explicit decision to accept and close.

## Techniques available
Benefits realisation and KPI/target-vs-actual comparison by default; before/after baselining;
root-cause analysis on shortfalls to tell a flawed solution from flawed delivery from a flawed
assumption. Use what the variance demands.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If success criteria were never set, flag it
and proceed qualitatively; if nothing is live yet, defer. **Ask, never assume.** (Tree already
clean from the session-start guard.)

### Gate 2 — Process
Gather the actual outcomes **with** the user and stakeholders, compare them to the targets, and
analyse the variance — don't accept a number without knowing where it came from. Draft:

```markdown
# Benefits Evaluation — <project / increment>
_Evaluated: <date> · Solution live since: <date>_

## Objectives vs outcomes
| Objective / success criterion (from Plan) | Target | Actual | Result | Evidence / source |
|-------------------------------------------|--------|--------|--------|-------------------|
| <criterion> | <target> | <measured> | met / partial / not met | <where the number came from> |

## Benefits realisation (vs business case)
| Expected benefit (appraisal) | Realised? | Variance & why |
|------------------------------|-----------|----------------|
| <benefit> | yes / partial / no | <explanation> |

## Unintended consequences
- <a positive or negative effect that wasn't planned for>

## Lessons learned
- <what to do differently next time>

## Follow-up actions
- <new requirement / change → ba-plan or ba-govern> · or: <benefits realised — accept and close>
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially honest variance and evidence-backed results.
Improve if short of the bar (ask the user where you need their data; never assume). When it meets
the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write `benefits-evaluation.md`, tick the evaluate step in `## Plan`, then hand
   off to `commit-work` (real project repo).
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill`.

You author the evaluation as the BA assistant, on the user's behalf, for the audit record.

---

## Handoff
- **Shortfalls or new needs** → hand back to `ba-plan` (a new effort) or `ba-govern` (a requirement
  change), so the loop continues rather than ending on an unmet objective.
- **Benefits realised** → record acceptance and close; the evaluation is the audit record that the
  effort delivered its intended value.
- Lessons about the **BA process itself** (not this project) → `improve-skill`.
