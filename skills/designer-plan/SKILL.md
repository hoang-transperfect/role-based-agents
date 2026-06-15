---
name: designer-plan
description: >
  Lays out the design plan for a task, frames the design problem, selects the work type and
  sub-mode, and owns the authoritative progress checklist that every other designer skill reads
  and ticks. Works in two types: product-design (PS) and design-system (DS). PS sub-modes:
  from-scratch / develop / maintain — frames the user need, checks for a design system source,
  produces the PS checklist (research → UI with IA+wireframe → organisms/templates/pages →
  test plan → review). DS sub-modes: from-scratch / add-component / update — frames the system
  scope, produces the DS checklist. Invoke when starting any design work, when the task file has
  no design progress checklist yet, or when the designer asks "what's the plan" or "what's next".
  Run designer-scan-context first so the plan builds on existing context.
---

# designer-plan

This skill turns a design task into a navigable plan. Its core value is the **progress checklist**:
a single, auditable record in the task file of which design steps are done, what artifact each
produced, and what's next. Because the state lives in the file, a designer can stop and resume
anytime, and any step skill can jump in by reading where the work stands.

This skill **owns** the checklist. Step skills only tick their own box and link their artifact.

**Design system gate (PS mode only):** If `related-context.md` reports no design system source
in `resource.md`, this skill surfaces the gap and asks the user to choose:
1. Switch to DS mode for this task (build the system first).
2. Proceed with story spec only (`designer-ui` can run — IA, wireframe, UX flows, AC alignment);
   artifact specs (`designer-organism`, `designer-template`, `designer-page`) are deferred until
   a DS source is added to `resource.md`.
3. User override: proceed anyway (risk noted in the plan).

This gate does not apply in DS mode — building the system is the task.

## Where the work lives

The checklist lives in the task file's `## Plan` section:
`<real_project_path>/designer-artifacts/tasks/<task-id>/task.md`.

**PS output:** `<real_project_path>/design-spec/` — one `story-spec.md` per user story (under
`epic/feature/story/`) plus artifact specs under `product-organisms/`, `templates/`, and `pages/`.

**DS output:** `<real_project_path>/design-system/` — atomic hierarchy: `foundations/`, `atoms/`,
`molecules/`, `organisms/`, `README.md`.

The design system source (Figma library, npm package, etc.) is always declared in
`<real_project_path>/designer-artifacts/resource.md`, not in a pointer file.

---

## The skill contract

### Inputs
- The task file (`<real_project_path>/designer-artifacts/tasks/<task-id>/task.md`).
- The `related-context.md` artifact from `designer-scan-context`.
- The design problem or system scope (from the task description, `resource.md`, or the user).

### Input Acceptance Criteria
- A task file exists.
- The **design problem or system scope** can be stated. If unclear, frame it with the user
  before planning.
- A `related-context.md` exists (from `designer-scan-context`). If not, run
  `designer-scan-context` first, or note the plan was made without a context scan if the user
  declines.

### Outputs
- A `## Plan` section in the task file with a tailored checklist.

### Output Quality Criteria
- **Problem / scope framing is complete** — stated at the top of the plan.
- **Work type is stated**: PS or DS.
- **Sub-mode is stated**: PS (from-scratch / develop / maintain) or DS (from-scratch /
  add-component / update).
- **PS mode**: design system source decision is recorded (present with link, or absent with
  the agreed path).
- **DS mode**: atomic scope is clear — which foundations and atomic levels are in scope.
- Steps that don't apply are marked `~~skipped~~ (reason)`, never silently dropped.
- It is unambiguous which step is next.

---

## The 3-gate flow

### Gate 1 — Input
Check inputs against Acceptance Criteria. If the problem is unclear or the context scan is
missing, **ask the user** or hand off to `designer-scan-context` first. Do not assume.

### Gate 2 — Process

**First, determine the work type with the user:**
- **PS (product-design)** — designing screens and flows for an application, backed by BA user
  stories.
- **DS (design-system)** — building or extending the foundational component system, following
  the atomic approach.

If the type is ambiguous, ask before proceeding.

---

**If PS mode:**

Settle the work sub-mode:
- **from-scratch** — no prior design specs exist. Run the full pipeline.
- **develop** — adding design for a new feature/story. Research and IA may be lighter.
- **maintain** — updating an existing design spec. Research and test plan typically skipped.

Surface the design system source from `related-context.md`:
- **Present** → record the name and link from `resource.md`.
- **Absent** → apply the gate (see intro). Record the chosen path.

Draft the PS checklist:

