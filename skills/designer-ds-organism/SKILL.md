---
name: designer-ds-organism
description: >
  Writes the component spec for one design system organism — a complex, generic, reusable UI
  component composed of molecules and/or atoms (e.g. NavigationBar, DataTable, Modal, Card).
  Follows the project's organism spec template: frontmatter (name, version, description, link,
  dependencies with separate molecules and atoms keys), Anatomy (Composition table + Layout +
  Spacing), Appearance (organism-level Variants + Lifecycle/Interactive State + Tokens),
  Responsive (Breakpoints + Reflow strategy + Mobile-specific patterns), Content (Copy with i18n
  namespace + Empty state + Error state + Notifications + Text expansion), Examples (Happy path +
  Edge cases + Worst-case content), Accessibility (Landmark structure + Heading hierarchy + ARIA
  + Keyboard + Focus management + Live regions + Screen reader + Skip links + Internationali-
  zation), and Checklist (Design + Engineering + QA). DS organisms are generic — no product-
  specific IA, data labels, or business logic. Invoke once per organism listed in ds-audit.md,
  after all dependencies are specced. Produces one component-spec.md per organism under
  design-system/organisms/.
---

# designer-ds-organism

A DS organism is a complex, self-contained UI component built from molecules and atoms. It is
**generic and reusable** — a NavigationBar, DataTable, Modal, Card, Sidebar, Form — something
that makes sense in any product without modification to its structure or visual rules.

Organisms are the primary level where responsive reflow decisions are made, where lifecycle
states (loading, empty, error) are fully defined, where content rules become complex, and where
accessibility requirements span multiple sub-components.

**No raw HTML elements for content** — every content-rendering slot in the Composition table
must reference a named DS molecule, atom, or foundation component, not a raw HTML element
(e.g. not `<span>`, `<img>`, `<p>`). Layout wrappers (`<div>`, `<section>`, `<ul>`, `<nav>`,
etc.) used purely to structure layout regions are the only exception.

The boundary with product-specific organisms (specced by `designer-organism`) is intent:
- **DS organism**: generic structure, could be dropped into a different product unchanged.
- **Product organism**: tightly coupled to this product's IA, data model, or feature context.

If a candidate organism references product-specific data labels, routes, or business logic in
its structure, it belongs in `designer-organism`, not here.

## Where things live

- **Read** `ds-audit.md` for the organism's scope, dependencies, and notes.
- **Read** foundation component specs at `<real_project_path>/design-system/foundation-components/`
  for any foundation components (Text, Icon) this organism uses directly.
- **Read** molecule specs at `<real_project_path>/design-system/molecules/` and atom specs at
  `<real_project_path>/design-system/atoms/` for the sub-components this organism uses.
- **Read** foundation files at `<real_project_path>/design-system/foundations/` for any
  organism-level layout tokens.
