---
name: designer-flow
description: >
  Writes the UX spec for one user story at a time — the user flows covering all cases: happy
  path, alternate paths, edge cases, error states, empty states, and loading states. Invoke when
  a designer is ready to define the full user journey for a story, after designer-plan and
  (when applicable) designer-research. This skill produces the UX spec section of the story's
  design-spec.md. Run once per user story in scope; the output feeds designer-ui, which adds
  the UI spec to the same file. Also invoke when updating existing flows in maintain mode — find
  the existing design-spec.md and edit in place.
---

# designer-flow

Flows are the contract between intent and interface: they answer "what can happen here?" before
anyone decides what it looks like. The goal of this skill is **complete case coverage** — a flow
that only shows the happy path is a design debt, because the missing cases get designed (badly)
at implementation time.

Each user story gets its own `design-spec.md`. This skill writes the **UX spec** section of that
file. `designer-ui` writes the **UI spec** section into the same file afterward.

## Where things live

- **Read** from the `## Plan` (user stories in scope, work mode) and `user-insights.md` (JTBD
  and design implications), if available.
- **Read** the BA user story from `<real_project_path>/ba-requirement/` for its acceptance
  criteria — these define the minimum set of cases that must be covered.
- **Write** the UX spec into
  `<real_project_path>/design-spec/<epic-slug>/<feature-slug>/<story-slug>/design-spec.md`
  (create the folder structure if needed). If the file already exists (maintain mode), update in
  place — do not rewrite unchanged sections.
- **Update** `<real_project_path>/design-spec/traceability.md`: add or update the row for this story.

---

## The skill contract

### Inputs
- The user story from the BA backlog: ID, title, and acceptance criteria.
- The `## Plan` (confirming this story's step is in scope) and `user-insights.md` (JTBD and
  design implications for this story), if available.

### Input Acceptance Criteria
- The user story ID and its BA acceptance criteria are available. If not, find them in
  `ba-requirement/` or ask the user — do not design flows without knowing what cases the story
  must handle.
- The work mode is known (from the plan).

### Outputs
- The **UX spec section** of `<real_project_path>/design-spec/<epic>/<feature>/<story>/design-spec.md`.
- An updated row in `<real_project_path>/design-spec/traceability.md`.

### Output Quality Criteria
- **Every case is covered** — happy path, alternate paths, edge cases, error states (validation,
  system errors, permission errors), empty states, and loading states. Missing a case is a quality
  failure. The BA acceptance criteria are the minimum set; go beyond them for edge and error cases.
- **Each flow step is unambiguous** — a developer or another designer can read it and know exactly
  what happens at each point without guessing.
- **Decisions and branches are explicit** — every conditional ("if the user has no items", "if the
  request fails") is called out, not implied.
- **The story's JTBD is traceable** — the happy path directly serves the job the user is trying
  to do (from `user-insights.md`), not a tangential path.

---

## The 3-gate flow

### Gate 1 — Input
Find the BA user story and its acceptance criteria. If the story doesn't exist in `ba-requirement/`,
**ask the user** where the business spec is before designing — flows without a business spec are
assumptions. Check that the work mode is known.

### Gate 2 — Process
Work through each case with the designer. Use the BA acceptance criteria as the starting checklist
for cases, then explicitly probe for what they don't cover:
- **Edge cases**: what happens with 0 items, 1 item, max items, very long text?
- **Error states**: what if the network fails, the server errors, the user lacks permission?
- **Empty states**: first-time experience, no results, no content yet?
- **Loading / async**: what does the user see while waiting?
- **Alternate paths**: any valid route to the same goal other than the main path?

For maintain mode, read the existing UX spec first and make targeted edits — don't rewrite
unchanged flows.

Write the UX spec section:

```markdown
# Design Spec — <Story ID>: <Story title>

**Business spec:** [<Story ID>](<path to story in ba-requirement/>)
**Work mode:** from-scratch / develop / maintain
**Status:** draft / reviewed

---

## UX Spec

### Overview
<1–2 sentences: what the user is trying to do and the key design decision>

### User flows

#### Happy path — <short label>
1. <step> → <what happens>
2. <step> → <what happens>
…
**End state:** <what the user sees when done>

#### Alternate path — <short label>
<describe the alternate route and how it differs>

#### Edge case — <short label>
<condition that triggers it> → <what happens>

#### Error state — <short label>
<what causes the error> → <what the user sees> → <recovery action available>

#### Empty state — <short label>
<condition> → <what the user sees> → <any action available>

#### Loading state
<what the user sees while the action is in progress>
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that all cases are covered and each
decision/branch is explicit. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write / update the file, update `traceability.md`, tick the UX flows step
   in `## Plan`, update **Next step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The completed UX spec section feeds `designer-ui`, which writes the UI spec into the same
`design-spec.md`. Run once per user story in scope; `designer-ui` picks up where this stops.
