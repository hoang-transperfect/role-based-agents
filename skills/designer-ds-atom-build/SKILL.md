---
name: designer-ds-atom-build
description: >
  Builds one design system atom into a design file as a Component with the full set of variants
  and states defined in its component-spec.md. Reads Anatomy, Appearance (props, variants, states,
  tokens), and Accessibility from the spec, then delegates the implementation to the configured
  adapter (default: figma:figma-generate-library). Run after designer-ds-foundation-build has
  published foundation Variables, and after this atom's component-spec.md is complete. Icon and
  Text must be built before any other atom. Invoke once per atom; all atoms must be built before
  molecules.
---

# designer-ds-atom-build

An atom build takes the complete component-spec.md and produces a Component that matches it
exactly: correct variant properties, all states, token references (not hardcoded values), anatomy
layers named to match the spec, and accessibility annotations.

This skill reads the spec, prepares the build brief, and delegates to the design tool adapter
(`figma:figma-generate-library` by default). Icon and Text must be built first — every other atom
embeds an icon slot, a text label, or both, and must reference those components by instance.

## Where things live

- **Read** `<real_project_path>/design-system/atoms/<component-name>/component-spec.md`.
- **Read** `<real_project_path>/designer-artifacts/resource.md` — the design file link
  (set by `designer-ds-foundation-build`).
- **Update** `<real_project_path>/design-system/atoms/<component-name>/component-spec.md` —
  add the component link to the frontmatter `link:` field after build.
- **Update** the task file `## Plan` — tick this atom's build step.

---

## The skill contract

### Inputs
- `design-system/atoms/<component-name>/component-spec.md` — the spec to build from.
- `resource.md` — the design file link.
- Foundation Variables must already be published in the design file.

### Input Acceptance Criteria
- `component-spec.md` for this atom exists and its Spec checklist items (Anatomy, Appearance,
  Content, Accessibility) are all checked or explicitly waived with justification.
- The design file link is present in `resource.md`.
- Foundation Variables are published in the design file.
- **If this atom is not Icon or Text**: both Icon and Text Components must already exist in the
  design file. If either is missing, stop: "Icon and Text must be built before any other atom.
  Let's build {missing one} first."

### Outputs
- Component for this atom in the target design file.
- `component-spec.md` frontmatter `link:` field updated with the component URL.

### Output Quality Criteria
- **Props:** every prop in Appearance > Props has a variant property in the design file with the
  exact same name and every listed value present — no prop omitted, no value missing.
- **Variants:** every row in every variant table in Appearance > Variants has a corresponding
  frame or mode in the design file. The style applied to that frame matches the spec row exactly
  — token reference, not a hardcoded approximation.
- **State:** every row in both Appearance > State tables (appearance states and interaction
  states) has a corresponding representation — as a variant property value, interactive behavior,
  or separate frame. No state from the spec is absent.
- **Tokens:** every row in Appearance > Tokens is applied as a Variable reference on the correct
  layer. No layer that the token table maps has a hardcoded hex, px, or font value.
- All layer names match the part names in Anatomy > Structure exactly.
- Accessibility annotations are attached: ARIA role, aria-* attributes, keyboard behavior,
  minimum touch target (44×44px).
- `component-spec.md` frontmatter `link:` field contains a working component URL.

---

## The 3-gate flow

### Gate 1 — Input
Check that `component-spec.md` exists and the Spec checklist is complete. Verify the design file
link is in `resource.md` and foundation Variables are present.

**If this atom is not Icon or Text**, confirm both Icon and Text Components exist in the design
file. If either is missing, stop: "Icon and Text must be built before any other atom. Let's build
{missing one} first." Do not proceed with any other atom until both exist.

### Gate 2 — Process
Read `component-spec.md` and extract:
- **Anatomy > Structure**: layer hierarchy and part names for the component layer tree.
- **Anatomy > Details**: slot behaviors, constraints, and any child component references.
- **Appearance > Props**: variant property names and all accepted values.
- **Appearance > Variants**: all variant combinations and their style rules.
- **Appearance > State**: appearance states (system-driven) and interaction states (user-driven).
- **Appearance > Tokens**: the token-to-layer mapping for Variable references.
- **Accessibility**: ARIA attributes, keyboard interactions, focus management, touch target.

Prepare the build brief: component name, layer structure, variant property definitions,
state definitions, token-to-layer mapping, accessibility annotations.

If any token name in the spec does not match a published Variable name in the design file, flag
it with the user before proceeding — do not substitute a different token or hardcode a value.

Invoke the adapter:
> Load `figma:figma-generate-library` and pass the build brief. Instruct the adapter to:
> 1. Create or update the Component in the target design file.
> 2. Set up variant properties matching the Props and Variants from the spec.
> 3. Name all layers to match the Anatomy > Structure part names.
> 4. Apply Variable references to all token-mapped properties (no hardcoded values).
> 5. Add accessibility annotations (ARIA, keyboard, focus management, touch target).
> 6. Return the component URL.

### Gate 3 — Output
Run a full appearance verification pass against the spec before confirming completion:

**Props check:** for each prop in Appearance > Props — verify the design file has a variant
property with that exact name and all listed values present.

**Variants check:** for each row in each variant table in Appearance > Variants — verify a
corresponding frame or mode exists and its style matches the spec row (token reference applied,
not hardcoded).

**State check:** for each row in both Appearance > State tables — verify a corresponding
representation exists (variant property value, interactive behavior, or separate frame).

**Tokens check:** for each row in Appearance > Tokens — verify the token is applied as a Variable
reference on the correct layer, not a hardcoded value.

Any row from the spec that has no matching element in the design file is a gap. Gaps must be
resolved before moving on — do not accept partial matches. When all rows are accounted for:
1. Present the component URL and the completed verification pass (rows checked, gaps resolved).
2. Ask the user to confirm.
3. **If confirmed** → update `component-spec.md` frontmatter `link:` field with the component
   URL, tick this atom's build step in `## Plan`, then hand off to `commit-work`.
4. **If not satisfied** → iterate with the user, then commit.

---

## Handoff
Completed atom builds feed `designer-ds-molecule-build` — molecules embed atom Components as
instances. Icon and Text builds unblock all remaining atom builds.
