---
name: resume-task
description: >
  Resumes an existing task and continues its conversation log. Expects inputs to be passed in
  directly — typically from gather-needs. Opens the next chat session on the task's existing
  conversation log and logs the continued conversation verbatim. Do NOT create a new task file.
  Trigger when gather-needs has detected "resume existing task" intent and confirmed the task.
---

# resume-task

Picks up an existing task and **continues its conversation log** — appending a new chat session
to the task's existing log file, then logging every further turn verbatim. All inputs are
assumed to already be confirmed by the user (via gather-needs).

## Projects root

```bash
PROJECTS_ROOT="$HOME/projects"   # must match the value used by create-project / gather-needs
```

## Inputs (provided by gather-needs)

- `project` — project folder name under `$PROJECTS_ROOT`
- `task-id` — the existing task's ID (e.g. `build-login-20260604`)

Derived paths:
- Task file: `$PROJECTS_ROOT/<project>/in-progress-tasks/<task-id>.md`
- Conversation log: `$PROJECTS_ROOT/<project>/raw-conversation/<task-id>-conv-001.md`

---

## Step 1 — Read the Task and Summarise

Read the task file and summarise for the user: the task ID, its description, and the current
`## Plan` contents (if any have been filled in).

---

## Step 2 — Ensure the Conversation Log Exists

The conversation log should already exist from when the task was created. If it does **not**
exist (e.g. it was deleted), recreate the header so logging can continue:

```markdown
---
id: <task-id>-conv-001
description: <short description of this conversation>
task: <task-id>
status: in-progress
updated: <YYYY-MM-DD>
---

# Conversation Log: <task-id>-conv-001

**Description:** <short description of this conversation>
**Started:** <original date if known, else today> 
**Participants:** <Human name>
**Agent:** <platform>/<model>
```

If it already exists, leave the existing content untouched — you are continuing it, not
overwriting it. Update the `updated:` field in the frontmatter to today's date.

---

## Step 3 — Open the Next Chat Session

Append the next session heading. The script auto-increments based on the highest existing
`## Chat Session N`, so a resumed task continues at Session 2, 3, and so on:

```bash
python scripts/log_session.py start \
  --log "$PROJECTS_ROOT/<project>/raw-conversation/<task-id>-conv-001.md"
```

---

## Step 4 — Log Every Turn Verbatim (standing behavior)

From this point on, for the rest of the conversation, **after every user message**, append that
turn to the conversation log. Capture both sides **verbatim** — the user's exact words and your
exact response. Use a bash heredoc with a quoted delimiter (preserves backticks, quotes, `$`,
and newlines without escaping):

```bash
cat >> "$PROJECTS_ROOT/<project>/raw-conversation/<task-id>-conv-001.md" << 'CLAUDE_LOG_EOF'

**Human (<name>):**
<the user's exact message>

**Agent (<platform>/<model>):**
<your exact response>
CLAUDE_LOG_EOF
```

Rules for logging:
- Do this every turn, automatically, without being asked.
- Verbatim — do not summarize, paraphrase, or trim either side.
- Append the user's message and your response together, once per turn.
- The new turns land under the session heading created in Step 3, continuing the same log file.

---

## Step 5 — Continue the Work

Ask the user: "Ready to continue — what would you like to work on?" Then proceed.
Do NOT create a new task file; this is a continuation of the existing task.
