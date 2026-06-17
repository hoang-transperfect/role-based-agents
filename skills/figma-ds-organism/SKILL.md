---
name: figma-ds-organism
description: >
  Figma adapter for building one design system organism. Reads the organism
  component-spec.md directly and creates or updates a Component in Figma by
  placing molecule and atom Component Instances, applying auto-layout with
  spacing Variable references, creating a separate responsive frame for each
  defined breakpoint demonstrating the correct reflow strategy, setting up
  lifecycle states (loading, empty, error) and interactive states with
  sub-component state propagation arranged as a grid table, applying
  organism-scope Variable references, and adding comprehensive accessibility
  annotations (landmark role, heading hierarchy, ARIA attributes, focus
  management, live regions, skip links). Invoked by designer-ds-organism-build
  when design-tool is figma.
---

# figma-ds-organism

This skill builds one DS organism Component in Figma by reading the organism
`component-spec.md` directly. Organisms are the most complex component level:
they add responsive reflow frames, lifecycle states, and a full accessibility
structure. All sub-components are molecule or atom Component Instances — never
raw shapes.

## Inputs

- **Spec file path** — `<real_project_path>/design-system/organisms/<component-name>/component-spec.md`
- **Design file link** — from `designer-artifacts/resource.md`
- **Dependency component URLs** — Figma component URLs for each molecule and atom
  in `dependencies.molecules` and `dependencies.atoms` (from the `link:` fields
  of their own `component-spec.md` files). Missing URLs result in placeholders,
  not a stop.

## Outputs
- Organism Component in the target Figma file.
- Responsive frames — one per breakpoint defined in the spec.
- Component URL.

---

## The 3-gate flow

### Gate 1 — Input
- Read `component-spec.md` at the given spec file path. Confirm it exists.
- Confirm the design file link is present in `resource.md`.
- Confirm the Spec checklist in `component-spec.md` is fully checked (Anatomy,
  Appearance, Responsive, Content, Examples, Accessibility). If any item is
  unchecked and not waived, stop: "Spec checklist incomplete — resolve before building."
- For each dependency in `dependencies.molecules` and `dependencies.atoms`,
  check whether its `link:` field has a component URL. Missing URLs are handled
  by placeholders in Step 3 — do not stop.
- Confirm Responsive > Breakpoints is present (at least one breakpoint must be defined).

### Gate 2 — Process

**Naming convention**
All Figma names — pages, components, and layers — use **PascalCase with spaces**: every word
starts with an uppercase letter and words are separated by a single space. No hyphens,
underscores, slashes, or camelCase.

| Type | Example spec name | Figma name |
|------|------------------|------------|
| Page | `navigation-bar` | `Navigation Bar` |
| Component | `data-table` | `Data Table` |
| Layer / slot | `header-region` | `Header Region` |
| Layer / slot | `bodyContent` | `Body Content` |
| Responsive frame | `data-table/mobile` | `Data Table / Mobile` |

Apply this conversion whenever a name comes from the spec. Token names in Variable
references are the only exception — they must match the published Variable name exactly.

**Step 1 — Create or navigate to the component page**
Convert the component name to PascalCase with spaces — this is the page name
(e.g. `navigation-bar` → `Navigation Bar`, `DataTable` → `Data Table`). Check whether the
page exists:
- If it does not exist, create it with that name, then navigate to it.
- If it exists, navigate to it.
All subsequent steps — including the Component frame and all responsive frames — are placed on
this page only.

**Step 2 — Create the Component frame and write the spec**
Create or locate the organism Component on the current page. Name it using PascalCase with
spaces (e.g. `Navigation Bar`, `Data Table`).

Write the full content of `component-spec.md` into the Component's **description** field
in Figma. This makes the spec readable directly from Figma without leaving the file.

**Step 3 — Place sub-component instances**
From Anatomy > Composition, for each slot in the listed order:
- Convert the slot name to PascalCase with spaces before using it as the instance layer name
  (e.g. `header-region` → `Header Region`).
