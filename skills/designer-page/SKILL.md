---
name: designer-page
version: 0.0.1
description: >
  Creates or updates a page spec — the full current state of one product page: which template it
  uses and how its slots are filled, the page lifecycle states, responsive and print overrides,
  the complete set of exact approved copy (all visible strings, errors, empty states, success
  messages, help text, legal, localization), page-level accessibility, a completion checklist, and
  a launch checklist. Invoke after designer-ui has written the story spec for a user story that
  creates or changes a page, or when designer-review finds a page spec is missing or incomplete.
  Always rewrites the page spec in full to reflect current state — never patches. Produces
  design-spec/pages/[name]/page-spec.md. One spec per page; all stories that change this page
  update the same file.
---

# designer-page

The page spec is the **full current state of one product page**. It answers "what does this page
look like right now?" — which template structures it, which organisms populate each slot, what
states it can be in, and — uniquely at this level — the exact, approved copy for every string a
user can see.

Because the page spec is always current, it is rewritten in full whenever a story changes it.
The story spec (`story-spec.md`) records what changed and why; the page spec records only the
resulting state.

**Pages are the only level where content is real, not placeholder.** Every string in the Content
section must be exact, approved copy — no `{placeholder}` text ships without sign-off.

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
- Approved copy for every visible string (from the BA/content owner). If copy is not yet approved,
  flag the string as pending sign-off — never invent final copy.

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
- **Full current state** — the page spec reflects the page after this story's changes are applied, not just the delta. A reader can understand the entire page from this file alone.
- **Composition**: template named in frontmatter and Composition; every slot filled with a named organism; organism props/configuration documented. No invented inline components — missing organisms flagged as DS gaps (⚠) or handed to `designer-organism`.
- **States**: every page lifecycle state defined with its trigger and visual treatment; allowed transitions listed.
- **Responsive & Print**: page-specific overrides documented (template-level behavior is inherited, not repeated); print behavior defined or marked N/A.
- **Content is exact and complete** — every user-facing string is real, approved copy, never a placeholder. Page title/meta, all visible strings, error messages, empty states, success messages, help text, legal, and localization status are all covered. Strings pending approval are explicitly flagged.
- **Accessibility**: page title, focus on load, complete heading hierarchy (exactly one `<h1>`), reading order, skip-link target IDs (matching the template), and form accessibility documented.
- **Checklist & Launch**: completion checklist filled with page-specific items; launch checklist present for release readiness.

---

## The 3-gate flow

### Gate 1 — Input
Check that the story spec exists and the affected organisms/template are specced. If the page
already exists, read it before writing. If any dependency is missing, hand off first. Confirm
which strings have approved copy and which are still pending.

### Gate 2 — Process
Construct the full current state of the page. If updating an existing spec: start from the
current spec, apply the story's changes, then write the complete updated spec. Do not carry
forward anything that is no longer correct after the story's changes.

Work through each section with the designer and content owner. The Content section requires exact,
approved copy for every string — flag any string still awaiting sign-off rather than inventing it.

Write the page spec:

```markdown
---
name: {page-name}
version: 0.0.1
description:
link:
  - {tool-name}: {tool-link}
dependencies:
  - template: {template-name}
  - organisms: {organism-a}, {organism-b}
---
# {Page Name}

Pages fill template slots with real organisms and real content. Unlike every other level, all content fields in this spec must contain exact, approved copy — not placeholders. No string ships without sign-off.

---

## Composition

Define which template this page uses and how its slots are filled.

### Template
- Template used: `{template-name}`
- Page-level layout additions beyond what the template provides: {describe or N/A}

### Slots filled

| Slot name | Organism or component placed |
|-----------|------------------------------|
| `{slot}` | `{organism}` |

### Organisms used

| Organism | Slot | Props / configuration |
|----------|------|----------------------|
| `{organism}` | `{slot}` | {props} |

---

## States

Define every state this page can be in, what causes it, and how it is treated visually.

### Page lifecycle states

| State | Trigger | Visual treatment |
|-------|---------|-----------------|
| {state} | {trigger} | {treatment} |

### State transitions
List allowed transitions and what triggers each.

---

## Responsive

Page-specific responsive overrides only. Template-level responsive behavior is inherited and does not need repeating.

| Breakpoint | Page-specific override |
|------------|----------------------|
| Mobile < 640px | |
| Tablet 640–1024px | |
| Desktop > 1024px | |
| Wide > 1440px | |

---

## Print

- Page needs to print well: Yes / No
- Elements hidden on print: {list}
- Page break rules: {describe}
- Print-specific layout notes: {describe}

---

## Content

All strings on this page must be exact, approved copy. Organize by section. Every word a user can see must be listed.

### Page title and meta

| Field | Value |
|-------|-------|
| `<title>` tag | |
| Meta description | |
| `<h1>` text | |

### All visible strings
List every user-facing string, organized by section or region on the page.

| Key | Copy | Section | Notes |
|-----|------|---------|-------|
| `{key}` | {exact text} | {section} | {notes} |

### Error messages

| Error condition | Headline | Body | CTA label |
|----------------|----------|------|-----------|
| `{error}` | {text} | {text} | {text} |

### Empty states

| Condition | Headline | Body | CTA label |
|-----------|----------|------|-----------|
| `{condition}` | {text} | {text} | {text} |

### Success and confirmation

| Action | Message | Type | Duration |
|--------|---------|------|----------|
| `{action}` | {text} | toast / inline | {ms} |

### Help text and tooltips

| Element | Help text |
|---------|-----------|
| `{element}` | {text} |

### Legal and disclaimer
(Skip if not applicable.)

| Location | Text |
|----------|------|
| `{location}` | {text} |

### Email and notifications
(Skip if not applicable — only for pages that trigger emails or push notifications.)

| Trigger | Recipient | Subject | Body summary |
|---------|-----------|---------|--------------|
| `{trigger}` | {recipient} | {subject} | {summary} |

### Localization

#### Supported locales

| Locale | Status |
|--------|--------|
| `en-US` | Complete — source |
| `{locale}` | In progress / Not started |

#### Locale-specific content
Content that differs by locale — different copy, different images, legal differences: {describe or N/A}

#### Text expansion
- Longest locale for layout QA: {locale}
- Strings most likely to overflow: {list keys}
- RTL: see Accessibility > Internationalization

---

## Accessibility

Page-level requirements only. Template and organism specs own their respective sub-trees. Mark any section N/A with justification if it does not apply.

### Page title
- `document.title` value: {exact string}
- Format: `{Page name} — {Site name}`
- On route change: `document.title` updates before focus is moved

### Focus on page load
- Where focus lands on first render: `<h1>` / skip link / first interactive element
- If data is loading on mount: {where focus lands after content appears}

### Heading hierarchy
The complete heading structure for this page. Must have exactly one `<h1>`. Text comes from the Content spec.

| Level | Text | Location |
|-------|------|----------|
| `h1` | {from Content spec} | {region} |
| `{h2}` | {text} | {region} |

### Reading order
- Desktop DOM order matches visual order: Yes / No — exceptions: {list}
- Mobile DOM order matches visual order: Yes / No — exceptions: {list}

### Skip link targets
Skip links are defined in the template. This page must provide matching IDs.

| Skip link text | Target ID | Element at target |
|----------------|-----------|------------------|
| `{text}` | `#{id}` | `{element}` |

