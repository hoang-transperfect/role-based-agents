---
name: designer-ds-foundation
description: >
  Defines the design token layer of the design system — color palette and semantic aliases,
  typography scale, spacing scale, elevation, border radius, and animation tokens — as written
  specs that components reference by token name. Invoke as the second step of a design-system
  mode task, after designer-ds-audit, when the designer is ready to define tokens before
  speccing components. Foundations must exist before designer-ds-component can reference token
  names. Produces one markdown file per token category under design-system/foundations/.
---

# designer-ds-foundation

Foundations are the token layer that everything else in the design system references. A button's
colour is not `#1D4ED8` — it is `color.action.primary`. A heading's size is not `24px` — it is
`typography.heading.lg`. This indirection is what makes a design system maintainable: change a
token, and every component that references it updates.

This skill defines each token category from the audit scope as a written spec. Components built
in `designer-ds-component` reference these token names — never raw values.

## Where things live

- **Read** `ds-audit.md` (foundation scope: which categories are needed, what sources exist).
- **Read** brand guidelines from `resource.md` (the authoritative colour, type, and brand values).
- **Write** one file per token category to
  `<real_project_path>/design-system/foundations/<category>.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` (foundation scope and any inconsistencies to resolve).
- Brand guidelines or existing token sources from `resource.md`.

### Input Acceptance Criteria
- `ds-audit.md` exists and lists which foundation categories are in scope.
- For each in-scope category, the source (brand guide, existing CSS variables, design file) is
  known or the designer can define it. If a category is in scope but has no source, ask the
  designer before defining tokens — do not invent values.

### Outputs
- `<real_project_path>/design-system/foundations/<category>.md` for each in-scope category.

### Output Quality Criteria
- **Two layers for color**: primitive palette (the raw values, e.g. `blue-500: #3B82F6`) and
  semantic aliases (the intent, e.g. `color.action.primary: blue-500`). UI components reference
  semantic aliases, not primitives. This separation means rebranding only touches primitives.
- **Typography** covers font families, the full scale (size, line-height, weight for each step),
  and usage rules (which step for body, headings, captions, etc.).
- **Spacing** follows a consistent scale (e.g. 4px base grid: 4, 8, 12, 16, 24, 32, 48, 64…)
  with named steps (spacing.xs, spacing.sm, spacing.md, spacing.lg, spacing.xl, etc.).
- **Each token is named consistently** — `category.variant.modifier` pattern (e.g.
  `color.feedback.error`, `spacing.md`, `typography.body.md`).
- **Usage rules are included** — each token file says when to use and when not to use each token,
  so components are built consistently.
- Values come from brand guidelines or the designer — never invented.

---

## The 3-gate flow

### Gate 1 — Input
Read the foundation scope from `ds-audit.md`. For any in-scope category without a defined source,
**ask the designer** for the values before proceeding. Do not invent token values.

### Gate 2 — Process
Work through each in-scope foundation category with the designer. For each, follow the template
below. Start with color (other categories often reference it) and typography, then spacing and
the rest.

For categories already partially defined (from brand guidelines or existing CSS), map them to the
token structure — don't replace working values, structure them correctly.

Token file template:

```markdown
# <Category> — Design System Foundations

_Source: <brand guide / existing CSS / designer-defined> · Last updated: <date>_

## Primitives
_(Raw values — components never reference these directly)_

| Token name | Value | Notes |
|---|---|---|
| <category>-<scale>-<step> | <value> | |
| blue-50 | #EFF6FF | |
| blue-500 | #3B82F6 | |

## Semantic aliases
_(Intent-named tokens — components always reference these)_

| Token name | References | Usage |
|---|---|---|
| color.action.primary | blue-500 | Primary buttons, links, active states |
| color.action.primary-hover | blue-600 | Hover state of primary actions |
| color.feedback.error | red-500 | Error messages, destructive states |
| color.surface.default | neutral-0 | Default page/card background |

## Usage rules
- Use semantic aliases in all component specs — never reference primitives.
- <specific rule for this token category>
```

For **typography**, additionally include:

```markdown
## Scale
| Step | Font family | Size | Line height | Weight | Usage |
|---|---|---|---|---|---|
| display.lg | Inter | 48px | 56px | 700 | Hero headings |
| heading.lg | Inter | 32px | 40px | 600 | Page headings |
| body.md | Inter | 16px | 24px | 400 | Default body text |
| caption.sm | Inter | 12px | 16px | 400 | Labels, captions |
```

For **spacing**, additionally include:

```markdown
## Scale
| Token | Value | Usage |
|---|---|---|
| spacing.xs | 4px | Tight gaps between related elements |
| spacing.sm | 8px | Default inner padding |
| spacing.md | 16px | Standard component padding |
| spacing.lg | 24px | Section spacing |
| spacing.xl | 32px | Large layout gaps |
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that color has two layers (primitives +
semantic aliases), and that every value came from the designer or brand guidelines, not invented.
When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the foundation files, tick Step 2 in `## Plan`, update **Next step**,
   then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The foundation files feed `designer-ds-component`. Every component spec references token names
from these files — never raw values. Remind the designer of this when starting component work.
