---
description: This file is readme for this project. Read by user only. Agent should not follow the instructions in this file. Agent still can update this file if user asks. If not, do not touch this file.
---
# Role-based Assistants

Role-based Assistants (RBA) is a framework to create, configure, and manage personalized AI assistants across different projects.

## Set up
In the `assistant/[user-assistant]` folder, copy the ai.json to your local folder
Run the following command to initialize the assistant:
```bash
npx asm install -t [your AI platform]
```
For example, if you want to use "claude", run ```npx asm init install -t claude```

### How to use
1. Ask the assistant to create a new project (if it doesn't exist)
2. Ask the assistant for your needs

## Architecture
### Diagram
```mermaid
graph TD
    subgraph "Remote Server"
        RBA["Role-based Assistants (This Repo)"]
    end

    subgraph "Local Environment (User Laptop)"
        UA["User Assistant (User's Repo)"]
        P["Projects (Other Repos)"]

        RBA -->|Creates/Configures| UA
        UA -->|Interacts with| P
    end
```
### Flow

The framework is generic: every assistant is the **same machine** running different domain skills.
Two flows describe how it works at runtime. A specific assistant (BA, FE, BE, Designer, ...) just
plugs its own skills into the second flow.

**1. Session lifecycle & routing** — what happens when a chat starts. `gather-needs` is the single
entry point; it guards the working tree, detects intent, and routes to the right skill.

```mermaid
flowchart TD
    Start(["User starts a chat session"]) --> GN["gather-needs (session entry)"]
    GN --> Guard{"commit-work guard: working tree clean?"}
    Guard -- "dirty" --> Stash["Ask user: stash or commit"]
    Stash --> Intent{"Detect intent"}
    Guard -- "clean" --> Intent
    Intent -- "new project" --> CP["create-project"]
    Intent -- "new task" --> CT["create-task"]
    Intent -- "resume task" --> RT["resume-task"]
    CP --> Work
    CT --> Work
    RT --> Work
    Work["Domain skills run (ba-*, fe-*, be-*, designer-*, ...)"] --> Log(["Every turn logged to the task's conversation log"])
```

**2. The skill contract & 3-gate flow** — the universal pattern every domain skill follows. Each
skill declares its own contract (Inputs / Input AC / Outputs / Output Quality); the gates and the
shared skills (`commit-work`, `improve-skill`) are the same for all.

```mermaid
flowchart TD
    In(["Domain skill invoked"]) --> G1{"Gate 1 - Input: meets Input AC?"}
    G1 -- "no" --> ImpIn["Improve the input (ask user if needed, never assume)"]
    ImpIn --> G1
    G1 -- "yes" --> G2["Gate 2 - Process: do the work WITH the user"]
    G2 --> G3{"Gate 3 - Output: meets Output Quality?"}
    G3 -- "no" --> ImpOut["Improve the output (ask user if needed)"]
    ImpOut --> G3
    G3 -- "yes" --> Conf{"User confirms the output?"}
    Conf -- "confirmed as-is" --> Commit["commit-work: commit the confirmed output"]
    Conf -- "not satisfied" --> Rework["Improve output with user, capturing feedback"]
    Rework --> Conf
    Commit --> Reworked{"Was the output reworked?"}
    Reworked -- "yes" --> IS["improve-skill: diagnose, then propose a SKILL.md change or a project note"]
    Reworked -- "no" --> Done(["Done"])
    IS --> Done
```

Together: flow 1 gets the user into the right skill; flow 2 is how that skill (and every other)
executes safely — never starting on bad input, never finishing on bad output, always committing
what's confirmed, and learning from any rework.
### User Assistant
This folder follows the following structure:
```text
.
├── .agent/, .cursor/, .claude/, ... # Configuration folder for IDE or platform
├── ai.json                          # AI settings: rules, skills, mcp, ...
├── AGENT.md                         # Agent definition
├── CLAUDE.md, ...                   # Link to AGENT.md
└── [project folders]/               # Individual projects
    ├── resource.md                # Project-specific resources such as name, working directory, knowledge
    ├── raw-conversation/    # Logs and transcripts of chat sessions
    └── in-progress-tasks/   # Manage in-progress tasks (Markdown files per task)
```
