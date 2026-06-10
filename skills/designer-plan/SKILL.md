---
name: designer-plan
description: >
  Lays out the design plan for a task, frames the design problem, selects the work mode, and
  owns the authoritative progress checklist that every other designer skill reads and ticks.
  Works in two modes: product-design mode (from-scratch / develop / maintain — frames the user
  need, checks for a design system source in resource.md, produces the product-design checklist)
  and design-system mode (frames the system scope, produces the ds checklist). Invoke when
  starting any design work on a task, when a designer asks "what's the plan", "where are we",
  or "what's next", or whenever the task file has no design progress checklist yet. Run
  designer-scan-context first so the plan builds on existing context.
---

# designer-plan

This skill turns a design task into a navigable plan. Its core value is the **progress checklist**:
a single, auditable record in the task file of which design steps are done, what artifact each
produced, and what's next. Because the state lives in the file, a designer can stop and resume
anytime, and any step skill can jump in by reading where the work stands.

This skill **owns** the checklist. Step skills only tick their own box and link their artifact.

**Design system gate (product-design mode only):** If `related-context.md` reports no design
system source in `resource.md`, this skill surfaces the gap and asks the user to choose:
1. Switch to design-system mode for this task (build the system first).
2. Proceed with story spec only (`designer-ui` can run — UX flows, affected artifacts, AC
   alignment); artifact specs (`designer-organism`, `designer-template`, `designer-page`) are
   deferred until a DS source is added to `resource.md`.
3. User override: proceed anyway (risk noted in the plan).

This gate does not apply in design-system mode — building the system is the task.

## Where the work lives

The checklist lives in the task file's `## Plan` section:
`<real_project_path>/designer-artifacts/tasks/<task-id>/task.md`.

**Product-design output:** `<real_project_path>/design-spec/` — one `story-spec.md` per user
story (under `epic/feature/story/`) plus artifact specs under `product-organisms/`, `templates/`,
and `pages/`.

**Design-system output:** `<real_project_path>/design-system/` — atomic hierarchy:
`foundations/`, `atoms/`, `molecules/`, `organisms/`, `README.md`.

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
- The **design problem or system scope** can be stated — what the work is trying to achieve.
  If unclear, frame it with the user before planning.
- A `related-context.md` exists (from `designer-scan-context`). If not, run `designer-scan-context`
  first, or note the plan was made without a context scan if the user declines.

### Outputs
- A `## Plan` section in the task file with a tailored checklist.

### Output Quality Criteria
- **Problem / scope framing is complete** — stated at the top of the plan.
- **Mode is stated**: product-design (from-scratch / develop / maintain) or design-system.
- **Product-design mode**: design system source decision is recorded (present with link from
  `resource.md`, or absent with the agreed path).
- **Design-system mode**: atomic scope is clear — which foundations and which atomic levels
  (atoms / molecules / organisms) are in scope for this task.
- Steps that don't apply are marked `~~skipped~~ (reason)`, never silently dropped.
- It is unambiguous which step is next.

---

## The 3-gate flow

### Gate 1 — Input
Check inputs against Acceptance Criteria. If the problem is unclear or the context scan is missing,
**ask the user** or hand off to `designer-scan-context` first. Do not assume.

### Gate 2 — Process

**First, determine the mode with the user:**
- **Product-design** — designing screens and flows for an application, backed by BA user stories.
- **Design-system** — building or extending the foundational component system, following the
  atomic approach.

If the mode is ambiguous from the task description, ask before proceeding.

---

**If product-design mode:**

Settle the work sub-mode:
- **from-scratch** — no prior design specs exist. Run the full pipeline.
- **develop** — adding design for a new feature/story. Research may be light.
- **maintain** — updating an existing design spec. Research typically skipped.

Surface the design system source from `related-context.md`:
- **Present** → record the name and link from `resource.md`; `designer-ui` can proceed.
- **Absent** → apply the gate (see intro). Record the chosen path.

Draft the product-design checklist:

```markdown
## Plan

**Mode:** product-design · **Work sub-mode:** develop  (from-scratch / develop / maintain)

### Problem framing
- **User need / design problem:** <what experience or outcome the design must deliver, and for whom>
- **User stories in scope:** US-01 <title>, US-02 <title>, …
- **Design objectives:** <the design outcomes we're after>
- **Constraints:** <platform, device, brand rules, existing patterns>

### Design system
- **Source:** <name> · `resource.md` → <link>
  OR
- **Source:** absent · Decision: <design-system mode / UX flows only / user override (risk noted)>

### Design Progress Checklist
- [ ] Step 1 — Research (users, goals, heuristics)                              → <artifact link>
- [ ] Step 2 — Story spec (UX flows + affected artifacts + AC alignment per story) → <artifact link>
- [ ] Step 3a — Product-specific organism specs (if needed)                     → <artifact link>
- [ ] Step 3b — Template specs (if needed)                                      → <artifact link>
- [ ] Step 3c — Page artifact specs (per page affected)                         → <artifact link>
- [ ] Step 4 — Design review (coverage + sign-off)                              → <artifact link>

Steps 3a and 3b are optional — mark `~~skipped~~` with a reason when all organisms are in the
DS (3a) or when no layout is shared across multiple stories (3b).

**Next step:** <the first applicable step>.
```

---

**If design-system mode:**

Frame the system scope with the user. What foundations and which atomic levels need to be
created or extended in this task? What reference products, brand guidelines, or existing
components should inform it (from `related-context.md`)?

Draft the design-system checklist:

```markdown
## Plan

**Mode:** design-system

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
`~~skipped~~` with a reason for any atomic level not in scope for this task.

**Next step:** Step 1 — designer-ds-audit.
```

---

### Gate 3 — Output
Check against Output Quality Criteria. When it meets the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write it to the task file, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
In product-design mode, the plan feeds `designer-research` (or `designer-ui` if research is
skipped). In design-system mode, it feeds `designer-ds-audit`. The checklist is the guide for
the rest of the effort.
