---
name: designer-ds-molecule
description: >
  Writes the component spec for one design system molecule — a simple combination of atoms that
  functions as a unit (e.g. FormField = Label + Input + InlineMessage). Follows the project's
  molecule spec template: frontmatter (name, version, description, link, dependencies with
  separate atoms and molecules keys), Anatomy (Composition table + Layout + Spacing), Appearance
  (molecule-level Variants + State with atoms-affected columns + Tokens), Content (Copy + Label +
  Helper text + Validation messages + Overflow + Text expansion), Accessibility (ARIA relationships
  table + Keyboard flow table + Focus management + Mouse + Touch + Screen reader + Internationali-
  zation), and Checklist (Design + Engineering + QA). Invoke once per molecule listed in
  ds-audit.md, after all atom dependencies are specced. Molecules must be specced before any DS
  organism that depends on them. Produces one component-spec.md per molecule under
  design-system/molecules/.
---

# designer-ds-molecule

A molecule is a simple, purposeful combination of atoms that works as a unit. A form field
(label + input + hint/error), a search bar (input + button), a pagination control — these are
molecules. The molecule adds meaning by combining atoms; it does not introduce new visual
primitives of its own.

The key constraint: **every sub-component in a molecule is a named DS atom, foundation
component (Text, Icon), or another named DS molecule**. Visual tokens (color, typography,
radius, shadow) are inherited from constituent components — the molecule spec specifies only
molecule-level rules: layout, spacing, state propagation, ARIA relationships between
sub-components, and keyboard flow order.

**No raw HTML elements for content** — every content-rendering slot in the Composition table
must reference a named DS atom or foundation component, not a raw HTML element (e.g. not `<span>`,
`<img>`, `<p>`). Layout wrappers (`<div>`, `<ul>`, `<nav>`, etc.) used purely to structure
layout are the only exception.

## Where things live

- **Read** `ds-audit.md` for the molecule's scope, dependencies, and notes.
- **Read** foundation component specs at `<real_project_path>/design-system/foundation-components/`
  for any foundation components (Text, Icon) this molecule uses directly.
- **Read** atom specs at `<real_project_path>/design-system/atoms/` for every atom this molecule
  composes.
- **Read** molecule specs at `<real_project_path>/design-system/molecules/` for any molecules
  this molecule composes.
- **Read** foundation files at `<real_project_path>/design-system/foundations/` for any spacing
  tokens needed at the molecule level.
- **Write** `<real_project_path>/design-system/molecules/<component-name>/component-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` — confirms this molecule is in scope and lists its dependencies.
- Atom specs (and molecule specs if any) for all sub-components — must be written before this
  molecule. If any dependency is missing, hand off to `designer-ds-atom` (or
  `designer-ds-molecule` for a molecule dependency) first.
- Foundation files — for spacing tokens used in the Layout and Spacing sections.

### Input Acceptance Criteria
- `ds-audit.md` lists this molecule as in scope.
- All foundation component, atom, and molecule dependencies are already specced. Never reference
  an undefined component.

### Outputs
- `<real_project_path>/design-system/molecules/<component-name>/component-spec.md`

### Output Quality Criteria

**Frontmatter:**
- `dependencies` uses separate `foundation-components`, `atoms`, and `molecules` keys. List every
  named dependency; use `N/A` for keys with no direct dependency.

**Anatomy:**
- Composition table lists every atom used with the props it receives and its purpose.
- Any direct Text or Icon foundation component reference in the Composition table names the
  specific style variant used (e.g. `Text / label-medium`). A generic "Text" entry with no
  variant is incomplete.
- Layout section specifies direction, cross-axis alignment, wrapping, and includes an ASCII or
  prose diagram.
- Spacing table lists the gap token between each pair of adjacent atoms.

**Appearance:**
- Every molecule-level style the component can exhibit is documented — no property may be omitted or left to inference. Full coverage ensures consistent, unambiguous implementation.
- Variants table includes an "Atoms affected" column — which atoms change and how.
- State tables (appearance + interaction) include "Atoms affected" and "Visual changes" columns
  — state propagation is explicit, never implied.
- Tokens section lists only molecule-level tokens; atom tokens are not repeated here.

**Content:**
- Copy table lists molecule-owned strings only (not consumer-provided or atom-owned).
- Label, Helper text, and Validation messages sections are present. Sections that don't apply
  are explicitly marked "(Skip if not applicable)" — never silently omitted.
- Overflow and Text expansion are specified.

**Accessibility:**
- ARIA table documents relationships *between* atoms (label→input, input→error, aria-required)
  — not individual atom ARIA, which is owned by atom specs. Columns: attribute / on element /
  points to / purpose.
- Keyboard flow table documents the tab order through all focusable child atoms with entry
  and exit behaviour. Every molecule must define this.
- Focus management specifies first focus target, whether focus moves to error on submit, and
  focus trap behaviour.
- Screen reader table covers only molecule-level state changes.
- Internationalization specifies RTL mirroring and `dir` strategy.