- If the molecule or atom component URL is present, place a Component Instance at that URL.
- If the component URL is missing, create a **placeholder component** on the current page:
  - Name it using PascalCase with spaces (e.g. `Navigation Item`, `Data Row`).
  - Fill it with a solid `#FF00FF` (magenta) rectangle and add a text layer reading
    `Placeholder — replace with {component name}`.
  - Place an instance of this placeholder in the slot.
  - Annotate the instance with a note: "⚠ Dependency not yet built."
- Never create raw shapes or groups in place of component instances.

**Step 4 — Apply auto-layout and spacing**
From Anatomy > Layout and Anatomy > Spacing:
- Set auto-layout direction, alignment, and gap using Variable references.
- Set padding on each side using spacing Variable references.

**Step 5 — Create Variant properties, states, and arrange as a table**
From Appearance > Variants:
- Add organism-level Variant properties and create variant frames.
- Apply style rules using Variable references only.

From Appearance > State (lifecycle and interactive):
- **Lifecycle states** (loading, empty, error) — create variant frames or, where the state
  differs structurally from the default, separate frames. Apply the visual treatment:
  - Replace or hide sub-component instances as described (e.g. skeleton loaders in loading
    state, illustration + CTA in empty state, error message organism in error state).
  - For each sub-component listed in the propagation column: switch its instance to the
    specified state.
- **Interactive states** — represent as Variant property values or Figma interactive
  component states using "Change to" interactions.

After all variant frames are created, arrange the component set as a grid table — no overlapping
or stacking:
- **Columns** = values of the first variant property.
- **Rows** = values of the second variant property (e.g. lifecycle state: default, loading,
  empty, error).
- If there are more than two variant properties, nest additional properties within each column
  group as sub-columns.
- Use a consistent gap of 40px between cells in both directions.
- Responsive frames (from Step 7) are placed below the component set, not inside it.

**Step 6 — Apply organism-scope Variable references**
From Appearance > Tokens:
- Apply each token as a Variable reference on the named layer. No hardcoded values.

**Step 7 — Create responsive frames**
From Responsive > Breakpoints, for each breakpoint:
- Create a separate artboard frame (not a variant) named `{Component Name} / {Breakpoint Name}`
  in PascalCase with spaces (e.g. `Data Table / Mobile`, `Data Table / Tablet`).
- Start from the default Component composition, then apply the reflow changes described in
  Responsive > Reflow strategy:
  - Layout direction changes (horizontal → vertical).
  - Slots that are hidden or reordered at this breakpoint.
  - Overflow behaviour (scroll, truncation, collapse).
- Apply any mobile-specific patterns from Responsive > Mobile-specific patterns (bottom sheet,
  collapsed navigation, etc.).

**Step 8 — Add accessibility annotations**
From Accessibility, annotate on the default Component frame:
- **Landmark** — annotate the ARIA landmark role on the outermost frame.
- **Heading hierarchy** — annotate the heading level on each text layer that carries a heading
  role (e.g. `h2`, `h3`). Levels must be consecutive — no skipped levels.
- **ARIA attributes** — annotate each aria-* attribute and the condition under which it applies.
- **Focus management** — annotate whether focus is trapped inside this organism (modal, dialog)
  and where focus returns after the organism is dismissed or closed.
- **Live regions** — annotate which state transitions trigger a live region announcement,
  the aria-live value (polite / assertive), and the content of the announcement.
- **Skip links** — if the spec defines skip links, annotate the target element IDs.

### Gate 3 — Output

**Instances check** — every slot in the Composition table has a molecule or atom Component
Instance. Layer names match slot names (PascalCase with spaces).

**Layout check** — auto-layout direction, alignment, gap, and padding match the spec using
Variable references.

**Variants check** — every organism-level variant combination has a matching frame with style
applied as Variable references.

**State check** — every lifecycle state and interactive state has a representation. Sub-component
state propagation matches the spec description for each state.

**Tokens check** — every organism-scope token is applied as a Variable reference on the correct
layer. No hardcoded values.

**Responsive check** — a frame named `{Component Name} / {Breakpoint Name}` exists for every
breakpoint in the spec, demonstrating the reflow strategy written for that breakpoint.

**Accessibility check** — landmark, heading hierarchy, ARIA attributes, focus management, live
regions, and skip links (if applicable) are all annotated on the Component frame.

Any gap must be corrected before returning. When all rows and breakpoints are accounted for,
return the component URL.
