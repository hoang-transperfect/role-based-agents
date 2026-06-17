---
name: figma-ds-foundation
description: >
  Figma adapter for designer-ds-foundation-build. Receives the foundation build brief and
  publishes design tokens into a Figma file as Variables and Styles: color tokens → Color
  Variables (grouped by semantic hierarchy using / separator), spacing tokens → Number Variables,
  typography → Text Styles, elevation/shadow → Effect Styles. Variable and Style names in Figma
  must match token names in the brief exactly — no renaming, no rounding, no approximation.
  Invoked by designer-ds-foundation-build when design-tool is figma.
---

# figma-ds-foundation

This skill translates the foundation build brief into Figma primitives. It is invoked by
`designer-ds-foundation-build` after the brief is prepared — it does not read spec files
directly. Its only job is to faithfully publish every token in the brief into the target Figma
file as Variables or Styles.

## Naming convention

All Figma artifact names — pages, Variable collection names, and Style group names — use
**lowercase kebab-case**. Token/Variable names within collections must match the brief exactly
(they use slash-separated hierarchy, e.g. `color/action/primary`).

## Inputs

The build brief from `designer-ds-foundation-build`, containing:
- **Design file link** — the Figma file URL to publish into.
- **Color tokens** — token name, hex/rgba value, and grouping hierarchy
  (e.g. `color/action/primary → #0066CC`). Semantic aliases reference a primitive token.
- **Spacing tokens** — token name and px value (e.g. `spacing/4 → 16`).
- **Typography tokens** — scale name, font family, weight, size (px), line-height, letter-spacing.
- **Elevation/shadow tokens** — token name and shadow definition (x, y, blur, spread, colour).
- **Other token categories** — token name → value pairs for any additional categories.

## Outputs
- Variables and Styles published in the Figma file.
- The Figma file URL.
- A creation summary listing every Variable collection, Variable, and Style created.

---

## The 3-gate flow

### Gate 1 — Input
Verify the build brief is complete:
- Design file link is present and accessible.
- At least one token category exists in the brief.

If the file link is missing or the brief is empty, stop and report the gap to
`designer-ds-foundation-build`. Do not proceed.

### Gate 2 — Process

Open the target Figma file. Before publishing any tokens, ensure a dedicated page exists for
each token category. Page names are fixed:

| Token category | Figma page name |
|----------------|----------------|
| Color tokens | `color` |
| Spacing tokens | `spacing` |
| Typography tokens | `typography` |
| Elevation / shadow tokens | `elevation` |
| Any other category | The category name in lowercase kebab-case |

For each page: if it does not exist, create it. If it exists, navigate to it before working on
that category. All Variables and Styles for a category are displayed on their own page — never
mixed across pages.

Work through each token category in order:

**Color tokens → Color Variables**
- Create (or open existing) a Variable collection named `color`.
- For each token, create a Color Variable. Use the token name exactly as the Variable name,
  preserving the grouping hierarchy with `/` as separator
  (e.g. token `color/action/primary` → Variable `color/action/primary` in group `color/action`).
- Set the raw hex or rgba value. Do not alter the value.
- If the token is a semantic alias referencing another token: create the primitive Variable
  first, then create the alias Variable and set it to reference the primitive — not a hardcoded
  value.

**Spacing tokens → Number Variables**
- Create (or open existing) a Variable collection named `spacing`.
- For each token, create a Number Variable with the exact token name and the px value.

**Typography tokens → Text Styles**
- For each scale entry, create a Text Style named exactly as the token name.
- Set: font family, font weight, font size (px), line height (px or %), letter spacing (px or em).
- Use exact values — do not round or approximate.

**Elevation/shadow tokens → Effect Styles**
- For each token, create an Effect Style named exactly as the token name.
- Set the drop shadow: x, y, blur, spread, colour, and opacity exactly as specified.

**Other token categories**
- For each category, create a Variable collection named after the category.
- Create Variables with exact token names and values.

After each category, spot-check that names in Figma match the brief exactly before moving on.

### Gate 3 — Output

For every token in the brief, verify:
- A Variable or Style exists in Figma with the **exact** token name (no renaming, no casing
  change, no abbreviation).
- The value matches the brief exactly (no rounding, no colour conversion).
- Grouping hierarchy is preserved in Variable names.
- Semantic alias Variables reference the primitive Variable — not a hardcoded value.

Any mismatch is a gap. Correct it before returning. When all tokens are accounted for, return
the Figma file URL and the creation summary to `designer-ds-foundation-build`.