### Page-specific keyboard shortcuts
(Skip if not applicable — list only shortcuts unique to this page. Global shortcuts are in the template spec.)

| Shortcut | Action |
|----------|--------|
| `{key}` | {action} |

### Form accessibility
(Skip if not applicable.)
- All form fields have visible labels: Yes / No
- Error summary appears at top of form on submit failure: Yes / No
- Focus moves to error summary on submit failure: Yes / No
- Required fields marked with `aria-required` and visible indicator: Yes / No

### Internationalization
- RTL locales on this page: {list}
- Layout mirrors fully: Yes / No — exceptions: {list}

---

## Checklist

All items must pass or be explicitly waived with justification before status moves to **Approved**.

### Spec
- [ ] Composition: template named; all slots filled with named organisms; props documented
- [ ] States: all page lifecycle states defined with trigger and treatment; transitions listed
- [ ] Responsive & Print: page-specific overrides documented or marked N/A
- [ ] Content: every visible string is exact approved copy; errors, empty, success, help, legal, and localization covered
- [ ] Accessibility: page title, focus on load, heading hierarchy, reading order, skip-link targets, and form a11y documented

### Design
- [ ] All page states designed at all key breakpoints
- [ ] All supported themes verified
- [ ] Real copy from Content spec used in all designs — no placeholder text
- [ ] RTL layout reviewed (if shipped in any RTL locale)
- [ ] Print layout reviewed (if applicable)
- [ ] {page-specific item}

### Product & content
- [ ] All visible strings match Content spec exactly
- [ ] Error messages, empty states, and success messages match spec
- [ ] Legal / disclaimer text present where required
- [ ] All supported locales accounted for in Content spec
- [ ] {page-specific item}

### Engineering
- [ ] All API integrations return correct data shapes
- [ ] Role-based and feature-flag variations behave correctly
- [ ] Form validation triggers at correct timing; errors announce correctly
- [ ] Security: auth check, input sanitization, PII handling
- [ ] No axe-core violations in any state
- [ ] {page-specific item}

### QA
- [ ] Cross-browser smoke test passed
- [ ] Real device testing on iOS Safari and Chrome Android
- [ ] Screen reader tested: NVDA + Firefox, VoiceOver + Safari
- [ ] All translations complete and QA'd in longest locale
- [ ] Performance targets met in staging
- [ ] Visual regression baseline captured per state × breakpoint
- [ ] {page-specific item}

---

## Launch

### Launch checklist
- [ ] Design approved
- [ ] Engineering approved
- [ ] Product approved
- [ ] Legal approved (if applicable)
- [ ] Security reviewed
- [ ] Accessibility audited — zero violations
- [ ] All translations complete
- [ ] Analytics events verified in staging
- [ ] Monitoring and error rate alerts configured
- [ ] Rollback plan documented
- [ ] URL redirects configured (if replacing an existing page)
- [ ] Support team informed

### Post-launch monitoring
- Dashboards to watch: {list}
- Error rate threshold that triggers rollback: {value}
- Performance regression alert threshold: {value}
- First-week review scheduled: Yes / {date}
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that the spec is a complete current state
(not a delta), every slot is filled with a named organism, and all Content strings are exact
approved copy (no placeholders, pending strings explicitly flagged). When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the page spec, tick Step 3c in `## Plan`, update **Next step**, then
   hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The completed page spec feeds `designer-review`, which validates that every page listed in every
story spec in scope has a complete, current page spec file.
