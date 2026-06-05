---
name: ba-plan
description: >
  Lays out the Business Analysis requirements-gathering plan for a task and owns the
  authoritative progress checklist that every other BA skill reads and ticks. Invoke this when
  a BA is starting requirements work on a task, when they ask "what's the plan", "where are we",
  or "what's next" in a BA effort, or whenever the task file has no BA progress checklist yet.
  It discusses with the BA which of the 9 BA steps are actually needed (not every effort needs
  the full process), then writes a tailored, auditable checklist into the task file's ## Plan,
  framed around the specific business problem. Run ba-scan-context first so the plan builds
  on existing context, and run this before the step skills (ba-discover, ba-elicit,
  ba-analyse, ba-document, ba-govern), since they tick the checklist this skill creates.
---

# ba-plan

This skill turns a task into a navigable BA plan. Its real value is the **progress checklist**:
a single, auditable record in the task file of which BA steps are done, what artifact each
produced, and what's next. Because the state lives in the file (not the conversation), a BA can
stop and resume anytime, and any step skill can "jump in" by reading where the work stands.

This skill **owns** that checklist. The step skills only tick their own box and link their
artifact; they never restructure the plan.

## Where the work lives

The checklist lives in the task file's `## Plan` section:
`<project>/in-progress-tasks/<task-id>.md` (created by `create-task`). Read `real_project_path`
from the project's `resource.md` frontmatter; under it the real project holds two BA areas:

- `<real_project_path>/ba-artifacts/<task-id>/` — the **working trail** for this task (per-task
  folder): related-context, stakeholder register, findings, prioritised requirements, sign-off.
- `<real_project_path>/ba-requirement/` — the **formal backlog** other teams consume, an agile
  Epic → Feature → User Story tree in markdown. This persists across tasks; tasks create or
  extend parts of it.

(The task file is the assistant's bookkeeping; both BA areas are real deliverables, so they live
with the real project.)

---

## The skill contract

Every BA skill — including this one — declares what it consumes and produces, and the bar each
must meet. This makes the gates below objective rather than vibes.

### Inputs
- The task file (`<project>/in-progress-tasks/<task-id>.md`).
- The business context / problem the task is meant to solve (from the task description, project
  `resource.md`, or the user).
- The **`related-context.md` artifact** (in `<real_project_path>/ba-artifacts/<task-id>/`) from
  `ba-scan-context`, if present — so the plan reflects what's already known and targets the gaps.

### Input Acceptance Criteria
- A task file exists for this work.
- The **problem and its objectives** can be stated — not just a solution request. This is the
  "context framing" check: planning requirements before understanding the problem (and what
  success looks like) risks building the wrong thing well. If the problem, objectives, or success
  criteria are unstated or vague, that's a gate failure → frame them with the user before planning.
- Existing context has been discovered. If there's no `related-context.md` artifact yet, run (or
  hand off to) `ba-scan-context` first, so the plan isn't drawn up blind to prior work. If the
  user declines, note that the plan was made without a context scan.

### Outputs
- A `## Plan` section in the task file containing a **tailored** BA progress checklist (template
  below), with the business problem stated at the top.

### Output Quality Criteria
- **Problem framing is complete and measurable** at the top of the plan: the problem, the
  objectives, **measurable success criteria**, scope (in/out), and key constraints & assumptions.
  Vague success criteria ("make it better") are a gate failure — push for a metric. This framing
  is the yardstick later steps (`ba-analyse`, `ba-document`) measure value and success against, so
  it must be crisp now, not discovered at Step 7.
- The **work mode is stated** — `from-scratch`, `develop`, or `maintain` — because it's the main
  driver of which steps are needed (see Process). If the mode isn't obvious from the request, ask.
- The checklist reflects a **deliberate decision about which steps this effort needs**, consistent
  with the work mode. Steps that apply are listed with a status box and an artifact slot; steps
  that were consciously skipped remain listed but are marked `~~skipped~~ (reason)` — never
  silently dropped, so the audit trail shows the scope decision and its rationale.
- The plan notes the cross-cutting concerns so later steps don't forget them: non-functional
  requirements, service-level/end-to-end perspective, and continuous stakeholder engagement
  beyond sign-off.
- It is unambiguous which step is next.

---

## The 3-gate flow

Every BA skill runs this same flow. The point is: never start on bad input, never finish on bad
output, and never assume — ask.

### Gate 1 — Input

Read the inputs and check them against the Input Acceptance Criteria above.
- Meets AC → proceed.
- Falls short → improve the input first. If improving needs information you don't have (e.g. the
  business problem is unclear), **ask the user**. Do not assume.

