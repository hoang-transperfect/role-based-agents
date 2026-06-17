---
name: figma-ds-atom
description: >
  Figma adapter for designer-ds-atom-build. Receives the atom build brief and creates or updates
  a Component in Figma: builds the layer hierarchy from Anatomy > Structure (part names become
  layer names exactly), creates Variant properties from Appearance > Props, creates variant frames
  from Appearance > Variants, applies Variable references from Appearance > Tokens (no hardcoded
  values), represents all states from Appearance > State, and adds accessibility annotations
  (ARIA role, aria-* attributes, keyboard interactions, 44×44px touch target). Where Anatomy
  references Icon or Text dependencies, places Component Instances — not raw shapes. Invoked by
  designer-ds-atom-build when design-tool is figma.
---

# figma-ds-atom

This skill builds one atom Component in Figma from the atom build brief. It maps every section
of the brief to Figma-specific operations. It does not read `component-spec.md` directly — the
brief is fully prepared by `designer-ds-atom-build`.

## Naming convention

All Figma artifact names — pages, component names, and frame names — use **lowercase kebab-case**.
Convert the component name from the brief before using it anywhere in Figma:
`Button` → `button`, `FormField` → `form-field`, `NavigationBar` → `navigation-bar`.

Exception: internal layer names inside a Component must match the Anatomy > Structure part names
from the spec exactly, regardless of casing, because they are the implementation contract with
engineering.

## Inputs

The build brief from `designer-ds-atom-build`, containing:
- **Component name** and **design file link**.
- **Anatomy > Structure** — the layer hierarchy: frame name, child layers, part names in order.
- **Anatomy > Details** — slot behaviours, constraints, child component references (Icon, Text,
  or other atom dependencies).
- **Appearance > Props** — variant property names and all accepted values.
- **Appearance > Variants** — rows: prop-value combination → style rules.
- **Appearance > State** — appearance states (system-driven) and interaction states
  (user-driven) with their visual treatment.
- **Appearance > Tokens** — rows: token name → layer name → CSS property mapping.
- **Accessibility** — ARIA role, aria-* attributes and conditions, keyboard interactions,
  minimum touch target size.
- **Dependency component URLs** — Figma component URLs for Icon, Text, and any other atoms
  this atom embeds as instances.

## Outputs
- Component in the target Figma file.
- Component URL.

---

## The 3-gate flow

### Gate 1 — Input
Verify:
- Component name and design file link are present.
- Anatomy, Props, Variants, State, and Tokens sections are all in the brief.
- For any child component reference in Anatomy > Details, the dependency URL is present.
  If missing, stop: "Cannot build — dependency component URL missing for `{name}`."

### Gate 2 — Process

**Step 1 — Create or navigate to the component page**
Convert the component name from the brief to lowercase kebab-case — this is the page name
(e.g. `Button` → `button`, `InputField` → `input-field`). Check whether the page already exists:
- If it does not exist, create it with the kebab-case name, then navigate to it.
- If it exists, navigate to it.
All subsequent steps place content on this page only.

**Step 2 — Create the Component frame**
Create a new Component (or locate the existing one to update by name) on the current page. Name
it using the same lowercase kebab-case form (e.g. `button`, `input-field`).

**Step 3 — Build the layer hierarchy**
From Anatomy > Structure, build the layer tree inside the Component:
- Each part name in the hierarchy becomes a named frame or layer.
- Layer names must match the part names **exactly** — no renaming, no abbreviation.
- Where Anatomy > Details specifies a child component reference (e.g. an Icon instance or a
  Text instance): place a Component Instance using the dependency URL. Never create a raw
  shape or group in place of a referenced component.

**Step 4 — Create Variant properties**
From Appearance > Props, add a Variant property for each prop:
- Property name = prop name from the brief, exactly.
- Values = all accepted values from the brief, in the same order listed.

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
- Every state in the brief must have a representation. No state may be silently omitted.

**Step 8 — Add accessibility annotations**
From Accessibility, add annotation layers (or use Figma's built-in annotation system):
- **ARIA role** — annotate the role on the outermost Component frame.
- **aria-* attributes** — annotate each attribute and the condition under which it applies
  (e.g. `aria-disabled="true"` when variant=disabled).
- **Keyboard interactions** — annotate Tab, Enter, Space, Arrow key behaviours as applicable.
- **Touch target** — annotate that the interactive hit area must be ≥ 44×44px, even if the
  visual component is smaller.

### Gate 3 — Output

Run a full verification pass against the brief before returning:

**Props check** — for each prop in Appearance > Props: a Variant property with that exact name
and every listed value exists in the Component.

**Variants check** — for each row in Appearance > Variants: a variant frame exists and its
style is applied as a Variable reference (not a hardcoded value).

**State check** — for each row in Appearance > State (both tables): a representation exists.
No state is absent.

**Tokens check** — for each row in Appearance > Tokens: the token is applied as a Variable
reference on the correct layer with the correct property.

**Layer names check** — all layer names inside the Component match the Anatomy > Structure
part names exactly.

**Accessibility check** — ARIA role, aria-* attributes, keyboard interactions, and touch
target annotation are all present.

Any gap must be corrected before returning. When all rows are accounted for, return the
component URL to `designer-ds-atom-build`.
