---
name: designer-review
description: >
  Validates that all design specs for a task are complete, consistent, and match the business
  spec — every user story in scope has a story-spec.md with IA section, wireframe section, and
  AC alignment; every affected artifact (organism/template/page) listed in the story spec has a
  current, complete spec file; every BA acceptance criterion is covered in the UX flows; every
  organism referenced is named from the DS or product-organisms; no DS gaps are left unresolved;
  and a test plan exists covering all stories in scope (for from-scratch and develop modes). Invoke
  as the final step of a PS task, after designer-ui, designer-organism (if any),
  designer-template (if any), designer-page, and designer-test have run for all stories in scope.
  If gaps are found, routes back to the responsible skill. When all specs pass, confirms with
  the user and finalizes for Dev.
---

# designer-review

A design spec that's almost right is still wrong — a missing error state, an undefined organism,
an unconfirmed wireframe, or a missing test plan becomes a developer's undocumented assumption.
This skill runs a structured check across all design artifacts produced in this task before they
are handed to Dev.

It does not redesign anything. It checks completeness and consistency, surfaces any gaps, routes
them to the right skill to fix, and finalizes only when everything passes.

## Where things live

- **Read** all `story-spec.md` files for the stories in scope (paths from `traceability.md`).
- **Read** the `## Plan` to confirm which stories and steps were in scope.
- **Read** `design-spec/product-organisms/` — all product-specific organism specs referenced.
- **Read** `design-spec/templates/` — all template specs referenced.
- **Read** `design-spec/pages/` — all page specs referenced.
- **Read** `designer-artifacts/resource.md` — the design system source.
- **Read** `ba-requirement/` — the BA user stories for acceptance criteria coverage.
- **Read** `designer-artifacts/tasks/<task-id>/test-plan.md` — the usability test plan.
- **Update** `design-spec/traceability.md` to set each story's status to `reviewed`.
- **No new specs created** — this skill only validates and updates existing outputs.

---

## The skill contract

### Inputs
- All `story-spec.md` files for stories in scope.
- The `## Plan` (checklist showing which steps ran and which stories are in scope).
- Product-specific organism specs (if Step 3a was in scope).
- Template specs (if Step 3b was in scope).
- Page specs (Step 3c — should exist for every page listed in any story spec).
- The BA user stories from `ba-requirement/` (for acceptance criteria coverage).
- `design-spec/traceability.md`, `designer-artifacts/resource.md`.
- `designer-artifacts/tasks/<task-id>/test-plan.md` (Step 4 — required for from-scratch and
  develop modes; skipped in maintain mode unless the change is structural or high-risk).

### Input Acceptance Criteria
- Steps 2, 3c (and 3a/3b if in scope) are ticked in the `## Plan` for all stories. If any
  required step is unticked, surface the incomplete state and ask the user before reviewing.
- All user stories listed in the `## Plan` have a `story-spec.md` file.

### Outputs
- Updated `design-spec/traceability.md` (status: reviewed for each passing story).
- A review summary presented to the user (not written to a file — it is a gate, not an artifact).

### Output Quality Criteria
The review passes when all of the following hold for every story in scope:

1. **Story spec exists** — a `story-spec.md` exists for every US-… in the plan.

2. **IA section is present** — the story spec includes an `## IA & Navigation` section. Each
   field (sitemap change, navigation change, entry points) is explicitly stated — not blank.

3. **Wireframe section is present and valid** — the story spec includes a `## Wireframe` section.
   If sub-mode is from-scratch or develop: at least one screen must be specced with all required
   fields (Zones, Navigation placement, Primary content zone, Key elements, Responsive note).
   If sub-mode is maintain and non-structural: section must explicitly state "Skipped — maintain
   mode, non-structural" — a blank or missing section is a gap.

4. **AC coverage** — every acceptance criterion in the BA story appears in the AC alignment
   table and maps to at least one UX flow case.

5. **Case coverage** — every error state, empty state, and loading state is present in the
   UX flows. No cases implied but missing.

6. **Organism resolution** — every organism listed in any story spec or page spec either:
   - Exists in the DS (named correctly), or
   - Has a spec in `design-spec/product-organisms/`.
   Unresolved organisms are gaps → `designer-organism`.

7. **Template resolution** — every template listed in any story spec or page spec has a spec
   in `design-spec/templates/`. Unresolved templates are gaps → `designer-template`.

8. **Page resolution** — every page listed in any story spec has a spec in `design-spec/pages/`.
   Unresolved pages are gaps → `designer-page`.

9. **DS gaps are flagged, not hidden** — any ⚠ DS gaps in any spec are acknowledged by the
   user (either resolved or explicitly deferred with a reason).

10. **Test plan exists and covers all stories** — `test-plan.md` exists and includes at least
    one scenario for every happy-path UX flow across all stories in scope. Required for
    from-scratch and develop modes. In maintain mode: required only when the change is
    structural or high-risk; otherwise mark as `~~skipped~~ (maintain mode — non-structural)`.

11. **Traceability** — `traceability.md` has a row for every story with the correct spec path
    and the BA story link.

---

## The 3-gate flow

### Gate 1 — Input
Check that all required step prerequisites are met. If any step is unticked for a story in
scope, surface the gap and ask the user whether to run the missing step or proceed with a
known gap.

### Gate 2 — Process
Run the checklist above across all design artifacts. For each failing check, record:
- Which story or spec is affected
- Which check failed
- What needs to be fixed

Route findings to the responsible skill:
- Missing or incomplete IA section → `designer-ui`
- Missing or incomplete wireframe section → `designer-ui`
- UX flow gaps or missing story spec → `designer-ui`
- Missing organism spec → `designer-organism`
- Missing template spec → `designer-template`
- Missing page spec → `designer-page`
- Missing or incomplete test plan → `designer-test`

For DS gaps (⚠): present each one to the user and confirm whether to resolve now (hand off to
`designer-ds-atom`, `designer-ds-molecule`, or `designer-ds-organism` in DS mode depending on
the missing component's atomic level) or defer with an explicit reason. Do not silently approve
a spec with open DS gaps.

Present all findings to the designer. For each, confirm: fix now or mark as a known exception
with a reason.

If all checks pass (or all exceptions are acknowledged), proceed to Gate 3.

### Gate 3 — Output
When all checks pass:
1. Present the review summary to the user and ask for final confirmation that the design specs
   are ready for Dev.
2. **If confirmed** → update `traceability.md` (status: reviewed for each story), tick Step 5
   in `## Plan`, update **Next step: complete**, then hand off to `commit-work`.
3. **If the user wants changes** → route to the responsible skill, then re-run this review
   after the fix. Once confirmed, commit, then hand off to `improve-skill`.

---

## Completing the design task

When Step 5 is the last applicable step and it has passed:
1. Set `status: completed` in the task file's frontmatter.
2. Set the conversation log frontmatter `status: completed`.
3. Remove the task's line from the project index file.
4. Hand off to `commit-work`.

## Handoff
The reviewed design artifacts — story specs per story, organism specs, template specs, page specs,
and test plan — are the designer's deliverable to the Dev team. `traceability.md` is the index
linking each story spec back to the BA business requirement.
