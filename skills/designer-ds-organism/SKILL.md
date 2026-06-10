---
name: designer-ds-organism
description: >
  Writes the component spec for one design system organism — a complex, generic, reusable UI
  component composed of molecules and/or atoms (e.g. NavigationBar, DataTable, Modal, Card).
  DS organisms are generic enough to be used across any product without modification. Invoke once
  per organism listed in ds-audit.md, after all molecule and atom dependencies are specced.
  Produces one component-spec.md per organism under design-system/organisms/. Not to be confused
  with designer-organism, which specs product-specific organisms that live in design-spec/.
---

# designer-ds-organism

A DS organism is a complex, self-contained UI component built from molecules and atoms. It is
**generic and reusable** — a NavigationBar, DataTable, Modal, Card, Sidebar, Form — something
that makes sense in any product without modification to its structure or visual rules.

The boundary with product-specific organisms (specced by `designer-organism`) is intent:
- **DS organism**: generic structure, could be dropped into a different product unchanged.
- **Product organism**: tightly coupled to this product's IA, data model, or feature context.

If a candidate organism references product-specific data labels, routes, or business logic in
its structure, it belongs in `designer-organism`, not here.

## Where things live

- **Read** `ds-audit.md` for the organism's scope, dependencies, and notes.
- **Read** molecule specs at `<real_project_path>/design-system/molecules/` and atom specs at
  `<real_project_path>/design-system/atoms/` for the sub-components this organism uses.
- **Read** foundation files at `<real_project_path>/design-system/foundations/` for any
  organism-level layout tokens.
- **Write** `<real_project_path>/design-system/organisms/<component-name>/component-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` — confirms this organism is in scope and lists its molecule/atom dependencies.
- Molecule specs and atom specs for all sub-components (must be written before this organism).
- Foundation files — for organism-level layout tokens (spacing, responsive breakpoints, etc.).

### Input Acceptance Criteria
- `ds-audit.md` lists this organism as in scope.
- All molecule and atom dependencies are already specced. If any dependency is missing, hand off
  to `designer-ds-molecule` or `designer-ds-atom` first — never reference an undefined component.
- The organism is confirmed as generic and reusable, not product-specific. If it references
  product-specific data or IA, redirect to `designer-organism`.

### Outputs
- `<real_project_path>/design-system/organisms/<component-name>/component-spec.md`

### Output Quality Criteria
- **Generic, not product-specific** — no product IA labels, routes, or business logic baked in.
  Product-specific content is supplied by the consuming page/product layer.
- **Sub-components are named molecules or atoms** — referenced by name, never redefined.
- **All variants are defined** — every variant noted in the audit.
- **All states are defined** — as applicable: default, loading, empty, error, as well as any
  responsive layout variants.
- **Anatomy references component names and token names** — sub-components by name; organism-level
  layout by token name. Never raw values.
- **Responsive behaviour is specified** — for organisms that change layout at breakpoints.
- **Behaviour is specified** — focus management, ARIA landmark or role, keyboard interaction.
- **Usage rules are actionable** — when to use this organism and when to reach for something else.

---

## The 3-gate flow

### Gate 1 — Input
Verify all molecule and atom dependencies are specced. If any are missing, hand off first.
Confirm the organism is generic (DS candidate), not product-specific. If it's product-specific,
redirect to `designer-organism`.

### Gate 2 — Process
Work through the organism spec with the designer. Start from the molecule/atom layer.

Probe for completeness:
- Is every sub-component a named molecule or atom?
- How does the organism behave when data is loading, empty, or in error state?
- Does it change layout at any breakpoint?
- What ARIA landmark or role does it carry?

Write the organism spec:

```markdown
# <ComponentName> — DS organism

_Level: organism · Last updated: <date>_

## Purpose
<1 sentence: what this organism does and why it belongs in the design system>

## Variants
| Variant | When to use |
|---|---|
| Default | Standard use |
| Compact | Dense data display in constrained spaces |

## States
| State | What changes | Notes |
|---|---|---|
| Default | All sub-components loaded | — |
| Loading | Rows replaced by SkeletonAtom × N | N configurable by page |
| Empty | Empty state zone shown | EmptyState atom |
| Error | Error state zone shown | ErrorMessage atom |

## Contains
| Component | Level | Role in this organism |
|---|---|---|
| TableHeader | molecule | Column labels + sort controls |
| TableRow | molecule | One data row |
| Pagination | molecule | Page navigation below the table |
| EmptyState | atom | Shown when no data |
| ErrorMessage | atom | Shown on load failure |

## Anatomy
_(Organism-level layout — sub-component appearance is owned by each component spec)_

| Part | Property | Token |
|---|---|---|
| Container | Background | `color.surface.default` |
| Container | Border | `color.border.default` 1px |
| Container | Border radius | `radius.lg` |
| Row gap | Between rows | `spacing.none` (flush rows) |

## Responsive behaviour
| Breakpoint | Change |
|---|---|
| < 768px | Horizontal scroll on overflow |
| ≥ 768px | Full table layout |

## Behaviour
- Keyboard: Tab moves through interactive cells; column sort headers respond to Enter/Space.
- ARIA: `role="table"` with `aria-label`. Rows use `role="row"`, cells use `role="cell"`.
- Focus management: after sort or page change, focus returns to the first data cell.

## Usage rules
**Do:**
- Use for any tabular data that needs sorting, pagination, or row-level actions.

**Don't:**
- Don't use for non-tabular lists — use a List atom or Card organism instead.
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that sub-components are named DS
components (not redefined), states cover loading/empty/error, and responsive behaviour is
specified. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick the organism in Step 3c in `## Plan`, update **Next
   step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed DS organism specs feed `designer-ds-document` (README index). In product design,
product pages reference DS organisms by name in page specs and organism specs — e.g.
"NavigationBar (DS)" maps to `design-system/organisms/nav-bar/component-spec.md`. Product-
specific organisms (built from these DS components) are specced separately by `designer-organism`.
