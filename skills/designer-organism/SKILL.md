---
name: designer-organism
description: >
  Creates or updates a product-specific organism spec — a complex UI component tightly coupled
  to the product's information architecture or data model, which therefore does not belong in the
  design system. Built exclusively from DS atoms and molecules by name — never from raw token
  values. Invoke when a story spec (designer-ui) lists a product-specific organism that needs a
  spec or an update (e.g. AppNavigationBar, UserProfileCard, OrderSummaryPanel). If the organism
  already has a spec, reads it first then rewrites it in full. Produces a dedicated
  organism-spec.md under design-spec/product-organisms/. Run before designer-template and
  designer-page so they can reference the organism by name. Spec once per organism; all
  subsequent stories that change it update the same file.
---

# designer-organism

Not all organisms belong in the design system. An organism that is tightly coupled to this
product's information architecture, data model, or specific feature context is intentionally
product-specific — it would not make sense extracted into a generic design system. This skill
specs those organisms.

The key constraint: a product-specific organism is **assembled from DS components** — atoms and
molecules from the design system. It never introduces new visual primitives. Token values come
from the design system foundations; sub-components come from the DS component library. Only the
composition and the product-specific content rules are defined here.

**If the same organism is needed in multiple stories:** spec it once here, then every subsequent
story references it by name and links to this file — do not re-spec it.

## Where things live

- **Read** the story spec (`design-spec/<epic>/<feature>/<story>/story-spec.md`) to understand
  what is changing for this organism and what the affected artifact entry says.
- **Read** the existing organism spec at
  `<real_project_path>/design-spec/product-organisms/<organism-name>/organism-spec.md` if it
  exists — always read before writing when the spec already exists.
- **Read** DS component specs at `<real_project_path>/design-system/` for the atoms/molecules
  this organism will use.
- **Write** (or overwrite) the spec to
  `<real_project_path>/design-spec/product-organisms/<organism-name>/organism-spec.md`
  (create the folder if needed).

---

## The skill contract

### Inputs
- The story spec that requires this organism (to understand what is changing and why).
- The existing organism spec if this is an update (read before writing — never overwrite blind).
- The DS component specs for the atoms/molecules it will be built from.
- Confirmation that this organism is product-specific (not a generic, reusable component that
  belongs in the DS). If uncertain, discuss with the designer: can this organism be used in a
  completely different product without modification? If yes → it belongs in the DS.

### Input Acceptance Criteria
- The story spec for the current story exists and is confirmed (from `designer-ui`).
- The organism is confirmed as product-specific, not a DS candidate.
- The DS atoms and molecules this organism depends on exist in the design system. If a dependency
  is missing from the DS, flag it as a DS gap and recommend adding it there first.
- If updating: the existing organism spec has been read before any changes are made.

### Outputs
- `<real_project_path>/design-spec/product-organisms/<organism-name>/organism-spec.md`

### Output Quality Criteria
- **Built from DS components only** — every sub-component is a named DS atom or molecule. No raw
  token values; no invented components. If a needed sub-component is missing from the DS, flag
  it as a DS gap (⚠) rather than defining it here.
- **Variants and states are defined** — all meaningful variants (if any) and the states this
  organism can be in on a screen (default, loading, empty, error).
- **Content rules are explicit** — what data this organism displays and any content rules
  (character limits, truncation, required vs. optional fields).
- **Context is documented** — which screens/stories use this organism, so a developer knows its
  scope without reading every story spec.

---

## The 3-gate flow

### Gate 1 — Input
Verify the organism is product-specific, not a DS candidate. If it could be generic and reusable,
discuss with the designer — the right place for it may be `designer-ds-component`, not here.
If an organism spec already exists, read it before proceeding. Verify DS component dependencies
exist; flag any missing ones as DS gaps before proceeding.

### Gate 2 — Process
If updating an existing spec: start from the current spec, apply the changes described in the
story spec, then write the complete updated spec. Do not carry forward anything that is no longer
correct after this story's changes.

Work through the organism structure with the designer. Identify:
- The DS atoms/molecules it is composed of
- Its variants (if it appears in meaningfully different forms)
- Its states and what triggers each
- The content rules for each sub-component

Write the organism spec:

```markdown
# <OrganismName> — product-specific organism

_Type: product-specific · Used in: <US-01>, <US-03>, …_

## Purpose
<1 sentence: what this organism does and why it is product-specific>

## Composition
| Sub-component | Level | Role |
|---|---|---|
| Avatar | DS atom | Displays the user's profile image |
| Heading / H3 | DS atom | User's display name |
| Button / Ghost | DS atom | "Edit profile" action |
| Badge / Status | DS atom | Online / offline indicator |

## Variants
| Variant | When to use |
|---|---|
| Default | Standard view |
| Compact | Used inside a list or sidebar |

## States
| State | Description |
|---|---|
| Default | All data loaded |
| Loading | Avatar and name replaced by SkeletonAtom |
| Empty | No user data — shows placeholder content |

## Content rules
- **Display name:** max 40 chars; truncate with ellipsis if longer
- **Status badge:** shown only when real-time status is available
- **Edit action:** visible only when viewing own profile

## DS gaps
- ⚠ <ComponentName>: needed as a sub-component but not yet in the DS — add to DS before build.
```

### Gate 3 — Output
Check against the Output Quality Criteria — especially that all sub-components are DS components
(never raw values), and that DS gaps are explicitly flagged. When the bar is met:
1. Present and ask the user to confirm.
2. **If confirmed** → write the file, tick Step 3a in `## Plan` (or note the organism in a list
   if multiple organisms are being specced), update **Next step**, then hand off to `commit-work`.
3. **If not satisfied** → improve with the user, commit, then hand off to `improve-skill`.

---

## Handoff
The organism spec feeds `designer-template` (which places it in layout zones) and `designer-page`
(which references it in page specs). All subsequent stories that change this organism update the
same spec file — rewriting it in full to reflect the new state.
