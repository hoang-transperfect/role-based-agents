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

All projects live under a single fixed root (no per-project working directory):

```bash
PROJECTS_ROOT="<assistant-folder>/projects"   # assistant-folder is the directory containing this assistant's definition file (e.g. assistants/ba-assistant)
```

---

## Step 0 — Before-work guard (start of session)

Because this skill runs once at the start of every conversation, it is the right place to make
sure work begins on a clean slate. Invoke the **`commit-work` before-work guard** (Job 1) against
the **real project repo** (`real_project_path` from `resource.md`) — where deliverables land — so
that if its tree is dirty, the user stashes or commits before anything proceeds.

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
| **D. Out of scope** | request unrelated to BA work — coding, DevOps, writing emails, general Q&A, etc. |

**If Intent D (out of scope):** do **not** continue to Step 2. Refuse per the assistant's scope
rule in `ba-assistant.md` — politely explain this is a BA assistant and redirect the user to BA
work. Only A/B/C proceed through the rest of this skill.

### Check existing tasks before deciding between B and C

Whenever the user describes wanting to *work on something* (i.e. it's not clearly a "new project"
request), list the existing in-progress tasks and check whether one already matches the need.
This prevents creating a duplicate task when the user actually wants to resume an existing one.

Run the following to list all in-progress tasks across projects:

```bash
for f in "$PROJECTS_ROOT"/*/in-progress-tasks/*.md; do
  [[ -f "$f" ]] || continue
  project=$(basename "$(dirname "$(dirname "$f")")")
  id=$(grep -m1 '^id:' "$f" | sed 's/^id: *//')
  desc=$(grep -m1 '^description:' "$f" | sed 's/^description: *//')
  printf '[%s] %s — %s\n' "$project" "${id:-$(basename "$f" .md)}" "${desc:-(no description)}"
done
```

(If the specific project is already known, replace `"$PROJECTS_ROOT"/*/` with `"$PROJECTS_ROOT/<slug>"/`.)

This scans `in-progress-tasks/` only. **Completed tasks** are moved to `completed-tasks/` when done,
so they intentionally don't appear here and won't be offered for resume.

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
  deliverables, and existing docs live *(ask if not stated; it is recorded in resource.md and is
  where project artifacts get written)*
- Resources: a list of links + descriptions *(infer any URLs/docs mentioned)*

(The workspace folder is created under `$PROJECTS_ROOT` automatically; the real project folder
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
Pass: project name, resources list.
Skip `create-project`'s intake — start directly from creating the folder structure.

### Intent B → `create-task`
Pass: project, task slug, task description.
Skip `create-task`'s intake — start directly from creating the files.
`create-task` then begins logging the conversation verbatim.

### Intent C → `resume-task`
Pass: project, task-id.
`resume-task` reads the task file, opens the next chat session on the task's existing
conversation log, and continues logging the conversation verbatim. It does NOT create a new task.