**Checklist:**
- Spec section is present and all four items (Anatomy, Appearance, Content, Accessibility) are checked or explicitly waived with justification.
- All three sections (Design, Engineering, QA) are present with molecule-specific items filled
  in. No `{component-specific item}` placeholder left unfilled.

---

## The 3-gate flow

### Gate 1 — Input
Verify all foundation component, atom, and molecule dependencies are specced. If any are
missing, hand off to the appropriate skill first. Confirm spacing tokens are defined in
foundations.

### Gate 2 — Process
Work through each section of the spec with the designer.

**Anatomy** — probe:
- Which atoms (and molecules) compose this molecule? What props does each receive? What is
  each one's purpose within the molecule?
- How are they arranged spatially? (direction, alignment, wrapping)
- What is the gap between each pair of adjacent atoms? Which spacing token?
- Can you sketch or describe the layout as a simple ASCII or prose diagram?

**Appearance** — probe:
- Are there molecule-level variants beyond what the individual atoms expose? Which atoms are
  affected by each variant value?
- Which system states apply (loading, error, success, disabled)? For each, which atoms are
  affected and what visual change occurs?
- Which user-driven interaction states apply at the molecule level (hover, focus, active)?
- Which spacing or layout tokens does this molecule introduce (not owned by atoms)?

**Content** — probe:
- Does this molecule own any strings directly? (validation messages, required indicators,
  helper text defaults — not consumer-provided content)
- Is there a label? Where does it sit (above / inline / floating)? Required indicator style?
  Max length and overflow behaviour?
- Is there helper text? Where does it sit? Max length and overflow?
- For form molecules: what validation rules apply? What is each message and when does it appear
  (on blur / on change / on submit)?
- What are the overflow and text expansion rules?

**Accessibility** — probe:
- What ARIA relationships exist *between* atoms? (label → input via `for`/`htmlFor`;
  input → helper text via `aria-describedby`; input → error via `aria-describedby` or
  `aria-errormessage`; `aria-required` on the input)
- What is the tab order through the focusable atoms? What happens on entry (first Tab into
  the molecule) and exit (Tab out of the last focusable atom)?
- What is the first focus target when the molecule is activated?
- On form submit with validation errors, does focus move to the error? Which element?
- Is there a focus trap?
- Cursor and click target for mouse. Touch target size.
- For every molecule-level state change a screen reader must announce: what text and how?
- RTL: does the layout mirror? Which atoms or elements do not mirror? `dir` strategy?

**Checklist** — verify each spec section in the Spec checklist (Anatomy, Appearance, Content,
Accessibility), then fill in component-specific items for Design, Engineering, and QA. Do not
leave `{component-specific item}` as a placeholder.

Write the spec using the project molecule template:

