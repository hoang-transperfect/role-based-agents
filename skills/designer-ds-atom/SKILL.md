---
name: designer-ds-atom
description: >
  Writes the component spec for one design system atom — the indivisible UI building block with
  no component dependencies (only token references). Follows the project's atom spec template:
  frontmatter (name, version, description, link, dependencies), Anatomy (Structure + Details),
  Appearance (Props + Variants + State + Tokens), Content (Copy + Empty state + Overflow + Case
  treatment + Allowed characters + Placeholder + Number and date formatting + Text expansion),
  Accessibility (ARIA table + Focus management + Keyboard table + Mouse + Touch + Screen reader
  table + Internationalization), and a Checklist (Design + Engineering + QA). Invoke once per
  atom listed in ds-audit.md, after designer-ds-foundation has defined the token layer. Icon and
  Text must be specced before any other atom. Atoms must be specced before any molecule or DS
  organism that depends on them. Produces one component-spec.md per atom under
  design-system/atoms/.
---

# designer-ds-atom

An atom is the smallest indivisible UI element in the design system — Button, Input, Checkbox,
Badge, Icon, Avatar, Spinner, Tooltip, etc. It has **no component dependencies**: its anatomy
references only foundation token names, never other components.

**Icon and Text must always be the first two atoms specced**, in that order. Nearly every other
atom embeds an icon slot or a text label — Button, Input, Badge, Alert, Tag, Avatar all reference
one or both. Speccing other atoms before Icon and Text forces forward references in their anatomy
that break the dependency chain. Once Icon and Text exist, all remaining atoms can be specced in
any order.

Getting atoms right is critical because every molecule and DS organism is built from them. A
missing variant, state, content rule, or accessibility behaviour here creates a gap that
cascades through every higher-level component.

## Where things live

- **Read** `ds-audit.md` for the atom's scope, notes, and any inconsistencies to resolve.
- **Read** the foundation files at `<real_project_path>/design-system/foundations/` for the
  token names this atom's anatomy will reference.
- **Write** `<real_project_path>/design-system/atoms/<component-name>/component-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` — confirms this atom is in scope and lists any noted inconsistencies.
- Foundation files — the token names for color, typography, spacing, radius, animation, etc.

### Input Acceptance Criteria
- `ds-audit.md` lists this atom as in scope for this task.
- Foundation files exist and define the token names this atom will reference. If a needed token
  category is missing, flag it as a foundation gap and hand off to `designer-ds-foundation`
  before proceeding.
- **If this atom is not Icon or Text**: both
  `<real_project_path>/design-system/atoms/icon/component-spec.md` and
  `<real_project_path>/design-system/atoms/text/component-spec.md` must exist. If either is
  missing, stop and route to spec the missing one first — do not proceed with any other atom.

### Outputs
- `<real_project_path>/design-system/atoms/<component-name>/component-spec.md`

### Output Quality Criteria

**Anatomy:**
- No component dependencies — anatomy references only token names, never other components.
  An atom that references a sub-component is actually a molecule; reclassify before proceeding.
- Structure captures every visual part, correctly nested, with layout role described.
- Details covers any constraint, rule, or slot behaviour not obvious from the structure.

**Appearance:**
- Every visual style the component can exhibit is documented — no property may be omitted or left to inference. Full coverage ensures consistent, unambiguous implementation.
- Every prop that affects visual output is listed with all accepted values and the default marked.
- Every variant has a table mapping each value to its token-based style. `N/A` is explicit where
  a variant has no style change.
- States are split correctly: appearance states (system-driven) vs interaction states
  (user-driven). Only states that produce a visual change are listed.
- Tokens table lists every token the component references — no raw values anywhere.

**Content:**
- Every string the component owns is listed in the Copy table with its ID, default text, context,
  and whether it is translatable. Skip only if the component renders no strings of its own.
- Empty state, Overflow, Case treatment, Allowed characters, Placeholder, Number/date formatting,
  and Text expansion sections are each present. Sections that do not apply are explicitly marked
  "(Skip if not applicable)" with a brief justification — never silently omitted.

**Accessibility:**
- ARIA table lists every attribute the component needs with value, required flag, and condition.
- Focus management specifies the HTML element, tab stop, focus order, and focus trap behaviour.
- Keyboard table lists every key the component responds to — at minimum Tab and Shift+Tab; Enter
  and/or Space for interactive components; arrow keys for composite widgets.
- Mouse and Touch specify cursor, click target, and minimum touch target (44×44px).
- Screen reader table documents every state change with the text announced and the method.
- Internationalization specifies RTL mirroring and the `dir` attribute strategy.

**Checklist:**
- Spec section is present and all four items (Anatomy, Appearance, Content, Accessibility) are checked or explicitly waived with justification.
- All checklist items are present for Design, Engineering, and QA sections.
- Component-specific items are filled in; generic placeholders are not left as `{component-specific item}`.
- Status is not set to Approved until all items are checked or explicitly waived with justification.

---

## The 3-gate flow

