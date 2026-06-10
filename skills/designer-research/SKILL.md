---
name: designer-research
description: >
  Builds the user understanding needed before flows and UI specs are written — personas,
  jobs-to-be-done, and a heuristic or competitive review of existing patterns. Invoke when a
  designer is starting from scratch or developing a significant new feature and needs to understand
  who the users are and what they are trying to achieve before designing. Skip or run lightly in
  maintain mode or when a strong user-insights.md already exists from prior work on this project.
  Run after designer-plan so it targets the right users and stories, and before designer-ui so
  flows reflect real user goals rather than assumptions.
---

# designer-research

Good flows and UI specs require a clear picture of who the users are, what they're trying to
achieve, and what patterns already exist in the space. This skill builds that picture — enough
to inform design decisions, not a research project for its own sake.

In **from-scratch** mode, this step often makes the difference between designing the right
experience and designing the obvious one. In **develop** mode, it's a lighter check: do the
existing personas and JTBD still hold for the new feature? In **maintain** mode, it's typically
skipped.

## Where things live

- **Read** user stories in scope from the `## Plan` in the task file.
- **Read** `related-context.md` for any existing personas, research, or user documentation
  already found by `designer-scan-context`.
- **Write** the result as `<real_project_path>/designer-artifacts/tasks/<task-id>/user-insights.md`.

---

## The skill contract

### Inputs
- The `## Plan` from the task file (user stories in scope, work mode).
- The `related-context.md` artifact from `designer-scan-context` (any existing user research,
  personas, or competitive material already found).
- Any user research, analytics, or user feedback the designer can share.

### Input Acceptance Criteria
- The user stories in scope are known (from the plan).
- Work mode is known. If mode is maintain, confirm with the user whether research is needed
  before running — it is typically skipped.

### Outputs
- `<real_project_path>/designer-artifacts/tasks/<task-id>/user-insights.md`

### Output Quality Criteria
- **Personas** cover the key user types for the stories in scope: name/type, goal, context, and
  pain points relevant to this design effort. Not exhaustive archetypes — just enough to make
  design decisions against.
- **Jobs-to-be-done (JTBD)** for each story: what is the user trying to accomplish (the job),
  and what currently gets in the way (the friction)?
- **Heuristic or competitive review** notes 2–4 relevant patterns from comparable products or the
  existing product — what works, what doesn't, what patterns are established in this space.
  Grounded in something real (a named product, an existing screen), not generic best practice.
- Insights are **actionable**: each finding connects to a design implication (e.g. "users expect
  inline validation → avoid submit-only error messages").
- The file doesn't bloat. Research that doesn't directly inform the flows or UI specs for these
  stories doesn't belong here.

---

## The 3-gate flow

### Gate 1 — Input
Check inputs against Acceptance Criteria. If mode is maintain and research isn't needed, confirm
with the user and tick the step as `~~skipped~~ (maintain mode)`. If the stories in scope are
unclear, ask before proceeding.

### Gate 2 — Process
Work with the designer to build the user picture. If the designer has research, analytics, or
feedback: use it — don't ask them to repeat what they know; capture it. If this is greenfield,
discuss personas and JTBD together, drawing from the BA's user stories as the source of user goals.

For the heuristic/competitive review, ask the designer which comparable products or existing
screens are relevant — don't invent comparisons.

Draft the user-insights artifact:

```markdown
# User Insights — <design need>

## Personas
### <Persona name / type>
- **Goal:** <what they're trying to achieve>
- **Context:** <when/where they use this>
- **Pain points:** <what frustrates or blocks them today>

## Jobs-to-be-done
| User story | Job (what they're trying to do) | Friction (what gets in the way today) |
|---|---|---|
| US-01 | <job> | <friction> |

## Heuristic / Competitive review
| Product / Screen | What works | What doesn't | Pattern to adopt or avoid |
|---|---|---|---|
| <name> | <…> | <…> | <…> |

## Design implications
- <Finding> → <what this means for the flows or UI>
```

### Gate 3 — Output
Check the draft against the Output Quality Criteria. When it meets the bar:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick Step 1 in the `## Plan` checklist, update **Next step**,
   then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
`user-insights.md` feeds `designer-ui`. The JTBD for each story and the design implications
are the most important inputs for shaping the UX flows in the story spec.
