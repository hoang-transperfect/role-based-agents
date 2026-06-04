---
name: create-project
description: >
  Creates a new project workspace under the fixed projects root, with a standard folder
  structure. Expects inputs to be passed in directly — typically from gather-needs.
  Do NOT re-ask the user for information already collected. Trigger when gather-needs has
  detected "create new project" intent and confirmed inputs with the user.
---

# create-project

Creates a structured project folder under the projects root. All inputs are assumed to already
be confirmed by the user (via gather-needs).

## Projects root

All projects live under a single fixed root. There is **no per-project working directory**.

```bash
PROJECTS_ROOT="$HOME/projects"   # change here if your root differs
```

## Inputs (provided by gather-needs)

- `project-name` — slugified folder name (lowercase, spaces → hyphens)
- `resources` — list of `{ url, description }` entries (may be empty)

---

## Step 1 — Create the Folder Structure

```bash
PROJECT_DIR="$PROJECTS_ROOT/<project-slug>"
mkdir -p "$PROJECT_DIR/raw-conversation"
mkdir -p "$PROJECT_DIR/in-progress-tasks"
```

---

## Step 2 — Create resource.md

Path: `$PROJECT_DIR/resource.md`

```markdown
# <Project Name> – Resources

A curated list of resources for this project. Each entry has a link and a description
so that agents can detect which resource is relevant and retrieve it when needed.

## Resources

- **[Resource Title](https://url)** — <one-sentence description of what this resource contains and when to use it>
```

Populate from the confirmed resources list. If empty, leave one placeholder line and a comment:
```markdown
<!-- Add resources as: **[Title](url)** — description of what it contains and when to use it -->
```

---

## Step 3 — Confirm Success

Tell the user:
- Full path to the new project folder (under the projects root)
- Brief explanation of each item:
  - `resource.md` — curated resource list; each entry has a link + description so agents know what to retrieve and when
  - `raw-conversation/` — one `.md` log file per chat session (created by `create-task`)
  - `in-progress-tasks/` — one `.md` file per task (created by `create-task`)
  
