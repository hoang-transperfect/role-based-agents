---
name: ba-scan-context
description: >
  Discovers existing documentation and artifacts relevant to a BA need before any requirements
  work begins, so the team builds on what already exists instead of missing context. Invoke this
  at the start of a BA effort, before ba-plan, and any time a BA asks "what do we already have on
  this?", "is there prior documentation?", or is about to do Document Analysis during elicitation.
  It scans the real project folder (path from resource.md), the project resources, and the
  workspace's prior tasks, then records a Related Context summary — what's relevant, what it
  covers, and the gaps — as a related-context.md artifact in the real project's ba-artifacts
  folder. Use it whenever starting or re-scoping BA work so existing context is never overlooked.
---

# ba-scan-context

The most expensive BA mistake is gathering requirements that already exist somewhere — or
contradicting a decision already documented. This skill front-loads discovery: it finds what's
already known about the need so planning and elicitation start from reality, not a blank page.

It records a **Related Context** summary: a short inventory of relevant existing material, what
each piece covers, and — just as important — the gaps it does *not* cover. `ba-plan` reads this
to decide which BA steps the effort actually needs, and later skills read it so they don't re-ask
what's already answered or miss what's already decided.

## Where things live

- **Search** the real project folder for existing material: read `real_project_path` from the
  project's `resource.md` frontmatter and look there.
- **Write** the result as a deliverable artifact at
  `<real_project_path>/ba-artifacts/<task-id>/related-context.md` (create the folder if needed). It's the
  first artifact of the effort and the audit record of what was already known, so it lives with
  the other deliverables in the real project, not in the workspace task file.

## Where to look (search order)

1. The **existing formal backlog** at `<real_project_path>/ba-requirement/` — the Epic → Feature →
   User Story tree. This is the **primary** source for `develop` and `maintain` work: the new
   feature may belong under an existing epic, or the change may target an existing story. Never
   re-specify what already lives here; find it first.
2. The **real project folder** (`real_project_path`) — existing docs, specs, prior BA artifacts,
   READMEs, design notes, anything under a `ba-artifacts/` folder from earlier tasks.
3. The **project resources** listed in `resource.md` (links + descriptions).
4. The **workspace** — prior task files and conversation logs under `$PROJECTS_ROOT/<project>/`
   that may hold earlier decisions or requirements.

If `real_project_path` is missing or unreadable, that's an input-gate failure — ask the user for
the location rather than guessing or scanning nothing.

---

## The skill contract

### Inputs
- The user's stated need / topic to scan for.
- `resource.md` (for `real_project_path` and the resource list).

### Input Acceptance Criteria
- There is a stated need or topic specific enough to search against (not just "scan the
  project"). If too vague, ask the user what the need is about before searching.
- A readable `real_project_path` exists, or the user supplies a location to search.

### Outputs
- `<real_project_path>/ba-artifacts/<task-id>/related-context.md` — the Related Context summary.

### Output Quality Criteria
- Each relevant item lists: where it is (path/link), what it covers, and how it relates to the
  need.
- **Gaps are stated explicitly** — what the need requires that no existing material covers. A
  summary with no gaps is incomplete; the gaps are what justify the BA work ahead.
- Relevance is honest: don't pad it with loosely-related documents. If little or nothing relevant
  exists, say so plainly — that itself is a useful finding.
- It does not fabricate sources. Every item points at something that actually exists.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If the need is too vague or the project path
is missing, **ask the user** — do not assume. (The working tree is already clean — the before-work
guard runs once at session start via `gather-needs`, not here.)

### Gate 2 — Process
Search the locations above for material related to the need. For each candidate, judge relevance
honestly and note what it covers. Where it helps, discuss findings with the user — they often
know of sources not in the obvious places, or can confirm whether an old doc is still current.

Draft the Related Context artifact:

```markdown
# Related Context — <need / topic>

_Scanned: <date> · Sources: <real_project_path>, resource.md, workspace_

## Relevant existing material
| Item | Location | Covers | Relation to the need | Current? |
|------|----------|--------|----------------------|----------|
| <name> | <path/link> | <what it documents> | <how it bears on the need> | yes/stale/unknown |

## Gaps — not covered by anything above
- <what the need requires that no existing material addresses>

## Notes for planning
- <implications: what can be reused, what must be gathered fresh, what to verify>
```

### Gate 3 — Output
Check the draft against the Output Quality Criteria — especially that gaps are explicit and
relevance is honest. Improve if short of the bar (ask the user if you need their knowledge — do
not assume). When it meets the bar:
1. Present it and **ask the user to confirm** before writing the file. Never write or update
   `related-context.md` without confirmation.
2. **If confirmed** → write `<real_project_path>/ba-artifacts/<task-id>/related-context.md`, then hand off
   to `commit-work` to commit it in the real project repo.
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill` to fold the lesson back into this skill.

You author the summary as the BA assistant, on the user's behalf, for the audit record.

---

## Handoff

The `related-context.md` artifact feeds `ba-plan`'s input gate (the gaps shape which steps are
actually needed) and serves as the starting point for Document Analysis in `ba-elicit`.
