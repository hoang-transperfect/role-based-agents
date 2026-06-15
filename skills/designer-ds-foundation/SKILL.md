---
name: designer-ds-foundation
description: >
  Defines the foundation layer of the design system — design principles, color palette and
  semantic aliases, typography scale, spacing scale, elevation, border radius, and animation
  tokens — as written specs that components reference by token name. Invoke as the second step
  of a design-system mode task, after designer-ds-audit, when the designer is ready to define
  principles and tokens before speccing components. Foundations must exist before
  designer-ds-component can reference token names. Produces principles.md and one markdown file
  per token category under design-system/foundations/.
---

# designer-ds-foundation

Foundations have two layers. The first is **principles**: the high-level statements that govern
every design decision in the system — what the DS stands for, and how to make calls when trade-offs
arise. The second is **tokens**: the named values everything else references. A button's colour is
not `#1D4ED8` — it is `color.action.primary`. A heading's size is not `24px` — it is
`typography.heading.lg`. This indirection is what makes a design system maintainable: change a
token, and every component that references it updates.

Principles come first because they inform token decisions. If accessibility is a principle,
that sets the minimum contrast floor for the color palette. If spatial clarity is a principle,
that shapes the spacing scale.

This skill defines principles and each token category from the audit scope as written specs.
Components built in `designer-ds-component` reference these token names — never raw values.

## Where things live

- **Read** `ds-audit.md` (foundation scope: which categories are needed, what sources exist).
- **Read** brand guidelines from `resource.md` (the authoritative colour, type, and brand values).
- **Write** `<real_project_path>/design-system/foundations/principles.md` — always first.
- **Write** one file per token category to
  `<real_project_path>/design-system/foundations/<category>.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` (foundation scope and any inconsistencies to resolve).
- Brand guidelines or existing token sources from `resource.md`.
- Product/brand values, strategy docs, or stakeholder input for principles (if available).

### Input Acceptance Criteria
- `ds-audit.md` exists and lists which foundation categories are in scope.
- For each in-scope token category, the source (brand guide, existing CSS variables, design file)
  is known or the designer can define it. If a category is in scope but has no source, ask the
  designer before defining tokens — do not invent values.
- For principles: at least one source exists (brand values, product vision, workshop output,
  existing principles doc). If none exist, the designer defines them collaboratively in Gate 2.

### Outputs
- `<real_project_path>/design-system/foundations/principles.md` — always produced.
- `<real_project_path>/design-system/foundations/<category>.md` for each in-scope token category.

### Output Quality Criteria

**Principles:**
- 3–7 principles: enough to be meaningful, few enough to be memorable.
- Each principle is actionable — "Be accessible" is too vague; "Design for extremes first: if it
  works for the edge case, it works for the common case" is actionable.
- Each has a rationale tied to the product or brand context — not generic DS wisdom.
- Each has "in practice" guidance specific enough to resolve a real design decision.
- No principle contradicts another.
- Principles came from the designer/brand/stakeholders — never invented.

**Tokens:**
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
Work through foundations in order: **principles first**, then token categories. Start with color
(other token categories often reference it) and typography, then spacing and the rest.

For token categories already partially defined (from brand guidelines or existing CSS), map them
to the token structure — don't replace working values, structure them correctly.

**Principles** — probe:
- What are the core values or beliefs this design system should embody?
- If sources exist (brand guide, product vision, workshop output): extract and structure them.
- If no sources exist: ask the designer — "What are 3–5 things you always want this system to
  stand for when someone faces a hard trade-off?"
- For each candidate principle: Is it actionable? Can it help resolve a real design decision?
  Does it have a clear in-practice meaning for this product?
- Confirm: do any principles conflict with each other? If yes, resolve before proceeding.

Principles file template:

```markdown
# Principles — Design System Foundations

_Source: <brand guide / stakeholder workshop / designer-defined> · Last updated: <date>_

## Purpose
{One sentence: what these principles are for and who they guide.}

---

## {Principle name}
**Statement:** {One sentence — the rule.}

**Rationale:** {Why this matters for this design system specifically.}

**In practice:**
- {Do: specific, actionable guidance}
- {Do: specific, actionable guidance}
- {Avoid: the anti-pattern this principle guards against}

---

## {Principle name}
…
```

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
Check against the Output Quality Criteria — principles are actionable and sourced from the
designer/brand (not invented); color has two layers (primitives + semantic aliases); every token
value came from the designer or brand guidelines, not invented. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write `principles.md` first, then the token files; tick Step 2 in `## Plan`,
   update **Next step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
`principles.md` guides all component decisions downstream — designers and engineers should read
it before speccing or building any component. The token files feed `designer-ds-component`;
every component spec references token names from these files — never raw values. Remind the
designer of both when starting component work.