```markdown
## Plan

**Work type:** PS · **Sub-mode:** develop  _(from-scratch / develop / maintain)_

### Problem framing
- **User need / design problem:** <what experience or outcome the design must deliver, and for whom>
- **User stories in scope:** US-01 <title>, US-02 <title>, …
- **Design objectives:** <the design outcomes we're after>
- **Constraints:** <platform, device, brand rules, existing patterns>

### Design system
- **Source:** <name> · `resource.md` → <link>
  OR
- **Source:** absent · Decision: <DS mode / UX flows only / user override (risk noted)>

### Design Progress Checklist
- [ ] Step 1 — Research (users, goals, heuristics)                              → <artifact link>
- [ ] Step 2 — UI: IA + wireframe + story spec per story                        → <artifact link>
- [ ] Step 3a — Product-specific organism specs (if needed)                     → <artifact link>
- [ ] Step 3b — Template specs (if needed)                                      → <artifact link>
- [ ] Step 3c — Page artifact specs (per page affected)                         → <artifact link>
- [ ] Step 4 — Test plan + usability scenarios                                  → <artifact link>
- [ ] Step 5 — Design review (coverage + sign-off)                              → <artifact link>

Steps 1, 3a, 3b, and 4 are conditional — mark `~~skipped~~` with a reason when:
- Step 1: maintain mode, or strong user-insights.md already exists.
- Step 3a: all organisms exist in the DS (no product-specific organisms needed).
- Step 3b: no layout is shared across multiple stories.
- Step 4: maintain mode and the change is not structural or high-risk.

**Next step:** <the first applicable step>.
```

---

**If DS mode:**

Settle the work sub-mode:
- **from-scratch** — no design system exists. Run the full pipeline from audit to document.
- **add-component** — adding a new component at a known atomic level. Audit is scoped to the
  new component's dependencies.
- **update** — changing an existing component. Audit is scoped to the affected component and
  its downstream dependents.

Frame the system scope with the user. What foundations and atomic levels are in scope?
What reference products, brand guidelines, or existing components inform it?

Draft the DS checklist based on sub-mode:

**From-scratch:**
```markdown
## Plan

**Work type:** DS · **Sub-mode:** from-scratch

### Scope framing
- **Goal:** <what this design system effort must achieve>
- **Atomic scope:** foundations (color, typography, spacing, …) · atoms · molecules · organisms
- **Reference baseline:** <existing UI framework / brand guide / competitor system>
- **Constraints:** <brand rules, platform, existing codebase tokens>

### Design Progress Checklist
- [ ] Step 1 — Audit (inventory + define scope)              → <artifact link>
- [ ] Step 2 — Foundations (tokens)                          → <artifact link>
- [ ] Step 3a — Atom component specs                         → <artifact link>
- [ ] Step 3b — Molecule component specs                     → <artifact link>
- [ ] Step 3c — DS organism component specs                  → <artifact link>
- [ ] Step 4 — Documentation (guidelines + README index)     → <artifact link>

Steps 3a–3c follow atomic order: atoms before molecules, molecules before organisms. Mark
`~~skipped~~` with a reason for any level not in scope for this task.

**Next step:** Step 1 — designer-ds-audit.
```

**Add-component:**
```markdown
## Plan

**Work type:** DS · **Sub-mode:** add-component

### Scope framing
- **Component:** <name>
- **Atomic level:** <atom / molecule / organism>
- **Dependencies (must exist first):** <list of atoms/molecules this component references>
- **Constraints:** <token constraints, existing patterns to align with>

### Design Progress Checklist
- [ ] Step 1 — Component spec: <name> at <level>             → <artifact link>
- [ ] Step 2 — Validate: dependency check                    → <artifact link>
- [ ] Step 3 — Document: update README index                 → <artifact link>

**Next step:** Step 1 — designer-ds-<atom / molecule / organism>.
```

**Update:**
```markdown
## Plan

**Work type:** DS · **Sub-mode:** update

### Scope framing
- **Component to update:** <name> at <level>
- **Nature of change:** <token rename / new variant / behaviour change / …>
- **Known downstream dependents:** <list if already known; designer-ds-validate will confirm>
- **Constraints:** <backwards-compatibility requirements, if any>

### Design Progress Checklist
- [ ] Step 1 — Audit: affected components                    → <artifact link>
- [ ] Step 2 — Update spec: <name>                           → <artifact link>
- [ ] Step 3 — Validate: downstream impact                   → <artifact link>
- [ ] Step 4 — Document: update README index                 → <artifact link>

**Next step:** Step 1 — designer-ds-audit (scoped to affected components).
```

---

### Gate 3 — Output
Check against Output Quality Criteria. When it meets the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write it to the task file, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
**PS mode:** the plan feeds `designer-research` (or `designer-ui` directly if research is
skipped). `designer-ui` covers IA, wireframe, and story spec per story in Step 2.

**DS from-scratch:** feeds `designer-ds-audit`.
**DS add-component:** feeds `designer-ds-atom`, `designer-ds-molecule`, or `designer-ds-organism`
at the correct level.
**DS update:** feeds `designer-ds-audit` (scoped), then the responsible component skill, then
`designer-ds-validate`.