### Gate 1 — Input
Confirm this atom is in scope in `ds-audit.md`. Verify the foundation tokens it needs are
defined. If a foundation token category is missing, hand off to `designer-ds-foundation` first.

**If this atom is not Icon or Text**, check that both
`<real_project_path>/design-system/atoms/icon/component-spec.md` and
`<real_project_path>/design-system/atoms/text/component-spec.md` exist. If either is missing,
stop: "Icon and Text must be specced before any other atom. Let's spec {missing one} first."
Do not proceed until both files exist.

### Gate 2 — Process
Work through each section of the spec with the designer. Complete each major section before
moving to the next.

**Anatomy** — probe:
- What visual parts compose this atom? (container, label, icon slot, indicator, overlay…)
- How are they nested? What is the layout role of each? (horizontal stack, icon slot, label)
- Any constraints or slot behaviours not obvious from the structure?

**Appearance** — probe:
- What props affect visual output? What are all accepted values and the default for each?
- Are there visual variants beyond the obvious? (icon-only, ghost, destructive, full-width…)
- Which states produce a visual change? Separate system-driven (loading, error, success) from
  user-driven (hover, focus, active, disabled).
- List every token referenced across all of the above.

**Content** — probe:
- Does this atom render any strings of its own? (built-in labels, ARIA announcements, defaults)
- What happens when there is no content? (fallback icon, initials, dash, hidden)
- Does text overflow? What are the max length and overflow rules?
- Is casing enforced or consumer-controlled?
- Are there character restrictions? (inputs: allowed charset, emoji, special chars, HTML entities)
- Is there a placeholder? When does it disappear?
- Does this atom render numbers, dates, or currency? If yes, are they locale-aware?
- What is the max text expansion budget? What happens when the label exceeds the max width?

**Accessibility** — probe:
- Which ARIA attributes are needed? Is a `role` needed (only if native HTML semantics are
  insufficient)? Which aria-* attributes (label, describedby, disabled, invalid, busy, expanded,
  pressed, checked, live) are required or optional and under what condition?
- What HTML element is used? Is it a tab stop? Natural DOM order or managed tabindex?
- What keys does this atom respond to? At minimum Tab/Shift+Tab. Enter/Space for interactive.
  Arrow keys if it is a composite widget.
- Cursor style and click target area for mouse.
- Minimum 44×44px touch target — does it equal visual bounds or is it extended?
- For every state change a screen reader user must be aware of: what text is announced and how?
- Does the layout mirror in RTL? Which icons or elements do not mirror? Does `dir` inherit or
  is it forced?

**Checklist** — verify each spec section in the Spec checklist (Anatomy, Appearance, Content,
Accessibility), then fill in component-specific items for Design, Engineering, and QA. Do not
leave `{component-specific item}` as a placeholder.

Write the spec using the project atom template:

