---
name: create-skill
description: >
  Authors a new skill for this framework so it matches the house standard — correct shape,
  verb-first name, a description that actually triggers, the contract + 3-gate flow for domain
  skills, wired handoffs, and platform-neutral content. Invoke whenever the user wants to add a
  capability, "create/add a skill", "make a skill for X", turn a repeated workflow into a skill, or
  extend an assistant with a new step. Pairs with improve-skill (which edits existing skills); this
  one creates new ones. Use it for any new skill so the set stays consistent instead of drifting.
---

# create-skill

A skill that doesn't match the others is worse than no skill — it triggers at the wrong time,
reads differently, and rots. This skill exists to make every new skill consistent with the set, so
the framework stays coherent as it grows across roles (ba, fe, be, designer, …). It produces a new
`skills/<name>/SKILL.md` (plus scripts/references/assets if warranted) and registers it.

It is itself a domain-shaped skill, so it runs the same 3-gate flow it teaches — clarify the spec
before writing, verify the result against the standard before finishing, confirm and commit.

## Decide the shape first

Every skill is one of two shapes — pick before writing, because they're structured differently:

- **Domain / workflow skill** — produces a deliverable for a role (e.g. a document, an analysis, an
  artifact). Follows the **full contract + 3-gate flow**. Named `<role>-<verb>` (e.g. `ba-analyse`).
  Exemplars: the `ba-*` skills.
- **Common / utility skill** — a cross-cutting mechanic used by other skills (committing, routing,
  bookkeeping). Lean and procedural; **exempt** from the contract+gate pattern because it's the
  machinery the gates call, not a gated deliverable. Exemplars: `commit-work`, `improve-skill`,
  `create-task`, `gather-needs`.

If unsure: does it hand a finished *thing* to a person, with a quality bar? → domain. Is it plumbing
other skills invoke? → utility.

## The standard every skill meets

- **Frontmatter**: `name` (kebab-case, **verb-first**, identical to the folder) and `description`.
- **The `description` is the trigger** — it's how the assistant decides to use the skill, so say
  *what it does* **and** *when to use it* (phrases, contexts). Lean slightly pushy: skills tend to
  under-trigger, so name the situations explicitly rather than hoping for a keyword match.
- **One skill, one capability.** If it needs "and" to describe it, consider splitting.
- **Register it** in the relevant assistant definition's `## Skills` list (common vs specific) — an
  unregistered skill is dead.
- **Explain the why, don't pile on MUSTs.** Today's models follow reasoning better than rigid
  rules; if you're writing ALL-CAPS NEVER, reframe and explain the cost instead.
- **Platform-neutral + portable**, so it isn't Claude-locked: plain-markdown instructions,
  natural-language handoffs ("hand off to `commit-work`"), generic `git`/shell, and any script in
  **Python 3 stdlib only** (`os.path` for paths, explicit `encoding="utf-8"`, no third-party deps).
- **Progressive disclosure**: keep `SKILL.md` focused; move long reference material to
  `references/` and bundle a `scripts/` helper only when the same multi-step work would otherwise be
  re-done on every run.

## Templates

**Domain / workflow skill** — the full shape:

```markdown
---
name: <role>-<verb>
description: > <what it does + when to invoke it; the trigger>
---
# <role>-<verb>
<one short paragraph: what it's for and why it matters>

## Where things live
- Read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`). Working artifacts → the task folder
  `<real_project_path>/<assistant-name>-artifacts/tasks/<task-id>/`; formal deliverables →
  their home. Tick `## Plan`.

## The skill contract
### Inputs            — what it consumes (artifacts, prior skills' output, the user)
### Input Acceptance Criteria — objective checks the input must pass before work starts
### Outputs           — exact artifact(s): name, location, format
### Output Quality Criteria   — the objective bar the output must meet to be "done"

## The 3-gate flow
### Gate 1 — Input   Check inputs vs Input AC. Falls short → improve it; if that needs info you
  don't have, **ask the user — never assume**. (Tree already clean from the session-start guard.)
### Gate 2 — Process  Do the real work WITH the user — suggest, question, draft.
### Gate 3 — Output  Check vs Output Quality; improve if short. Then present and confirm:
  confirmed → write, tick `## Plan`, hand off to `commit-work`; not satisfied → improve with the
  user until confirmed, commit, then hand off to `improve-skill`.

## Handoff   — which skill consumes this output next
```

**Common / utility skill** — lean: a one-line purpose, the job(s) it does, when each fires, and the
rules/boundaries. No contract or gates. Model it on `commit-work`.

## The 3-gate flow (this skill runs it too)

### Gate 1 — Input
Clarify the new skill's **single capability** and **when it should trigger** with the user. Check:
- the capability is clear and singular (not a vague bundle);
- its **shape** (domain vs utility) is decided;
- a **verb-first name** is chosen and doesn't collide with or duplicate an existing skill — scan
  `skills/` first;
- it's clear which assistant (or "common") it belongs to.

If any are unclear, **ask** — don't invent a skill the user didn't mean. (Tree already clean from
the session-start guard.)

### Gate 2 — Process
Draft the `SKILL.md` **with** the user from the matching template. Write the `description` last and
sharpen it for triggering. Decide if a `scripts/`/`references/` file is warranted (only for repeated
work or long docs). Read the draft once with fresh eyes against "The standard" above and tighten it.
Where a step would benefit, dry-run the trigger: would *this* description fire on the user's example
phrasing, and not on a near-miss?

### Gate 3 — Output
Check the draft against the Output Quality Criteria below. Improve if short (ask the user where
intent is unclear; never assume). When it meets the bar:
1. Present it and ask the user to confirm.
2. **If confirmed** → write `skills/<name>/SKILL.md` (+ any scripts), **register it** in the
   assistant definition's `## Skills` list, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill` to fold the lesson back into *this* skill.

### Output Quality Criteria for the new skill
- Frontmatter `name` is verb-first and matches the folder; `description` states *what + when* and is
  written to trigger reliably (covers real phrasings, avoids obvious near-misses).
- The correct **shape** is applied — domain skills have the full contract + 3-gate with `commit-work`
  and `improve-skill` wired at the output gate; utility skills stay lean and say they're exempt.
- Principles are honoured: never-assume (ask), commit-on-confirmation, file-based/resumable state.
- Content is platform-neutral and any script is portable (Python 3 stdlib, `os.path`, utf-8).
- The skill is **registered** in an assistant definition, and its handoffs name real skills.

---

## Boundaries
- Create the skill the user asked for — don't bundle extra skills or speculative features.
- Don't duplicate an existing skill; if one is close, propose extending it via `improve-skill` instead.
- A skill's intent must not surprise the user if described plainly — no hidden or misleading behaviour.