(The working tree is already clean — the before-work guard runs once at session start via
`gather-needs`, not here.)

### Gate 2 — Process

**First, frame the problem with the user.** A plan is only as good as the problem it serves. Agree,
in measurable terms: the **problem** (and for whom), the **objectives**, the **success criteria**
(a metric, not a mood), **scope** in/out, and the key **constraints & assumptions**. This is the
yardstick `ba-analyse` and `ba-document` will measure value and success against — so it has to be
crisp now, not discovered at Step 7. If the user can't yet state a measurable success criterion,
that's a finding in itself: surface it.

**Then settle the work mode with the user**, because it's the strongest signal for which steps
are needed:

- **from-scratch** — greenfield product/area, `ba-requirement/` is empty. Expect the full process:
  map stakeholders, elicit broadly, analyse, build the Epic→Feature→Story tree from zero.
- **develop** — a new feature/epic on an existing product. Stakeholders mostly known; the existing
  `ba-requirement/` backlog and code are the main inputs. Expect: read the backlog, focused
  elicitation, analyse against what exists, extend the tree.
- **maintain** — a fix or small change to an existing requirement. Expect: find the affected
  story, light clarification, impact analysis, update it in place; change-log and RTM are central.

Detect the mode from the request; if it's unclear, ask. Record it at the top of the plan.

**Then decide scope with the user.** Walk the steps and, for each, agree *needed* or *skipped, and
why* — using the mode as the default and the `related-context.md` artifact to refine it (if
context already covers something, the matching step may shrink or drop). This conversation is the
heart of the skill; don't pre-decide it mechanically from the mode, and don't pad the plan with
steps that add no value here.

Draft the plan **with** the user, framed around their business problem. Keep every step visible
for the audit trail — applicable ones as open boxes, skipped ones struck through with a reason:

```markdown
## Plan

**Work mode:** develop  (from-scratch / develop / maintain)

### Problem framing
- **Problem:** <what's wrong / the need, and for whom>
- **Objectives:** <the outcomes we're after>
- **Success criteria (measurable):** <metrics/targets that prove it worked>
- **Scope:** In — <…> · Out — <…>
- **Constraints & assumptions:** <hard limits; assumptions to validate later>

### BA Progress Checklist
- ~~Step 1 — Identify Stakeholders~~             → skipped (develop: stakeholders already known)
- [ ] Step 2 — Plan Requirements Gathering       → <artifact link>
- [ ] Step 3 — Conduct Elicitation Sessions      → <artifact link>
- [ ] Step 4 — Document Observations & Findings  → <artifact link>
- [ ] Step 5 — Analyse & Validate Requirements   → <artifact link>
- [ ] Step 6 — Prioritise Requirements           → <artifact link>
- [ ] Step 7 — Document Requirements (epic/feature/story) → <artifact link>
- [ ] Step 8 — Review & Stakeholder Sign-Off     → <artifact link>
- [ ] Step 9 — Manage Changes & Maintain RTM     → <artifact link>

**Cross-cutting (apply throughout, don't defer):**
- Non-functional requirements — performance, usability, accessibility, security.
- Service-level perspective — end-to-end journeys, governance, support models, not only features.
- Continuous stakeholder engagement — keep validating after sign-off; requirements evolve.

**Next step:** <the first applicable step>.
```

(The Step 1 strikethrough above is just an illustration of a `develop`-mode skip — decide each
step's status with the user; any step may be needed or skipped depending on mode and effort.)

Map the skill that handles each step so the BA knows where to go next:
Steps 1–2 → `ba-discover` · 3–4 → `ba-elicit` · 5–6 → `ba-analyse` · 7 → `ba-document` ·
8–9 → `ba-govern`.

### Gate 3 — Output

Check the drafted plan against the Output Quality Criteria. If it falls short, improve it (ask
the user if you need their input — never assume). When it meets the bar:
1. Present it and ask the user to confirm.
2. **If confirmed as-is** → write it to the task file, then hand off to `commit-work` to
   commit the confirmed plan.
3. **If the user is not satisfied** → improve the plan with them until they confirm, commit the
   confirmed plan, then hand off to `improve-skill` to fold the lesson back into *this* skill.

You are the author of the plan (BA assistant), writing on the user's behalf for the audit record.

---

## How step skills use this checklist

When a step skill finishes and the user confirms its artifact, that skill:
- ticks its box (`[ ]` → `[x]`), fills the artifact link, and updates **Next step**, then
- commits via `commit-work`.

It does not otherwise alter the plan. If the plan structure itself needs to change, that comes
back to `ba-plan`.
