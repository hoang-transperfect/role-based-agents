---
name: gather-needs
description: >
  Runs automatically at the start of every conversation to detect the user's intent
  and route to the right skill. Handles three scenarios: creating a new project,
  creating a new task in an existing project, or resuming an existing task.
  Always trigger this skill at the beginning of a new conversation before doing anything else.
  Do not re-run if context has already been gathered earlier in the same conversation.
---

# gather-needs

Entry point for every conversation. Detects what the user wants to do, confirms, then
hands off to the appropriate skill with all needed information — no re-asking required downstream.

## Projects root

The assistant folder keeps one **index file per project** under a single fixed root — frontmatter
holds `real_project_path`; the body lists the in-progress tasks. All other project content (task
files, conversation logs, resources, artifacts) lives in the real project under
`<assistant-name>-artifacts/`.

```bash
PROJECTS_ROOT="<assistant-folder>/projects"   # assistant-folder is the directory containing this assistant's definition file (e.g. assistants/<assistant-name>)
# project index file: $PROJECTS_ROOT/<project-slug>.md
```

---

## Step 0 — Before-work guard (start of session)

Because this skill runs once at the start of every conversation, it is the right place to make
sure work begins on a clean slate. Invoke the **`commit-work` before-work guard** (Job 1) against
the **real project repo** (`real_project_path` from the project index file) — where deliverables
land — so that if its tree is dirty, the user stashes or commits before anything proceeds.

Timing: the guard needs the project's `real_project_path`, so run it as soon as the target project
is known. For **resume / new-task** intents the project is identified during intent detection
below, so guard right after. For a **new-project** intent the path is supplied during intake
(Step 2) and recorded by `create-project`, so guard once it exists. This is the *only* place the
guard runs — individual skills do **not** re-check the tree in their input gates; they assume the
session started clean.

---

## Step 1 — Scan the Conversation for Intent

Read the user's opening message(s) and infer which of the three scenarios applies:

| Intent | Signals |
|---|---|
| **A. Create a new project** | "new project", "start a project", "set up a project", no existing project mentioned |
| **B. Create a new task** | existing project mentioned or known, "new task", "I want to work on X", specific goal described |
| **C. Resume an existing task** | task ID or task name mentioned, "continue", "pick up where we left off", "work on [task]" |
| **D. Out of scope** | request outside this assistant's domain — anything the scope rule in the assistant's definition file excludes |

**If Intent D (out of scope):** do **not** continue to Step 2. Refuse per the scope rule in this
assistant's definition file — politely explain what this assistant focuses on and redirect the
user back to that domain. Only A/B/C proceed through the rest of this skill.

### Check existing tasks before deciding between B and C

Whenever the user describes wanting to *work on something* (i.e. it's not clearly a "new project"
request), list the existing in-progress tasks and check whether one already matches the need.
This prevents creating a duplicate task when the user actually wants to resume an existing one.

Run the following to list all in-progress tasks across projects — it reads the
`## In-Progress Tasks` section of every project index file:

```bash
for f in "$PROJECTS_ROOT"/*.md; do
  [[ -f "$f" ]] || continue
  project=$(basename "$f" .md)
  sed -n '/^## In-Progress Tasks/,$p' "$f" | grep -E '^- ' | sed "s/^- /[$project] /"
done
```

(If the specific project is already known, run it on `"$PROJECTS_ROOT/<slug>.md"` only.)

This lists in-progress tasks only. **Completed tasks** are removed from the index when they
close (their task files keep `status: completed` in the real project), so they intentionally
don't appear here and won't be offered for resume.

Each line is in the format `[project] id — description`. Compare the user's
stated need against these descriptions:
- **Strong match found** → treat as Intent C (resume). Confirm with the user: "Looks like this
  matches your existing task `<id>` — want to continue that one?"
- **No good match** → treat as Intent B (create new task).

If the intent is still ambiguous, ask the user one short question to clarify.

---

## Step 2 — Collect Missing Info (minimal, in one message)

Only ask for what is strictly needed for the detected intent. Pre-fill anything already
inferrable from context and present it as the default.

### If Intent A — New Project
Needed by `create-project`:
- Project name *(infer from context if possible)*
- Real project path — absolute path to the **real project folder** where the actual work,
  deliverables, and existing docs live *(ask if not stated; it is recorded in the project index
  file, and everything the assistant produces is written under it in
  `<assistant-name>-artifacts/`)*
- Resources: a list of links + descriptions *(infer any URLs/docs mentioned)*

(The project index file is created under `$PROJECTS_ROOT` automatically; the real project folder
is a separate location the user supplies.)

### If Intent B — New Task
Needed by `create-task`:
- Project *(infer which project under `$PROJECTS_ROOT`, or ask which one)*
- Task slug *(infer from the user's goal, e.g. "build-login")*
- Task description *(infer a one-sentence summary)*

### If Intent C — Resume Existing Task
Needed to open the task:
- Project *(infer which project under `$PROJECTS_ROOT`, or ask)*
- Task ID or task name *(infer from what the user mentioned)*

Format the ask like this — showing defaults clearly:
```
Got it! Here's what I'm about to do:

**Intent:** Create a new task
- Project: my-project ← OK, or different?
- Task slug: "build-login" ← OK, or change it?
- Description: "Implement login flow with JWT auth" ← OK, or update it?

Confirm and I'll set it up.
```

---

## Step 3 — User Confirms

Wait for the user to confirm or correct the defaults. Apply any corrections, then proceed to Step 4.

---

## Step 4 — Hand Off to the Right Skill

Once confirmed, pass all collected information directly to the appropriate skill.
Do not re-ask the user for any information already gathered here.

### Intent A → `create-project`
Pass: project name, real project path, resources list.
Skip `create-project`'s intake — start directly from creating the index file and artifacts folder.

### Intent B → `create-task`
Pass: project, task slug, task description.
Skip `create-task`'s intake — start directly from creating the files.
`create-task` then begins logging the conversation verbatim.

### Intent C → `resume-task`
Pass: project, task-id.
`resume-task` reads the task file, opens the next chat session on the task's existing
conversation log, and continues logging the conversation verbatim. It does NOT create a new task.
