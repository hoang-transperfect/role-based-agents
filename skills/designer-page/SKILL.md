---
name: designer-page
description: >
  Creates or updates a page spec — the full current state of one product page: which template
  it uses (or its own inline layout), which organisms occupy which zones, and page-level layout
  rules and responsive behaviour. Invoke after designer-ui has written the story spec for a user
  story that creates or changes a page, or when designer-review finds a page spec is missing or
  incomplete. Always rewrites the page spec in full to reflect current state — never patches.
  Produces design-spec/pages/[name]/page-spec.md. One spec per page; all stories that change
  this page update the same file.
---

# designer-page

The page spec is the **full current state of one product page**. It answers "what does this page
look like right now?" — which template structures it, which organisms populate each zone, and
what layout and responsive rules apply.

Because the page spec is always current, it is rewritten in full whenever a story changes it.
The story spec (`story-spec.md`) records what changed and why; the page spec records only the
resulting state.

## Where things live

- **Read** the story spec (`design-spec/<epic>/<feature>/<story>/story-spec.md`) — to understand
  what this story changes on this page.
- **Read** the existing page spec at `<real_project_path>/design-spec/pages/<page-name>/page-spec.md`
  if it exists (update path); create the folder if it does not (from-scratch).
- **Read** the template spec at `<real_project_path>/design-spec/templates/<name>/template-spec.md`
  if the page uses a template.
- **Read** organism specs (DS organisms or `design-spec/product-organisms/`) for any organisms on
  this page.
- **Write** (or overwrite) `<real_project_path>/design-spec/pages/<page-name>/page-spec.md`.

---

## The skill contract

### Inputs
- The story spec (what changes on this page for this story).
- The existing page spec, if one exists (read before rewriting).
- The template spec this page uses, if applicable.
- Organism specs for organisms on this page.

### Input Acceptance Criteria
- The story spec for the current story exists and is confirmed (from `designer-ui`).
- If updating: the existing page spec is read before any changes are made — never overwrite
  without reading first.
- All organisms referenced on this page are named (DS or product-specific). If a needed organism
  is missing its spec, hand off to `designer-organism` first.
- The template this page uses is named (DS template or `design-spec/templates/`). If a template
  spec is missing, hand off to `designer-template` first.

### Outputs
- `<real_project_path>/design-spec/pages/<page-name>/page-spec.md` (full current state)

### Output Quality Criteria
- **Full current state** — the page spec reflects the page after this story's changes are applied,
  not just the delta. A reader can understand the entire page from this file alone.
- **Template or inline layout declared** — every page either references a named template or
  defines its own layout zones inline (if the layout is unique to this page).
- **Every zone is specified** — all zones from the template are filled with the organism for this
  page, including any zones that are conditionally present.
- **Organisms are named from DS or product-organisms** — never invented inline. Missing organisms
  are flagged as DS gaps (⚠) if they should be in the DS, or handed to `designer-organism` if
  they are product-specific.
- **Stories that have changed this page are tracked** — so a developer knows the history.

---

## The 3-gate flow

### Gate 1 — Input
Check that the story spec exists and the affected organisms/template are specced. If the page
already exists, read it before writing. If any dependency is missing, hand off first.

### Gate 2 — Process
Construct the full current state of the page. If updating an existing spec: start from the
current spec, apply the story's changes, then write the complete updated spec. Do not carry
forward anything that is no longer correct after the story's changes.

Write the page spec:

```markdown
# <PageName> — page spec

_Stories that have changed this page: [US-01](path), [US-04](path)_

## Template
[<TemplateName>](../../templates/<name>/template-spec.md)
OR
**Inline layout** (unique to this page)

## Zone assignments
| Zone | Organism | Notes |
|---|---|---|
| Header | NavigationBar (DS) | — |
| Sidebar | FilterPanel ([product](../../product-organisms/filter-panel/organism-spec.md)) | Desktop only |
| Main content | <varies by page state — see below> | |
| Footer | PageFooter (DS) | — |

## Page states

### Default state
- Main content zone: **DataTable** (DS organism) — shows all items
- Sidebar: expanded by default on desktop

### Loading state
- Main content zone: **SkeletonTable** (DS atom) × 3 rows

### Empty state
- Main content zone: **EmptyState** (DS organism) — "No items yet"
  - Primary action: **Button / Primary** "Create first item"

### Error state
- Main content zone: **ErrorMessage** (DS organism) — "Something went wrong"
  - Secondary action: **Button / Secondary** "Try again"

## Layout rules
- Max content width: 1200px, centred
- Spacing between zones: `spacing.xl`
- Sidebar collapses to drawer below 1024px (see template spec)

## DS gaps
- ⚠ <component>: missing from DS — needs DS update before build.
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that the spec is a complete current state
(not a delta) and every zone is filled. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the page spec, tick Step 3c in `## Plan`, update **Next step**, then
   hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The completed page spec feeds `designer-review`, which validates that every page listed in every
story spec in scope has a complete, current page spec file.
