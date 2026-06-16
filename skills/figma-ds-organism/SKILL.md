---
name: figma-ds-organism
description: >
  Figma adapter for designer-ds-organism-build. Receives the organism build brief and creates or
  updates a Component in Figma by placing molecule and atom Component Instances, applying
  auto-layout with spacing Variable references, creating a separate responsive frame for each
  defined breakpoint demonstrating the correct reflow strategy, setting up lifecycle states
  (loading, empty, error) and interactive states with sub-component state propagation, applying
  organism-scope Variable references, and adding comprehensive accessibility annotations
  (landmark role, heading hierarchy, ARIA attributes, focus management, live regions, skip links).
  Invoked by designer-ds-organism-build when design-tool is figma.
---

# figma-ds-organism

This skill builds one DS organism Component in Figma from the organism build brief. Organisms
are the most complex component level: they add responsive reflow frames, lifecycle states, and
a full accessibility structure. All sub-components are molecule or atom Component Instances —
never raw shapes. It does not read `component-spec.md` directly.

## Inputs

The build brief from `designer-ds-organism-build`, containing:
- **Component name** and **design file link**.
- **Composition table** — slot name → molecule/atom component name → component URL.
- **Anatomy > Layout** — auto-layout direction, alignment, gap token.
- **Anatomy > Spacing** — internal padding tokens.
- **Appearance > Variants** — organism-level Variant property names, values, and style rules.
- **Appearance > State** — lifecycle states (loading, empty, error) and interactive states,
  each with sub-component state propagation described.
- **Appearance > Tokens** — organism-scope token-to-layer mapping.
- **Responsive > Breakpoints** — breakpoint name and px threshold for each.
- **Responsive > Reflow strategy** — what changes at each breakpoint (layout direction,
  visible slots, overflow behaviour).
- **Responsive > Mobile-specific patterns** — mobile-only patterns (bottom sheet, collapsed
  nav, etc.) where applicable.
- **Content > Empty state, Error state** — visual treatment for content lifecycle states.
- **Accessibility > Landmark** — the landmark role this organism carries.
- **Accessibility > Heading hierarchy** — heading levels used within the organism.
- **Accessibility > ARIA** — aria-* attributes and the conditions under which they apply.
- **Accessibility > Focus management** — focus trap behaviour (modal/dialog) or
  return-to-trigger behaviour after dismissal.
- **Accessibility > Live regions** — which state changes trigger live announcements and the
  aria-live value (polite / assertive).
- **Accessibility > Skip links** — whether skip links are needed and their target IDs.

## Outputs
- Organism Component in the target Figma file.
- Responsive frames — one per breakpoint defined in the brief.
- Component URL.

---

## The 3-gate flow

### Gate 1 — Input
Verify:
- Component name and design file link are present.
- Every molecule and atom component URL in the Composition table is valid. If any is missing,
  stop: "Cannot build — component URL missing for slot `{slot}`."
- Responsive > Breakpoints is present (at least one breakpoint must be defined).

### Gate 2 — Process

**Step 1 — Create the Component frame**
Create or locate the organism Component in the design file. Name it exactly as in the brief.

**Step 2 — Place sub-component instances**
From the Composition table, for each slot in the listed order:
- Place a Component Instance of the molecule or atom at the given URL.
- Name the instance layer exactly as the slot name.
- Never create raw shapes or groups in place of component instances.

**Step 3 — Apply auto-layout and spacing**
From Anatomy > Layout and Anatomy > Spacing:
- Set auto-layout direction, alignment, and gap using Variable references.
- Set padding on each side using spacing Variable references.

**Step 4 — Create Variant properties and states**
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

**Step 5 — Apply organism-scope Variable references**
From Appearance > Tokens:
- Apply each token as a Variable reference on the named layer. No hardcoded values.

**Step 6 — Create responsive frames**
From Responsive > Breakpoints, for each breakpoint:
- Create a separate artboard frame (not a variant — a standalone frame) named
  `{ComponentName} / {breakpoint-name}` (e.g. `DataTable / mobile`).
- Start from the default Component composition, then apply the reflow changes described in
  Responsive > Reflow strategy:
  - Layout direction changes (horizontal → vertical).
  - Slots that are hidden or reordered at this breakpoint.
  - Overflow behaviour (scroll, truncation, collapse).
- Apply any mobile-specific patterns from Responsive > Mobile-specific patterns (bottom sheet,
  collapsed navigation, etc.).

**Step 7 — Add accessibility annotations**
From Accessibility, annotate on the default Component frame:
- **Landmark** — annotate the ARIA landmark role on the outermost frame (e.g. `role="main"`,
  `role="navigation"`, `role="complementary"`).
- **Heading hierarchy** — annotate the heading level on each text layer that carries a heading
  role (e.g. `h2`, `h3`). Levels must be consecutive — no skipped levels.
- **ARIA attributes** — annotate each aria-* attribute and the condition under which it applies.
- **Focus management** — annotate whether focus is trapped inside this organism (modal, dialog)
  and where focus returns after the organism is dismissed or closed.
- **Live regions** — annotate which state transitions trigger a live region announcement,
  the aria-live value (polite / assertive), and the content of the announcement.
- **Skip links** — if the brief specifies skip links, annotate the target element IDs that
  the skip-link anchors must point to.

### Gate 3 — Output

**Instances check** — every slot in the Composition table has a molecule or atom Component
Instance. Layer names match slot names exactly.

**Layout check** — auto-layout direction, alignment, gap, and padding match the brief using
Variable references.

**Variants check** — every organism-level variant combination has a matching frame with style
applied as Variable references.

**State check** — every lifecycle state and interactive state has a representation. Sub-component
state propagation matches the brief description for each state.

**Tokens check** — every organism-scope token is applied as a Variable reference on the correct
layer. No hardcoded values.

**Responsive check** — a frame named `{ComponentName} / {breakpoint}` exists for every
breakpoint in the brief, demonstrating the reflow strategy written for that breakpoint.

**Accessibility check** — landmark, heading hierarchy, ARIA attributes, focus management, live
regions, and skip links (if applicable) are all annotated on the Component frame.

Any gap must be corrected before returning. When all rows and breakpoints are accounted for,
return the component URL to `designer-ds-organism-build`.
