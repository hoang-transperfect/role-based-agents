---
name: designer-ds-document
description: >
  Writes the usage guidelines and builds the README index for the design system — the human-
  readable layer on top of the token and component specs that tells designers and developers
  how to use the system correctly. Invoke as the final step of a design-system mode task, after
  all in-scope foundation files and component specs from designer-ds-atom, designer-ds-molecule,
  and designer-ds-organism have been written and confirmed. Produces design-system/README.md.
  Also invoke when the design system grows and
  the index or guidelines need updating.
---

# designer-ds-document

Token files and component specs answer "what does this component do?" precisely, but they don't
tell a new designer or developer where to start, which component to reach for, or how the pieces
fit together. This skill writes that layer: the README index and usage guidelines that make the
design system usable, not just correct.

## Where things live

- **Read** all foundation files at `<real_project_path>/design-system/foundations/`.
- **Read** all component specs at `<real_project_path>/design-system/atoms/`,
  `molecules/`, and `organisms/`.
- **Write** `<real_project_path>/design-system/README.md`.

---

## The skill contract

### Inputs
- All in-scope foundation files (from `designer-ds-foundation`).
- All in-scope atom specs (from `designer-ds-atom`).
- All in-scope molecule specs (from `designer-ds-molecule`).
- All in-scope DS organism specs (from `designer-ds-organism`).
- The `## Plan` (confirming all components and foundations in scope are complete).

### Input Acceptance Criteria
- All Step 2 (foundations), Step 3a (atoms), Step 3b (molecules), and Step 3c (organisms) items
  in `## Plan` are ticked.
- If any in-scope foundation or component is unticked, surface the incomplete state and ask the
  user before documenting — a README that indexes incomplete specs misleads users.

### Outputs
- `<real_project_path>/design-system/README.md`

### Output Quality Criteria
- **The index is complete**: every foundation file and component spec in scope is linked from
  the README, grouped by section (foundations / atoms / molecules / organisms).
- **Getting started section is present**: tells a new user what foundations to read first, and
  the key rule: reference token names from foundations, reference component names from specs —
  never use raw values.
- **Cross-cutting guidelines are included**: at least accessibility (ARIA roles, keyboard
  navigation, focus management) and the token-naming convention.
- **Known gaps are documented**: components or foundations that were audited but deferred (from
  `ds-audit.md`'s out-of-scope section) are listed as "planned / not yet specced" so users know
  what's missing intentionally vs. accidentally.
- **It is navigable**: the README is a starting point, not a full specification — keep it short,
  link to the detail files rather than duplicating them.

---

## The 3-gate flow

### Gate 1 — Input
Check that all in-scope foundations and components are complete. If any are missing, surface the
gap and ask the user whether to proceed with a partial README (marking gaps as in-progress) or
wait until all specs are done.

### Gate 2 — Process
Build the README index from the actual files on disk — list what exists, not what was planned.
Read `ds-audit.md` for the out-of-scope list to include as "planned / not yet specced."

Write the README:

```markdown
# Design System — <Project name>

_Last updated: <date> · Mode: design-system_

## Getting started
This design system follows the atomic design hierarchy: **foundations → atoms → molecules →
organisms**.

- **When speccing components**, always reference token names from `foundations/` — never use raw
  values (colours, sizes, spacing). Use semantic aliases, not primitives.
- **When referencing components in design specs**, use the component name only (e.g. "Button /
  Primary") — the spec in this system defines the detail.
- **Build order**: spec atoms before molecules, molecules before organisms.

## Foundations
| Category | File | Covers |
|---|---|---|
| Color | [foundations/color.md](foundations/color.md) | Palette + semantic aliases |
| Typography | [foundations/typography.md](foundations/typography.md) | Scale + usage rules |
| Spacing | [foundations/spacing.md](foundations/spacing.md) | Scale + named steps |
| Elevation | [foundations/elevation.md](foundations/elevation.md) | Shadow levels |
| Border radius | [foundations/radius.md](foundations/radius.md) | Radius scale |
| Animation | [foundations/animation.md](foundations/animation.md) | Duration + easing |

## Atoms
| Component | File | Purpose |
|---|---|---|
| Button | [atoms/button/component-spec.md](atoms/button/component-spec.md) | Primary interactive action |
| Input | [atoms/input/component-spec.md](atoms/input/component-spec.md) | Text entry field |

## Molecules
| Component | File | Purpose | Depends on |
|---|---|---|---|
| Form field | [molecules/form-field/component-spec.md](molecules/form-field/component-spec.md) | Label + input + hint/error | Input, Label, InlineMessage |

## Organisms
| Component | File | Purpose | Depends on |
|---|---|---|---|
| Navigation bar | [organisms/nav-bar/component-spec.md](organisms/nav-bar/component-spec.md) | Top-level navigation | Button, Avatar, Icon |

## Cross-cutting guidelines

### Accessibility
- All interactive components must have an ARIA role. See each component spec for details.
- Focus management: keyboard users must be able to reach all interactive elements via Tab.
- Disabled elements: use `aria-disabled="true"` rather than the `disabled` attribute to keep
  keyboard focus and communicate state to assistive technology.

### Token naming convention
`<category>.<semantic-group>.<variant>` — e.g. `color.action.primary`, `spacing.md`,
`typography.heading.lg`. Components reference semantic aliases; primitives are for foundations
only.

## Planned / not yet specced
_(From ds-audit.md out-of-scope list — these exist as design patterns but are not yet
documented in this system)_

| Item | Level | Notes |
|---|---|---|
| <component / foundation> | atom / molecule / organism / foundation | <reason deferred> |
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that the index links to real files
(nothing invented), and that the out-of-scope items from `ds-audit.md` are listed as planned.
When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write `README.md`, tick Step 4 in `## Plan`, update **Next step: complete**,
   then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Completing the design-system task

When Step 4 is ticked and it is the last applicable step in the `## Plan`:
1. Set `status: completed` in the task file's frontmatter.
2. Set the conversation log frontmatter `status: completed`.
3. Remove the task's line from the project index file.
4. Hand off to `commit-work`.

The completed `design-system/` folder is now the authoritative source for the design system.
In product-design tasks, `designer-ui` references components by name — the README is the index
that tells the designer where to look up the detail.
