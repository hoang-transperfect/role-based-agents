---
name: fe-implement
description: >
  Implements each task in sequence following the project's conventions rules file,
  running tests after each task and fixing until green. Invoke after fe-write-tests.
  Works through all task files in order; "done" means all tests pass for all tasks.
---

# fe-implement

Implements each task produced by fe-lib-plan, one after another, following the
project's conventions rules file. After implementing each task, runs the tests and
fixes until they pass before moving to the next task.

## Where things live

Read `real_project_path` from the project's index file
(`<assistant-folder>/projects/<project-slug>.md`). Task files are at
`<real_project_path>/fe-assistant-artifacts/tasks/<task-id>/task.md`.
Source files are written in the project at `real_project_path`.
Conventions rules file: `<real_project_path>/fe-conventions.md`.

## The skill contract

### Inputs
- All task files with their test files (produced by `fe-lib-plan` and `fe-write-tests`).
- The project's conventions rules file (`fe-conventions.md`).

### Input Acceptance Criteria
- All task files have corresponding test files.
- Tests are red (unimplemented).
- The project's conventions rules file exists and is readable. If it doesn't exist,
  suggest a default set of conventions rules to the user and ask them to confirm
  or adjust before starting.

### Outputs
- Implemented source files for all tasks, with all tests passing.
- Each task file's `## Plan` checklist has the implement step ticked.

### Output Quality Criteria
- All tests pass (green) for every task before moving to the next.
- Each rule in the conventions rules file has been applied and verified.
- No implementation goes beyond what the task's ACs require.
- All task implement steps are ticked before handoff.

## The 3-gate flow

### Gate 1 — Input
Check all task files have corresponding test files and tests are red.
Check the conventions rules file exists at `<real_project_path>/fe-conventions.md`.
If it doesn't exist, suggest a default set of conventions rules and ask the user
to confirm or adjust — do not infer or invent conventions without confirmation.

### Gate 2 — Process
For each task in sequence:
1. Read the task file and its test file.
2. Implement the task following the conventions rules file.
3. Run the tests. If any fail, fix and re-run — repeat until all pass.
4. Tick the implement step in the task file's `## Plan`.
5. Confirm with the user before moving to the next task.

### Gate 3 — Output
Check the output against Output Quality Criteria:
- Run the full test suite — all tests must be green.
- Go through each rule in the conventions rules file and verify it was followed
  in the implementation.
- If short, fix (ask the user where intent is unclear — never assume).

When all tasks are implemented and all tests pass:
1. Present a summary of completed tasks and ask the user to confirm.
2. Confirmed → hand off to `commit-work`.
3. Not satisfied → improve with the user, commit, then hand off to `improve-skill`.

## Handoff
- `commit-work` — commits the implementation
