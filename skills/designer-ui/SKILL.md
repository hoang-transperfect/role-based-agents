---
name: designer-ui
description: >
  Writes the story spec for one user story in three sequential phases: (1) IA & UX flows —
  information architecture changes and all flow cases (happy, alternate, edge, error, empty,
  loading); (2) wireframe — a lo-fi layout spec of affected screens confirmed by the user before
  visual design begins; (3) visual spec — the affected artifact map and AC alignment that feeds
  organism, template, and page skills. This is the per-story design record connecting the business
  requirement to the UI changes. Invoke after designer-scan-context (and designer-research if in
  plan), before the artifact-level skills (designer-organism, designer-template, designer-page).
  One story-spec.md per user story; artifact specs are updated separately by their own skills.
---

# designer-ui

The story spec is the immutable audit record of a user story's design intent. It answers three
questions in order — and the designer confirms each answer before the next phase begins:

1. **What can happen on screen?** (IA & UX flows — all cases)
2. **What does the layout structure look like?** (wireframe — lo-fi, confirmed before hi-fi)
3. **Which design artifacts change, and how do flows map to acceptance criteria?** (visual spec)

The story spec does **not** describe what components look like — that belongs in the artifact
specs (organism/template/page). It references artifacts by name and describes flows and structure.

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

**Phase 1 — IA & UX flows:**
- **IA changes are explicit**: any sitemap, navigation, or entry-point change this story
  introduces is stated. If none, state "none" — never leave it blank.
- **Every case is covered** — happy path, alternate paths, edge cases, error states, empty
  states, loading states. BA acceptance criteria are the minimum; go beyond for edge/error cases.
- **Every flow step is unambiguous** — a developer or designer reads it without guessing.
- **Every decision/branch is explicit** — every conditional is called out, not implied.

**Phase 2 — Wireframe:**
- **Skipped correctly in maintain mode** — if sub-mode is maintain and no structural change,
  both IA and wireframe sections are marked "Skipped — maintain mode, non-structural". Any
  other case must have a wireframe.
- **Every affected screen has a wireframe section** — zones, nav placement, primary content,
  key elements, and any responsive note.
- **No DS component references** — zone names only (e.g. "Sidebar zone" not "FilterPanel"). The
  visual spec layer assigns DS components to zones.
- **User has confirmed the wireframe** before the skill proceeds to Phase 3.

**Phase 3 — Visual spec:**
- **AC alignment is complete** — every acceptance criterion maps to at least one flow case. No AC
  left unmapped. If a criterion cannot be mapped, surface it as an open question.
- **Affected artifacts are listed** — every organism/template/page this story changes is named
  with a link to its spec file and a one-line description of what changes.

---

## The 3-gate flow

### Gate 1 — Input
Verify the BA user story and acceptance criteria exist. Verify `related-context.md` has the
affected artifacts map. If either is missing, hand back to the appropriate skill first.

### Gate 2 — Process (three phases)

Work through each phase with the designer. Complete and confirm each phase before starting the
next — do not jump ahead.

**Maintain mode check (run before Phase A):**
If sub-mode is **maintain**, ask the designer two questions before proceeding:
1. Is the layout/structure of any affected screen changing? (new zones, reordered sections,
   navigation changes)
2. Is this a structural or high-risk behaviour change?

If **no** to both → skip Phase A (IA) and Phase B (wireframe). Record in the story spec:
`IA: no structural change` and `Wireframe: skipped — maintain mode, non-structural`. Proceed
directly to Phase C.

If **yes** to either → run all three phases as normal.

---

#### Phase A — IA & UX flows

Map any IA changes this story introduces (new page, renamed nav item, new entry point). Then
work through all flow cases using the BA acceptance criteria as the starting checklist, probing
for what they don't cover:

- **Edge cases**: 0 items, max items, very long text, concurrent actions?
- **Error states**: network failure, permission denied, validation failure, server error?
- **Empty states**: first-time use, no results, no content yet?
- **Loading/async**: what does the user see while waiting?
- **Alternate paths**: any valid route to the same goal other than the main path?

For each flow case, note which acceptance criterion it satisfies — or mark it as a robustness
case that goes beyond the AC.

Present the IA and UX flows section and ask the user to confirm before moving to Phase B.

---

#### Phase B — Wireframe (lo-fi layout)

For each screen affected by this story, sketch the layout structure in text — zones, rough
element placement, navigation position. No DS component references at this stage. The wireframe
answers: "Does the layout structure make sense?" before visual design begins.

Guide the designer with these questions:
- What are the main layout zones on this screen? (header, sidebar, main, footer, modal, etc.)
- Where does navigation sit, and what key nav elements are present?
- What is in the primary content zone for this flow?
- What are the most important UI elements and roughly where do they sit?
- Does the layout change at smaller breakpoints?

Present the wireframe section and ask the user to confirm the structure before proceeding.
**Do not move to Phase C until the wireframe is confirmed.**

---

#### Phase C — Visual spec

Map each AC to a flow case and list all design artifacts affected by this story. This section
feeds the artifact skills (designer-organism, designer-template, designer-page).

---

Write the story spec:

```markdown
# Story Spec — <Story ID>: <Story title>

**Business spec:** [<Story ID>](<path to story in ba-requirement/>)
**Work mode:** from-scratch / develop / maintain

## IA & Navigation
<!-- If maintain mode AND non-structural: replace section body with "Skipped — maintain mode, non-structural" -->
- **Sitemap change:** <new page / renamed page / removed page, or "none">
- **Navigation change:** <new nav item / updated label / removed entry, or "none">
- **Entry points:** <how users reach the affected screens for this story>

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

## Wireframe
<!-- If maintain mode AND non-structural: replace section body with "Skipped — maintain mode, non-structural" -->
_Lo-fi layout of affected screens — zones and structure only, no DS component refs_

### <ScreenName>
- **Zones:** <header / sidebar / main / footer / modal — list all present>
- **Navigation placement:** <where nav sits and what key items appear>
- **Primary content zone:** <what fills the main zone in the default state>
- **Key elements:** <essential UI elements and their rough position on screen>
- **Responsive note:** <layout change at smaller breakpoints, or "none">

## Affected design artifacts
| Artifact | Type | Spec | What changes |
|---|---|---|---|
| <OrganismName> | product organism | [link](../../product-organisms/<name>/organism-spec.md) | <one-line description> |
| <TemplateName> | template | [link](../../templates/<name>/template-spec.md) | <one-line description> |
| <PageName> | page | [link](../../pages/<name>/page-spec.md) | <one-line description> |

## AC alignment
| Acceptance criterion | Covered by |
|---|---|
| AC-1: <text> | Happy path — step 3 |
| AC-2: <text> | Error state — network failure |
| AC-3: <text> | Empty state |
```

### Gate 3 — Output
Check against the Output Quality Criteria — all three phases. Ensure every AC is mapped, every
decision/branch in the flows is explicit, every affected screen has a confirmed wireframe, and
all DS component references are absent from the wireframe section.

Also verify:
- **Business spec field** — `story-spec.md` must have the BA story link filled in (not blank or
  placeholder). If it is missing, do not proceed — ask the user for the story ID.
- **Affected artifacts are named** — every organism in the Affected artifacts table is either a
  named DS organism or flagged for `designer-organism`. No invented or unnamed components.

When the bar is met:
1. Present the full story spec and ask the user to confirm.
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
