---
name: create-project
description: >
  Registers a new project: a project index file in the assistant folder plus the assistant's
  artifacts folder inside the real project. Expects inputs to be passed in directly — typically
  from gather-needs. Do NOT re-ask the user for information already collected. Trigger when
  gather-needs has detected "create new project" intent and confirmed inputs with the user.
---

# create-project

Registers a new project with the assistant. All inputs are assumed to already be confirmed by
the user (via gather-needs). Two things get created:

1. A **project index file** in the assistant folder — the assistant's only record of the
   project: the pointer to the real project plus the searchable list of in-progress tasks.
2. The **assistant artifacts folder** inside the real project — where everything the assistant
   produces for this project lives (resources, task files, conversation logs, working artifacts).

(The real project also gains the assistant's **output of work** — the deliverable other teams
consume — but not from this skill: the role's own skills create it where the role dictates,
e.g. BA → `ba-requirement/`, design → `design-requirement/`, dev → the source code itself.)

## Projects root

All project index files live under a single fixed root. There is **no per-project folder** in
the assistant workspace — one index file per project.

```bash
PROJECTS_ROOT="<assistant-folder>/projects"   # assistant-folder is the directory containing this assistant's definition file (e.g. assistants/<assistant-name>)
```

## Inputs (provided by gather-needs)

- `project-name` — slugified name (lowercase, spaces → hyphens)
- `real-project-path` — absolute path to the **real project folder**: where the actual work and
  deliverables live (the codebase, project docs, existing documentation). Everything the
  assistant produces for this project is stored under here too, inside
  `<assistant-name>-artifacts/`. Ask for it if not provided.
- `resources` — list of `{ url, description }` entries (may be empty)

---

## Step 1 — Create the Project Index File

Path: `$PROJECTS_ROOT/<project-slug>.md`

The frontmatter is the **single source of truth** for where the real project lives — skills read
`real_project_path` from here rather than assuming a location. The body lists the in-progress
tasks so `gather-needs` can search them without leaving the assistant folder.

```markdown
---
project_name: <Project Name>
real_project_path: <absolute path to the real project folder>
---

# <Project Name>

All project content (resources, task files, conversation logs, artifacts) lives in the real
project under `<assistant-name>-artifacts/`. This file only points there and lists what is
in progress.

## In-Progress Tasks

<!-- One line per task, added by create-task and removed on completion: `- <task-id> — <description>` -->
```

---

## Step 2 — Create the Artifacts Folder in the Real Project

The folder is named after the assistant, so several assistants can share one real project
without colliding:

```bash
ARTIFACTS_DIR="<real-project-path>/<assistant-name>-artifacts"   # named after this assistant
mkdir -p "$ARTIFACTS_DIR/tasks"
```

- `tasks/` — one folder per task (created by `create-task`), holding the task file
  (`task.md`), its conversation log (`conversation.md`), and the task's working artifacts.

---

## Step 3 — Create resource.md

Path: `$ARTIFACTS_DIR/resource.md`

```markdown
---
project_name: <Project Name>
---

# <Project Name> – Resources

A curated list of resources for this project. Each entry has a link and a description
so that agents can detect which resource is relevant and retrieve it when needed.

## Resources

- **[Resource Title](https://url)** — <one-sentence description of what this resource contains and when to use it>

## Notes

Project-specific preferences and decisions that should guide future work on this project. Any
skill may append here when it learns something local to this project (for example, `improve-skill`
records preferences that are project-specific rather than a skill gap). Keep entries short and
dated so future work can honour them.

<!-- - <date>: <preference or decision, stated as guidance for future work> -->
```

Populate from the confirmed resources list. If empty, leave one placeholder line and a comment:
```markdown
<!-- Add resources as: **[Title](url)** — description of what it contains and when to use it -->
```

---

## Step 4 — Confirm Success

Tell the user:
- Path of the project index file (in the assistant folder) and the recorded real project path
- Path of the artifacts folder created inside the real project
- Brief explanation of each item:
  - the index file — the pointer to the real project plus the in-progress task list that
    `gather-needs` searches
  - `<assistant-name>-artifacts/resource.md` — curated resource list + project notes; each
    resource entry has a link + description so agents know what to retrieve and when
  - `<assistant-name>-artifacts/tasks/` — one folder per task: `task.md`, `conversation.md`,
    and the task's working artifacts. A finished task keeps its folder (the audit record);
    completion is recorded by `status: completed` in `task.md` and by removing the task's
    line from the index file
