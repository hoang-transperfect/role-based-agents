---
name: fe-setup-project
description: >
  Sets up a new frontend project from scratch — repo, framework, dependencies,
  linting, testing tools, and folder structure — so the environment is ready before
  task-specific work begins. Invoke only when no existing project is found at the
  target path; check for that before calling this skill.
---

# fe-setup-project

Sets up everything a new frontend project needs before task-specific work can begin.
The output is a generic, ready environment — no task-specific configuration.

## Where things live

Read `real_project_path` from the project's index file
(`<assistant-folder>/projects/<project-slug>.md`). The new project is created at
`real_project_path`.

## The skill contract

### Inputs
- Project name and any known constraints (framework preferences, team conventions)
  from the user.

### Input Acceptance Criteria
- No existing project is found at `real_project_path`. The assistant must verify
  this before invoking the skill. If a project exists, do not invoke.
- Project name is known.

### Outputs
- A new project at `real_project_path` with: git repo initialised, framework
  installed and configured, dependencies installed, linting and testing tools
  configured, and folder structure in place.

### Output Quality Criteria
- The project builds, lints without errors, and the test runner executes
  successfully on the empty setup.
- Nothing task-specific is configured — generic scaffolding only.
- The environment is ready to hand off to `fe-plan`.
- Use the latest stable version of each package, especially framework packages.

## The 3-gate flow

### Gate 1 — Input
Verify no project exists at `real_project_path`. If one exists, stop and notify
the user — do not proceed.
Confirm the project name is known. If not, ask.

### Gate 2 — Process
Discuss and confirm each decision with the user before acting:
- **Framework** — e.g. React, Vue, Next.js
- **Language** — TypeScript or JavaScript
- **Package manager** — npm, yarn, or pnpm
- **Linting** — ESLint config, Prettier
- **Testing** — unit runner (e.g. Vitest, Jest), component testing (e.g. Testing Library)
- **Folder structure** — agree top-level structure before scaffolding

Scaffold step by step, confirming each major step with the user.

### Gate 3 — Output
Verify the Output Quality Criteria are met:
- Project builds without errors
- Linter passes
- Test runner executes on the empty setup

When met:
1. Present a setup summary and ask the user to confirm.
2. Confirmed → hand off to `commit-work`, then proceed to `fe-plan`.
3. Not satisfied → improve with the user, commit, then hand off to `improve-skill`.

## Handoff
- `commit-work` — commits the new project setup
- `fe-plan` — next step after setup is done
