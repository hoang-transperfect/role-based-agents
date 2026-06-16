---
name: designer-ds-audit
description: >
  Inventories existing UI patterns, identifies inconsistencies and gaps, and defines the scope
  of the design system — which foundations and which components at each atomic level (atoms,
  molecules, organisms) need to be created or documented. Invoke as the first step of a
  design-system mode task, after designer-plan, when a designer asks "what components do we
  need?", "what already exists?", "what's the scope of the design system?", or is about to start
  building a design system. Run after designer-scan-context and designer-plan so the audit builds
  on existing context and an agreed scope. Produces ds-audit.md which feeds designer-ds-foundation
  and designer-ds-component.
---

# designer-ds-audit

A design system built without an audit is likely to be incomplete, inconsistent, or misaligned
with what the product actually needs. This skill answers two questions: **what already exists?**
and **what needs to exist?** The audit output defines the scope that every subsequent ds step
executes against.

Following atomic design, scope is defined at three levels:
- **Foundations** — the token layer: color, typography, spacing, elevation, radius, animation.
- **Foundation components** — primitive display elements with no component dependencies: Text
  and Icon. Must exist before any atom can be specced.
- **Components** — atoms (indivisible UI elements that may use foundation components), molecules
  (simple atom combinations), organisms (complex, composed components). Templates and pages are
  product-design deliverables, not design-system components.

## Where things live

- **Read** `related-context.md` (existing foundations, component inventory, brand guidelines,
  reference products from `designer-scan-context`).
- **Read** the `## Plan` (scope framing and atomic scope from `designer-plan`).
- **Write** `<real_project_path>/designer-artifacts/tasks/<task-id>/ds-audit.md`.

---

## The skill contract

### Inputs
- `related-context.md` from `designer-scan-context`.
- The `## Plan` (scope framing: atomic scope, reference baseline, constraints).
- Any existing UI — screenshots, code components, Figma files, or a running application the
  designer can share or describe.

### Input Acceptance Criteria
- The `## Plan` scope framing is complete (from `designer-plan`).
- There is enough existing UI or reference material to audit against. If the product has no UI
  at all and no brand guidelines, note this — the audit becomes a scope-definition exercise
  guided by the product vision.

### Outputs
- `<real_project_path>/designer-artifacts/tasks/<task-id>/ds-audit.md`

### Output Quality Criteria
- **Foundation scope is explicit**: each token category is listed as needed / already exists /
  out of scope for this task, with a brief reason.
- **Component scope is explicit**: each component is listed with its level (foundation component
  / atom / molecule / organism), its status (new / extend / already done), and the priority
  order in which it should be built — foundation components before atoms, atoms before
  molecules, molecules before organisms.
- **Inconsistencies are documented**: where the existing UI uses the same element differently
  in different places (different spacing, different colours for the same intent), these are noted
  so the design system can resolve them.
- **Out-of-scope is stated explicitly**: components or foundations that were considered and
  decided out of scope for this task, with the reason. No silent omissions.
- The priority order is actionable: the designer can pick the next component to build from
  the list without needing to re-discuss scope.

---

## The 3-gate flow

### Gate 1 — Input
Check inputs against Acceptance Criteria. If the scope framing from `designer-plan` is missing,
hand back to `designer-plan` first. If there is no existing UI to audit, note this and proceed
as a scope-definition exercise — do not assume components or patterns.

### Gate 2 — Process
Work through the existing UI with the designer. For each atomic level:

**Foundations** — ask: which token categories does this system need? For each: does anything
already define it (brand guide, existing CSS variables, design file)? Note gaps.

**Foundation components** — Text and Icon. These are always in scope if any atom depends on
them (which nearly all do). Confirm both are needed; note any inconsistencies in how text styles
or icon sets are currently applied.

**Atoms** — the indivisible building blocks: button, input, checkbox, radio, toggle, badge,
tag, avatar, spinner, tooltip, etc. For each candidate, note: does it exist consistently?
Any variants or states that are used but undefined?

**Molecules** — simple combinations: form field (label + input + hint + error), search bar
(input + button), dropdown, pagination, etc.

**Organisms** — complex components: navigation bar, sidebar, card, table, modal, form, etc.

For each component, agree with the designer: in scope for this task or deferred?

Draft the audit:

```markdown
# Design System Audit — <project>

_Audit date: <date> · Scope from: designer-plan_

## Foundation scope
| Token category | Status | Notes |
|---|---|---|
| Color | new / extend / done / out of scope | <source if exists, gaps if new> |
| Typography | … | … |
| Spacing | … | … |
| Elevation | … | … |
| Border radius | … | … |
| Animation | … | … |

## Inconsistencies found
- <Element>: <how it varies across the existing UI> → <what the system should resolve>

## Component scope — build order
_(Foundation components before atoms, atoms before molecules, molecules before organisms)_

### Foundation components
| Component | Status | Notes / inconsistencies |
|---|---|---|
| Text | new / extend / done | … |
| Icon | new / extend / done | … |

### Atoms
| Component | Status | Notes / inconsistencies |
|---|---|---|
| Button | new | 3 visual variants found; states inconsistent |
| Input | new | … |

### Molecules
| Component | Status | Notes |
|---|---|---|
| Form field | new | depends on: Input, Label, InlineMessage |

### Organisms
| Component | Status | Notes |
|---|---|---|
| Navigation bar | new | depends on: Button, Avatar, Icon |

## Out of scope (this task)
| Item | Reason |
|---|---|
| <component / foundation> | <deferred / not needed / already complete> |
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that the build order is correct (no atom
listed before foundation components, no molecule listed before its atom dependencies) and that
out-of-scope items are explicit. When
the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write `ds-audit.md`, tick Step 1 in `## Plan`, update **Next step**,
   then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
`ds-audit.md` feeds `designer-ds-foundation` (the token scope), `designer-ds-foundation-component`
(Text and Icon), `designer-ds-atom`, `designer-ds-molecule`, and `designer-ds-organism` (the
component build order). All five skills read the audit before starting any work.