- **Write** `<real_project_path>/design-system/organisms/<component-name>/component-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- `ds-audit.md` — confirms this organism is in scope and lists its dependencies.
- Foundation component, molecule, and atom specs for all sub-components (must be written before
  this organism).
- Foundation files — for organism-level layout and spacing tokens.

### Input Acceptance Criteria
- `ds-audit.md` lists this organism as in scope.
- All foundation component, molecule, and atom dependencies are already specced. If any are
  missing, hand off to the appropriate skill first.
- The organism is confirmed as generic and reusable, not product-specific. If it references
  product-specific data or IA, redirect to `designer-organism`.

### Outputs
- `<real_project_path>/design-system/organisms/<component-name>/component-spec.md`

### Output Quality Criteria

**Frontmatter:**
- `dependencies` uses separate `foundation-components`, `molecules`, and `atoms` keys. List every
  named dependency; use `N/A` for keys with no direct dependency.

**Anatomy:**
- Composition table lists every foundation component, molecule, and atom with its type and
  purpose.
- Any direct Text or Icon foundation component reference in the Composition table names the
  specific style variant used (e.g. `Text / heading-2`, `Text / body-medium`). A generic
  "Text" entry with no variant is incomplete.
- Layout names each region by function and includes an ASCII or prose diagram showing the
  region structure. Layout system (CSS Grid / Flexbox / combination) is specified.
- Spacing table lists the gap token between each pair of adjacent regions or sub-components.

**Appearance:**
- Every organism-level style the component can exhibit is documented — no property may be omitted or left to inference. Full coverage ensures consistent, unambiguous implementation.
- Variants table includes a "Components affected" column.
- State is split into lifecycle states (data/system status: loading, empty, error, success)
  and interactive states (in-progress user actions). Both include "Components affected" and
  "Visual treatment" columns.
- Tokens section lists only organism-level tokens.

**Responsive:**
- Breakpoints table covers all four breakpoints (Mobile, Tablet, Desktop, Wide).
- Reflow strategy describes what stacks, collapses, or hides and why.
- Mobile-specific patterns section is present (or explicitly skipped with reason).

**Content:**
- Copy table includes the i18n namespace if applicable.
- Empty state table defines headline/body/CTA for each condition. Skip only if truly not
  applicable, with a reason.
- Error state table defines headline/body/CTA for each error type. Skip only if truly not
  applicable, with a reason.
- Notifications table covers async action outcomes. Skip only if not applicable.
- Text expansion covers non-translatable strings and pluralization.

**Examples:**
- Happy path uses real product data — no placeholder text.
- Edge cases cover all five listed scenarios (long names, special chars, empty optional fields,
  number scale, multi-script content).
- Worst-case content is defined.

**Accessibility:**
- Landmark structure specifies outer element, aria-label/labelledby, and nested landmarks.
- Heading hierarchy table is present (no h1; levels, text, and purpose defined).
- ARIA table covers organism-level attributes only — columns: attribute / on element /
  value or points to / purpose.
- Keyboard table lists organism-level keys; tab order visual-reading-order confirmation present.
- Focus management covers all six significant moments (mount, first data load, user refresh,
  successful action, error, loading→empty transition).
- Live regions table is present for any dynamic content updates. Assertive used only for
  time-critical alerts.
- Screen reader table covers organism-level state changes.
- Skip links section is present (yes/no with link text and target ID if yes).
- Internationalization specifies RTL mirroring and `dir` strategy.

**Checklist:**
- Spec section is present and all six items (Anatomy, Appearance, Responsive, Content, Examples, Accessibility) are checked or explicitly waived with justification.
- All three sections (Design, Engineering, QA) are present with organism-specific items filled
  in. No `{component-specific item}` placeholder left unfilled.

---

## The 3-gate flow

### Gate 1 — Input
Verify all foundation component, molecule, and atom dependencies are specced. Confirm the
organism is generic (DS candidate), not product-specific. If it references product-specific IA,
redirect to `designer-organism`.

### Gate 2 — Process
Work through each section of the spec with the designer.

**Anatomy** — probe:
- Which foundation components, molecules, and atoms compose this organism? What is each one's
  purpose?
- What are the named regions? (header, body, footer, sidebar, overlay, toolbar…)
- What is the layout system? (CSS Grid for two-dimensional; Flexbox for one-dimensional)
- Can you sketch the region structure as ASCII or prose?
- What gap tokens apply between regions or adjacent sub-components?

**Appearance** — probe:
- Any organism-level variants? Which components or regions are affected and how?
- Which lifecycle states apply? (loading, empty, error, success — which are relevant?)
  For each, which components are affected and what is the visual treatment?
- Which interactive states apply at the organism level? (e.g. drag-in-progress, selected)
- Which layout or surface tokens does this organism introduce?

**Responsive** — probe:
- What changes at each breakpoint? (Mobile <640, Tablet 640–1024, Desktop >1024, Wide >1440)
- What stacks, collapses, or hides at smaller sizes and why?
- Any mobile-specific patterns? (bottom sheet, swipe gesture, pull-to-refresh)

**Content** — probe:
- Does this organism own strings? What i18n namespace? List every key with default text and
  whether it is translatable.
- What conditions produce an empty state? For each: headline, body copy, CTA label.
- What error types can occur? For each: headline, body copy, CTA label.
- Are there async action notifications? (save success, delete confirmed, load failed) For each:
  message text and type (success / error / info).
- Max text expansion budget? What strings must never be translated? Any pluralization needs?

**Examples** — probe:
- Provide a realistic happy-path example with real product domain values.
- Work through all five edge cases with realistic values (long names, special chars, empty
  optional fields, numbers at scale 0/1/1K/1M, multi-script content).
- What is the worst-case realistic content this organism could receive?

**Accessibility** — probe:
- What HTML5 sectioning element or landmark role does this organism use? If multiple of the
  same type exist on a page, what is the unique aria-label?
- What heading levels are used inside? What text do they carry? (No h1 — that is the page's.)
- What organism-level ARIA attributes span multiple components? (aria-busy during loading,
  aria-live for async updates, aria-label on the landmark)
- What keys does the organism respond to at its level? Does tab order match visual reading order?
  Any organism-level keyboard shortcuts?
- Define focus for each significant moment: mount, first data load, user-triggered refresh,
  successful action, error appearance, loading→empty transition.
- Are there dynamic content regions that update without a page reload? For each: aria-live
  value (polite vs assertive), what changes, aria-atomic.
- Every organism-level state change a screen reader must be aware of: text announced and method.
- Does this organism need a skip link? If yes: link text and target ID.
- RTL: which elements mirror, which do not? `dir` strategy?

**Checklist** — verify each spec section in the Spec checklist (Anatomy, Appearance, Responsive,
Content, Examples, Accessibility), then fill in component-specific items for Design, Engineering,
and QA. Do not leave `{component-specific item}` as a placeholder.

Write the spec using the project organism template:

```markdown
---
name: {organism-name}
version: 0.0.1
description: {one sentence — what this organism does and why it belongs in the DS}
link:
  - {tool-name}: {tool-link}
