---
name: designer-organism
description: >
  Creates or updates a product-specific organism spec using the designer-ds-organism spec template
  format. Product-specific organisms are tightly coupled to the product's IA or data model and do
  not belong in the design system — but are built exclusively from DS atoms and molecules by name.
  Invoke when a story spec (designer-ui) lists a product-specific organism that needs a spec or an
  update (e.g. AppNavigationBar, UserProfileCard, OrderSummaryPanel). If the organism already has
  a spec, reads it first then rewrites it in full. Produces a dedicated organism-spec.md under
  design-spec/product-organisms/. Run before designer-template and designer-page so they can
  reference the organism by name. Spec once per organism; all subsequent stories that change it
  update the same file.
---

# designer-organism

Not all organisms belong in the design system. An organism that is tightly coupled to this
product's information architecture, data model, or specific feature context is intentionally
product-specific — it would not make sense extracted into a generic design system. This skill
specs those organisms.

The key constraint: a product-specific organism is **assembled from DS components** — atoms and
molecules from the design system. It never introduces new visual primitives. Token values come
from the design system foundations; sub-components come from the DS component library. Only the
composition and the product-specific content rules are defined here.

**No raw HTML elements for content** — every content-rendering slot in the Composition table
must reference a named DS molecule, atom, or foundation component, not a raw HTML element
(e.g. not `<span>`, `<img>`, `<p>`). Layout wrappers (`<div>`, `<section>`, `<ul>`, `<nav>`,
etc.) used purely to structure layout regions are the only exception. Any content slot that
cannot be satisfied by an existing DS component is a DS gap — flag it with ⚠ and recommend
adding it to the DS first.

**If the same organism is needed in multiple stories:** spec it once here, then every subsequent
story references it by name and links to this file — do not re-spec it.

## Where things live

- **Read** the story spec (`design-spec/<epic>/<feature>/<story>/story-spec.md`) to understand
  what is changing for this organism and what the affected artifact entry says.
- **Read** the existing organism spec at
  `<real_project_path>/design-spec/product-organisms/<organism-name>/organism-spec.md` if it
  exists — always read before writing when the spec already exists.
- **Read** DS component specs at `<real_project_path>/design-system/` for the atoms/molecules
  this organism will use.
- **Write** (or overwrite) the spec to
  `<real_project_path>/design-spec/product-organisms/<organism-name>/organism-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- The story spec that requires this organism (to understand what is changing and why).
- The existing organism spec if this is an update (read before writing — never overwrite blind).
- The DS component specs for the atoms/molecules it will be built from.
- Confirmation that this organism is product-specific (not a generic, reusable component that
  belongs in the DS). If uncertain, discuss with the designer: can this organism be used in a
  completely different product without modification? If yes → it belongs in the DS.

### Input Acceptance Criteria
- The story spec for the current story exists and is confirmed (from `designer-ui`).
- The organism is confirmed as product-specific, not a DS candidate.
- The DS atoms and molecules this organism depends on exist in the design system. If a dependency
  is missing from the DS, flag it as a DS gap and recommend adding it there first.
- If updating: the existing organism spec has been read before any changes are made.

### Outputs
- `<real_project_path>/design-spec/product-organisms/<organism-name>/organism-spec.md`

### Output Quality Criteria
Follows the `designer-ds-organism` Output Quality Criteria, with these product-specific
distinctions:
- **Built from DS components only** — every sub-component is a named DS atom or molecule. No raw
  token values; no invented components. DS gaps flagged with ⚠ in the relevant section.
- **Product-specific data and context documented** — data labels, routes, and business logic
  specific to this product are permitted and should be named explicitly. This is the key
  distinction from DS organisms, which must be fully generic.
- **Used-in metadata present** — the `_Type: product-specific · Used in: …_` line lists all
  stories so a developer knows the organism's scope without reading every story spec.

---

## The 3-gate flow

### Gate 1 — Input
Verify the organism is product-specific, not a DS candidate. If it could be generic and reusable,
discuss with the designer — the right place for it may be `designer-ds-component`, not here.
If an organism spec already exists, read it before proceeding. Verify DS component dependencies
exist; flag any missing ones as DS gaps before proceeding.

### Gate 2 — Process
If updating an existing spec: start from the current spec, apply the changes described in the
story spec, then write the complete updated spec. Do not carry forward anything that is no longer
correct after this story's changes.

Write the organism spec following the `designer-ds-organism` spec template format exactly
(Anatomy, Appearance, Content, Accessibility, Checklist). The only differences from a DS
organism spec:
- Output path: `design-spec/product-organisms/<organism-name>/organism-spec.md` (not in
  `design-system/organisms/`).
- Product-specific data labels, routes, and business logic are permitted — do not strip them
  to make the organism look generic.
- Add `_Type: product-specific · Used in: <US-01>, …_` as the first line after the `#` heading.
- DS gaps are flagged inline with ⚠ in the relevant section, not in a separate section.

### Gate 3 — Output
Check against the `designer-ds-organism` Output Quality Criteria — especially that all
sub-components are named DS components (never raw values), DS gaps are flagged with ⚠, and the
used-in metadata line is present. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick Step 3a in `## Plan` (or note the organism in a list
   if multiple organisms are being specced), update **Next step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The organism spec feeds `designer-template` (which places it in layout zones) and `designer-page`
(which references it in page specs). All subsequent stories that change this organism update the
same spec file — rewriting it in full to reflect the new state.
