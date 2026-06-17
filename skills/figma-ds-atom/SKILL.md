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

> **Step 1 ACs — all must pass before Step 2. Fix any failure before proceeding:**
> - ✓ A page named `{Component Name}` (PascalCase with spaces) exists in the Figma file.
> - ✓ The page is the currently active page.

**Step 2 — Create the Component frame and write the spec**
Create a new Component (or locate the existing one to update by name) on the current page.
Name it using PascalCase with spaces (e.g. `Button`, `Icon Button`).

Write the full content of `component-spec.md` into the Component's **description** field
in Figma. This makes the spec readable directly from Figma without leaving the file.

> **Step 2 ACs — all must pass before Step 3. Fix any failure before proceeding:**
> - ✓ A Component named `{Component Name}` (PascalCase with spaces) exists on the current page.
> - ✓ The Component's description field contains the full `component-spec.md` content, not a summary.

**Step 3 — Build the layer hierarchy**
From Anatomy > Structure, build the layer tree inside the Component:
- Convert each part name to PascalCase with spaces before using it as the layer name
  (e.g. `icon-slot` → `Icon Slot`, `labelText` → `Label Text`).
- Where Anatomy > Details specifies a child component reference (e.g. an Icon instance or a
  Text instance): place a Component Instance using the dependency URL.
- If a dependency URL is missing, create a **placeholder component** on the current page:
  - Name it using PascalCase with spaces (e.g. `Icon`, `Text`).
  - For icon-type dependencies: embed the `not_interested` SVG from Icon V2 as the
    placeholder visual (see Icon samples below). For all other dependencies: fill with
    a solid `#FF00FF` (magenta) rectangle and a text layer reading
    `Placeholder — replace with {component name}`.
  - Place an instance of this placeholder in the slot.
  - Annotate the placeholder instance with a note: "⚠ Dependency not yet built — Icon V2 / not_interested used as sample."
- Never create a raw shape or group in place of a referenced component.

