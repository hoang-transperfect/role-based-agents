---
name: designer-ds-molecule
description: >
  Writes the component spec for one design system molecule — a simple combination of atoms that
  functions as a unit (e.g. FormField = Label + Input + InlineMessage). Anatomy references atom
  names and token names; never raw values. Invoke once per molecule listed in ds-audit.md, after
  all atom dependencies are specced by designer-ds-atom. Molecules must be specced before any DS
  organism that depends on them. Produces one component-spec.md per molecule under
  design-system/molecules/.
---

# designer-ds-molecule

A molecule is a simple, purposeful combination of atoms that works as a unit. A form field
(label + input + hint/error), a search bar (input + button), a pagination control — these are
molecules. The molecule adds meaning by combining atoms; it does not introduce new visual
primitives of its own.

The key constraint: **every sub-component in a molecule is a named atom** from the design
system — referenced by name, never redefined. Token references are allowed only for molecule-
level layout properties not covered by the atoms themselves (e.g. gap between sub-components).

## Where things live

- **Read** `ds-audit.md` for the molecule's scope, dependencies, and notes.
- **Read** the atom specs at `<real_project_path>/design-system/atoms/` for the atoms this
  molecule composes.
- **Read** foundation files at `<real_project_path>/design-system/foundations/` for any layout
  tokens needed at the molecule level.
- **Write** `<real_project_path>/design-system/molecules/<component-name>/component-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` — confirms this molecule is in scope and lists its atom dependencies.
- Atom specs for all atoms this molecule composes (must be written before this molecule).
- Foundation files — for any molecule-level layout token references.

### Input Acceptance Criteria
- `ds-audit.md` lists this molecule as in scope.
- All atom dependencies are already specced (have a `component-spec.md` under `atoms/`). If
  any atom dependency is missing, hand off to `designer-ds-atom` first — never reference an
  undefined component.

### Outputs
- `<real_project_path>/design-system/molecules/<component-name>/component-spec.md`

### Output Quality Criteria
- **Sub-components are named atoms** — every component in the "Contains" section is a named DS
  atom. A molecule that contains another molecule should be reconsidered; discuss atomic level
  with the designer.
- **All variants are defined** — every variant noted in the audit.
- **All states are defined** — as applicable: the molecule may inherit states from its atoms
  (e.g. FormField in error state drives Input's error state) — document the inheritance clearly.
- **Anatomy references token names or atom names** — molecule-level layout properties use tokens;
  sub-component properties reference atom names, not raw values.
- **Behaviour is specified** — especially focus management and state propagation between atoms.
- **Usage rules are actionable** — when to use this molecule vs. its constituent atoms separately.

---

## The 3-gate flow

### Gate 1 — Input
Verify all atom dependencies are specced. If any are missing, hand off to `designer-ds-atom`
first. Confirm foundation tokens for molecule-level layout are defined.

### Gate 2 — Process
Work through the molecule spec with the designer. Start from the atom layer — what atoms compose
this molecule and what role does each play?

Probe for completeness:
- How do states propagate? (e.g. when the molecule enters error state, which atom changes?)
- Are there variants of the molecule beyond its atoms' variants?
- How does focus move between atoms inside the molecule?

Write the molecule spec:

```markdown
# <ComponentName> — molecule

_Level: molecule · Last updated: <date>_

## Purpose
<1 sentence: what this molecule does and why these atoms are combined>

## Variants
| Variant | When to use |
|---|---|
| Default | Standard use |
| Inline | Compact, horizontal layout for tight spaces |

## States
| State | What changes | Notes |
|---|---|---|
| Default | — | All atoms in their default state |
| Error | Input → error state; InlineMessage shown with error text | Set by form validation |
| Disabled | Input → disabled; Label opacity 60% | All sub-atoms disabled together |

## Contains
| Component | Level | Role in this molecule |
|---|---|---|
| Label | atom | Identifies the field |
| Input | atom | The text entry element |
| InlineMessage | atom | Error or hint text (shown conditionally) |

## Anatomy
_(Molecule-level layout properties only — sub-component appearance is owned by the atom spec)_

| Part | Property | Token |
|---|---|---|
| Container | Gap between Label and Input | `spacing.xs` |
| Container | Gap between Input and InlineMessage | `spacing.xs` |

## Behaviour
- Focus: Tab enters the Input atom; the molecule does not intercept focus.
- Error state: the parent form sets the molecule to error state, which sets Input's error state
  and shows InlineMessage with the error text.
- ARIA: `role="group"` with `aria-labelledby` pointing to the Label atom.

## Usage rules
**Do:**
- Use FormField whenever a Label + Input pair appears — it ensures consistent spacing and error
  handling.

**Don't:**
- Don't use Label and Input atoms separately when they are logically paired — use this molecule.
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that sub-components are named atoms (not
redefined) and states are fully specified including propagation. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick the molecule in Step 3b in `## Plan`, update **Next
   step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed molecule specs feed `designer-ds-organism` (which references molecules and atoms by
name) and `designer-ds-document` (which indexes them in the README). In product design,
molecules are referenced by name in organism specs — e.g. "FormField" maps to
`design-system/molecules/form-field/component-spec.md`.
