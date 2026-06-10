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
PROJECTS_ROOT="<assistant-folder>/projects"   # must match the value used by create-project / gather-needs
```

## Inputs (provided by gather-needs)

- `project` — project slug; its index file is `$PROJECTS_ROOT/<project>.md`
- `task-id` — the existing task's ID (e.g. `build-login-2026-06-04`)

Derived paths — read `real_project_path` from the index file's frontmatter, then:

- Task folder: `<real_project_path>/<assistant-name>-artifacts/tasks/<task-id>/`
- Task file: `<task folder>/task.md`
- Conversation log: `<task folder>/conversation.md`

If the task file's frontmatter says `status: completed`, the task was closed — that's why it no
longer appears in the index's in-progress list. If the user wants to reopen it: set
`status: in-progress` in `task.md` and re-add its line under `## In-Progress Tasks` in the index
file (`- <task-id> — <description>`), then continue from Step 1.

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
task: <task-id>
description: <short description of this conversation>
status: in-progress
updated: <YYYY-MM-DD>
---

# Conversation Log: <task-id>

**Description:** <short description of this conversation>
**Started:** <original date if known, else today>
**Participants:** <Human name>
**Agent:** <platform>/<model>
```

If it already exists, leave the existing content untouched — you are continuing it, not
overwriting it. Update the `updated:` field in the frontmatter to today's date.

---

## Step 3 — Open the Next Chat Session

Append the next session heading. Auto-increments based on the highest existing
`## Chat Session N`, so a resumed task continues at Session 2, 3, and so on:

```bash
log_path="<real_project_path>/<assistant-name>-artifacts/tasks/<task-id>/conversation.md"
n=$(grep -E '^## Chat Session [0-9]+' "$log_path" | grep -oE '[0-9]+' | sort -n | tail -1 || true)
n=$(( ${n:-0} + 1 ))
[[ -s "$log_path" ]] && [[ "$(tail -c1 "$log_path" | wc -l)" -eq 0 ]] && printf '\n' >> "$log_path"
printf '\n## Chat Session %s — %s\n' "$n" "$(date +%Y-%m-%d)" >> "$log_path"
```

---

## Step 4 — Log Every Turn Verbatim (standing behavior)

From this point on, the log append is the **final tool call of every response**: after you finish
replying to the user, your last action that turn is to append the turn to the conversation log —
nothing else follows it. This fires unconditionally, regardless of which skill is active or whether
one skill is handing off to another. Never defer it to the end of a skill block, never batch
multiple turns into one append, never skip it because a handoff is in progress.

Use a bash heredoc with a quoted delimiter (preserves backticks, quotes, `$`, and newlines):

```bash
cat >> "$log_path" << 'CLAUDE_LOG_EOF'

**Human (<name>):**
<the user's exact message>

**Agent (<platform>/<model>):**
<your exact response>
CLAUDE_LOG_EOF
```

Rules for logging:
- **Append immediately** — the log append is the last tool call of every single response, no exceptions.
- **Never batch** — each turn gets its own append. Do not accumulate turns and flush later.
- **Never skip on handoff** — if a skill is handing off to another skill, still append this turn before the handoff completes.
- Verbatim — do not summarize, paraphrase, or trim either side.
- The new turns land under the session heading created in Step 3, continuing the same log file.

---

## Step 5 — Continue the Work

Ask the user: "Ready to continue — what would you like to work on?" Then proceed.
Do NOT create a new task file; this is a continuation of the existing task.
