---
name: designer-template
description: >
  Creates or updates a layout template spec — the reusable page-level structure defining the
  grid system, named slots, responsive reflow, scroll behavior, navigation, loading strategy,
  structural content, and full landmark/accessibility map for every page that uses it, without
  real content. Invoke when a story spec (designer-ui) lists a template that needs a spec or an
  update, or when the designer needs an explicit layout contract before writing page specs. If the
  template already has a spec, reads it first then rewrites it in full. Produces a dedicated
  template-spec.md under design-spec/templates/. Run after designer-organism (so all organisms are
  named) and before designer-page. If a layout is used only once, it may be defined inline in the
  page spec instead — only create a dedicated template when it is reused across multiple stories.
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
- **Layout**: grid (columns, gutters, margins, max-width) documented with tokens; layout method described per region; ASCII or prose diagram present.
- **Slots**: all named regions defined with required flag, max children, allowed content types, and empty-state behavior. Each slot references an organism by name — no inline component definitions.
- **Responsive**: all four breakpoints (Mobile/Tablet/Desktop/Wide) covered; reflow strategy explains what stacks/hides/collapses and why; mobile-specific patterns present or explicitly skipped.
- **Scroll**: scroll containers and sticky elements identified; scroll restoration and anchor scroll behavior defined.
- **Navigation**: primary navigation documented; secondary navigation, breadcrumbs, and global keyboard shortcuts present or explicitly skipped with justification.
- **Loading**: initial skeleton described per slot; progressive loading order listed with priority reasoning; above-the-fold requirement defined.
- **Content**: structural strings documented; text expansion and overflow rules for navigation labels and breadcrumbs present.
- **Accessibility**: landmark structure complete (every landmark has a unique label where needed); skip link is first focusable element targeting correct ID; `<h1>` appears exactly once per page — template does not inject its own; focus on route change specified; live regions in DOM on initial mount.
- **Cross-template**: transitions and persistent regions documented.

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

Identify the shared layout structure across the stories in scope. Work through each section of
the spec with the designer. Write the template spec:

```markdown
---
name: {template-name}
version: 0.0.1
description:
link:
  - {tool-name}: {tool-link}
---
# {Template Name}

Templates define page structure only — slots, regions, grid, scroll, and navigation rules. They contain no real content and have no visual states. Organisms placed inside slots own their own appearance.

---

## Layout

Define the page-level grid system and how regions are arranged within it.

### Grid

| Property | Value | Token |
|----------|-------|-------|
| Column count | | |
| Gutter width | | |
| Outer margin / padding | | |
| Max content width | | |
| Centering strategy | | |

### Layout method
Describe the layout strategy per region (CSS Grid / Flexbox / combination).

### Layout diagram
Illustrate how regions are arranged spatially.

```
{ASCII layout diagram showing named regions}
```

---

## Slots

Define every named region this template exposes. Slots are the contract between the template and the organisms placed inside it.

| Slot name | Required | Max children | Allowed content types | When empty |
|-----------|----------|--------------|----------------------|------------|
| `{slot}` | Yes / No | {n} / unlimited | {types} | collapse / placeholder / hidden |

---

## Responsive

Templates are the primary level where page-level reflow is decided.

### Breakpoints

| Breakpoint | Layout change |
|------------|--------------|
| Mobile < 640px | |
| Tablet 640–1024px | |
| Desktop > 1024px | |
| Wide > 1440px | |

### Reflow strategy
Describe what stacks, hides, collapses, or reorders at each breakpoint. Note which slot visibility changes.

### Mobile-specific patterns
(Skip if not applicable.) Patterns that only apply on mobile — e.g. hamburger replacing sidebar, bottom navigation, drawer overlay.

### Density rules
(Skip if not applicable.) Compact vs comfortable spacing per breakpoint.

---

## Scroll

### Scroll containers
List any region that scrolls independently from the page.

| Region | Scrolls independently | Overflow | Notes |
|--------|----------------------|----------|-------|
| `{region}` | Yes / No | auto / scroll | {notes} |

### Sticky elements
List elements that stick during scroll.

| Element | Sticks at | Releases at |
|---------|-----------|-------------|
| `{element}` | {position} | {condition} |

### Scroll restoration
Behavior on browser back / forward navigation: restore position / reset to top.

### Scroll to anchor
Supported: Yes / No. If Yes, offset for sticky header: {value}.

---

## Navigation

(Skip any sub-section that does not apply to this template.)

### Primary navigation
- Location: top / left sidebar / bottom
- Mobile collapse behavior: {e.g. hamburger, drawer, bottom bar}
- Active state indication: {e.g. highlight, underline, icon fill}

### Secondary navigation
- Location: {position}
- Type: tabs / breadcrumbs / sub-nav / none

### Breadcrumbs
- Position: {position}
- Max items before collapsing: {n}
- Mobile behavior: {e.g. show last 2 items only}

---

## Loading

### Initial skeleton
Describe which slots show a skeleton before content loads, and what the skeleton structure looks like.

### Progressive loading
List slots in the order they should become interactive (highest priority first).

1. {slot} — {reason for priority}

### Above-the-fold requirement
What must be visible and interactive within the first render: {describe}

---

## Content

Templates contain no real content. This section covers only structural strings that are part of the template itself.

### Structural strings

| String ID | Default text | Context | Translatable? |
|-----------|-------------|---------|---------------|
| `{id}` | {text} | {where it appears} | Yes / No |

### Text expansion
- Navigation label overflow behavior: truncate with tooltip / wrap
- Breadcrumb overflow behavior: {e.g. collapse middle items}
- RTL: see Accessibility > Internationalization

---

## Accessibility

Templates define the full landmark map for every page that uses them. Mark any section N/A with justification if it does not apply.

### Landmark structure
Every template must establish the complete landmark map. When multiple landmarks of the same type exist, each must have a unique `aria-label`.

| Element | `aria-label` | Purpose | Required |
|---------|-------------|---------|----------|
| `{element}` | {label or —} | {purpose} | Yes / No |

### Skip links
Skip links must be the first focusable elements in the DOM and visible on keyboard focus.

- "Skip to main content": required on every template
- Skip link target ID: `#{id}`
- Additional skip links (e.g. "Skip to navigation"): list if present
- Skip links visible on focus: Yes — must never be permanently hidden

