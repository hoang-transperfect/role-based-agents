---
name: ba-govern
description: >
  Handles Business Analysis steps 8–9 — getting stakeholder review and sign-off, then maintaining
  traceability and managing change through delivery. Invoke when a BA needs to record approval,
  build or update the Requirements Traceability Matrix (RTM), track requirement changes, or when
  the task's ## Plan marks Step 8 or 9 as next. It records a per-task sign-off, and maintains an
  RTM and change log in the real project's ba-requirement folder that trace each requirement back
  to its source and record its status and changes, ticks the checklist boxes, and keeps
  requirements aligned as they evolve — including continued validation after sign-off.
---

# ba-govern

Covers **Step 8 (Review & Stakeholder Sign-Off)** and **Step 9 (Manage Changes & Maintain
Traceability)**. This step makes the requirements auditable and keeps them honest over time:
approval is captured, every requirement is traceable **back to its origin**, and changes to
requirements are tracked rather than silently absorbed. Sign-off is **not** the end — requirements
keep being validated and adjusted as understanding evolves.

**Scope boundary:** the BA's responsibility ends at the **signed-off, change-managed
requirement**. What happens next — design, build, test — is owned by the delivery teams and
tracked in their tools (Bitbucket). This skill does **not** trace delivery status; doing so would
duplicate Bitbucket and claim work that isn't the BA's.

## Where things live

- Read `real_project_path` from the project's `resource.md` frontmatter.
- **Sign-off record** (per task/increment) → `ba-artifacts/<task-id>/sign-off.md`.
- **RTM** and **change log** (living, product-wide) → `ba-requirement/RTM.md` and
  `ba-requirement/change-log.md`. They span all tasks and grow as requirements evolve.
- Tick Steps 8–9 in the task file's `## Plan` checklist when confirmed. Step 9 is ongoing — the
  RTM and change log are living documents.

---

## The skill contract

### Inputs
- The `ba-requirement/` backlog from `ba-document` (epics/features/stories with IDs).
- The stakeholder register (who holds sign-off authority).
- For ongoing work: the existing `RTM.md` and `change-log.md`, plus any proposed or observed
  **changes to requirements**.

### Input Acceptance Criteria
- Documented, ID'd stories exist to review and trace. If items have no unique IDs, hand back to
  `ba-document` — an RTM is impossible without them.
- For sign-off: the stakeholders with approval authority are known. If not, hand back to
  `ba-discover`.

### Outputs
- `ba-artifacts/<task-id>/sign-off.md` — what was presented, ambiguities resolved, and the formal
  approval (who approved what, when; full or partial/conditional).
- `ba-requirement/RTM.md` — each requirement traced **back to its source**, with its requirement
  status and dependencies.
- `ba-requirement/change-log.md` — requirement changes over time, each with status and impact.

### Output Quality Criteria
- The sign-off record shows stories were **presented and ambiguities resolved** before approval,
  and captures **who approved what and when**. It supports **partial/conditional** sign-off (e.g.
  approve the Musts, defer the Coulds) rather than forcing all-or-nothing.
- The RTM links **every** requirement (by ID) **back to its source** (finding / business goal),
  with its **requirement status** (proposed / validated / signed-off / changed / deferred /
  superseded) and dependencies. It deliberately does **not** track design/build/test status — that
  belongs to the delivery teams in Bitbucket; the BA's traceability stops at the signed-off
  requirement.
- The change log tracks each requirement change with **status and impact** (on other
  requirements), so the backlog's evolution is reconstructable.
- **Continuous engagement is built in:** the record provides for revisiting requirements as needs
  change through delivery — requirements aren't "locked" and forgotten.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If stories lack IDs or sign-off authority is
unknown, hand back to `ba-document` / `ba-discover` — do not assume. (Tree already clean from the
session-start guard.)

### Gate 2 — Process
Adapt to the **work mode** in `## Plan`: `from-scratch` establishes the RTM and runs first
sign-off; `develop` extends the RTM with the new requirements and signs off the increment;
`maintain` centres on the change log and RTM status updates with a lighter sign-off. Help the BA present
stories to the right stakeholders, capture clarifications, and record approval; then build or
update the RTM and change log. Draft:

```markdown
# Sign-Off Record — <task-id>
**Presented:** <date> to <stakeholders>
**Clarifications / corrections:** <what changed during review>
**Approval:** <name/role> approved <story IDs / scope> on <date>  (full / partial / conditional: <terms>)

# Requirements Traceability Matrix — <project>
| Req ID | Title | Source (finding / goal) | Depends on | Status | Sign-off (ref / date) |
|--------|-------|-------------------------|------------|--------|-----------------------|
<!-- Status = requirement lifecycle: proposed / validated / signed-off / changed / deferred / superseded.
     No design/build/test columns — delivery status lives in Bitbucket, not here. -->

# Change Log — <project>
| Date | Req ID | Change | Reason | Status | Impact (on other requirements) |
|------|--------|--------|--------|--------|--------------------------------|
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that every requirement is traced **back to
its source**, approval is attributed and dated, and continued validation is provided for.
Improve if short of the bar (ask the user where you need their input; never assume). When it meets
the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write `sign-off.md` to `ba-artifacts/<task-id>/` and update `RTM.md` /
   `change-log.md` under `ba-requirement/`, tick Steps 8–9 in `## Plan` (links + **Next step**),
   then hand off to `commit-work` (real project repo).
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill`.

You author the records as the BA assistant, on the user's behalf, for the audit record.

---

## Closing the loop
Step 9 is ongoing: as delivery proceeds and understanding changes, return here to update the RTM
and change log and to re-validate affected stories with stakeholders. If a change is large enough
to reshape scope, hand back to `ba-plan` to revise the `## Plan` (and likely re-run as a new
`develop` or `maintain` effort).
