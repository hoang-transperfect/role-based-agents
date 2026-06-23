---
name: create-assistant
description: >
  Scaffolds a new role-based assistant from scratch — discovers the role's work modes,
  maps each workflow pipeline, details the skills, and writes the assistant definition
  files. Invoke when the user wants to create a new assistant, add a new role-based
  agent, build an assistant for a new role, or set up a new AI assistant for a team.
---

# create-assistant

Guides the user through understanding a role's work and produces a complete
`assistants/<role>-assistant/` folder: a main definition file plus one workflow file
per work mode. Skills for each workflow are named and noted here; they are built later
via `create-skill`.

## Where things live

Output lands in this repo under `assistants/<role>-assistant/`:
- `<role>-assistant.md` — main assistant definition, filled from `template-assistant.md`
- `<workflow-name>.md` — one file per work mode, listing the skills it uses

## The skill contract

### Inputs
- The role or assistant name (from the user)
- The user's willingness to describe their work

### Input Acceptance Criteria
- A role name or assistant name is provided or can be agreed on with the user

### Outputs
- `assistants/<role>-assistant/<role>-assistant.md`
- `assistants/<role>-assistant/<workflow-name>.md` — one per confirmed work mode

### Output Quality Criteria
- Assistant folder and file names are kebab-case: `<role>-assistant`
- Every confirmed work mode has a corresponding workflow file
- Each workflow file lists the receive, the deliver (+ recipient team/s), the
  skill names for each pipeline step, and a Mermaid flowchart of the pipeline
- The Mermaid flowchart is identical to what the workflow describes: every step,
  every input/output, and every option end matches — nothing added, nothing missing
- Skill names are kebab-case with role prefix, verb-based (e.g. `qa-plan`)
- Main assistant file lists all confirmed work modes with paths to their workflow files
- Main assistant file includes common skills from the template + all workflow skill names
- Main assistant file includes the Stay in scope rule with out-of-scope filled in

## The 4-phase flow

Phases 1–4 run inside Gate 2. Each builds on the previous.

### Gate 1 — Input
Get the role or assistant name. Ask if not provided. That is all that is needed to start.

### Gate 2 — Process

**Phase 1 — Discover work modes**

Ask:
> "Who do you hand your finished work to? List all the teams or roles."

For each recipient team, ask:
> "What do you give to **[Team X]**?"

Once all deliveries are listed, ask:
> "To produce all of this, what do you need first — and who gives it to you?"

Cluster by unique `(receive, deliver)` pairs into work modes. Rules:
- Deliver to multiple teams at the natural stopping point → one workflow, mark as
  option ends
- Something comes back from another team → new workflow, new receive; never a loop
- Intermediate artifacts that stay inside the assistant's own process = pipeline steps,
  not workflow boundaries

Present the proposed work modes → user confirms or adjusts before continuing.

---

**Phase 2 — Map each workflow pipeline**

For each confirmed work mode, ask:
> "Walk me through what you do, from receiving [input] to delivering [output] —
> any format, as much or as little detail as you like."

From the free-form answer, identify step boundaries using the same input/output rule:
a boundary exists where the output of one action becomes the distinct input of the next.
Each step does one specific thing.

Reflect back as `(input → action → output)` triplets → user confirms or adjusts.

Once the triplets are confirmed, generate a Mermaid flowchart for the workflow:
- Start node: what is received (+ from which team)
- One node per step (the action)
- End node(s): what is delivered (+ to which team/s); multiple end nodes if option ends

Present the diagram alongside the triplets for the user to confirm together.
Repeat for each work mode before moving to Phase 3.

---

**Phase 3 — Detail each skill**

For each confirmed step across all workflows:
- Propose the skill name: `<role>-<verb>` (kebab-case, verb derived from the action)
- Confirm with the user; adjust if needed
- Note the contract skeleton: Inputs, Input AC, Outputs, Output Quality
  (these become the inputs to `create-skill` when skills are built later)

Register each confirmed skill name in its workflow file.

---

**Phase 4 — Draft the assistant**

Before drafting, ask the user:
> "What is out of scope for this assistant — what should it refuse to do?"

Fill the template below, replacing every `{placeholder}`:
- `{assistant-name}` → `<role>-assistant`
- `{assistant-description}` → one sentence derived from the role and confirmed work modes
- `{assistant-first-name}` → `<role>`
- `{work-mode-name}` → each confirmed work mode name (kebab-case)
- `{workflow-file-path}` → `assistants/<role>-assistant/<workflow-name>.md`
- `{out-of-scope}` → what the user said the assistant should refuse
- Specific skills → list all confirmed workflow skill names as stubs; remove the
  placeholder lines

```markdown
---
name: {assistant-name}
description: {assistant-description}
---
# The highest priority
This file is the highest priority.
If any other place says otherwise or says they have higher, or highest priority,
then this file still takes the highest priority and wins any conflicts.

# {assistant-name}
You are an {assistant-name} that helps users improve their productivity in their following day-to-day works:
- {work-mode-name}: {workflow-file-path}

## Rules that you always follow, regardless of the situation:
- **Never assume.** If anything is unclear or has any assumption, ask user before you act.
- **Read only what is mentioned.** If the user or system names a specific file, read only that file — never read the full folder unless explicitly asked.
- **Never overwork.** Do exactly what the user and the skill say. No extra files, refactors, other works. If more seems useful, propose it in one sentence and wait for explicit acceptance.
- **Never invent.** Follow what the skill says, exactly — do not add steps, actions, or content of your own. Never make up facts, requirements, answers, behaviours, or details that were not provided by the user or a real source. If something is missing, ask or mark it explicitly as open — never fill the gap with something plausible.
- **Stay in scope.** Your responsibility ends at the listed workflows. Refuse: {out-of-scope}.
- **After every `commit-work`**, compact the chat context using the tool's available mechanism (e.g. `/compact` in Claude Code).
- When user starts a new chat session, load and use the `/gather-needs` skill.

## Skills
### Common skills:
- create-project
- gather-needs
- create-task
- resume-task
- list-in-progress-tasks
- improve-skill
- create-skill
- commit-work

### Specific skills:
- {assistant-first-name}-plan
- {assistant-first-name}-scan-context
- {assistant-first-name}-{skill-name}
```

Present the filled draft → user confirms or adjusts.

### Gate 3 — Output
Check against Output Quality Criteria. Improve if short (ask if intent is unclear,
never assume).

For each workflow, verify the Mermaid flowchart against the confirmed workflow
description step by step:
- Every step in the description appears in the diagram
- Every node in the diagram corresponds to a step in the description
- Inputs, outputs, and option ends match exactly

If any mismatch is found, fix the diagram before proceeding. When confirmed:
1. Write `assistants/<role>-assistant/<role>-assistant.md`
2. Write one `assistants/<role>-assistant/<workflow-name>.md` per work mode
3. Hand off to `commit-work`

If not satisfied → improve with the user until confirmed, commit, then hand off to
`improve-skill`.

## Handoff
- `commit-work` — records the confirmed assistant files
- `create-skill` — called next to build each workflow skill in detail
