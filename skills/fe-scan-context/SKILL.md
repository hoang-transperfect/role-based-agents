---
name: fe-scan-context
description: >
  Discovers existing code, components, conventions, and artifacts relevant to a frontend
  task before any implementation begins, so work builds on what already exists instead of
  duplicating or contradicting it. Invoke at the start of any FE task, before fe-lib-plan
  or fe-implement, and any time the user asks "what do we already have?", "is there an
  existing component for this?", or is about to start building something new. Scans the
  real project folder for existing components, conventions rules file, test patterns, and
  prior task artifacts, then records a related-context summary in the task folder.
---

# fe-scan-context

The most expensive FE mistake is building a component that already exists, or implementing
in a style that contradicts the project's established conventions. This skill front-loads
discovery: it finds what's already in the codebase so planning and implementation start
from reality, not a blank slate.

It records a **Related Context** summary: a short inventory of relevant existing material,
what each piece covers, and the gaps it does not cover. `fe-lib-plan` reads this to avoid
duplicating existing components, and `fe-implement` reads it to follow established patterns.

## Where things live

- **Search** the real project folder: read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`) and scan there.
- **Write** the result as a deliverable artifact at
  `<real_project_path>/fe-assistant-artifacts/tasks/<task-id>/related-context.md`.

## The skill contract

### Inputs
- The task file describing what needs to be built (produced by `create-task`).
- The real project folder at `real_project_path`.

### Input Acceptance Criteria
- The task file exists with a description of the work.
- `real_project_path` is readable.

### Outputs
- `related-context.md` in the task folder, containing:
  - Existing components relevant to the task
  - Conventions rules file location (if found)
  - Existing test patterns relevant to the task
  - Gaps — what is not yet covered by existing artifacts

### Output Quality Criteria
- Every finding names the file path so it can be read directly.
- Gaps are explicitly listed — a clean gap list is as valuable as findings.
- The summary is concise enough to read in under two minutes.

## The 3-gate flow

### Gate 1 — Input
Confirm the task file exists and `real_project_path` is readable. If not, ask the user.

### Gate 2 — Process
Scan the project for:
- **Existing components** — anything matching the task's scope (name, function, or UI pattern)
- **Conventions rules file** — `fe-conventions.md` or equivalent
- **Test patterns** — how tests are structured for similar components or features
- **Prior task artifacts** — any related `related-context.md` from past tasks

Summarise findings as a short inventory. List gaps explicitly.

### Gate 3 — Output
Check the output against Output Quality Criteria. When met:
1. Present the summary and ask the user to confirm.
2. Confirmed → write `related-context.md`, hand off to `commit-work`, then proceed to
   `fe-lib-plan`.
3. Not satisfied → improve with the user, commit, then hand off to `improve-skill`.

## Handoff
- `commit-work` — commits the related-context artifact
- `fe-lib-plan` — next step: plan the work using this context
