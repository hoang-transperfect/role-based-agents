---
name: designer-ds-organism-build
description: >
  Builds one design system organism into a design file as a Component that composes molecule and
  atom instances. Reads Anatomy (Composition, Layout, Spacing), Appearance (variants,
  lifecycle/interactive states, tokens), Responsive (breakpoints, reflow), and Accessibility from
  the component-spec.md, then delegates the implementation to the configured adapter (default:
  determined by the `design-tool` field in `resource.md`). Run after all molecule and atom dependencies for this organism
  are built. Invoke once per DS organism; organisms are the last component level before
  designer-ds-document.
---

# designer-ds-organism-build

An organism build takes the component-spec.md and produces a Component whose sub-layers are
instances of already-built molecule and atom Components. Organisms are where responsive reflow,
lifecycle states (loading, empty, error), and complex accessibility structures are fully expressed
in the design file.

This skill reads the spec, prepares the build brief, and delegates to the design tool adapter
declared in `resource.md`. All molecule and atom dependencies must be built before this skill runs.

## Where things live

- **Read** `<real_project_path>/design-system/organisms/<component-name>/component-spec.md`.
- **Read** molecule specs at `<real_project_path>/design-system/molecules/` and atom specs at
  `<real_project_path>/design-system/atoms/` for dependency component URLs.
- **Read** `<real_project_path>/designer-artifacts/resource.md` — the design file link.
- **Update** `<real_project_path>/design-system/organisms/<component-name>/component-spec.md` —
  add the component link to the frontmatter `link:` field after build.
- **Update** the task file `## Plan` — tick this organism's build step.

---

## The skill contract

### Inputs
- `design-system/organisms/<component-name>/component-spec.md` — the spec to build from.
- `resource.md` — the design file link.
- All molecule and atom dependencies listed in `dependencies.molecules` and `dependencies.atoms`
  must already be built and their `link:` fields updated with component URLs.

### Input Acceptance Criteria
- `component-spec.md` for this organism exists and its Spec checklist items are all checked or
  explicitly waived with justification.
- The design file link is present in `resource.md`.
- Every dependency listed in `dependencies.molecules` and `dependencies.atoms` has a component
  URL in its own `link:` field. If any is missing, stop and route to the missing dependency's
  build skill first.

### Outputs
- Component for this organism in the target design file, with frames for each breakpoint (if
  Responsive section defines multiple breakpoints).
- `component-spec.md` frontmatter `link:` field updated with the component URL.

### Output Quality Criteria
- Every sub-component is an instance of an existing molecule or atom Component — no raw shapes
  that duplicate a dependency's appearance.
- **Variants:** every row in every variant table in Appearance > Variants has a corresponding
  frame or mode. The style applied matches the spec row exactly — no row omitted.
- **State:** every row in Appearance > State (both lifecycle and interactive) has a corresponding
  representation — variant property value, interactive behavior, or separate frame. For each
  state, sub-components' state propagation matches the spec description. No state is absent.
- **Tokens:** every row in Appearance > Tokens is applied as a Variable reference on the correct
  layer — no hardcoded hex, px, or font value where the spec names a token.
- Responsive frames are present for each breakpoint defined in Responsive > Breakpoints, each
  demonstrating the correct reflow strategy as written in the spec.
- Layout uses auto-layout with spacing Variables matching the Anatomy > Spacing section.
- Accessibility annotations cover: landmark role, heading hierarchy, ARIA attributes, focus
  management, live regions, skip links (if applicable).
- `component-spec.md` frontmatter `link:` field contains a working component URL.

---

## The 3-gate flow

### Gate 1 — Input
Check that `component-spec.md` exists and the Spec checklist is complete. Verify the design file
link is in `resource.md`. For every dependency in `dependencies.molecules` and
`dependencies.atoms`, confirm a component URL exists in that dependency's `link:` field.

If any dependency is not yet built, stop: "The dependency {name} has not been built yet. Let's
build that first." Do not proceed until all dependencies have component URLs.

