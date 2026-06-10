---
name: designer-ui
description: >
  Writes the story spec for one user story — the UX flows covering all cases (happy, alternate,
  edge, error, empty, loading), the map of affected design artifacts, and the alignment between
  BA acceptance criteria and flows. This is the per-story design record connecting the business
  requirement to the UI changes and proving every acceptance criterion is covered. Invoke after
  designer-scan-context (which identifies affected artifacts) and designer-research (if in plan),
  and before the artifact-level skills (designer-organism, designer-template, designer-page).
  One story-spec.md per user story; artifact specs are updated separately by their own skills.
---

# designer-ui

The story spec is the immutable audit record of a user story's design intent. It answers:
- What can happen on screen for this story? (UX flows — all cases)
- Which design artifacts does this story change? (affected map)
- How does each acceptance criterion map to a flow case? (AC alignment)

The story spec does **not** describe what components look like — that belongs in the artifact
specs (organism/template/page). It references artifacts by name and describes the user journey.

## Where things live

- **Read** `related-context.md` (affected artifacts from `designer-scan-context`).
- **Read** the BA user story from `<real_project_path>/ba-requirement/` — acceptance criteria are
  the minimum set of cases the flows must cover.
- **Read** `user-insights.md` (JTBD, design implications), if available.
- **Write** `<real_project_path>/design-spec/<epic>/<feature>/<story>/story-spec.md`
  (create the folder if needed).
- **Update** `<real_project_path>/design-spec/traceability.md` — add or update the row for this
  story.

---

## The skill contract

### Inputs
- The BA user story (ID, title, acceptance criteria).
- `related-context.md` — especially the affected artifacts section from `designer-scan-context`.
- `user-insights.md` (JTBD and design implications), if available.

### Input Acceptance Criteria
- The BA user story and its acceptance criteria are available. If not, find them in
  `ba-requirement/` or ask — do not write flows without knowing what cases must be covered.
- `related-context.md` exists and includes an affected artifacts map. If missing, hand back to
  `designer-scan-context`.

### Outputs
- `<real_project_path>/design-spec/<epic>/<feature>/<story>/story-spec.md`
- An updated row in `<real_project_path>/design-spec/traceability.md`.

### Output Quality Criteria
- **Every case is covered** — happy path, alternate paths, edge cases, error states, empty
  states, loading states. BA acceptance criteria are the minimum; go beyond for edge/error cases.
- **Every flow step is unambiguous** — a developer or designer reads it without guessing.
- **Every decision/branch is explicit** — every conditional is called out, not implied.
- **AC alignment is complete** — every acceptance criterion maps to at least one flow case. No AC
  left unmapped. If a criterion cannot be mapped, surface it as an open question.
- **Affected artifacts are listed** — every organism/template/page this story changes is named
  with a link to its spec file and a one-line description of what changes.

---

## The 3-gate flow

### Gate 1 — Input
Verify the BA user story and acceptance criteria exist. Verify `related-context.md` has the
affected artifacts map. If either is missing, hand back to the appropriate skill first.

### Gate 2 — Process
Work through each case with the designer. Use the BA acceptance criteria as the starting
checklist, then probe for what they don't cover:
- **Edge cases**: 0 items, max items, very long text, concurrent actions?
- **Error states**: network failure, permission denied, validation failure, server error?
- **Empty states**: first-time use, no results, no content yet?
- **Loading/async**: what does the user see while waiting?
- **Alternate paths**: any valid route to the same goal other than the main path?

For each flow case, note which acceptance criterion it satisfies — or mark it as a robustness
case that goes beyond the AC.

Write the story spec:

```markdown
# Story Spec — <Story ID>: <Story title>

**Business spec:** [<Story ID>](<path to story in ba-requirement/>)
**Work mode:** from-scratch / develop / maintain

## Affected design artifacts
| Artifact | Type | Spec | What changes |
|---|---|---|---|
| <OrganismName> | product organism | [link](../../product-organisms/<name>/organism-spec.md) | <one-line description> |
| <TemplateName> | template | [link](../../templates/<name>/template-spec.md) | <one-line description> |
| <PageName> | page | [link](../../pages/<name>/page-spec.md) | <one-line description> |

## UX flows

### Happy path — <short label>
1. <step> → <what happens>
2. <step> → <what happens>
**End state:** <what the user sees when done>

### Alternate path — <short label>
<describe the alternate route>

### Edge case — <short label>
<condition that triggers it> → <what happens>

### Error state — <short label>
<what causes the error> → <what the user sees> → <recovery action available>

### Empty state — <short label>
<condition> → <what the user sees> → <action available>

### Loading state
<what the user sees while the action is in progress>

## AC alignment
| Acceptance criterion | Covered by |
|---|---|
| AC-1: <text> | Happy path — step 3 |
| AC-2: <text> | Error state — network failure |
| AC-3: <text> | Empty state |
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that every AC is mapped and every
decision/branch in the flows is explicit. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write `story-spec.md`, update `traceability.md`, tick Step 2 in `## Plan`,
   update **Next step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The story spec feeds the artifact-level skills. For each affected artifact listed:
- Organism changes → `designer-organism`
- Template changes → `designer-template`
- Page changes → `designer-page`

Run one artifact skill per affected artifact, then `designer-review` to validate the full set.
