---
name: figma-ds-molecule
description: >
  Figma adapter for designer-ds-molecule-build. Receives the molecule build brief and creates or
  updates a Component in Figma by placing atom Component Instances (never raw shapes), applying
  auto-layout with spacing Variable references (direction, alignment, gap, padding), setting up
  molecule-level Variant properties and state propagation to the correct atom instances within
  each variant frame, applying molecule-scope Variable references, and annotating ARIA
  relationships and keyboard tab order. Invoked by designer-ds-molecule-build when design-tool
  is figma.
---

# figma-ds-molecule

This skill builds one molecule Component in Figma from the molecule build brief. Sub-components
are always Component Instances of already-built atoms — never raw shapes or groups that duplicate
an atom's appearance. It does not read `component-spec.md` directly.

## Naming convention

All Figma artifact names — pages, component names, and frame names — use **lowercase kebab-case**.
Convert the component name from the brief before using it anywhere in Figma:
`FormField` → `form-field`, `SearchBar` → `search-bar`.

Exception: internal layer names inside a Component must match the Anatomy > Structure part names
from the spec exactly, regardless of casing.

## Inputs

The build brief from `designer-ds-molecule-build`, containing:
- **Component name** and **design file link**.
- **Composition table** — slot name → atom component name → atom component URL.
- **Anatomy > Layout** — direction (horizontal / vertical), alignment, gap token, wrap behaviour.
- **Anatomy > Spacing** — internal padding tokens (top, right, bottom, left).
- **Appearance > Variants** — molecule-level Variant property names, values, and style rules.
- **Appearance > State** — molecule states with the atoms-affected column: which atom instances
  change state and to what value for each molecule state.
- **Appearance > Tokens** — molecule-scope token-to-layer mapping (spacing, radius).
- **Accessibility > ARIA relationships** — which atom instances carry aria-labelledby /
  aria-describedby pointing to other instances, and the conditions under which each applies.
- **Accessibility > Keyboard flow** — tab order across atom instances within the molecule.

## Outputs
- Molecule Component in the target Figma file.
- Component URL.

---

## The 3-gate flow

### Gate 1 — Input
Verify:
- Component name and design file link are present.
- Every atom component URL in the Composition table is valid. If any slot is missing a URL,
  a placeholder component will be created in Step 3 — do not stop.
- Layout and Spacing sections are present in the brief.

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

Apply this conversion whenever a name comes from the spec or brief. Token names in Variable
references are the only exception — they must match the published Variable name exactly.

**Step 1 — Create or navigate to the component page**
Convert the component name to PascalCase with spaces (per the naming convention above) — this
is the page name (e.g. `form-field` → `Form Field`, `search-bar` → `Search Bar`). Check
whether the page exists:
- If it does not exist, create it with that name, then navigate to it.
- If it exists, navigate to it.
All subsequent steps place content on this page only.

**Step 2 — Create the Component frame and write the spec**
Create or locate the molecule Component on the current page. Name it using PascalCase with
spaces (e.g. `Form Field`, `Search Bar`).

Write the full component spec from the build brief into the Component's **description** field
in Figma. Include all sections: Anatomy, Appearance (Variants, State, Tokens), Content, and
Accessibility. This makes the spec readable directly from Figma without leaving the file.

**Step 3 — Place atom instances**
From the Composition table, for each slot in the listed order:
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
  named in the brief.

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
  property to the value named in the brief.
- Every atom-state pairing in the brief must be reflected in the corresponding variant frame.

**Step 7 — Apply molecule-scope Variable references**
From Appearance > Tokens:
- Apply each token as a Variable reference on the named layer (spacing gaps, border radius
  at molecule scope, etc.).
- No hardcoded values where the brief names a token.

**Step 8 — Add ARIA and keyboard annotations**
From Accessibility > ARIA relationships:
- Annotate each atom instance that carries an aria-labelledby or aria-describedby reference,
  naming the target instance it points to and the condition under which the relationship applies.

From Accessibility > Keyboard flow:
- Annotate the tab order across atom instances, numbered in the sequence specified in the brief.

### Gate 3 — Output

**Instances check** — every slot in the Composition table has a Component Instance of the
correct atom (not a raw shape). Instance layer names match slot names exactly.

**Layout check** — auto-layout direction, alignment, gap, and padding match the brief using
Variable references (no hardcoded px values).

**Variants check** — every molecule-level variant combination has a matching variant frame with
style rules applied as Variable references.

**State check** — every molecule state has a representation; atoms-affected column is honoured
in each state frame (correct atom instances are in the correct state).

**Tokens check** — every molecule-scope token is applied as a Variable reference on the correct
layer.

**Accessibility check** — ARIA relationship annotations and keyboard tab order are present.

Any gap must be corrected before returning. When all rows are accounted for, return the
component URL to `designer-ds-molecule-build`.
