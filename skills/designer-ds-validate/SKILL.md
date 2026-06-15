---
name: designer-ds-validate
description: >
  Validates downstream impact after a design system component is added or updated — checks
  which molecules, organisms, templates, or pages reference the changed component, identifies
  any breaking changes in dependent specs, and confirms the atomic hierarchy is intact. Invoke
  after designer-ds-atom, designer-ds-molecule, or designer-ds-organism when working in
  add-component or update sub-mode. Not needed in from-scratch mode (the full pipeline builds
  components in dependency order, so breaking changes cannot occur). Produces a validation
  report and routes any broken specs back to the responsible skill.
---

# designer-ds-validate

Changing one component in an atomic design system can break the components built on top of it.
An updated atom may invalidate a molecule's anatomy. A renamed token may silently orphan a dozen
component specs. This skill catches those ripples before they reach the developer.

It does not redesign anything. It reads the updated component and every spec that references it,
identifies discrepancies, and either confirms no action is needed or routes specific specs back
to their responsible skill to be corrected.

## Where things live

- **Read** the updated or newly created component spec (atom / molecule / organism) that
  triggered this validation.
- **Read** all component specs at dependent atomic levels:
  - Updated **atom** → read all molecule specs that list this atom in their anatomy.
  - Updated **molecule** → read all organism specs that list this molecule in their anatomy.
  - Updated **organism** → read all product organism specs, template specs, and page specs
    that reference this organism.
- **Read** `designer-artifacts/tasks/<task-id>/ds-audit.md` (scope and component list).
- **Read** `design-system/README.md` (index of all DS components).
- **No new component specs created** — this skill only validates and routes fixes.

---

## The skill contract

### Inputs
- The updated or new component spec (path and content).
- All dependent component specs (read from `design-system/` and `design-spec/` trees).
- `ds-audit.md` and `design-system/README.md` for the full component inventory.

### Input Acceptance Criteria
- The triggering component spec is confirmed (committed from its responsible ds skill).
- The component's atomic level is known — determines which dependent levels to check.

### Outputs
- A validation report presented to the user (not written to a file unless breaking changes
  are found that require routing).
- If breaking changes are found: a written
  `<real_project_path>/designer-artifacts/tasks/<task-id>/ds-validation.md` listing each
  affected spec and the required fix.

### Output Quality Criteria
- **Every dependent spec is checked** — no component at a dependent level is skipped. If the
  README index is incomplete, flag the gap rather than silently skipping.
- **Breaking changes are explicit**: for each affected spec, the validation names exactly what
  changed (token renamed, variant removed, anatomy item renamed) and what the dependent spec
  must update.
- **Non-breaking changes are confirmed**: if a change is additive (new variant, new token) and
  downstream specs do not reference the added item, this is confirmed as safe — not left ambiguous.
- **Routing is specific**: each broken spec is routed to the correct skill
  (`designer-ds-atom`, `designer-ds-molecule`, or `designer-ds-organism`), not flagged
  generically.

---

## The 3-gate flow

### Gate 1 — Input
Confirm the triggering component spec is finalized. Identify its atomic level and derive the
dependent levels to check:
- Atom changed → check: molecules, organisms (transitively), DS organisms
- Molecule changed → check: organisms, DS organisms
- Organism changed → check: product organisms, templates, pages (in design-spec/)

If the component inventory (README.md) is missing or incomplete, note the gap before proceeding.

### Gate 2 — Process

**Step 1 — Build the dependency map**
From `design-system/README.md` and `ds-audit.md`, list every component at dependent levels.
Cross-reference each against the updated component's spec to determine: does it reference
the changed component?

**Step 2 — Check each dependent spec for breaking changes**

For each dependent component that references the updated component, check:

| Change type | What to look for |
|---|---|
| Token renamed | Any token reference in dependent specs using the old name |
| Variant removed | Dependent specs using a variant that no longer exists |
| Variant renamed | Dependent specs using the old variant name |
| Anatomy item renamed | Dependent specs referencing the old slot/part name |
| Anatomy item removed | Dependent specs depending on a slot that no longer exists |
| New required property | Dependent specs that don't supply the now-required property |
| Behaviour changed | Dependent specs whose documented behaviour relies on the old behaviour |

Additive changes (new tokens, new optional variants) are safe — confirm and move on.

**Step 3 — Compile findings**

If no breaking changes: confirm validation passed.

If breaking changes found, draft `ds-validation.md`:

```markdown
# DS Validation Report — <component name> (<atom / molecule / organism>)

_Updated component: [<ComponentName>](path-to-spec)_
_Validation date: <date>_

## Result: BREAKING CHANGES FOUND / NO BREAKING CHANGES

## Breaking changes
### <DependentComponentName> — <atomic level>
- **Spec:** [link](path)
- **What changed:** <token renamed from X to Y / variant "outlined" removed / …>
- **What must update:** <the anatomy table references token X — update to Y>
- **Route to:** `designer-ds-<atom / molecule / organism>`

## Confirmed safe (additive changes)
- <Change description> — no dependent specs reference this; no action needed.

## Dependent specs checked
| Component | Level | References updated component | Breaking change |
|---|---|---|---|
| <ButtonGroup> | molecule | yes | no |
| <FormField> | molecule | yes | yes — see above |
| <NavBar> | organism | no | — |
```

### Gate 3 — Output
When the report is complete:

**If no breaking changes:**
1. Confirm to the user: "Validation passed — no downstream specs affected."
2. Tick the validate step in `## Plan`, update **Next step** to `designer-ds-document`, then
   hand off to `commit-work`.

**If breaking changes found:**
1. Present `ds-validation.md` to the user.
2. Write the file.
3. For each broken spec, ask the user whether to fix now (hand off to the responsible ds skill)
   or defer with an explicit reason noted in the validation report.
4. Once all breaking changes are resolved or explicitly deferred, tick the validate step in
   `## Plan`, then hand off to `commit-work`.

---

## Handoff
After validation passes (or all exceptions are acknowledged), the pipeline continues to
`designer-ds-document` to update the README index. If breaking changes are routed to
`designer-ds-atom`, `designer-ds-molecule`, or `designer-ds-organism`, re-run this skill
after those fixes are committed.
