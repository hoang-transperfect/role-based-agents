---
name: ba-discover
description: >
  Handles the first two Business Analysis steps — identifying stakeholders and planning how
  requirements will be gathered. Invoke when a BA is starting requirements work and needs to map
  who is affected and decide elicitation approach, when the task's ## Plan marks Step 1 or Step 2
  as next, or when the BA asks "who are the stakeholders?" or "how should we gather requirements?"
  It produces a stakeholder register and a requirements-gathering plan in the project's ba-artifacts
  folder, then ticks the matching boxes in the task file checklist. Run after ba-scan-context and
  ba-plan so it builds on existing context and an agreed scope.
---

# ba-discover

Covers **Step 1 (Identify Stakeholders)** and **Step 2 (Plan Requirements Gathering)**. Getting
these right is what stops a project gathering the wrong requirements from the wrong people — so
the work here is mapping *everyone* affected (not just the obvious sponsors) and choosing
elicitation techniques that actually fit those people and the problem.

## Where things live

- Read `real_project_path` from the project's `resource.md` frontmatter.
- Write deliverables to `<real_project_path>/ba-artifacts/<task-id>/` (create it if needed):
  `stakeholder-register.md` and `gathering-plan.md`.
- Tick Steps 1–2 in the task file's `## Plan` checklist when each is confirmed.

---

## The skill contract

### Inputs
- The task file (`## Plan` showing Steps 1–2 are in scope) and the `related-context.md` artifact
  from `ba-scan-context`.
- The business problem the effort is solving.
- An existing `stakeholder-register.md` from earlier work, if `ba-scan-context` surfaced one
  (common in `develop`/`maintain`, where stakeholders are mostly already known).

### Input Acceptance Criteria
- The business problem is framed (from `ba-plan`). If not, that context is missing → ask the user
  before mapping stakeholders, since who matters depends on what we're solving.
- A `## Plan` exists with Step 1 and/or Step 2 marked as needed. If planning hasn't happened, hand
  off to `ba-plan` first.

### Outputs
- `stakeholder-register.md` — every individual/group affected, with their role, interest,
  influence, and who holds sign-off authority.
- `gathering-plan.md` — objectives, scope, and a **detailed plan per session**: the technique, its
  objective, a prepared question/focus list tailored to that technique, probes for easily-missed
  areas, and space for notes.

### Output Quality Criteria
- The register covers the **full** range of affected parties, not just sponsors: end-users,
  project sponsors, SMEs, developers, and — per the service-level perspective — operations,
  support, and governance owners who live with the end-to-end service. Missing a stakeholder
  group here is the costliest gap, so probe for who's *implicitly* affected.
- Each stakeholder has role, interest, influence, and whether they sign off — enough to know who
  to involve for which decision.
- The gathering plan matches **technique to stakeholder and goal**: interviews for depth,
  workshops for collaboration/conflict, surveys for breadth, observation for tacit/real behaviour,
  document analysis for existing material (start from the `related-context.md` findings). The
  choice is justified, not generic.
- **Each session is prepared, not just named** — it lists the actual opening questions (or, by
  technique: the focus points to observe, the agenda/decisions for a workshop, the items to
  extract from a document), the **themes it must cover**, plus explicit probes for easily-missed
  areas (NFRs, edge cases and exceptions, the end-to-end journey). The guide's job is **coverage
  assurance**: it's an opening set the BA adapts live, not a fixed script — the multi-turn
  follow-up digging happens in `ba-elicit`, which tracks the session against these themes.
- Scope and objectives are explicit, so elicitation doesn't sprawl.

---

## The 3-gate flow

### Gate 1 — Input
Read inputs, check against Input Acceptance Criteria. If the business problem or plan scope is
missing, **ask the user** or hand back to `ba-plan` — do not assume. (The tree is already clean
from the session-start guard.)

### Gate 2 — Process
**If a stakeholder register already exists** (from earlier work / `develop`/`maintain`), don't
rebuild it — present it, confirm it's still accurate with the BA, and ask whether anyone should be
added or changed for this effort. Capture only the delta.

Otherwise, brainstorm with the BA from scratch. Suggest stakeholder groups they may have missed
(especially operational, support, and governance roles behind the obvious sponsors), and debate
which elicitation techniques fit. This is collaborative — propose, question, refine. Draft both
artifacts:

```markdown
# Stakeholder Register — <project>
| Stakeholder | Role | Interest in the outcome | Influence | Sign-off? |
|-------------|------|--------------------------|-----------|-----------|
| <name/group> | <e.g. end-user> | <what they need> | high/med/low | yes/no |
```

```markdown
# Requirements-Gathering Plan — <project>
**Objectives:** <what this elicitation must achieve>
**Scope:** <in / out>

## <Stakeholder group> — <technique>
**Objective:** <what this session must produce>
**Themes to cover:** <the areas this session must not leave without — ba-elicit tracks these>
**When / prep:** <timing · what to prepare or bring>
**Opening questions / focus:**   <!-- a starting set the BA adapts live, not a script. Adapt to
technique: questions for interview/survey · what to watch for observation · agenda + decisions to
reach for workshop · what to extract for document analysis -->
1. <question / focus point>
2. <…>
**Probe — don't forget:** NFRs (performance, usability, accessibility, security) · edge cases &
exceptions · the end-to-end journey, not just the happy path.
**Notes:** <pre-session context>

## <next stakeholder group> — <technique>
…
```

### Gate 3 — Output
Check both artifacts against the Output Quality Criteria — especially stakeholder coverage and
technique justification. Improve if short of the bar (ask the user where you need their knowledge,
never assume). When they meet the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write the files to `ba-artifacts/<task-id>/`, tick Steps 1–2 in the `## Plan`
   checklist (fill the artifact links, update **Next step**), then hand off to `commit-work`.
3. **If not satisfied** → improve with the user until confirmed, commit, then hand off to
   `improve-skill` to fold the lesson back into this skill.

You author both as the BA assistant, on the user's behalf, for the audit record.

---

## Handoff
The stakeholder register and gathering plan feed `ba-elicit` (Steps 3–4), which runs the chosen
techniques and documents what they surface.
