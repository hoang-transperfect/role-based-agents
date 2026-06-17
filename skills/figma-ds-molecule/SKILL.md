---
name: figma-ds-molecule
description: >
  Figma adapter for building one design system molecule. Reads the molecule
  component-spec.md directly and creates or updates a Component in Figma by
  placing atom Component Instances (never raw shapes), applying auto-layout
  with spacing Variable references (direction, alignment, gap, padding), setting
  up molecule-level Variant properties and state propagation to the correct atom
  instances within each variant frame arranged as a grid table, applying
  molecule-scope Variable references, and annotating ARIA relationships and
  keyboard tab order. Invoked by designer-ds-molecule-build when design-tool
  is figma.
---

# figma-ds-molecule

This skill builds one molecule Component in Figma by reading the molecule
`component-spec.md` directly. Sub-components are always Component Instances of
already-built atoms — never raw shapes or groups that duplicate an atom's appearance.

## Inputs

- **Spec file path** — `<real_project_path>/design-system/molecules/<component-name>/component-spec.md`
- **Design file link** — from `designer-artifacts/resource.md`
- **Dependency component URLs** — Figma component URLs for each atom in
  `dependencies.atoms` (from the `link:` fields of their own `component-spec.md`
  files). Missing URLs result in placeholders, not a stop.

## Outputs
- Molecule Component in the target Figma file.
- Component URL.

---

## The 3-gate flow

### Gate 1 — Input
- Read `component-spec.md` at the given spec file path. Confirm it exists.
- Confirm the design file link is present in `resource.md`.
- Confirm the Spec checklist in `component-spec.md` is fully checked (Anatomy,
  Appearance, Content, Accessibility). If any item is unchecked and not waived,
  stop: "Spec checklist incomplete — resolve before building."
- For each dependency in `dependencies.atoms` (and `dependencies.molecules`),
  check whether its `link:` field has a component URL. Missing URLs are handled
  by placeholders in Step 3 — do not stop.
- Confirm Layout and Spacing sections are present in the spec.

### Gate 2 — Process

**Naming convention**
All Figma names — pages, components, and layers — use **PascalCase with spaces**: every word
starts with an uppercase letter and words are separated by a single space. No hyphens,
underscores, slashes, or camelCase.

| Type | Example spec name | Figma name |
|------|------------------|------------|
| Page | `form-field` | `Form Field` |
| Component | `search-bar` | `Search Bar` |
| Layer / slot | `input-slot` | `Input Slot` |
| Layer / slot | `helperText` | `Helper Text` |

Apply this conversion whenever a name comes from the spec. Token names in Variable
references are the only exception — they must match the published Variable name exactly.

**Step 1 — Create or navigate to the component page**
Convert the component name to PascalCase with spaces — this is the page name
(e.g. `form-field` → `Form Field`, `search-bar` → `Search Bar`). Check whether the page exists:
- If it does not exist, create it with that name, then navigate to it.
- If it exists, navigate to it.
All subsequent steps place content on this page only.

**Step 2 — Create the Component frame and write the spec**
Create or locate the molecule Component on the current page. Name it using PascalCase with
spaces (e.g. `Form Field`, `Search Bar`).

Write the full content of `component-spec.md` into the Component's **description** field
in Figma. This makes the spec readable directly from Figma without leaving the file.

**Step 3 — Place atom instances**
From Anatomy > Composition, for each slot in the listed order:
- Convert the slot name to PascalCase with spaces before using it as the instance layer name
  (e.g. `input-slot` → `Input Slot`).
- If the atom component URL is present, place a Component Instance at that URL.
- If the atom component URL is missing, create a **placeholder component** on the current page:
  - Name it using PascalCase with spaces (e.g. `Button`, `Input`).
  - Fill it with a solid `#FF00FF` (magenta) rectangle and add a text layer reading
    `Placeholder — replace with {component name}`.
  - Place an instance of this placeholder in the slot.
  - Annotate the instance with a note: "⚠ Dependency not yet built."
- Never create a raw shape, group, or local frame in place of a component instance.

**Step 4 — Apply auto-layout**
From Anatomy > Layout:
- Set auto-layout direction (horizontal / vertical).
- Set alignment (start / center / end / space-between) as specified.
- Set gap using the spacing Variable reference for the gap token. Do not hardcode a px value.
- Set wrap behaviour (no wrap / wrap) if specified.

From Anatomy > Spacing:
- Set padding on each side (top, right, bottom, left) using the spacing Variable references
  named in the spec.

**Step 5 — Create molecule-level Variant properties and arrange as a table**
From Appearance > Variants:
- Add Variant properties at the molecule Component level.
- For each variant combination, create or select the variant frame.
- Apply style rules using Variable references only — no hardcoded values.

After all variant frames are created, arrange the component set as a grid table — no overlapping
or stacking:
- **Columns** = values of the first variant property.
- **Rows** = values of the second variant property.
- If there are more than two variant properties, nest additional properties within each column
  group as sub-columns.
- Use a consistent gap of 40px between cells in both directions.
- Every cell position in the grid must correspond to exactly one variant combination — no cell
  is left empty or duplicated.

**Step 6 — Set up state propagation**
From Appearance > State, for each molecule state:
- Determine the representation: Variant property value or Figma interactive state.
- Within each state's variant frame, for every atom listed in the atoms-affected column:
  switch that atom's Component Instance to the specified state by updating its Variant
  property to the value named in the spec.
- Every atom-state pairing in the spec must be reflected in the corresponding variant frame.

**Step 7 — Apply molecule-scope Variable references**
From Appearance > Tokens:
- Apply each token as a Variable reference on the named layer (spacing gaps, border radius
  at molecule scope, etc.).
- No hardcoded values where the spec names a token.

**Step 8 — Add ARIA and keyboard annotations**
From Accessibility > ARIA:
- Annotate each atom instance that carries an aria-labelledby or aria-describedby reference,
  naming the target instance it points to and the condition under which the relationship applies.

From Accessibility > Keyboard flow:
- Annotate the tab order across atom instances, numbered in the sequence specified in the spec.

### Gate 3 — Output

**Instances check** — every slot in the Composition table has a Component Instance of the
correct atom (not a raw shape). Instance layer names match slot names (PascalCase with spaces).

**Layout check** — auto-layout direction, alignment, gap, and padding match the spec using
Variable references (no hardcoded px values).

**Variants check** — every molecule-level variant combination has a matching variant frame with
style rules applied as Variable references.

**State check** — every molecule state has a representation; atoms-affected column is honoured
in each state frame (correct atom instances are in the correct state).

**Tokens check** — every molecule-scope token is applied as a Variable reference on the correct
layer.

**Accessibility check** — ARIA relationship annotations and keyboard tab order are present.

Any gap must be corrected before returning. When all rows are accounted for, return the
component URL.
