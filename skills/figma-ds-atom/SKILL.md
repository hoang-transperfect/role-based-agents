---
name: figma-ds-atom
description: >
  Figma adapter for building one design system atom. Reads the atom
  component-spec.md directly and creates or updates a Component in Figma:
  builds the layer hierarchy from Anatomy > Structure, creates Variant
  properties from Appearance > Props, creates variant frames from Appearance >
  Variants arranged as a grid table, applies Variable references from
  Appearance > Tokens (no hardcoded values), represents all states from
  Appearance > State, and adds accessibility annotations (ARIA role, aria-*
  attributes, keyboard interactions, 44×44px touch target). Where Anatomy
  references Icon or Text dependencies, places Component Instances or
  placeholders. Invoked by designer-ds-atom-build when design-tool is figma.
---

# figma-ds-atom

This skill builds one atom Component in Figma by reading the atom
`component-spec.md` directly. It maps every section of the spec to
Figma-specific operations.

## Inputs

- **Spec file path** — `<real_project_path>/design-system/atoms/<component-name>/component-spec.md`
- **Design file link** — from `designer-artifacts/resource.md`
- **Dependency component URLs** — Figma component URLs for Icon, Text, and any
  other atoms this atom embeds as instances (from the `link:` fields of their
  own `component-spec.md` files). Missing URLs result in placeholders, not a stop.

## Outputs
- Component in the target Figma file.
- Component URL.

---

## The 3-gate flow

### Gate 1 — Input
- Read `component-spec.md` at the given spec file path. Confirm it exists.
- Confirm the design file link is present in `resource.md`.
- Confirm the Spec checklist in `component-spec.md` is fully checked (Anatomy,
  Appearance, Content, Accessibility). If any item is unchecked and not waived,
  stop: "Spec checklist incomplete — resolve before building."
- For each dependency in `dependencies`, check whether its `link:` field has a
  component URL. Missing URLs are handled by placeholders in Step 3 — do not stop.

### Gate 2 — Process

**Naming convention**
All Figma names — pages, components, and layers — use **PascalCase with spaces**: every word
starts with an uppercase letter and words are separated by a single space. No hyphens,
underscores, slashes, or camelCase.

| Type | Example spec name | Figma name |
|------|------------------|------------|
| Page | `button` | `Button` |
| Component | `icon-button` | `Icon Button` |
| Layer / part | `icon-slot` | `Icon Slot` |
| Layer / part | `labelText` | `Label Text` |

Apply this conversion whenever a name comes from the spec. Token names in Variable
references are the only exception — they must match the published Variable name exactly.

**Step 1 — Create or navigate to the component page**
Convert the component name to PascalCase with spaces — this is the page name
(e.g. `button` → `Button`, `icon-button` → `Icon Button`). Check whether the
page already exists:
- If it does not exist, create it with that name, then navigate to it.
- If it exists, navigate to it.
All subsequent steps place content on this page only.

**Step 2 — Create the Component frame and write the spec**
Create a new Component (or locate the existing one to update by name) on the current page.
Name it using PascalCase with spaces (e.g. `Button`, `Icon Button`).

Write the full content of `component-spec.md` into the Component's **description** field
in Figma. This makes the spec readable directly from Figma without leaving the file.

**Step 3 — Build the layer hierarchy**
From Anatomy > Structure, build the layer tree inside the Component:
- Convert each part name to PascalCase with spaces before using it as the layer name
  (e.g. `icon-slot` → `Icon Slot`, `labelText` → `Label Text`).
- Where Anatomy > Details specifies a child component reference (e.g. an Icon instance or a
  Text instance): place a Component Instance using the dependency URL.
- If a dependency URL is missing, create a **placeholder component** on the current page:
  - Name it using PascalCase with spaces (e.g. `Icon`, `Text`).
  - Fill it with a solid `#FF00FF` (magenta) rectangle and add a text layer reading
    `Placeholder — replace with {component name}`.
  - Place an instance of this placeholder in the slot.
  - Annotate the placeholder instance with a note: "⚠ Dependency not yet built."
- Never create a raw shape or group in place of a referenced component.

**Step 4 — Create Variant properties**
From Appearance > Props, add a Variant property for each prop:
- Property name = prop name from the spec, exactly.
- Values = all accepted values from the spec, in the same order listed.

**Step 5 — Create variant frames and arrange as a table**
From Appearance > Variants, for each row (prop combination → style rules):
- Create or select the variant frame matching that combination.
- Apply the style rules (fill, stroke, radius, opacity, spacing) using Variable references only.
  If a style rule names a token, apply it as a Variable reference — never as a hardcoded value.

After all variant frames are created, arrange the component set as a grid table — no overlapping
or stacking:
- **Columns** = values of the first variant property (e.g. `variant: primary, secondary, ghost`).
- **Rows** = values of the second variant property (e.g. `size: sm, md, lg`).
- If there are more than two variant properties, nest additional properties within each column
  group as sub-columns.
- Use a consistent gap of 40px between cells in both directions.
- Every cell position in the grid must correspond to exactly one variant combination — no cell
  is left empty or duplicated.

**Step 6 — Apply Variable references**
From Appearance > Tokens, for each row (token name → layer → property):
- Navigate to the named layer within the Component.
- Apply the token as a Variable reference on the specified property.
- If the token name does not match a published Variable in the file, stop:
  "Token `{name}` not found in Figma Variables. Resolve before continuing."

**Step 7 — Represent states**
From Appearance > State (both appearance states and interaction states):
- **Appearance states** (disabled, error, loading, read-only) — represent as Variant property
  values on the existing Variant property set. Apply the visual treatment for each using
  Variable references.
- **Interaction states** (hover, focus, pressed, active) — represent as Figma interactive
  component states using the "Change to" interaction trigger where possible; otherwise as
  additional Variant property values.
- Every state in the spec must have a representation. No state may be silently omitted.

**Step 8 — Add accessibility annotations**
From Accessibility, add annotation layers (or use Figma's built-in annotation system):
- **ARIA role** — annotate the role on the outermost Component frame.
- **aria-* attributes** — annotate each attribute and the condition under which it applies
  (e.g. `aria-disabled="true"` when variant=disabled).
- **Keyboard interactions** — annotate Tab, Enter, Space, Arrow key behaviours as applicable.
- **Touch target** — annotate that the interactive hit area must be ≥ 44×44px, even if the
  visual component is smaller.

### Gate 3 — Output

Run a full verification pass against the spec before returning:

**Props check** — for each prop in Appearance > Props: a Variant property with that exact name
and every listed value exists in the Component.

**Variants check** — for each row in Appearance > Variants: a variant frame exists and its
style is applied as a Variable reference (not a hardcoded value).

**State check** — for each row in Appearance > State (both tables): a representation exists.
No state is absent.

**Tokens check** — for each row in Appearance > Tokens: the token is applied as a Variable
reference on the correct layer with the correct property.

**Layer names check** — all layer names inside the Component match the Anatomy > Structure
part names (converted to PascalCase with spaces).

**Accessibility check** — ARIA role, aria-* attributes, keyboard interactions, and touch
target annotation are all present.

Any gap must be corrected before returning. When all rows are accounted for, return the
component URL.