### Heading hierarchy
The template defines where `<h1>` lives but does not render it — page content supplies the text.

- `<h1>` location in template: {e.g. first child of main slot}
- `<h1>` count per page: exactly 1 — template must not inject its own
- Expected nesting under `<h1>`: {e.g. h2 for major sections, h3 for sub-sections}

### Focus on route change
When a new page using this template mounts via client-side navigation:

- Focus goes to: `<h1>` of new page / skip link / top of `<main>`
- Method: programmatic `focus()` on target element
- Screen reader announcement: via `document.title` change + focus target

### Global keyboard shortcuts
(Skip if not applicable.) Shortcuts available across all pages using this template.

List only shortcuts owned at the template level. Component-level shortcuts are owned by their specs. Shortcuts must not override browser or OS defaults.

| Shortcut | Action |
|----------|--------|
| `{key}` | {action} |

### Live regions
Template-level live regions must exist in the DOM on initial mount — not injected dynamically — so screen readers register them.

| Region | `aria-live` | Purpose |
|--------|-------------|---------|
| `{region}` | `polite` / `assertive` | {purpose} |

Use `assertive` only for time-critical events (session expiry, destructive confirmations). Prefer `polite` for everything else.

### Internationalization
- RTL layout mirrors fully: Yes / No — list any elements that do not mirror
- `dir` attribute: inherits / always LTR / always RTL
- Vertical scripts (e.g. traditional CJK): supported / not supported

---

## Cross-template

### Transitions between templates
Describe the visual transition when navigating from this template to another (fade / slide / none / inherits global setting).

### Persistent regions
List any regions that survive a template change without unmounting (e.g. global nav, notification tray, audio player).

| Region | Persists across | Notes |
|--------|----------------|-------|
| `{region}` | {templates} | {notes} |

---

## Checklist

All items must pass or be explicitly waived with justification before status moves to **Approved**.

### Spec
- [ ] Layout: grid system, layout method, and layout diagram documented
- [ ] Slots: all named regions defined with required flag, max children, allowed content, and empty-state behavior
- [ ] Responsive: all four breakpoints defined; reflow strategy and mobile patterns documented
- [ ] Scroll: scroll containers and sticky elements identified or explicitly skipped
- [ ] Navigation: primary navigation defined; secondary sections present or explicitly skipped
- [ ] Loading: initial skeleton, progressive loading order, and above-the-fold requirement defined
- [ ] Content: structural strings documented or marked N/A
- [ ] Accessibility: landmark structure, skip links, heading hierarchy, focus on route change, and i18n documented

### Design
- [ ] All slot regions defined with correct names and empty-state behavior
- [ ] Grid system documented (columns, gutters, margins)
- [ ] Responsive reflow demonstrated at all breakpoints
- [ ] All supported themes verified
- [ ] Sticky elements and independent scroll containers identified
- [ ] RTL layout reviewed (if shipped in any RTL locale)
- [ ] {template-specific item}

### Engineering
- [ ] Landmark structure matches spec exactly
- [ ] Skip link is first focusable element and targets correct ID
- [ ] `<h1>` appears exactly once per page — template does not inject its own
- [ ] Focus management on route change implemented
- [ ] Live region zones exist in DOM on initial mount
- [ ] CLS score < 0.1 — dynamic region dimensions reserved upfront
- [ ] {template-specific item}

### QA
- [ ] Cross-browser smoke test at all breakpoints
- [ ] Skip link works: Tab → Enter navigates to main content
- [ ] Screen reader announces route change correctly
- [ ] Mobile virtual keyboard — sticky bottom bar position correct
- [ ] Visual regression baseline captured per breakpoint
- [ ] {template-specific item}
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that slots reference organisms by name,
accessibility landmark structure is complete, skip link is first focusable element targeting
correct ID, and live regions are in DOM on initial mount. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick Step 3b in `## Plan`, update **Next step**, then
   hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The template spec feeds `designer-page`. Each page spec declares which template it uses and then
specifies only the page-level content and states for each organism zone. All subsequent stories
that change this template update the same spec file — rewriting it in full.