```markdown
---
name: {component-name}
version: 0.0.1
description: {one sentence — what this atom does}
link:
  - {tool-name}: {tool-link}
dependencies:
  - components: N/A
---
# {Component Name}

## Anatomy

Define the component's structure and the role of each part. Structure captures the layout
nesting; Details describes what each part does or receives.

### Structure
Map every part, nested under its parent. Name each part by its function. Describe the layout
role (e.g. horizontal stack, icon slot, label).

- {layer name}: {layout description}
    - {child layer}
    - {child layer}

### Details
Describe constraints, rules, or slot behavior that are not obvious from the structure alone.
Note which layers receive a child component.

- {layer name}: {detail}
- {child layer}: receive a `{component-name}` component

---

## Appearance

Define all visual properties — props, variants, states, and the tokens that drive them. This section must be exhaustive: every style the component can exhibit must be documented here. No visual property may be left to inference — gaps create inconsistent, ambiguous implementations.

### Props
List every prop that affects visual output. Format: prop name, all accepted values with the
default marked.

1. {prop-name}: `{value}` (default), `{value}`

### Variants
List each variant prop as a numbered item. For each, provide a table mapping every value to
its visual style. `N/A` means no style change from default.

1. {variant name} (default value: {default})

   | {variant name}  | {style} |
   |-----------------|---------|
   | {variant value} | {value} |

### State

Appearance states are driven by the **system** (what the UI is showing). Interaction states
are driven by the **user** (what the user is doing). Only list states that produce a visual
change.

1. Appearance states — system-driven UI status

   | State    | {styles} |
   |----------|----------|
   | {state}  | {value}  |

2. Interaction states — user-driven UX response

   | State    | {styles} |
   |----------|----------|
   | {state}  | {value}  |

### Tokens
List all design tokens this component references.

| Name    | Component or Semantic Token |
|---------|-----------------------------|
| {token} | {value}                     |

---

## Content

### Copy
List every string this component owns — built-in labels, defaults, and announcements. Skip if
the component renders no strings of its own.

| String ID | Default text | Context | Translatable? |
|-----------|-------------|---------|---------------|
| `{id}` | {text} | {where it appears} | Yes / No |

### Empty state
(Skip if not applicable.)
- What renders when there is no content: {e.g. fallback icon, initials, dash, hidden}
- Empty state is: component-defined / consumer-provided

### Overflow
| Rule | Spec |
|------|------|
| Max length (characters) | |
| Overflow behavior | ellipsis / wrap / scroll |
| Tooltip on truncation | Yes / No |
| Line clamp | {n} lines / N/A |

### Case treatment
(Skip if not applicable.)
- Enforced casing: sentence case / title case / ALL CAPS / none — consumer controls
- Can the consumer override: Yes / No

### Allowed characters
(Skip if not applicable — most relevant for inputs.)
- Allowed character set: {e.g. Unicode / alphanumeric only}
- Emoji support: Yes / No
- Special characters (©, ™, →, etc.): allowed / stripped / escaped
- HTML entities: allowed / escaped

### Placeholder
(Skip if not applicable — inputs and selects only.)
- Placeholder text: {text}
- Disappears on: focus / first character typed
- Returns on: clear / blur while empty

### Number and date formatting
(Skip if not applicable — only for components that render numbers, dates, or currency.)
- Number format: locale-aware / fixed pattern
- Date format: locale-aware / fixed pattern
- Currency: locale-aware / fixed pattern / not applicable

### Text expansion
- Max text expansion (e.g. +40% for German): {value}
- Layout when label exceeds max width: truncate / wrap / push container
- RTL: see Accessibility > Internationalization

---

## Accessibility

Specify requirements for keyboard, pointer, touch, and screen reader users. Mark any section
N/A with justification if it does not apply to this component.

### ARIA

List only the attributes this component needs. Common ones to consider: `role` (only if native
HTML semantics are insufficient), `aria-label` / `aria-labelledby` (when no visible label
exists), `aria-describedby` (hint or error text), `aria-disabled`, `aria-invalid`, `aria-busy`,
`aria-expanded`, `aria-pressed`, `aria-checked`, `aria-live`.

| Attribute | Value | Required? | Condition |
|-----------|-------|-----------|-----------|
| `{attr}` | `{value}` | Yes / No | {when} |

### Focus management
- Element: `<{tag}>` (justify if non-semantic element is used)
- Tab stop: Yes / No
- Focus order: natural DOM order / managed with `tabindex`
- Focus trap: none / traps within / returns to trigger on close

### Keyboard

List every key this component responds to. Every focusable component handles `Tab` and
`Shift+Tab` at minimum. Interactive components typically also handle `Enter` and/or `Space`.
Composite widgets (menus, tabs, sliders) use arrow keys with roving `tabindex`.

| Key | Action |
|-----|--------|
| `{key}` | {action} |

### Mouse
- Cursor: `pointer` / `default` / `not-allowed` (disabled)
- Click target area: visual bounds / extended hit area

### Touch
- Minimum touch target: 44×44px
- Touch target equals visual bounds: Yes / No — if No, describe extension

### Screen reader

Document every state change a screen reader user needs to be aware of. Common ones: error
becomes visible, loading starts/ends, value changes, disabled. For each, specify what text is
announced and how (native semantics, `aria-describedby`, `aria-live`, etc.).

| State change | Text announced | Method |
|--------------|---------------|--------|
| {state} | {text} | {method} |

### Internationalization
- RTL layout mirrors: Yes / No — list any icons or elements that do not mirror
- `dir` attribute: inherits / always LTR / always RTL

---

## Checklist

All items must pass or be explicitly waived with justification before status moves to
**Approved**.

### Spec
- [ ] Anatomy: structure and details documented; no raw values
- [ ] Appearance: all props, variants, states, and tokens complete
- [ ] Content: all sections present or explicitly marked N/A with justification
- [ ] Accessibility: ARIA, focus, keyboard, mouse, touch, screen reader, and i18n documented

### Design
- [ ] All variants and states are designed, or marked N/A with justification
- [ ] All values applied via design tokens — no hardcoded hex, px, or font values
- [ ] Dark mode verified for all variants and states
- [ ] Focus ring visible and meets contrast in light and dark mode
- [ ] RTL layout reviewed (if shipped in any RTL locale)
- [ ] {component-specific item}

### Engineering
- [ ] Rendered output matches spec at all breakpoints
- [ ] All props documented with types and defaults
- [ ] Keyboard interactions implemented per spec
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
Check against the Output Quality Criteria across all sections. Key checks: no raw values in
Anatomy or Tokens, every Content section present (or explicitly skipped with reason), ARIA
and Screen reader use table format, Checklist has component-specific items filled in. When the
bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick the atom in Step 3a in `## Plan`, update **Next
   step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed atom specs feed `designer-ds-molecule` (which references atoms by name in its
Dependencies and Anatomy) and `designer-ds-organism`. They also feed `designer-ds-document`,
which indexes them in the README. In product design, atoms are referenced by name —
e.g. "Button / Primary" maps to `design-system/atoms/button/component-spec.md`.
