---
name: create-task
description: >
  Creates a new task file and a linked conversation log inside an existing project,
  then begins logging the current conversation verbatim. Expects inputs to be passed in
  directly — typically from gather-needs. Do NOT re-ask the user for information already
  collected. Trigger when gather-needs has detected "create new task" intent and confirmed inputs.
---

# create-task

Creates two linked files inside an existing project, then starts live conversation logging.
All inputs are assumed to already be confirmed by the user (via gather-needs).

## Inputs (provided by gather-needs)

- `project-directory` — full path to the project folder
- `task-slug` — short kebab-case label (e.g. `build-login`)
- `task-description` — one sentence describing the task

The **task ID** is `<slug>-<YYYY-MM-DD>` using today's date.
The **conversation ID** is `<task-id>-conv-001`.

---

## Step 1 — Create the Task File

Path: `<project>/in-progress-tasks/<task-id>.md`

```markdown
---
id: <task-id>
description: <task description>
---

# Task: <task-id>

**Description:** <task description>

## Plan
<!-- To be populated by the planning skill -->
```

---

## Step 2 — Create the Conversation Log (header only)

Path: `<project>/raw-conversation/<task-id>-conv-001.md`

Create the file with frontmatter and header **only** — do NOT reconstruct or backfill any
prior turns. The current conversation is the first session, and it will be logged live going
forward (see Step 4).

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
**Started:** <YYYY-MM-DD HH:MM>
**Participants:** <Human name>
**Agent:** <platform>/<model>
```

---

## Step 3 — Open Session 1

Append the first session heading to the conversation log:

```bash
log_path="<project>/raw-conversation/<task-id>-conv-001.md"
n=$(grep -E '^## Chat Session [0-9]+' "$log_path" | grep -oE '[0-9]+' | sort -n | tail -1 || true)
n=$(( ${n:-0} + 1 ))
[[ -s "$log_path" ]] && [[ "$(tail -c1 "$log_path" | wc -l)" -eq 0 ]] && printf '\n' >> "$log_path"
printf '\n## Chat Session %s — %s\n' "$n" "$(date +%Y-%m-%d)" >> "$log_path"
echo "$n"
```

This appends `## Chat Session 1 — <today>` and prints the session number.

---

## Step 4 — Log Every Turn Verbatim (standing behavior)

From this point on, for the rest of the conversation, **the very last action of every response**
must be appending that turn to the active log file — before anything else starts for the next
turn. This fires unconditionally: regardless of which skill is active, whether a skill is handing
off to another, or whether anything else is happening.

**Timing rule: append first, then do nothing else for this turn.** The log append is the final
tool call of every response. Do not defer it to the end of a skill block, do not batch multiple
turns, do not skip it because a handoff is in progress.

Append using a bash heredoc with a quoted delimiter (this preserves backticks, quotes, `$`,
and newlines without escaping):

```bash
cat >> <project>/raw-conversation/<task-id>-conv-001.md << 'CLAUDE_LOG_EOF'

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

## Step 5 — Confirm Success (first turn only)

On the turn where the task is created, tell the user:
- Task ID created and paths to both files
- That this conversation is now being logged verbatim to the conversation log
- That `## Plan` will be filled in by the planning skill later

