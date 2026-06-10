---
name: ba-document
description: >
  Handles Business Analysis step 7 — turning prioritised, validated requirements into the formal
  agile backlog other teams build from. Invoke when a BA needs to write or update epics, features,
  and user stories, or when the task's ## Plan marks Step 7 as next. It authors the Epic → Feature
  → User Story tree as markdown in the real project's ba-requirement folder — each story clear,
  uniquely ID'd, and testable (Given/When/Then acceptance criteria), with non-functional,
  service-level, and transition needs explicitly captured and terminology kept consistent via a
  shared glossary — then ticks the checklist box. Behaviour adapts to the
  work mode (build the tree from scratch, extend it, or update a story in place).
---

# ba-document

Covers **Step 7 (Document Requirements)**. This is where validated requirements become the formal
**agile backlog** — the Epic → Feature → User Story tree that Designers and Developers build from
(tracked alongside Bitbucket). The bar is high because other teams act on this directly: every
story must be **clear, traceable, and testable**, and the easily-forgotten things — non-functional
requirements and the end-to-end service view — must be captured, not dropped.

## Where things live

- Read `real_project_path` from the project's index file
  (`<assistant-folder>/projects/<project-slug>.md`).
- Write the formal backlog under `<real_project_path>/ba-requirement/` as markdown:

```
ba-requirement/
  epic-01-<slug>/
    epic.md                      # EPIC-01: goal, scope, linked features
    feature-01-<slug>/
      feature.md                 # FEAT-01: description + its user stories (US-001…) with AC
  non-functional.md              # NFR-01…: cross-cutting NFRs, linked to the features they constrain
  transition.md                  # TR-01…: transition requirements (migration, training, cutover) — temporary by nature
  glossary.md                    # Shared terms (ubiquitous language) — one meaning per term; all items use these terms
```

- IDs: `EPIC-01`, `FEAT-01`, `US-001`, `NFR-01`, `TR-01` — unique and never reused. **Read the
  existing tree first** and continue numbering from the highest used, so develop/maintain work never
  collides with or renumbers what's already there. To find the next free number per prefix:

  ```bash
  grep -rhoE 'EPIC-[0-9]+|FEAT-[0-9]+|US-[0-9]+|NFR-[0-9]+|TR-[0-9]+' "<real_project_path>/ba-requirement/" 2>/dev/null \
    | awk -F- '{n=$2+0; if (n>m[$1]) m[$1]=n} END{for (p in m) printf "%s next: %d\n", p, m[p]+1}'
  ```
- Tick Step 7 in the task file's `## Plan` checklist when confirmed. (Working notes for this task
  stay in the task folder `ba-assistant-artifacts/tasks/<task-id>/`; only the formal backlog goes
  in `ba-requirement/`.)

---

## The skill contract

### Inputs
- `ba-assistant-artifacts/tasks/<task-id>/prioritised-requirements.md` from `ba-analyse`.
- The existing `ba-requirement/` tree (for develop/maintain — what to extend or change).
- The stakeholder register (who each item serves) and the business problem.

### Input Acceptance Criteria
- A prioritised, validated requirements set exists. If requirements are still unvalidated or
  unranked, hand back to `ba-analyse` — publishing assumptions as a formal backlog is exactly what
  this step must avoid.
- For `develop`/`maintain`: the relevant part of the existing tree has been located (via
  `ba-scan-context`). If it wasn't, find it before writing, so you extend/edit rather than
  duplicate.

### Outputs
- New or updated `epic.md` / `feature.md` files (and `non-functional.md`, `transition.md`,
  `glossary.md`) under `ba-requirement/`.

### Output Quality Criteria
- **Hierarchy is sound:** every story sits under a feature, every feature under an epic. A story
  that's really an epic (too big to build/test as one increment) is split.