dependencies:
  - foundation-components: N/A  # list Text and/or Icon if used directly
  - molecules: {molecule-a}, {molecule-b}
  - atoms: {atom-a}
---
# {Organism Name}

## Anatomy

Define which foundation components, molecules, and atoms compose this organism, how regions are
structured, and the spacing between them. Visual tokens are inherited from constituent
components — specify only organism-level rules here.

### Composition
List every foundation component, molecule, and atom used. For each, describe its purpose within
the organism.

| Component | Type | Purpose |
|-----------|------|---------|
| `{name}` | Foundation component / Molecule / Atom | {purpose} |

### Layout
Describe the region structure and layout strategy. Name each region by its function.

- Layout system: CSS Grid / Flexbox / combination
- Regions and their roles:

```
{ASCII or prose layout diagram showing regions}
```

### Spacing
List the gap between each pair of adjacent regions or sub-components.

| Gap | Token |
|-----|-------|
| {region-a} → {region-b} | {token} |

---

## Appearance

Specify only organism-level variants, states, and token overrides. Component-level styles are
owned by their respective specs. This section must be exhaustive for all organism-level styles:
every variant, state, and token the organism introduces must be documented. Leave nothing to
inference — gaps create inconsistent, ambiguous implementations.

### Variants
List each organism-level variant. Describe its use case and which components or regions are
affected.

1. {variant name} (default: {default})

   | {variant name}  | Components affected | {style change} |
   |-----------------|---------------------|----------------|
   | {variant value} | {components}        | {value}        |

### State

Organisms have two categories of state.

**Lifecycle states** reflect the data and system status of the organism. **Interactive states**
reflect an in-progress user action.

1. Lifecycle states — data and system status

   | State | Components affected | Visual treatment |
   |-------|---------------------|-----------------|
   | {state} | {components} | {value} |

2. Interactive states — in-progress user actions

   | State | Components affected | Visual treatment |
   |-------|---------------------|-----------------|
   | {state} | {components} | {value} |

### Tokens
List only tokens this organism introduces. Tokens already defined in constituent components do
not need repeating.

| Name    | Component or Semantic Token |
|---------|-----------------------------|
| {token} | {value}                     |

---

## Responsive

Organisms are the primary level where layout reflow decisions are made.

### Breakpoints

| Breakpoint | Layout change |
|------------|--------------|
| Mobile < 640px | |
| Tablet 640–1024px | |
| Desktop > 1024px | |
| Wide > 1440px | |

### Reflow strategy
Describe what stacks, collapses, or hides at smaller breakpoints and why.

### Mobile-specific patterns
(Skip if not applicable.) Note any mobile-only patterns such as bottom sheets, swipe gestures,
or pull-to-refresh.

---

## Content

### Copy
List every string this organism owns. If strings are managed via an i18n library, declare the
namespace and list the keys.

- i18n namespace (if applicable): `{namespace}`

| Key | Default text | Context | Translatable? |
|-----|-------------|---------|---------------|
| `{key}` | {text} | {where it appears} | Yes / No |

### Empty state
(Skip if not applicable.) Define copy for each condition that produces an empty state.

| Condition | Headline | Body | CTA label |
|-----------|----------|------|-----------|
| {condition} | {text} | {text} | {text} |

### Error state
(Skip if not applicable.) Define copy for each error type.

| Error type | Headline | Body | CTA label |
|------------|----------|------|-----------|
| {error} | {text} | {text} | {text} |

### Notifications
(Skip if not applicable.) Define messages for async action outcomes.

| Trigger | Message | Type |
|---------|---------|------|
| {trigger} | {text} | success / error / info |

### Text expansion
- Max text expansion (e.g. +40% for German): {value}
- Layout behavior when a string overflows its container: truncate / wrap / push container
- Strings that must NOT be translated (e.g. brand names, codes): {list}
- Pluralization: list any strings requiring plural forms
- RTL: see Accessibility > Internationalization

---

## Examples

Use real product data — not placeholder text. These examples validate that the spec holds
under realistic conditions.

### Happy path
Populate every field with realistic values from the actual product domain.

### Edge cases
- Very long names or titles:
- Names with special characters or emoji:
- Empty optional fields:
- Numbers at various scales (0, 1, 1K, 1M):
- Multi-script content (e.g. English + Arabic):

