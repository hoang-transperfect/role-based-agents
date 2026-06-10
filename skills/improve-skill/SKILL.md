---
name: improve-skill
description: >
  Turns user dissatisfaction with an output into a lasting improvement of the skill that produced
  it. Invoke this whenever a user does NOT confirm a skill's output as-is — when they push back,
  correct, or ask for changes. It faithfully records the rejection, lets the producing skill fix
  the output first, then — automatically, once the user confirms the fixed output — diagnoses why
  the skill produced the rejected version and either proposes a concrete SKILL.md change or, when
  the feedback is project-specific rather than a skill gap, a note for the project's resource.md.
  It asks the user only to confirm the improvement (or the note), never to diagnose. Any skill
  whose output the user wanted improved should hand off here so the lesson is not lost next time.
---

# improve-skill

A skill that gets corrected once but never learns wastes the user's time forever. This skill
closes that loop: when an output is rejected and then fixed, it works out *why the skill produced
the bad version* and folds that lesson somewhere durable — into the skill itself, or, when the
feedback is really just this-project preference, into the project's notes.

It runs **inside another skill's output gate**, after the output failed to be confirmed as-is.
The producing skill owns fixing the actual output; this skill rides alongside to harvest the
lesson. The user is asked to **confirm** the result — never to do the diagnosis.

---

## Step 1 — Record the rejection faithfully

As the user and the producing skill work to fix the output, keep a plain, verbatim record of
what the user actually objected to and what the corrected version became. No interpretation yet —
just the raw signal, because the specifics are easy to lose and the diagnosis in Step 3 depends
on them.

```
- Rejected output (excerpt): <what the skill produced that the user pushed back on>
- User's objection (verbatim): <what they actually said was wrong>
- Corrected version (excerpt): <what it became once fixed>
```

One block per distinct point of feedback. If an objection is unclear, ask the user to clarify the
*objection* — that's about understanding their words, not about diagnosing the skill.

## Step 2 — Let the output be confirmed first

Improvement never blocks the user's real work. The producing skill keeps iterating until **the
user confirms the fixed output**, and commits the confirmed artifact via `commit-work`. Only then
does this skill act. Until the output is confirmed, do nothing here but keep recording (Step 1).

## Step 3 — Diagnose the root cause automatically

Once the output is confirmed, diagnose **on your own** — do not ask the user why it happened. For
each recorded objection, ask: *what about the skill let it produce the rejected version?* Sort it
into one of these, because the cause determines the fix:

| Root cause | Durable fix it points to |
|---|---|
| **Missing step** — the skill never told it to do/ask this | add a step or question to the process |
| **Weak gate** — a quality criterion should have caught it but didn't | strengthen the Output Quality Criteria |
| **Unclear instruction** — present but ambiguous, so misread | reword it and explain the *why* |
| **Didn't follow** — clear instruction the run ignored | raise emphasis / move it earlier |
| **Project-specific preference** — the skill was fine; this is taste for *this* project | NOT a skill change → a project note (Step 4B) |

The sharpest judgement here is the last row. A rejection is a sample of one, and the standing
temptation is to overfit it into a rigid global rule. If the lesson would only ever help this one
project, it is **not** a skill gap — route it to 4B, not 4A.

## Step 4 — Confirm the result with the user

Based on the diagnosis, take exactly one of these branches. Either way, the user is asked only to
confirm — the diagnosis is already done.

### 4A — A real skill gap → propose a SKILL.md change

Show the previous rejected output next to the change you detected, so the user sees what the
improvement is reacting to. Frame it as something the skill detected, then ask for confirmation:

```
While producing this, you rejected:
  <rejected output excerpt>

I diagnosed why `<skill-name>` produced that, and detected an improvement:

1. [<location — e.g. Output Quality Criteria / Step N>]
   <the concrete change, as an addition or before→after reword>
   Why: <the generalised root cause this addresses>

Apply this to the skill? (all / specific numbers / none)
```

- Apply **only** the accepted items by editing the producing skill's SKILL.md.
- Part accepted → apply that part, drop the rest without argument. None accepted → stop; the
  output is still fixed.
- Then hand off to `commit-work` to commit the SKILL.md edit as its **own** commit (separate from
  the artifact commit) — e.g. `skill(<skill-name>): <what the lesson changed>`.

### 4B — Project-specific preference → propose a resource.md note

Don't touch the skill. Log the preference so future work on *this* project honours it, in the
`## Notes` section of the project's `resource.md` — which lives in the real project at
`<real_project_path>/<assistant-name>-artifacts/resource.md` (create the section if it doesn't
exist). Present the note and confirm it is correct before writing:

```
This looks project-specific rather than a skill gap — a preference for this project, not
something to bake into the skill globally. I'd record it as a project note:

  - <date>: <the preference, stated as guidance for future work on this project>

Is that note correct? (yes / edit it / skip)
```

- On confirmation, append the note under `## Notes` in `resource.md`, then hand off to
  `commit-work` to commit it — e.g. `docs(<project>): note project preference on <topic>`.
- If the user edits it, record their version. If they skip, change nothing.

---

## Boundaries

- Diagnose automatically; ask the user only to confirm the improvement or the note.
- Never edit a skill the user did not agree to change.
- Never block or delay confirming the user's actual output to do this work.
- Improve the **producing** skill, not unrelated ones, unless the user asks otherwise.
- When in doubt between a skill change and a project note, prefer the note — it's reversible and
  local, where a bad global rule misfires on every future run.
