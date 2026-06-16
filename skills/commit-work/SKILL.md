---
name: commit-work
description: >
  Keeps the working tree clean and creates an auditable commit history around any work. Two jobs:
  (1) a before-work guard that refuses to start on a dirty tree until the user stashes or commits,
  and (2) commit-on-confirmation, which records every user-confirmed deliverable or skill change
  as its own clearly-messaged commit in the repository that contains it. Invoke this skill at the
  start of any working session, and again every time the user confirms an output or a skill
  improvement. Other skills call into this skill at their commit points — use it whenever something
  has just been confirmed and needs to be recorded.
---

# commit-work

This skill exists so that work is **auditable**. Every confirmed deliverable and every accepted
skill change should map to a commit, so anyone can later trace *what* was agreed and *when*. It
has two responsibilities that fire at different moments.

## Which repository?

Commit each confirmed thing in the git repository that **contains it** — because that's where its
audit trail belongs:

- **Everything project-specific** — confirmed deliverables/artifacts, task files (`task.md`),
  conversation logs (`conversation.md`), and `resource.md` notes — lives in the **real project**:
  the folder recorded as `real_project_path` in the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`), under `<assistant-name>-artifacts/`. Commit
  them there. This is the primary target.
- **Accepted skill improvements** edit a `SKILL.md`, which lives in the **skills repository**
  (the current working directory). Commit those there.
- **The project index file** (the only per-project record in the assistant folder) also lives in
  the skills repository — commit index updates there as bookkeeping.

Run git against the right repo explicitly, e.g. `git -C "<repo path>" …`, so a commit never lands
in the wrong history.

---

## Job 1 — Before-work guard

Run this **once at the start of a working session**, before any skill does real work — it is
invoked by the session-entry skill (`gather-needs`, Step 0), not from inside other skills' input
gates. A dirty tree mixes unrelated changes into the audit trail, so we never start on top of one.
Because the session starts clean, downstream skills don't need to re-check the tree.

Guard the **real project repo** — the `real_project_path` from the project's index file, where
deliverables land — as soon as the project (and thus that path) is known. For an existing project
that's immediately; for a brand-new project, once the path has been supplied. If
`real_project_path` isn't a git repo yet, Step 0 will offer to initialise one before the guard
runs.

### Step 0 — Ensure the real project folder is a git repo

Before inspecting the tree, check whether the folder is a git repository:

```bash
git -C "<real_project_path>" rev-parse --is-inside-work-tree 2>/dev/null
```

- **Exit 0 (is a repo)** → proceed to Step 1.
- **Non-zero / command fails (not a repo)** → explain to the user why git is needed, then offer to initialise it:

```
This project folder isn't a git repository yet.

Git is how we keep your work safe and auditable — every confirmed output gets recorded
as a commit, so you can always see what changed, when, and why. Without it, there's no
audit trail and no way to undo changes safely.

I can run `git init` here for you. Want me to go ahead?
```

If the user agrees, initialise the repo:

```bash
git -C "<real_project_path>" init
git -C "<real_project_path>" add -A
git -C "<real_project_path>" commit -m "chore: initial commit before assistant work begins" --allow-empty
```

After initialisation, proceed to Step 1. If the user declines, note that commit-related steps will be skipped for this session and continue.

### Step 1 — Inspect the tree

```bash
git -C "<real_project_path>" status --short
```

- **Clean (no output)** → say so briefly and proceed. Nothing else to do.
- **Dirty (any output)** → do NOT start work. Go to Step 2.

### Step 2 — Ask the user how to handle existing changes

Never decide this for the user — these are their changes. Show the dirty files and ask:

```
The working tree has uncommitted changes:
<paste the git status --short output>

Before we start, how do you want to handle these?
  - commit  → I'll commit them now (tell me a message, or accept my suggestion)
  - stash   → I'll stash them so you can restore later with `git stash pop`
```

Apply exactly what the user chooses (in the same repo you inspected):

```bash
# commit
git -C "<real_project_path>" add -A && git -C "<real_project_path>" commit -m "<user's message>"

# stash
git -C "<real_project_path>" stash push -u -m "pre-work stash <YYYY-MM-DD>"
```

Only once the tree is clean (or the user has explicitly chosen how to proceed) does work begin.

---

## Job 2 — Commit on confirmation

Whenever the user **confirms** something, record it immediately as its own commit. Small,
single-purpose commits make the history readable — so an artifact and a skill change are
**separate commits**, never bundled.

### When this fires

- The user confirms a deliverable/artifact → commit it in the **real project repo**.
- The user accepts a skill improvement (via `improve-skill`) → a **separate** commit for the
  SKILL.md change, in the **skills repo**.
- Any other discrete thing the user signs off on → commit it in the repo that contains it.

### How to commit

Pick the repo that contains what was confirmed (see "Which repository?" above). Stage only what
belongs to this confirmation, then commit with a message that explains the *what* and the *why* so
the history reads as an audit log:

```bash
git -C "<repo containing the confirmed files>" add <specific paths for this confirmation>
git -C "<repo containing the confirmed files>" commit -m "<type>(<scope>): <what was confirmed>"
```

Message guidance (keep it honest and specific — this is the audit record):

| Situation | Example message |
|---|---|
| New artifact/document | `docs(<scope>): add <artifact> for <project>` |
| Updated artifact/document | `docs(<scope>): refine <artifact> after review` |
| Progress checklist tick | `chore(<scope>): mark <step> complete` |
| Accepted skill improvement | `skill(<skill-name>): <what the lesson changed>` |

### Rules

- **One confirmation, one commit.** Do not batch multiple unrelated confirmations together.
- **Deliverable and skill change never share a commit** — they answer different audit questions
  and live in different repos (real project vs skills repo).
- Stage specific paths, not blanket `git add -A`, so a commit contains only what was confirmed.
- If you're unsure what the user wants the message to say, propose one and let them adjust —
  do not invent a message that misrepresents the change.
- Never force-push, rewrite history, or commit on the user's behalf for something they have
  **not** confirmed.

### After every commit

Remind the user to compact the chat context before continuing:

> "Commit done. Please run `/compact` (or your tool's equivalent context-compaction command) before we continue — this keeps the context clean for the next step."
