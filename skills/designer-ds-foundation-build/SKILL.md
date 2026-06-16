---
name: designer-ds-foundation-build
description: >
  Builds the foundation layer of the design system into a design file — design tokens published
  as Variables (color, spacing, radius, elevation) and Text Styles (typography). Reads the token
  spec files from design-system/foundations/ and delegates the implementation to the configured
  adapter (default: figma:figma-generate-library). Run after designer-ds-foundation has produced
  all foundation spec files, and before any component build skill. Foundation Variables must exist
  in the design file before atoms, molecules, or organisms can reference them by token name.
---

# designer-ds-foundation-build

Foundation build translates token spec files into live design tool primitives: Variables (for
color, spacing, number, and boolean values) and Styles (for typography and effects). Every
component build skill that follows depends on these Variables being present — building components
before foundations produces hardcoded values instead of token references.

This skill reads the spec, prepares the build brief, and delegates to the design tool adapter
(`figma:figma-generate-library` by default). The adapter pattern keeps this skill decoupled from
the tool: a different adapter can be substituted in the future without changing the spec or this
skill.

## Where things live

- **Read** foundation spec files at `<real_project_path>/design-system/foundations/`:
  `principles.md`, `color.md`, `typography.md`, `spacing.md`, and any other token category files.
- **Read** `<real_project_path>/designer-artifacts/resource.md` — the design file link is the
  build target.
- **Update** `<real_project_path>/designer-artifacts/resource.md` — add or confirm the design
  file link after build.
- **Update** the task file `## Plan` — tick the foundation-build step.

---

## The skill contract

### Inputs
- Foundation spec files in `design-system/foundations/` — all in-scope categories must exist.
- A design file target — either an existing link in `resource.md` or the user provides one.
  If no file exists, ask the user whether to create a new one.

### Input Acceptance Criteria
- `design-system/foundations/principles.md` exists.
- At minimum one token category file (`color.md`, `typography.md`, or `spacing.md`) exists.
- A design file target is known, or the user confirms a new file should be created.

### Outputs
- Variables and Styles published in the target design file.
- `resource.md` updated with the design file link (if not already present).

### Output Quality Criteria
- All color tokens from `color.md` are published as Color Variables, grouped by semantic alias
  (e.g. `color/action/primary`).
- All spacing tokens from `spacing.md` are published as Number Variables.
- All typography specs from `typography.md` are published as Text Styles with the correct font
  family, size, weight, line-height, and letter-spacing.
- All elevation/shadow tokens are published as Effect Styles.
- Variable names in the design file match token names in the spec exactly — no renaming or
  reformatting.
- `resource.md` contains a working design file link.

---

## The 3-gate flow

### Gate 1 — Input
Verify all in-scope foundation spec files exist. Check `resource.md` for a design file link.
If no link is present, ask the user:
> "Which design file should receive the foundation tokens? Paste the file URL, or confirm you
> want a new file created."

Do not proceed without a confirmed target.

### Gate 2 — Process
Read each in-scope foundation spec file and extract:
- **Color:** token names, values, and semantic grouping hierarchy (from `color.md`).
- **Typography:** scale entries — name, font family, weight, size, line-height, letter-spacing
  (from `typography.md`).
- **Spacing:** token names and px values (from `spacing.md`).
- **Other categories:** token name → value pairs.

Prepare the build brief: token names, values, grouping hierarchy, Variable collection names.

If any token name is ambiguous or a value is missing from the spec, flag it with the user before
proceeding — do not invent values.

Invoke the adapter:
> Load `figma:figma-generate-library` and pass the build brief. Instruct the adapter to:
> 1. Create or update Variables in the target file, grouped by token category.
> 2. Create or update Text Styles for all typography entries.
> 3. Create or update Effect Styles for elevation/shadow tokens.
> 4. Return the design file URL and confirm which Variables/Styles were created.

### Gate 3 — Output
Verify the Output Quality Criteria — confirm that Variable names in the design file match spec
token names exactly. When the bar is met:
1. Present the design file link and a summary of what was created.
2. Ask the user to confirm.
3. **If confirmed** → update `resource.md` with the design file link (if not already there),
   tick the foundation-build step in `## Plan`, then hand off to `commit-work`.
4. **If not satisfied** → iterate with the user, then commit.

---

## Handoff
Foundation build feeds `designer-ds-atom-build` — atom components reference foundation Variables
by token name in the design file. No component build skill may run before this one.
