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

> **Step 1 ACs — verify before continuing to Step 2:**
> - ✓ A page named `{Component Name}` (PascalCase with spaces) exists in the Figma file.
> - ✓ The page is the currently active page.

**Step 2 — Create the Component frame and write the spec**
Create or locate the organism Component on the current page. Name it using PascalCase with
spaces (e.g. `Navigation Bar`, `Data Table`).

Write the full content of `component-spec.md` into the Component's **description** field
in Figma. This makes the spec readable directly from Figma without leaving the file.

> **Step 2 ACs — verify before continuing to Step 3:**
> - ✓ A Component named `{Component Name}` (PascalCase with spaces) exists on the current page.
> - ✓ The Component's description field contains the full `component-spec.md` content, not a summary.

**Step 3 — Place sub-component instances**
From Anatomy > Composition, for each slot in the listed order:
- Convert the slot name to PascalCase with spaces before using it as the instance layer name
  (e.g. `header-region` → `Header Region`).
- If the molecule or atom component URL is present, place a Component Instance at that URL.
- If the component URL is missing, create a **placeholder component** on the current page:
  - Name it using PascalCase with spaces (e.g. `Navigation Item`, `Data Row`).
  - For icon-type dependencies: embed the Icon V2 / not_interested SVG (see Icon samples below).
    For all other dependencies: fill with a solid `#FF00FF` (magenta) rectangle and a text
    layer reading `Placeholder — replace with {component name}`.
  - Place an instance of this placeholder in the slot.
  - Annotate the instance with a note: "⚠ Dependency not yet built."
- Never create raw shapes or groups in place of component instances.

> **Step 3 ACs — verify before continuing to Step 4:**
> - ✓ Every slot in Anatomy > Composition has a Component Instance (or annotated placeholder).
> - ✓ Every instance layer name matches the slot name in PascalCase with spaces.
> - ✓ No raw shapes or groups stand in for component instances.
> - ✓ Every placeholder uses the correct visual (Icon V2 / not_interested SVG for icon-type; magenta #FF00FF for others) and carries the annotation note.

**Step 4 — Apply auto-layout and spacing**
From Anatomy > Layout and Anatomy > Spacing:
- Set auto-layout direction, alignment, and gap using Variable references.
- Set padding on each side using spacing Variable references.

> **Step 4 ACs — verify before continuing to Step 5:**
> - ✓ Auto-layout direction, alignment, and gap use Variable references — no hardcoded px values.
> - ✓ Padding on each side uses the spacing Variable named in Anatomy > Spacing.

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

> **Step 5 ACs — verify before continuing to Step 6:**
> - ✓ A Variant property exists for every property in Appearance > Variants.
> - ✓ A variant frame exists for every combination, with every style rule applied as a Variable reference.
> - ✓ Every lifecycle state (loading, empty, error) has a variant frame or separate frame.
> - ✓ Every interactive state is represented as a Variant value or Figma interactive state.
> - ✓ Variant frames form a grid table: columns = first property values, rows = lifecycle states (default, loading, empty, error), 40px gap in both directions.
> - ✓ Responsive frames are placed below the component set, not inside it.

**Step 6 — Apply organism-scope Variable references**
From Appearance > Tokens:
- Apply each token as a Variable reference on the named layer. No hardcoded values.

> **Step 6 ACs — verify before continuing to Step 7:**
> - ✓ Every token in Appearance > Tokens is applied as a Variable reference on the correct layer.
> - ✓ No hardcoded hex, px, or font value on any mapped layer.

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

> **Step 7 ACs — verify before continuing to Step 8:**
> - ✓ A separate artboard frame named `{Component Name} / {Breakpoint Name}` (PascalCase with spaces) exists for every breakpoint in Responsive > Breakpoints.
> - ✓ Each responsive frame demonstrates the correct reflow: layout direction changes, hidden or reordered slots, and overflow behaviour match the spec.
> - ✓ Mobile-specific patterns (bottom sheet, collapsed navigation, etc.) are applied where the spec defines them.

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

> **Step 8 ACs — verify before Gate 3:**
> - ✓ The ARIA landmark role is annotated on the outermost Component frame with the correct aria-label or aria-labelledby value.
> - ✓ Every heading level in the Accessibility > Heading hierarchy table is annotated on the correct text layer; no levels are skipped.
> - ✓ Every aria-* attribute from the ARIA table is annotated with its value and condition.
> - ✓ Focus management behaviour (trap, return point) is annotated.
> - ✓ Every live region in the Live regions table is annotated with its aria-live value (polite/assertive) and aria-atomic.
> - ✓ Skip links and their target element IDs are annotated (if specified in the spec).

### Gate 3 — Output

Run a section-by-section verification pass against every section of the spec before returning.
Every row in every table must be accounted for — a missing row is a gap, not a skip.

**Anatomy > Composition check** — every slot in the Composition table has a Component Instance
(or annotated placeholder). Layer names match slot names in PascalCase with spaces.

**Anatomy > Layout check** — auto-layout direction, alignment, and gap match the spec using
Variable references. No hardcoded px values.

**Anatomy > Spacing check** — padding on each side uses the spacing Variable named in the spec.

**Appearance > Variants check** — every row in Appearance > Variants has a matching variant
frame with style applied as Variable references (no hardcoded value).

**Appearance > State check** — every lifecycle state (loading, empty, error) and every
interactive state has a representation. Sub-component state propagation matches the spec
description for each state. The `loading` state uses Icon V2 / loader for any spinner element.
Empty and error states use the correct copy from Content > Empty state and Content > Error state.

**Appearance > Tokens check** — every row in Appearance > Tokens is applied as a Variable
reference on the correct layer. No hardcoded hex, px, or font value on any mapped layer.

**Responsive check** — a frame named `{Component Name} / {Breakpoint Name}` exists for every
breakpoint in Responsive > Breakpoints. Each frame demonstrates the reflow strategy written
for that breakpoint (layout direction, hidden slots, overflow behaviour).

**Content > Empty state check** — the empty state frame matches the headline, body, and CTA
label from the spec exactly.

**Content > Error state check** — the error state frame matches the headline, body, and CTA
label from the spec exactly.

**Content > Copy check** — every string in the Copy table is present on the correct layer.

**Accessibility > Landmark check** — the landmark role is annotated on the outermost frame
with the correct aria-label or aria-labelledby value.

**Accessibility > Heading hierarchy check** — every heading level in the spec table is
annotated on the correct text layer. No levels are skipped.

**Accessibility > ARIA check** — every attribute in the ARIA table is annotated with its
value and condition.

**Accessibility > Focus management check** — focus behaviour is annotated for every moment
defined in the spec (mount, data load, refresh, action, error, loading→empty).

**Accessibility > Live regions check** — every region in the Live regions table is annotated
with its aria-live value (polite/assertive) and aria-atomic.

**Accessibility > Skip links check** — if skip links are specified, the target element IDs
are annotated.

Any gap must be corrected before returning. When all rows and breakpoints are accounted for,
return the component URL.

---

## Icon samples

When a sub-component dependency is unavailable or a loading spinner is needed, use these SVGs
inline. Reference the icon by its Icon V2 name in any annotation or note.

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
