---
name: create-task
description: >
  Creates a new task folder (task file + conversation log) inside the real project, registers
  the task in the project index file, then begins logging the current conversation verbatim.
  Expects inputs to be passed in directly — typically from gather-needs. Do NOT re-ask the user
  for information already collected. Trigger when gather-needs has detected "create new task"
  intent and confirmed inputs.
---

# create-task

Creates the task's folder in the real project, registers it in the project index, then starts
live conversation logging. All inputs are assumed to already be confirmed by the user
(via gather-needs).

## Inputs (provided by gather-needs)

- `project` — project slug; its index file is `<assistant-folder>/projects/<project>.md`
- `task-slug` — short kebab-case label (e.g. `build-login`)
- `task-description` — one sentence describing the task

The **task ID** is `<slug>-<YYYY-MM-DD>` using today's date.

## Where the task lives

Read `real_project_path` from the index file's frontmatter, then create the task folder inside
the real project:

```bash
TASK_DIR="<real_project_path>/<assistant-name>-artifacts/tasks/<task-id>"   # e.g. …/tasks/build-login-2026-06-10
mkdir -p "$TASK_DIR"
```

It holds the task file, the conversation log, and (added later by other skills) the task's
working artifacts.

---

## Step 1 — Create the Task File

Path: `$TASK_DIR/task.md`

```markdown
---
id: <task-id>
description: <task description>
status: in-progress
---

# Task: <task-id>

**Description:** <task description>

## Plan
<!-- To be populated by the planning skill -->
```

---

## Step 2 — Create the Conversation Log (header only)

Path: `$TASK_DIR/conversation.md` — each task has exactly one conversation log.

Create the file with frontmatter and header **only** — do NOT reconstruct or backfill any
prior turns. The current conversation is the first session, and it will be logged live going
forward (see Step 5).

```markdown
---
task: <task-id>
description: <short description of this conversation>
status: in-progress
updated: <YYYY-MM-DD>
---

# Conversation Log: <task-id>

**Description:** <short description of this conversation>
**Started:** <YYYY-MM-DD HH:MM>
**Participants:** <Human name>
**Agent:** <platform>/<model>
```

---

## Step 3 — Register the Task in the Project Index

Append one line under `## In-Progress Tasks` in `<assistant-folder>/projects/<project>.md`.
That section is the last thing in the file, so appending to the file is enough:

```bash
printf -- '- %s — %s\n' "<task-id>" "<task description>" >> "<assistant-folder>/projects/<project>.md"
```

This line is what `gather-needs` searches when checking for existing tasks; it is removed when
the task completes.

---

## Step 4 — Open Session 1

Append the first session heading to the conversation log:

```bash
log_path="$TASK_DIR/conversation.md"
n=$(grep -E '^## Chat Session [0-9]+' "$log_path" | grep -oE '[0-9]+' | sort -n | tail -1 || true)
n=$(( ${n:-0} + 1 ))
[[ -s "$log_path" ]] && [[ "$(tail -c1 "$log_path" | wc -l)" -eq 0 ]] && printf '\n' >> "$log_path"
printf '\n## Chat Session %s — %s\n' "$n" "$(date +%Y-%m-%d)" >> "$log_path"
echo "$n"
```

This appends `## Chat Session 1 — <today>` and prints the session number.

---

## Step 5 — Log Every Turn Verbatim (standing behavior)

From this point on, the log append is the **final tool call of every response**: after you finish
replying to the user, your last action that turn is to append the turn to the active log file —
nothing else follows it. This fires unconditionally, regardless of which skill is active or whether
one skill is handing off to another. Never defer it to the end of a skill block, never batch
multiple turns into one append, never skip it because a handoff is in progress.

Append using a bash heredoc with a quoted delimiter (this preserves backticks, quotes, `$`,
and newlines without escaping):

```bash
cat >> "$TASK_DIR/conversation.md" << 'CLAUDE_LOG_EOF'

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
- Keep the `updated:` field in the frontmatter current if you revise the file.
- The active log file is the one created above; keep using it for the whole session.

---

## Step 6 — Confirm Success (first turn only)

On the turn where the task is created, tell the user:
- Task ID created, the task folder path inside the real project, and the index line added
- That this conversation is now being logged verbatim to the conversation log
- That `## Plan` will be filled in by the planning skill later
