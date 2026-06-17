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
  - For icon-type dependencies: embed the Icon V2 / not_interested SVG (see Icon samples below).
    For all other dependencies: fill with a solid `#FF00FF` (magenta) rectangle and a text
    layer reading `Placeholder — replace with {component name}`.
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

Run a section-by-section verification pass against every section of the spec before returning.
Every row in every table must be accounted for — a missing row is a gap, not a skip.

**Anatomy > Composition check** — every slot in the Composition table has a Component Instance
(or annotated placeholder). Instance layer names match slot names in PascalCase with spaces.
No raw shape or group stands in for a component.

**Anatomy > Layout check** — auto-layout direction, alignment, gap, and wrap match the spec.
All spacing values use Variable references — no hardcoded px values.

**Anatomy > Spacing check** — padding on each side uses the spacing Variable named in the spec.

**Appearance > Variants check** — every row in Appearance > Variants has a matching variant
frame. Every style rule is applied as a Variable reference (no hardcoded value).

**Appearance > State check** — every row in Appearance > State has a representation. The
atoms-affected column is honoured in each state frame — correct atom instances are switched
to the specified state. The `loading` state uses Icon V2 / loader for any spinner element.

**Appearance > Tokens check** — every row in Appearance > Tokens is applied as a Variable
reference on the correct layer. No hardcoded hex, px, or font value on any mapped layer.

**Content check** — every row in Content > Copy has its default text present on the correct
layer. Label, Helper text, and Validation messages sections are verified or confirmed N/A.

**Accessibility > ARIA check** — every relationship in the ARIA table is annotated
(aria-labelledby, aria-describedby, aria-required, etc.) with its target and condition.

**Accessibility > Keyboard flow check** — tab order annotations are numbered and match the
spec sequence. Entry and exit behaviour are annotated.

**Accessibility > Screen reader check** — every molecule-level state change in the Screen
reader table is annotated with the announced text and method.

Any gap must be corrected before returning. When all rows in all sections are accounted for,
return the component URL.

---

## Icon samples

When an atom dependency is unavailable or a loading spinner is needed, use these SVGs inline.
Reference the icon by its Icon V2 name in any annotation or note.

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