```markdown
---
name: {molecule-name}
version: 0.0.1
description: {one sentence — what this molecule does and why these atoms are combined}
link:
  - {tool-name}: {tool-link}
dependencies:
  - foundation-components: N/A  # list Text and/or Icon if used directly
  - atoms: {atom-a}, {atom-b}
  - molecules: {molecule-a}
---
# {Molecule Name}

## Anatomy

Define which atoms compose this molecule, how they are arranged, and the spacing between them.
Visual tokens (color, typography, radius, shadow) are inherited from constituent atoms —
specify only molecule-level rules here.

### Composition
List every atom used. For each, describe what props it receives and its purpose within the
molecule.

| Atom | Props passed | Purpose |
|------|-------------|---------|
| `{atom-name}` | {props} | {purpose} |

### Layout
Describe how the atoms are arranged spatially — direction, alignment, wrapping behavior.

- Direction: horizontal / vertical
- Cross-axis alignment: start / center / end / stretch
- Wrapping: yes / no

```
{ASCII or prose layout diagram}
```

### Spacing
List the gap between each pair of adjacent atoms.

| Gap | Token |
|-----|-------|
| {atom-a} → {atom-b} | {token} |

---

## Appearance

Specify only molecule-level variants, states, and token overrides. Atom-level styles are owned
by their respective atom specs. This section must be exhaustive for all molecule-level styles:
every variant, state, and token the molecule introduces must be documented. Leave nothing to
inference — gaps create inconsistent, ambiguous implementations.

### Variants
List each molecule-level variant. For each, describe which atoms are affected and how.

1. {variant name} (default: {default})

   | {variant name}  | Atoms affected | {style change} |
   |-----------------|----------------|----------------|
   | {variant value} | {atoms}        | {value}        |

### State

Appearance states are driven by the **system** (what the UI is showing). Interaction states
are driven by the **user** (what the user is doing). For each state, describe which child atoms
are affected and what changes.

1. Appearance states — system-driven UI status

   | State   | Atoms affected | Visual changes |
   |---------|----------------|----------------|
   | {state} | {atoms}        | {value}        |

2. Interaction states — user-driven UX response

   | State   | Atoms affected | Visual changes |
   |---------|----------------|----------------|
   | {state} | {atoms}        | {value}        |

### Tokens
List only tokens this molecule introduces. Tokens already defined in constituent atoms do not
need repeating.

| Name    | Component or Semantic Token |
|---------|-----------------------------|
| {token} | {value}                     |

---

## Content

### Copy
List every string this molecule owns directly — not strings passed through from atoms or
provided by consumers. Common examples: validation messages, required field indicators, helper
text defaults.

| String ID | Default text | Context | Translatable? |
|-----------|-------------|---------|---------------|
| `{id}` | {text} | {where it appears} | Yes / No |

### Label
(Skip if not applicable.)
- Position: above / inline / floating / none
- Required indicator: asterisk / text "(required)" / none
- Max length: {value}
- Overflow: truncate / wrap

### Helper text
(Skip if not applicable.)
- Position: below / inline / tooltip
- Max length: {value}
- Overflow: truncate / wrap

### Validation messages
(Skip if not applicable — form molecules only.)
List each validation rule, its message, and when the message appears.

| Rule | Message | Timing |
|------|---------|--------|
| `{rule}` | {message text} | on blur / on change / on submit |

### Overflow
| Rule | Spec |
|------|------|
| Max length (characters) | |
| Overflow behavior | ellipsis / wrap / scroll |
| Tooltip on truncation | Yes / No |
| Line clamp | {n} lines / N/A |

### Text expansion
- Max text expansion (e.g. +40% for German): {value}
- Layout when label exceeds max width: truncate / wrap / push container
- RTL: see Accessibility > Internationalization

---

## Accessibility

Specify molecule-level accessibility requirements. Individual atom requirements are owned by
their respective atom specs. Mark any section N/A with justification if it does not apply.

### ARIA
Document relationships **between** atoms — associations that cannot be specified in individual
atom specs. Common ones: label → input (`for`/`htmlFor`), input → helper text
(`aria-describedby`), input → error message (`aria-describedby` or `aria-errormessage`),
required state (`aria-required`).

| Attribute | On element | Points to | Purpose |
|-----------|-----------|-----------|---------|
| `{attr}` | `{element}` | `{target}` | {purpose} |

### Keyboard flow
Document the tab order through all focusable child atoms. Every molecule must define entry
and exit behavior.

| Order | Element | Key | Behavior |
|-------|---------|-----|----------|
| 1 | {element} | `Tab` | enter molecule |
| {n} | {element} | `{key}` | {behavior} |

### Focus management
- First focus target when molecule is activated: {element}
- Focus moves to error on submit: Yes / No — if Yes, target: {element}
- Focus trap: none / traps within / returns to trigger on close

### Mouse
- Cursor: `pointer` / `default` / `not-allowed` (disabled)
- Click target area: visual bounds / extended hit area

### Touch
- Minimum touch target: 44×44px
- Touch target equals visual bounds: Yes / No — if No, describe extension

### Screen reader
Document every molecule-level state change a screen reader user needs to be aware of.
Atom-level announcements are owned by atom specs.

| State change | Text announced | Method |
|--------------|---------------|--------|
| {state} | {text} | {method} |

### Internationalization
- RTL layout mirrors: Yes / No — list atoms or elements that do not mirror
- `dir` attribute: inherits / always LTR / always RTL

---

## Checklist

All items must pass or be explicitly waived with justification before status moves to
**Approved**.

### Spec
- [ ] Anatomy: composition, layout, and spacing documented
- [ ] Appearance: molecule-level variants, states, and tokens complete; "atoms affected" columns filled
- [ ] Content: all sections present or explicitly marked N/A with justification
- [ ] Accessibility: ARIA relationships, keyboard flow, focus management, screen reader, and i18n documented

### Design
- [ ] All variants and states are designed, or marked N/A with justification
- [ ] Spacing between atoms matches tokens in spec
- [ ] All values applied via design tokens — no hardcoded hex, px, or font values
- [ ] Dark mode verified for all variants and states
- [ ] RTL layout reviewed (if shipped in any RTL locale)
- [ ] {component-specific item}

### Engineering
- [ ] Rendered output matches spec at all breakpoints
- [ ] All props documented with types and defaults
- [ ] ARIA relationships between atoms implemented per spec
- [ ] Keyboard tab order matches spec
- [ ] Validation messages appear at correct timing per spec
- [ ] No axe-core violations in any state
- [ ] {component-specific item}

### QA
- [ ] Cross-browser smoke test passed
- [ ] Touch target ≥ 44×44px confirmed
- [ ] Screen reader tested: NVDA + Firefox, VoiceOver + Safari
- [ ] Visual regression baseline captured
- [ ] {component-specific item}
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that Anatomy has all three subsections
(Composition, Layout, Spacing), state tables include the "Atoms affected" column, ARIA covers
inter-atom relationships (not individual atom ARIA), and the Keyboard flow table defines entry
and exit. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick the molecule in Step 3b in `## Plan`, update **Next
   step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed molecule specs feed `designer-ds-organism` (references molecules and atoms by name
in its Dependencies and Anatomy), `designer-ds-validate` (for add/update sub-modes), and
`designer-ds-document` (README index). In product design, molecules are referenced by name
in organism and page specs.
