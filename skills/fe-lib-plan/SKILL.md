---
name: fe-lib-plan
description: >
  Reviews BA requirements and Designer specs for issues, conflicts, and gaps, then
  breaks the work into task files — one per UI component or functional step. Invoke
  at the start of component library work, after fe-setup-project (or when opening
  an existing project), and before fe-write-tests. Other skills (fe-write-tests,
  fe-implement) read and act on the task files this skill produces.
---

# fe-lib-plan

Reviews the incoming requirements before any implementation starts, surfaces issues
early, then breaks the work into concrete, trackable task files. Each task file
becomes the unit of work for the downstream skills.

## Where things live

Read `real_project_path` from the project's index file
(`<assistant-folder>/projects/<project-slug>.md`). Task files are created at
`<real_project_path>/fe-assistant-artifacts/tasks/<task-id>/task.md`.

## The skill contract

### Inputs
- BA requirements document
- Designer specs (design requirements, mockups, or references)

### Input Acceptance Criteria
- BA requirements are available and reference a specific feature or scope.
- Designer specs are available for the same scope.

### Outputs
- A set of task files, one per UI component or functional step, each containing:
  - Task description
  - Acceptance criteria (ACs)
  - Breakdown strategy used (UI component or functional)
  - `## Plan` section with step checklist (for `fe-write-tests` and `fe-implement` to tick)

### Output Quality Criteria
- All issues, conflicts, and gaps found during review are surfaced to the user and
  resolved (or explicitly flagged as open) before task files are written.
- Every task file maps to exactly one component or one functional step — no bundling.
- ACs are concrete and testable — not vague.
- The breakdown strategy is stated and consistent across all task files.
- Task files are ready to hand off to `fe-write-tests`.

## The 3-gate flow

### Gate 1 — Input
Check that both BA requirements and Designer specs are available for the scope.
If either is missing, ask the user before proceeding.

### Gate 2 — Process
**Step 1 — Review the inputs.**
Read BA requirements and Designer specs together. Look for:
- **Issues** — unclear, contradictory, or untestable requirements
- **Conflicts** — mismatches between BA and design (e.g. a flow in BA that the design
  doesn't account for, or a UI state in design with no BA requirement behind it)
- **Gaps** — missing ACs, undefined edge cases, unstated error states

Surface all findings to the user and resolve each one before moving on.
Never assume a resolution — ask.

**Step 2 — Choose the breakdown strategy with the user.**
- **By UI component** — when the work is primarily building or updating UI components
- **By functional step** — when the work is a feature flow or behaviour

If the scope mixes both, discuss with the user how to split.

**Step 3 — Break into tasks and create task files.**
For each component or functional step, create a task file with description, ACs,
and a `## Plan` checklist (steps: write tests → implement → commit).

### Gate 3 — Output
Check the output against Output Quality Criteria. If short, improve (ask the user —
never assume). When met:
1. Present the list of task files and ask the user to confirm.
2. Confirmed → hand off to `commit-work`, then proceed to `fe-write-tests`.
3. Not satisfied → improve with the user, commit, then hand off to `improve-skill`.

## Handoff
- `commit-work` — commits the task files
- `fe-write-tests` — next step: write tests for each task