- **Clear:** each item is unambiguous — a developer/designer can't reasonably read it two ways.
- **Gathered, not invented:** every item, behaviour, and acceptance criterion traces to a
  requirement actually gathered/validated (`prioritised-requirements.md` / findings). Never
  fabricate variants, states, behaviours, business rules, or AC to satisfy the template or the
  see/do/get fields. If a field would require inventing, **omit it or mark it deferred** — a
  thin-but-true backlog beats a rich-but-fabricated one. A story may legitimately be as small as
  *"provide a shared `<component>`, consistent with the design system."*
- **Design/UI detail stays out:** the BA backlog states *what capability* is needed and *why*, not
  how it looks or behaves visually. Appearance, variants, visual states, and interaction behaviour
  belong to the design requirement (Design's) — reference it, don't restate it. Especially for
  UI-component-library work.
- **Traceable:** each item has a unique ID and references its source (prioritised requirement /
  finding), so it can be traced **back to its origin**. (Forward tracing to design/build/test
  belongs to the delivery teams in their tools — not the BA backlog.)
- **Testable:** each story has acceptance criteria in **Given/When/Then** form. If you can't write
  the test, the story isn't specified well enough yet.
- **Behaviour is explicit (see / do / get):** each story states what **information the user must
  see**, what **actions** they can take, and what **response** each action returns — success *and*
  failure — never left to inference from the story sentence.
- **Ready for other teams (Definition of Ready):** each story carries enough *functional* context
  that **Design can write its design requirement and Dev can build — without coming back to the
  BA**: the see/do/get **behaviour**, business rules, roles/permissions, dependencies, error/edge
  cases, and explicit out-of-scope. (Experience/UX is Design's to define; analytics only when the
  BA has raised it.) A field left blank that a team would need is a defect in the item.
- **Non-functional requirements are explicit** — performance, usability, accessibility, security —
  captured as their own `NFR-*` items and linked to the features/stories they constrain, not
  buried or assumed.
- **Transition requirements are explicit** — data migration, training, cutover, parallel running,
  decommissioning — captured as their own `TR-*` items linked to the features they enable, each
  marked with when it retires: they describe **getting to** the future state, not the future state
  itself, so they must not linger as permanent requirements.
- **Terminology is consistent (glossary):** every domain term means one thing, defined in
  `glossary.md`. New terms are added with a definition; synonyms for an existing concept are
  replaced with the glossary term. Two names for one concept — or one name for two — is a defect
  in the backlog.
- **The functional user flow is documented** — main flow plus **alternate/exception paths** — at
  the feature level (epic level for a cross-feature journey; story level only when a single story's
  sequence is non-trivial). This is the end-to-end journey, not the UI (Design's). Exception
  branches must be explicit — that's where requirements are usually weakest.
- **Service-level perspective is represented** — end-to-end journeys, governance, support/
  operational needs — not only discrete features.
- **Priority carries through:** each story keeps the MoSCoW/Kano priority agreed in `ba-analyse`.
- **Goals trace down:** the epic's goal and success metrics align with the Plan's Problem framing
  (objectives + success criteria) — the backlog serves the stated problem, not a drifted one.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If requirements aren't validated/prioritised,
hand back to `ba-analyse`; for develop/maintain, make sure you've located the existing tree first.
Do not assume. (Tree already clean from the session-start guard.)

### Gate 2 — Process
Author the backlog, adapting to the **work mode** recorded in `## Plan`:

- **from-scratch** — derive epics from the big capabilities, break each into features, then write
  stories. Build the whole tree.
- **develop** — slot new stories under the right existing feature/epic, or add a new feature/epic;
  assign the next free IDs; keep existing items intact.
- **maintain** — edit the affected story/feature in place; keep its ID; note what changed (the
  change record itself is `ba-govern`'s job).

Write items in these shapes. Fill every field a consuming team would need **from what was actually
gathered** — a thin field forces a round-trip back to the BA. But **never invent content to fill a
field**: if the requirement wasn't gathered, or it's design/UX detail, omit the field or mark it
deferred rather than fabricating it. Completeness means capturing all *known* facts, not
manufacturing plausible ones.

```markdown
# EPIC-01 — <name>
**Goal / outcome:** <the capability and the business outcome it delivers>
**Business value / why:** <the problem it solves>
**Success metrics:** <how we'll know it worked>
**Scope:** In — <…> · Out — <…>
**Owner / sponsor:** <who>   **Priority:** Must
**Features:** FEAT-01, FEAT-02
**Dependencies / constraints:** <other epics, systems, regulatory>

# FEAT-01 — <name>   (epic: EPIC-01)
**Intent / user value:** <what this feature enables and for whom>
**Scope:** In — <…> · Out — <…>
**Stories:** US-001, US-002       **Applies NFRs / TRs:** NFR-01, TR-01
**Dependencies:** <APIs, other features>     **Open questions:** <…>
**User flow (functional — not UI):**
  _Main flow:_ 1. <step> → 2. <step> → 3. <step>
  _Alternate / exception flows:_ 2a. <branch>; 3a. <exception → which story handles it>

## US-001 — <title>   (feature: FEAT-01)
**Priority:** Must   **Source:** <req/finding ref>   **Status:** ready / provisional
**Story:** As a <role>, I want <capability> so that <benefit>.
**Roles / permissions:** <who may perform this>
**Preconditions / trigger:** <entry state; what starts the flow>
**Behaviour (what the user sees / does / gets):**
- **Information shown:** <data/elements the user must see — conceptual, not UI layout>
- **Actions available:** <what the user can do here>
- **Responses:** <what each action returns — the success result *and* the failure/feedback>
**Acceptance criteria (Given/When/Then):**   *(verifies the behaviour above)*
- Given <context>, when <action>, then <result>.
**Business rules:** <the logic Dev must encode>
**Dependencies:** <other stories, systems, APIs>
**NFRs / constraints:** <which NFR-* apply>
**Error / edge cases:** <exceptional paths beyond the standard responses>
**Out of scope:** <explicit non-goals>
**Open questions / assumptions:** <…>

# NFR-01 — <category: performance/usability/accessibility/security>
**Requirement (measurable):** <target>   **Applies to:** FEAT-01, US-001
**Acceptance criteria:** <how verified>
**Priority:** Must   **Source:** <ref>   **Rationale:** <why it matters>

# TR-01 — <category: data-migration / training / cutover / parallel-run / decommissioning>
**Requirement:** <what must happen to move from the current state to the future state>
**Applies to:** FEAT-01   **Needed until:** <when it retires — transition requirements are temporary>
**Acceptance criteria:** <how verified>
**Priority:** Must   **Source:** <ref>   **Rationale:** <why the transition fails without it>

# Glossary — <project>   (glossary.md)
| Term | Definition | Avoid (synonyms) | Source |
|------|------------|------------------|--------|
| <term> | <one meaning, in business language> | <words people use that mean this> | <ref> |
```

**Conditional fields — add to a story only when they apply:**
- **Analytics / tracking** — include *only if the BA has raised* a tracking need; otherwise omit.
- **Experience / UX intent** — normally **omit**. Defining the experience/UX is **Design's** job
  (they author the design requirement). Add it only if a BA stakeholder has handed you an explicit
  experience requirement to pass on — and even then keep it to the requirement, not a UI design.

Discuss anything ambiguous with the BA rather than guessing intent.

### Gate 3 — Output
Check against the Output Quality Criteria — especially unique IDs (no collisions with the existing
tree), Given/When/Then testability, and explicit NFR/service-level coverage. Improve if short of
the bar (ask the user to clarify intent where needed; never assume). When it meets the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write/update the files under `ba-requirement/`, tick Step 7 in `## Plan`
   (links + **Next step**), then hand off to `commit-work` (real project repo).
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill`.

You author the backlog as the BA assistant, on the user's behalf, for the audit record.

---

## Handoff
- **Design and Dev** receive the requirement docs and continue in their own tools (Bitbucket):
  Design writes the design requirement (UI/UX), Dev builds and tests. That work — and its status —
  is **theirs to track, not the BA's**.
- **`ba-govern`** (Steps 8–9): stakeholder sign-off, then requirement **change management** and
  traceability **back to source** (the RTM). The BA's responsibility ends at the signed-off,
  change-managed requirement.