### Worst-case content
The most stressful realistic content this organism could receive.

---

## Accessibility

Specify organism-level accessibility requirements. Component-level requirements are owned by
their respective specs. Mark any section N/A with justification if it does not apply.

### Landmark structure
Organisms must use the correct HTML5 sectioning element or ARIA landmark. When multiple
landmarks of the same type exist on a page, each must have a unique label.

- Outer element: `<section>` / `<article>` / `<aside>` / `<div role="region">` / other
- `aria-label` or `aria-labelledby` on landmark: {value}
- Nested landmarks (list each with its label):

### Heading hierarchy
The organism must not contain an `<h1>` — that belongs to the page. Define which heading
levels are used and what text they carry.

| Level | Text | Purpose |
|-------|------|---------|
| `{h2}` | {text} | {purpose} |

### ARIA
Document organism-level ARIA requirements — attributes and relationships that span multiple
components. List only attributes this organism introduces.

| Attribute | On element | Value / points to | Purpose |
|-----------|-----------|-------------------|---------|
| `{attr}` | `{element}` | `{value}` | {purpose} |

### Keyboard
List every key the organism responds to at the organism level. Component-level keys are owned
by their respective specs.

| Key | Action |
|-----|--------|
| `{key}` | {action} |

- Tab order matches visual reading order: Yes / must verify
- Organism-level keyboard shortcuts (if any):

### Focus management
Define where focus goes at each significant moment.

- On mount: {where focus goes}
- After first data load: {where focus goes}
- After user-triggered refresh: focus stays / goes to {element}
- After successful action: {where focus goes}
- After error appears: {where focus goes}
- On state transition loading → empty: {where focus goes}

### Live regions
(Skip if not applicable.) Define `aria-live` regions for dynamic content that updates without
a page reload.

| Region | `aria-live` | Content | `aria-atomic` |
|--------|-------------|---------|---------------|
| {region} | `polite` / `assertive` | {what changes} | Yes / No |

Use `assertive` only for time-critical alerts (session expiry, destructive confirmations).
Prefer `polite` for everything else.

### Screen reader
Document organism-level state changes a screen reader user needs to be aware of.

| State change | Text announced | Method |
|--------------|---------------|--------|
| {state} | {text} | {method} |

### Skip links
- Skip link to this organism needed: Yes / No
- If Yes, link text: {e.g. "Skip to {organism name}"}
- Skip link target ID: `{id}`

### Internationalization
- RTL layout mirrors: Yes / No — list elements that do not mirror
- `dir` attribute: inherits / always LTR / always RTL

---

## Checklist

All items must pass or be explicitly waived with justification before status moves to
**Approved**.

### Spec
- [ ] Anatomy: composition, layout, and spacing documented
- [ ] Appearance: variants, lifecycle/interactive states, and tokens complete; "components affected" columns filled
- [ ] Responsive: all four breakpoints defined; reflow strategy described
- [ ] Content: all sections present or explicitly marked N/A with justification
- [ ] Examples: happy path uses real data; all five edge cases covered; worst-case defined
- [ ] Accessibility: landmark, heading hierarchy, ARIA, keyboard, focus management, live regions, screen reader, skip links, and i18n documented

### Design
- [ ] All variants and lifecycle states are designed, or marked N/A with justification
- [ ] All values applied via design tokens — no hardcoded hex, px, or font values
- [ ] Real content examples used in designs — no placeholder text
- [ ] Dark mode verified for all variants and states
- [ ] Responsive layout reviewed at all breakpoints
- [ ] RTL layout reviewed (if shipped in any RTL locale)
- [ ] {component-specific item}

### Engineering
- [ ] Rendered output matches spec in all lifecycle states
- [ ] All props documented with types and defaults
- [ ] Error handling covers all error types defined in spec
- [ ] Optimistic UI behaves correctly on success and rollback
- [ ] Focus management implemented for all async state transitions
- [ ] Live regions announce all state changes per spec
- [ ] No axe-core violations in any state
- [ ] {component-specific item}

### QA
- [ ] Cross-browser smoke test passed
- [ ] Mobile device testing on iOS Safari and Chrome Android
- [ ] Screen reader tested: NVDA + Firefox, VoiceOver + Safari
- [ ] Performance benchmark within budget
- [ ] Visual regression baseline captured for all lifecycle states
- [ ] {component-specific item}
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that Examples use real product data,
all six focus management moments are defined, live regions use polite vs assertive correctly,
and the Checklist has component-specific items filled in. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick the organism in Step 3c in `## Plan`, update **Next
   step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
Completed DS organism specs feed `designer-ds-validate` (for add/update sub-modes) and
`designer-ds-document` (README index). In product design, product pages and product-specific
organisms reference DS organisms by name.
