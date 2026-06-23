---
name: fe-write-tests
description: >
  Writes unit and component tests for a single task file based on its acceptance
  criteria — one task at a time, confirmed before moving to the next. Invoke after
  fe-lib-plan has created the task files and before fe-implement. Tests are expected
  to be red at this stage; "done" means all cases in the task are covered, not that
  tests pass.
---

# fe-write-tests

Turns a task file's acceptance criteria into a full test suite before any
implementation begins. Each task is handled one at a time and confirmed before
proceeding to the next.

## Where things live

Read `real_project_path` from the project's index file
(`<assistant-folder>/projects/<project-slug>.md`). Task files are at
`<real_project_path>/fe-assistant-artifacts/tasks/<task-id>/task.md`.
Tests are written in the project's test file co-located with or mirroring the
source file they cover.

## The skill contract

### Inputs
- A task file with description and acceptance criteria (produced by `fe-lib-plan`).

### Input Acceptance Criteria
- The task file exists and has testable ACs.
- The project environment is set up (test runner is configured).

### Outputs
- A test file for the task, containing unit and component tests covering all cases
  defined in the task's ACs.

### Output Quality Criteria
- Every AC in the task file has at least one corresponding test case.
- Edge cases, error states, and boundary conditions implied by the ACs are covered.
- Tests are atomic — each test covers one specific case.
- Tests are red (failing) at this stage — no implementation has been written yet.
- The task file's `## Plan` checklist has the write-tests step ticked.

## The 3-gate flow

### Gate 1 — Input
Check the task file exists and has testable ACs.
Check the test runner is configured. If either fails, resolve before proceeding.

### Gate 2 — Process
For the current task:
1. Read the task file and list all ACs and implied edge cases.
2. Propose the test cases to the user — one per AC plus edge cases.
3. Confirm the test case list with the user before writing any code.
4. Write the tests.

Work one task at a time. After the tests for a task are written, confirm with the
user before moving to the next task.

### Gate 3 — Output
Check the output against Output Quality Criteria. If short, improve (ask the user —
never assume). When met:
1. Present the test file and ask the user to confirm.
2. Confirmed → tick the write-tests step in the task file's `## Plan`, hand off to
   `commit-work`, then proceed to `fe-implement` for this task.
3. Not satisfied → improve with the user, commit, then hand off to `improve-skill`.

## Handoff
- `commit-work` — commits the test file
- `fe-implement` — next step: implement the task so the tests pass
