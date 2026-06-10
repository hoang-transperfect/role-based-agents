---
name: designer-ds-atom
description: >
  Writes the component spec for one design system atom — the indivisible UI building block that
  has no component dependencies (only token references). Variants, states, anatomy (token names
  only, never raw values), behaviour, and usage rules. Invoke once per atom listed in ds-audit.md,
  after designer-ds-foundation has defined the token layer. Atoms must be specced before any
  molecule or DS organism that depends on them. Produces one component-spec.md per atom under
  design-system/atoms/.
---

# designer-ds-atom

An atom is the smallest indivisible UI element in the design system — Button, Input, Checkbox,
Badge, Icon, Avatar, Spinner, Tooltip, etc. It has **no component dependencies**: its anatomy
references only foundation token names, never other components.

Getting atoms right is critical because every molecule and DS organism is built from them. A
missing variant or state here creates a gap that cascades through every higher-level component.

## Where things live

- **Read** `ds-audit.md` for the atom's scope, notes, and any inconsistencies to resolve.
- **Read** the foundation files at `<real_project_path>/design-system/foundations/` for the
  token names this atom's anatomy will reference.
- **Write** the spec to `<real_project_path>/design-system/atoms/<component-name>/component-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` — confirms this atom is in scope and lists any noted inconsistencies.
- Foundation files — the token names for color, typography, spacing, radius, animation, etc.

### Input Acceptance Criteria
- `ds-audit.md` lists this atom as in scope for this task.
- Foundation files exist and define the token names this atom will reference. If a needed token
  category is missing (e.g. spacing is undefined), flag it as a foundation gap and hand off to
  `designer-ds-foundation` before proceeding.

### Outputs
- `<real_project_path>/design-system/atoms/<component-name>/component-spec.md`

### Output Quality Criteria
- **No component dependencies** — anatomy references only token names, never other components.
  An atom that references a sub-component is actually a molecule; reclassify before proceeding.
- **All variants are defined** — every meaningfully different version noted in the audit.
- **All interactive states are defined** — default, hover, focus, active, disabled, loading,
  error, success, empty — as applicable to this atom's nature.
- **Anatomy references token names only** — every visual property is a token name
  (e.g. `color.action.primary`), never a raw value.
- **Behaviour is specified** — focus management, keyboard shortcuts, ARIA role.
- **Usage rules are actionable** — do/don't rules preventing common misuse.

---

## The 3-gate flow

### Gate 1 — Input
Confirm this atom is in scope in `ds-audit.md`. Verify the foundation tokens it needs are
defined. If a foundation token category is missing, hand off to `designer-ds-foundation` first.

### Gate 2 — Process
Work through the atom spec with the designer. Start from the token layer up.

Probe for completeness:
- Are there more variants than the obvious ones? (e.g. Button needs icon-only variant)
- Are all interactive states covered, including loading and disabled?
- Are there accessibility requirements (ARIA role, keyboard navigation, focus ring)?

Write the atom spec:

```markdown
# <ComponentName> — atom

_Level: atom · Last updated: <date>_

## Purpose
<1 sentence: what this atom does and when to use it>

## Variants
| Variant | When to use |
|---|---|
| Primary | The main call-to-action on a page or section |
| Secondary | Secondary actions alongside a primary action |
| Ghost | Low-emphasis actions or icon-only triggers |
| Danger | Destructive or irreversible actions |

## States
| State | Visual change | Notes |
|---|---|---|
| Default | — | Base appearance |
| Hover | Background: `color.action.primary-hover` | On pointer hover |
| Focus | Outline: `color.focus.ring` 2px offset | Keyboard / programmatic focus |
| Active | Background: `color.action.primary-active` | On press |
| Disabled | Opacity: 40% · cursor: not-allowed | Not interactive |
| Loading | Spinner replaces label | Async action in progress |

## Anatomy
_(All values are token names — never raw values)_

| Part | Property | Token |
|---|---|---|
| Container | Background | `color.action.primary` |
| Container | Padding (horizontal) | `spacing.md` |
| Container | Padding (vertical) | `spacing.sm` |
| Container | Border radius | `radius.md` |
| Label | Font | `typography.label.md` |
| Label | Color | `color.text.on-action` |

## Behaviour
- On click/tap: triggers the action; enters loading state if async.
- Keyboard: `Enter` and `Space` activate. Tab moves focus to the next interactive element.
- ARIA: `role="button"`. Use `aria-disabled="true"` (not `disabled`) to keep keyboard focus.
- Animation: loading spinner uses `animation.spin`; no other transitions.

## Usage rules
**Do:**
- Use Primary for the single most important action per section.

**Don't:**
- Don't use two Primary variants side by side — choose one.
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that all anatomy references are token names
(never raw values) and all variants and states are covered. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick the atom in Step 3a in `## Plan`, update **Next step**,
   then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed atom specs feed `designer-ds-molecule` (which references these atoms by name) and
`designer-ds-organism` (for DS organisms). They also feed `designer-ds-document`, which indexes
them in the README. In product design, components are referenced by name — e.g. "Button / Primary"
maps to `design-system/atoms/button/component-spec.md`.
