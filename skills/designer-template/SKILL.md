---
name: designer-template
description: >
  Creates or updates a layout template spec — the reusable page-level structure that defines
  which organisms occupy which zones on a screen (header, sidebar, main content, footer, etc.)
  and the layout rules between them, without real content. Invoke when a story spec (designer-ui)
  lists a template that needs a spec or an update, or when the designer needs an explicit layout
  contract before writing page specs. If the template already has a spec, reads it first then
  rewrites it in full. Produces a dedicated template-spec.md under design-spec/templates/. Run
  after designer-organism (so all organisms are named) and before designer-page. If a layout is
  used only once, it may be defined inline in the page spec instead — only create a dedicated
  template when it is reused across multiple stories.
---

# designer-template

A template is the **layout layer** of a screen — it answers "which organisms go where?" without
specifying what content they contain. Because templates are reusable across multiple pages (user
stories), defining them separately avoids repeating layout decisions in every page spec and gives
developers a stable layout contract independent of content changes.

Templates reference organisms by name only (DS organisms or product-specific organisms from
`design-spec/product-organisms/`). They do not spec content, states, or behaviour — those belong
in the page spec (`designer-ui`).

**When NOT to create a dedicated template:** if a layout is unique to a single user story, define
it inline in that story's page spec section rather than creating a template file that is never
reused.

## Where things live

- **Read** the story spec (`design-spec/<epic>/<feature>/<story>/story-spec.md`) to understand
  what is changing for this template and what the affected artifact entry says.
- **Read** the existing template spec at
  `<real_project_path>/design-spec/templates/<template-name>/template-spec.md` if it exists —
  always read before writing when the spec already exists.
- **Read** organism names from the DS and from `design-spec/product-organisms/`.
- **Write** (or overwrite) `<real_project_path>/design-spec/templates/<template-name>/template-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- The story spec that requires this template (from `designer-ui`) — to understand what is
  changing for this template.
- The existing template spec if this is an update (read before writing — never overwrite blind).
- Organism names available: DS organisms + any product-specific organisms already specced.

### Input Acceptance Criteria
- The story spec for the current story exists and is confirmed (from `designer-ui`).
- If creating: at least two user stories share a layout that warrants a dedicated template. If
  only one story uses this layout, recommend inline definition in the page spec instead.
- If updating: the existing template spec has been read before any changes are made.
- All organisms the template references are named (either in the DS or in
  `design-spec/product-organisms/`). If an organism is missing, hand off to `designer-organism`
  first.

### Outputs
- `<real_project_path>/design-spec/templates/<template-name>/template-spec.md`

### Output Quality Criteria
- **Zones are exhaustive** — every area of the layout is accounted for (including zones that are
  conditionally present, e.g. a sidebar that only appears on desktop).
- **Each zone references an organism by name** — no inline component definitions.
- **Layout rules are explicit** — spacing tokens between zones, max-width constraints, responsive
  breakpoints and how the layout changes at each breakpoint.
- **Stories using this template are listed** — so a developer knows the scope.

---

## The 3-gate flow

### Gate 1 — Input
If creating: confirm the template is used by multiple stories. If only one story uses it, advise
inline definition and skip this skill. If a template spec already exists, read it before
proceeding — this is an update. Verify all referenced organisms are named.

### Gate 2 — Process
If updating an existing spec: start from the current spec, apply the changes described in the
story spec, then write the complete updated spec. Do not carry forward anything that is no longer
correct after this story's changes.

Identify the shared layout structure across the stories in scope. Define each zone and its rules.

Write the template spec:

```markdown
# <TemplateName> — layout template

_Used in: <US-01 title>, <US-03 title>, …_

## Purpose
<1 sentence: what type of screen this template is for>

## Layout zones

| Zone | Organism | Position / size | Conditional? |
|------|----------|-----------------|--------------|
| Header | NavigationBar (DS) | Full width, sticky, 64px height | Always |
| Sidebar | FilterPanel (product) | 280px fixed, left | Desktop only (≥ 1024px) |
| Main content | — (filled by page spec) | Remaining width, `spacing.xl` padding | Always |
| Footer | PageFooter (DS) | Full width | Always |

## Layout rules
- Max content width: 1200px, centered
- Spacing between main zones: `spacing.xl`
- Sidebar collapses to a drawer (triggered by IconButton / Menu) below 1024px
- Main content becomes full width below 1024px

## Responsive behaviour
| Breakpoint | Change |
|---|---|
| < 768px | Sidebar hidden; NavigationBar collapses to hamburger |
| 768px – 1024px | Sidebar becomes collapsible drawer |
| ≥ 1024px | Full two-column layout |
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that every zone references an organism
by name and layout rules use spacing tokens. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick Step 3b in `## Plan`, update **Next step**, then
   hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The template spec feeds `designer-page`. Each page spec declares which template it uses and then
specifies only the page-level content and states for each organism zone. All subsequent stories
that change this template update the same spec file — rewriting it in full.
