---
name: designer-scan-context
description: >
  Discovers existing design artifacts and detects what is affected before any design work begins.
  In product-design mode: reads the BA user story, scans existing organism/template/page specs
  to find which ones the story touches (the blast radius), checks the design system source in
  resource.md, and lists any prior story specs for context. In design-system mode: scans existing
  component inventory, partial token definitions, and brand guidelines. Invoke at the start of
  any design effort, before designer-plan, whenever a designer asks "what already exists?",
  "what will this change affect?", "is there a design system?", or is about to start a new design
  task. Records a Related Context summary including an explicit affected artifacts map for
  product-design tasks. Use it whenever starting or re-scoping design work.
---

# designer-scan-context

The most expensive design mistake is starting work without knowing what already exists — or
discovering mid-task that a change cascades across more artifacts than expected. This skill
front-loads both discovery and blast-radius mapping: it finds what's already known and what
the incoming story will actually touch.

**Product-design mode** produces two critical outputs:
1. **Affected artifacts map** — which existing organisms, templates, and pages this story changes.
   `designer-ui` and the artifact-level skills depend on this to know what to update.
2. **Design system source** — whether a ready design system is defined in `resource.md`. Without
   this, `designer-plan` cannot decide whether artifact specs can proceed.

**Design-system mode** produces: a component inventory and any partial work already done
(foundations, component specs, brand guidelines) as the starting point for `designer-ds-audit`.

## Where things live

- **Search** the real project folder: read `real_project_path` from the project index file
  (`<assistant-folder>/projects/<project-slug>.md`).
- **Write** `<real_project_path>/designer-artifacts/tasks/<task-id>/related-context.md`
  (create the folder if needed).

## Where to look (search order)

**Always scan regardless of mode:**
1. **Project resources** at `<real_project_path>/designer-artifacts/resource.md` — look for
   any design system entry (Figma library link, npm package). Record as present (with source)
   or absent.
2. **Brand or style guidelines** — in `resource.md` and the real project folder.
3. **Prior tasks** — earlier task folders under `<real_project_path>/designer-artifacts/tasks/`
   for earlier design decisions.

**Product-design mode — additionally:**
4. **BA user story** at `<real_project_path>/ba-requirement/` — read the story's description and
   acceptance criteria to understand what is changing. This is required to detect affected artifacts.
5. **Affected artifact detection** — for each of the three artifact stores, search for specs that
   relate to the story's scope:
   - `<real_project_path>/design-spec/product-organisms/` — organism specs
   - `<real_project_path>/design-spec/templates/` — template specs
   - `<real_project_path>/design-spec/pages/` — page specs
   For each candidate, judge whether the story's change touches it: does the story add, modify,
   or remove something in that organism/template/page? List every affected one explicitly.
6. **Prior story specs** — `<real_project_path>/design-spec/<epic>/<feature>/<story>/story-spec.md`
   for earlier stories that touched the same artifacts, so the designer knows the history.

**Design-system mode — additionally:**
4. **Existing design system output** at `<real_project_path>/design-system/` — existing
   foundations and component specs.
5. **Existing component inventory** — component library, storybook, or UI framework in use
   (from `resource.md` or the project source code).

---

## The skill contract

### Inputs
- The user's stated design need or topic.
- The project index file (for `real_project_path`) and `resource.md`.
- The BA user story (for product-design mode affected artifact detection).

### Input Acceptance Criteria
- There is a stated need or topic specific enough to search against. If too vague, ask.
- A readable `real_project_path` exists, or the user supplies a location.
- For product-design mode: the user story ID is known so BA acceptance criteria can be read.
  If no story ID is given, ask — affected artifact detection requires knowing what is changing.

### Outputs
- `<real_project_path>/designer-artifacts/tasks/<task-id>/related-context.md`

### Output Quality Criteria
- **Design system source is explicit**: present (name + link from `resource.md`) or absent.
- **Product-design mode — affected artifacts are explicit**: every organism, template, and page
  the story touches is listed. If nothing is found, state that explicitly — it may mean all
  artifacts are new (from-scratch). An empty list with no explanation is not acceptable.
- **Product-design mode — prior story history** is noted for any artifact that has been touched
  before, so the designer knows what already changed and when.
- **Design-system mode**: existing foundations and components are inventoried.
- Gaps are stated explicitly. Relevance is honest.

---

## The 3-gate flow

### Gate 1 — Input
Check inputs. If the need is too vague, ask. For product-design mode, if no story ID is provided,
ask before scanning — affected artifact detection cannot proceed without knowing the story.

### Gate 2 — Process
Run the scan for the applicable mode. For affected artifact detection, read the story's acceptance
criteria, then walk each artifact store and judge relevance. Discuss with the designer where
needed — they often know about relationships not obvious from the files.

Draft the Related Context artifact:

```markdown
# Related Context — <story ID / design need>

_Scanned: <date> · Mode: product-design / design-system_

## Design system source (from resource.md)
**Present:** <name> · <link> · <type: Figma library / npm package / token file>
OR
**Absent:** No design system source found in resource.md.

## [Product-design mode] Affected design artifacts
_(Artifacts this story adds to or changes — updated in full by the artifact-level skills)_

| Artifact | Type | Spec location | What changes |
|---|---|---|---|
| <name> | product organism / template / page | <path> | <one-line description of the change> |

_None found — all artifacts for this story are new (from-scratch)._

## [Product-design mode] Prior story history for affected artifacts
| Artifact | Prior story | What was changed |
|---|---|---|
| <name> | [US-02](path) | Added loading state |

## [Design-system mode] Existing design system output
| Item | Location | Covers | Current? |
|---|---|---|---|

## [Design-system mode] UI framework / component library in use
| Library | Source | Notes |
|---|---|---|

## Brand & style guidelines
| Item | Location | Covers |
|---|---|---|

## Other relevant material
| Item | Location | Covers | Relation to the need |
|---|---|---|---|

## Gaps — not covered by anything above
- <what the design effort requires that no existing material covers>

## Notes for planning
- <implications: what can be reused, what must be created, what to verify>
```

### Gate 3 — Output
Check the draft against the Output Quality Criteria — especially that affected artifacts are
explicit and the design system source is unambiguous. Improve if short of the bar (ask the user;
do not assume).
1. Present and ask the user to confirm before writing.
2. **If confirmed** → write the file, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
`related-context.md` feeds `designer-plan`. In product-design mode, the affected artifacts map
and design system source are the two inputs `designer-plan` and `designer-ui` need most. In
design-system mode, the component inventory and partial work are the key inputs for
`designer-ds-audit`.
