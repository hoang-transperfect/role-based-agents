---
name: designer-ds-molecule-build
description: >
  Builds one design system molecule into a design file as a Component that composes atom
  instances. Reads Anatomy (Composition, Layout, Spacing), Appearance (variants, states, tokens),
  and Accessibility from the component-spec.md, then delegates the implementation to the configured
  adapter (default: figma:figma-generate-library). Run after all atom dependencies for this
  molecule are built (via designer-ds-atom-build), and after this molecule's component-spec.md is
  complete. Invoke once per molecule; all molecules must be built before organisms.
---

# designer-ds-molecule-build

A molecule build takes the component-spec.md and produces a Component whose sub-layers are
instances of already-built atom (or molecule) Components — not raw layers. The molecule spec
only defines molecule-level rules: layout, spacing, state propagation, and ARIA relationships.
Visual token values come from the constituent atoms via their Variable references.

This skill reads the spec, prepares the build brief, and delegates to the design tool adapter
(`figma:figma-generate-library` by default). Every atom dependency must be built before this
skill runs.

## Where things live

- **Read** `<real_project_path>/design-system/molecules/<component-name>/component-spec.md`.
- **Read** atom specs at `<real_project_path>/design-system/atoms/` for dependency names
  (to reference the correct Component instances).
- **Read** `<real_project_path>/designer-artifacts/resource.md` — the design file link.
- **Update** `<real_project_path>/design-system/molecules/<component-name>/component-spec.md` —
  add the component link to the frontmatter `link:` field after build.
- **Update** the task file `## Plan` — tick this molecule's build step.

---

## The skill contract

### Inputs
- `design-system/molecules/<component-name>/component-spec.md` — the spec to build from.
- `resource.md` — the design file link.
- All atom (and molecule) dependencies listed in the spec's frontmatter `dependencies:` must
  already be built and their `link:` fields updated with component URLs.

### Input Acceptance Criteria
- `component-spec.md` for this molecule exists and its Spec checklist items are all checked or
  explicitly waived with justification.
- The design file link is present in `resource.md`.
- Every dependency listed in `dependencies.atoms` (and `dependencies.molecules`, if any) has a
  component URL in its own `link:` field. If any dependency is missing, stop and route to
  `designer-ds-atom-build` (or `designer-ds-molecule-build`) for the missing dependency first.

### Outputs
- Component for this molecule in the target design file.
- `component-spec.md` frontmatter `link:` field updated with the component URL.

### Output Quality Criteria
- Every sub-component in the molecule is an instance of an existing atom (or molecule) Component
  — no raw shapes or layers that duplicate an atom's appearance.
- Layout matches the Anatomy > Layout section (direction, alignment, wrapping behavior).
- Spacing between sub-components uses spacing Variables matching the Anatomy > Spacing section.
- **Variants:** every row in every variant table in Appearance > Variants has a corresponding
  frame or mode. The style applied matches the spec row exactly — no row omitted.
- **State:** every row in Appearance > State has a corresponding representation (variant property
  value or interactive behavior). For each state, the atoms listed in the "atoms-affected" column
  have their state properties updated as described — no state from the spec is absent.
- **Tokens:** every row in Appearance > Tokens is applied as a Variable reference on the correct
  layer — no hardcoded value where the spec names a token.
- ARIA relationships from Accessibility > ARIA relationships are annotated on the component.
- `component-spec.md` frontmatter `link:` field contains a working component URL.

---

## The 3-gate flow

### Gate 1 — Input
Check that `component-spec.md` exists and the Spec checklist is complete. Verify the design file
link is in `resource.md`. For every dependency in `dependencies.atoms` and
`dependencies.molecules`, confirm a component URL exists in that dependency's `link:` field.

If any dependency is not yet built, stop: "The dependency {name} has not been built yet. Let's
build that first." Do not proceed with any molecule before all its dependencies are built.

### Gate 2 — Process
Read `component-spec.md` and extract:
- **Frontmatter > dependencies**: the list of atom (and molecule) component names and their URLs.
- **Anatomy > Composition table**: each sub-component, its slot name, and which atom it maps to.
- **Anatomy > Layout**: layout direction, alignment, gap/spacing tokens, wrap behavior.
- **Anatomy > Spacing**: internal padding and spacing tokens.
- **Appearance > Variants**: molecule-level variant properties and values.
- **Appearance > State**: which atoms' states are affected for each molecule state.
- **Appearance > Tokens**: molecule-level token references (spacing, radius at molecule scope).
- **Accessibility > ARIA relationships**: which atoms carry aria-labelledby/describedby pointing
  to other atoms within the molecule.
- **Accessibility > Keyboard flow**: tab order across atoms within the molecule.

Prepare the build brief: component name, sub-component instance map (slot → atom component URL),
layout rules, spacing token references, variant properties, state propagation rules, ARIA
relationship annotations, keyboard flow order.

If any dependency component URL is invalid or a token name does not match a published Variable,
flag it with the user before proceeding.

Invoke the adapter:
> Load `figma:figma-generate-library` and pass the build brief. Instruct the adapter to:
> 1. Create or update the molecule Component in the target design file.
> 2. Place atom (or molecule) Component instances for each slot — not raw shapes.
> 3. Apply layout rules (auto-layout direction, alignment, gap) and spacing Variables.
> 4. Set up molecule-level variant properties and state propagation to sub-components.
> 5. Add ARIA relationship annotations and keyboard flow order.
> 6. Return the component URL.

### Gate 3 — Output
Run a full appearance verification pass against the spec before confirming completion:

**Variants check:** for each row in every variant table in Appearance > Variants — verify a
corresponding frame or mode exists and its style matches the spec row exactly (token applied, not
hardcoded).

**State check:** for each row in Appearance > State — verify a corresponding representation
exists, and confirm the atoms-affected column is honoured: the correct atom instances are in the
matching state.

**Tokens check:** for each row in Appearance > Tokens — verify the token is applied as a Variable
reference on the correct layer, not a hardcoded value.

**Layout and spacing check:** verify auto-layout direction, alignment, and gap values match the
Anatomy > Layout and Spacing sections, using spacing Variables.

Any row from the spec that has no matching element in the design file is a gap. Gaps must be
resolved before moving on. When all rows are accounted for:
1. Present the component URL and the completed verification pass (rows checked, gaps resolved).
2. Ask the user to confirm.
3. **If confirmed** → update `component-spec.md` frontmatter `link:` field, tick this molecule's
   build step in `## Plan`, then hand off to `commit-work`.
4. **If not satisfied** → iterate with the user, then commit.

---

## Handoff
Completed molecule builds feed `designer-ds-organism-build` — organisms embed molecule (and atom)
Component instances. All molecules must be built before any organism that depends on them.