> **Step 3 ACs — all must pass before Step 4. Fix any failure before proceeding:**
> - ✓ Every part from Anatomy > Structure exists as a named layer in PascalCase with spaces.
> - ✓ Layer nesting matches the hierarchy in the spec.
> - ✓ Every child component reference from Anatomy > Details has a Component Instance or an annotated placeholder — no raw shapes.
> - ✓ Every placeholder uses the correct visual (Icon V2 / not_interested SVG for icon-type; magenta #FF00FF for others) and carries the annotation note.

**Step 4 — Create Variant properties**
From Appearance > Props, add a Variant property for each prop:
- Property name = prop name from the spec, exactly.
- Values = all accepted values from the spec, in the same order listed.

> **Step 4 ACs — all must pass before Step 5. Fix any failure before proceeding:**
> - ✓ A Variant property exists for every prop in Appearance > Props.
> - ✓ Each property name matches the spec exactly.
> - ✓ Each property includes all values from the spec in the same order.

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

> **Step 5 ACs — all must pass before Step 6. Fix any failure before proceeding:**
> - ✓ A variant frame exists for every row in Appearance > Variants.
> - ✓ Every style rule on every variant frame is applied as a Variable reference — no hardcoded hex, px, or font value.
> - ✓ Variant frames form a grid table: columns = first property values, rows = second property values.
> - ✓ Gap between all cells is 40px horizontally and vertically.
> - ✓ No cell is empty or duplicated.

**Step 6 — Apply Variable references**
From Appearance > Tokens, for each row (token name → layer → property):
- Navigate to the named layer within the Component.
- Apply the token as a Variable reference on the specified property.
- If the token name does not match a published Variable in the file, stop:
  "Token `{name}` not found in Figma Variables. Resolve before continuing."

> **Step 6 ACs — all must pass before Step 7. Fix any failure before proceeding:**
> - ✓ Every token in Appearance > Tokens is applied as a Variable reference on the correct layer and the correct CSS property.
> - ✓ No hardcoded hex, px, or font value exists on any layer that Appearance > Tokens maps.

**Step 7 — Represent states**
From Appearance > State (both appearance states and interaction states):
- **Appearance states** (disabled, error, loading, read-only) — represent as Variant property
  values on the existing Variant property set. Apply the visual treatment for each using
  Variable references. For the `loading` state, use the `loader` SVG from Icon V2 as the
  spinner visual (see Icon samples below).
- **Interaction states** (hover, focus, pressed, active) — represent as Figma interactive
  component states using the "Change to" interaction trigger where possible; otherwise as
  additional Variant property values.
- Every state in the spec must have a representation. No state may be silently omitted.

> **Step 7 ACs — all must pass before Step 8. Fix any failure before proceeding:**
> - ✓ Every appearance state (disabled, error, loading, read-only) is represented as a Variant property value.
> - ✓ Every interaction state (hover, focus, pressed, active) is represented as a Figma interactive state or Variant value.
> - ✓ The `loading` state uses the Icon V2 / loader SVG as the spinner visual.
> - ✓ No state from either State table is absent.

**Step 8 — Add accessibility annotations**
From Accessibility, add annotation layers (or use Figma's built-in annotation system):
- **ARIA role** — annotate the role on the outermost Component frame.
- **aria-* attributes** — annotate each attribute and the condition under which it applies
  (e.g. `aria-disabled="true"` when variant=disabled).
- **Keyboard interactions** — annotate Tab, Enter, Space, Arrow key behaviours as applicable.
- **Touch target** — annotate that the interactive hit area must be ≥ 44×44px, even if the
  visual component is smaller.

> **Step 8 ACs — all must pass before Gate 3. Fix any failure before proceeding:**
> - ✓ The ARIA role is annotated on the outermost Component frame.
> - ✓ Every aria-* attribute from the ARIA table is annotated with its value and the condition under which it applies.
> - ✓ Every keyboard interaction from the Keyboard table is annotated.
> - ✓ The touch target minimum (44×44px) is annotated.
> - ✓ Every state change in the Screen reader table is annotated with the announced text and method.

### Gate 3 — Output

Run a section-by-section verification pass against every section of the spec before returning.
Every row in every table must be accounted for — a missing row is a gap, not a skip.

**Anatomy > Structure check** — every part listed in Structure exists as a named layer in the
Component, converted to PascalCase with spaces. Layer nesting matches the spec hierarchy.

**Anatomy > Details check** — every child component reference in Details has a Component
Instance (or an annotated placeholder). No raw shapes stand in for a referenced component.

**Appearance > Props check** — for each prop in Appearance > Props: a Variant property exists
with that exact name and every listed value present, in the same order.

**Appearance > Variants check** — for each row in Appearance > Variants: a variant frame
exists and every style rule is applied as a Variable reference (no hardcoded value).

**Appearance > State check** — for each row in both Appearance > State tables (appearance
states and interaction states): a representation exists. The `loading` state uses the
Icon V2 / loader SVG. No state is absent.

**Appearance > Tokens check** — for each row in Appearance > Tokens: the token is applied
as a Variable reference on the correct layer with the correct CSS property. No hardcoded
hex, px, or font value on any layer that the Tokens table maps.

**Content check** — for each row in Content > Copy: the default text is present on the
correct layer. Sections marked "(Skip if not applicable)" are confirmed as truly N/A for
this component.

**Accessibility > ARIA check** — every attribute in the ARIA table is annotated on the
Component with its value and condition.

**Accessibility > Keyboard check** — every key in the Keyboard table is annotated.

**Accessibility > Focus management check** — the HTML element, tab stop, and focus trap
behaviour are annotated.

**Accessibility > Touch target check** — minimum 44×44px hit area is annotated.

**Accessibility > Screen reader check** — every state change in the Screen reader table is
annotated with the announced text and method.

Any gap must be corrected before returning. When all rows in all sections are accounted for,
return the component URL.

---

## Icon samples

When an icon dependency is unavailable (no component URL) or when a loading spinner is needed,
use these SVGs inline. Reference the icon by its Icon V2 name in any annotation or note.

**Icon V2 / not_interested** — use for generic icon placeholders:
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.58 20 4 16.42 4 12C4 10.15 4.63 8.45 5.69 7.1L16.9 18.31C15.55 19.37 13.85 20 12 20ZM18.31 16.9L7.1 5.69C8.45 4.63 10.15 4 12 4C16.42 4 20 7.58 20 12C20 13.85 19.37 15.55 18.31 16.9Z" fill="#393F4C"/>
</svg>
```

**Icon V2 / loader** — use for loading states:
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 22.4805C10.558 22.4805 9.20053 22.2059 7.92753 21.6565C6.6547 21.1074 5.54311 20.3576 4.59278 19.4073C3.64245 18.4569 2.8927 17.3454 2.34353 16.0725C1.7942 14.7995 1.51953 13.442 1.51953 12C1.51953 10.5494 1.79411 9.19053 2.34328 7.92353C2.89245 6.65636 3.64211 5.54653 4.59228 4.59403C5.54245 3.64153 6.65411 2.89095 7.92728 2.34228C9.20045 1.79378 10.558 1.51953 12 1.51953C12.3682 1.51953 12.681 1.64836 12.9385 1.90603C13.1962 2.1637 13.325 2.47653 13.325 2.84453C13.325 3.2127 13.1962 3.52561 12.9385 3.78328C12.681 4.04078 12.3682 4.16953 12 4.16953C9.83037 4.16953 7.98286 4.9322 6.45753 6.45753C4.9322 7.98286 4.16953 9.83028 4.16953 11.9998C4.16953 14.1694 4.9322 16.017 6.45753 17.5425C7.98286 19.0679 9.83028 19.8305 11.9998 19.8305C14.1694 19.8305 16.017 19.0679 17.5425 17.5425C19.0679 16.0172 19.8305 14.1697 19.8305 12C19.8305 11.6319 19.9593 11.319 20.2168 11.0615C20.4744 10.8039 20.7874 10.675 21.1555 10.675C21.5235 10.675 21.8364 10.8039 22.094 11.0615C22.3517 11.319 22.4805 11.6319 22.4805 12C22.4805 13.442 22.2059 14.7997 21.6568 16.073C21.1076 17.3464 20.3579 18.4584 19.4078 19.409C18.4576 20.3595 17.3484 21.1091 16.0803 21.6578C14.8121 22.2063 13.452 22.4805 12 22.4805Z" fill="#393F4C"/>
</svg>
```
