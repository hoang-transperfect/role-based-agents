---
name: designer-ds-component
description: >
  Writes the component spec for one design system component at a time — variants, states,
  anatomy (referencing foundation token names), behaviour, and usage rules — following the
  atomic design hierarchy: atoms first, then molecules (which reference atoms), then organisms.
  Invoke once per component listed in ds-audit.md, after designer-ds-foundation has defined
  the token layer. Run atoms before molecules, molecules before organisms — a component cannot
  reference another component that hasn't been specced yet. Produces one component-spec.md
  per component under design-system/atoms/, molecules/, or organisms/.
---

# designer-ds-component

A component spec answers "what is this component?" so precisely that a developer can implement
it, and a designer can use it, without ambiguity. It covers every variant, every interactive
state, the anatomy (what token names drive each visual property), the behaviour (what happens
when the user interacts), and the rules (when to use it and when not to).

This skill runs **once per component**. Work through atoms first, then molecules (which are
combinations of already-specced atoms), then organisms. Attempting a molecule before its atom
dependencies are specced produces a spec that references undefined components.

## Where things live

- **Read** `ds-audit.md` for the component scope and build order.
- **Read** the foundation files at `<real_project_path>/design-system/foundations/` for token
  names to reference.
- **Write** the spec to
  `<real_project_path>/design-system/<level>/<component-name>/component-spec.md`
  where `<level>` is `atoms`, `molecules`, or `organisms`.

---

## The skill contract

### Inputs
- `ds-audit.md` (the component's atomic level, status, and any noted inconsistencies).
- The foundation files (token names for color, typography, spacing, etc.).
- For molecules/organisms: the already-written specs of the atom/molecule dependencies.

### Input Acceptance Criteria
- `ds-audit.md` lists this component as in scope for this task.
- Foundation files exist and define the token names this component will reference. If a needed
  token is missing, flag it as a foundation gap before proceeding.
- For molecules/organisms: all atom/molecule dependencies are already specced. If a dependency
  is missing, spec it first — never reference an undefined component.

### Outputs
- `<real_project_path>/design-system/<level>/<component-name>/component-spec.md`

### Output Quality Criteria
- **Atomic level is correct**: atoms have no component dependencies (only token references);
  molecules reference only atoms; organisms reference molecules and/or atoms.
- **All variants are defined** — a variant is a meaningfully different version of the component
  (e.g. Button: Primary, Secondary, Ghost, Danger). If the audit noted variants, they are all
  covered.
- **All states are defined** — for each interactive or variable component, the full set of
  states: default, hover, focus, active, disabled, loading, error, success, empty (as applicable).
- **Anatomy references token names** — every visual property (color, font, spacing, radius,
  shadow) is expressed as a token name (e.g. `color.action.primary`), never a raw value.
- **Molecule/organism anatomy references component names** — sub-components are referenced by
  their name (e.g. "contains: Input (atom), InlineMessage (atom)"), never redefined.
- **Behaviour is specified** — what happens on interaction: focus management, transitions,
  animation token used, any ARIA role or keyboard behaviour.
- **Usage rules are actionable** — do/don't rules that prevent common misuse of this component.

---

## The 3-gate flow

### Gate 1 — Input
Identify the component from `ds-audit.md`. Confirm its atomic level and check that all
dependencies (foundations for atoms; atom specs for molecules; atom/molecule specs for organisms)
exist. If a dependency is missing, **do not proceed** — hand off to spec the dependency first.

### Gate 2 — Process
Work through the component spec with the designer. For atoms, start from the token layer up.
For molecules/organisms, start from the component dependencies.

Explicitly probe for completeness:
- Are there more variants than the obvious ones? (e.g. Button also needs an icon-only variant)
- Are all interactive states covered, including loading and disabled?
- Are there accessibility requirements (ARIA role, keyboard navigation, focus ring)?
- For organisms: are the responsive/layout rules defined?

Write the component spec:

```markdown
# <ComponentName> — <atom / molecule / organism>

_Level: atom · Last updated: <date>_

## Purpose
<1 sentence: what this component does and when to use it>

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
| Loading | Spinner (Spinner atom) replaces label | Async action in progress |

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

## [Molecules/Organisms only] Contains
| Component | Level | Role in this component |
|---|---|---|
| Input | atom | The text entry field |
| InlineMessage | atom | Error or hint text below the input |

## Behaviour
- On click/tap: triggers the action; enters loading state if async.
- Keyboard: `Enter` and `Space` activate. Tab moves focus to the next interactive element.
- ARIA: `role="button"`. Use `aria-disabled="true"` (not `disabled`) to keep keyboard focus.
- Animation: none on state change (use `animation.none`); loading spinner uses `animation.spin`.

## Usage rules
**Do:**
- Use Primary for the single most important action per section.
- Use Danger only for destructive actions (delete, remove, cancel irreversibly).

**Don't:**
- Don't use two Primary buttons side by side — choose one.
- Don't use Ghost for primary or important actions.
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that all anatomy references are token names
(never raw values), and that all variants and states are covered. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file under the correct atomic-level folder, tick the component
   step in `## Plan` (or note which components remain if this skill runs multiple times), update
   **Next step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed component specs feed `designer-ds-document`, which writes usage guidelines and builds
the system index. In product-design work, `designer-ui` references these components by name —
e.g. "Button / Primary" maps to `design-system/atoms/button/component-spec.md`.