Check `resource.md` for the `design-tool` field. If missing or empty, stop:
> "No `design-tool` declared in `resource.md`. Add it before running this build skill. Supported values: `figma`."

### Gate 2 — Process
Read `component-spec.md` and extract:
- **Frontmatter > dependencies**: molecule and atom component names and their URLs.
- **Anatomy > Composition table**: each sub-component, its slot name, and which molecule/atom
  it maps to.
- **Anatomy > Layout**: auto-layout direction, alignment, gap, and spacing tokens.
- **Anatomy > Spacing**: internal padding and spacing tokens.
- **Appearance > Variants**: organism-level variant properties and values.
- **Appearance > State**: lifecycle states (loading, empty, error) and interactive states, and
  which sub-components' states are propagated.
- **Appearance > Tokens**: organism-level token references.
- **Responsive > Breakpoints**: each breakpoint name and px threshold.
- **Responsive > Reflow strategy**: what changes at each breakpoint (layout direction, visible
  slots, overflow behavior).
- **Responsive > Mobile-specific patterns**: any mobile-only patterns (bottom sheet, collapsed
  nav, etc.).
- **Content > Empty state, Error state**: the visual representation of these content states.
- **Accessibility > Landmark structure**: the landmark role this organism carries.
- **Accessibility > Heading hierarchy**: heading levels used within the organism.
- **Accessibility > ARIA**: attributes and their conditions.
- **Accessibility > Focus management**: focus trap or return-to-trigger behavior.
- **Accessibility > Live regions**: which state changes trigger live announcements.
- **Accessibility > Skip links**: whether skip links are needed.

Prepare the build brief: component name, sub-component instance map, layout rules, breakpoint
frames, state/variant structure, token references, accessibility annotations.

If any dependency component URL is invalid or a token name does not match a published Variable,
flag it with the user before proceeding.

Determine the adapter from the `design-tool` field in `resource.md`:

| `design-tool` | Adapter |
|---|---|
| `figma` | `figma-ds-organism` |

If `design-tool` is not in the table above, stop:
> "No build adapter exists for `{tool}`. Supported: `figma`. Update `resource.md` or build manually."

Load the adapter and pass the build brief. Instruct the adapter to:
1. Create or update the organism Component in the target design file.
2. Place molecule and atom Component instances for each slot — not raw shapes.
3. Apply auto-layout with spacing Variables per the spec.
4. Set up variant properties and lifecycle/interactive states.
5. Create breakpoint frames demonstrating the reflow strategy for each defined breakpoint.
6. Add accessibility annotations (landmark, headings, ARIA, focus management, live regions,
   skip links).
7. Return the component URL.

### Gate 3 — Output
Run a full appearance verification pass against the spec before confirming completion:

**Variants check:** for each row in every variant table in Appearance > Variants — verify a
corresponding frame or mode exists and its style matches the spec row exactly (token applied, not
hardcoded).

**State check:** for each row in Appearance > State (lifecycle and interactive) — verify a
corresponding representation exists, and confirm sub-component state propagation matches the spec
description for that state.

**Tokens check:** for each row in Appearance > Tokens — verify the token is applied as a Variable
reference on the correct layer, not a hardcoded value.

**Responsive check:** for each breakpoint in Responsive > Breakpoints — verify a frame exists
that demonstrates the reflow strategy written for that breakpoint.

Any row or breakpoint from the spec that has no matching element in the design file is a gap.
Gaps must be resolved before moving on. When all rows and breakpoints are accounted for:
1. Present the component URL and the completed verification pass (rows checked, gaps resolved).
2. Ask the user to confirm.
3. **If confirmed** → update `component-spec.md` frontmatter `link:` field, tick this organism's
   build step in `## Plan`, then hand off to `commit-work`.
4. **If not satisfied** → iterate with the user, then commit.

---

## Handoff
Completed organism builds feed `designer-ds-document` — the final step that indexes the full
design system and produces the README. After any add/update sub-mode, run
`designer-ds-validate` before documenting.
