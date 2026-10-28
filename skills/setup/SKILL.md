---
name: setup
description: >-
  Optional configuration helper for the engineering skills pipeline — checks the
  global install and manages the personal defaults file and project deviations.
  The pipeline works without it.
disable-model-invocation: true
model: sonnet
effort: high
---

# Setup

Optional. The pipeline works with no configuration: tracker and monorepo are detected and every other setting has a built-in default (see `{skills-root}/pipeline/config.md`, the single description of settings, resolution order and detection). Run `/setup` inside the **target project** (not the skills repo) to check the install or change defaults.

The shared pack is one git checkout with `skills/` (one folder per skill), `agents/` (one subagent per file) and `generated/` (agents built per provider). Its `install.sh` links skills into `~/.claude/skills/` and `~/.agents/skills/` and agents into `~/.claude/agents/`. Pack root is the parent of the `skills/` directory containing this skill. `/setup` never pulls or updates the pack.

Every step shows a preview and waits for confirmation before writing or deleting anything. Ask one question at a time with a recommended option using `AskUserQuestion`, with a text fallback.

## Process

### 1. Global install

Skip when the current working directory **is** the pack (it contains `skills/setup/SKILL.md` and `agents/`).

The pipeline is the skills `pipeline`, `idea`, `analyze`, `analyze-modify`, `implement`, `change`, `verify`, `code-review`, `ux-review`, `complete`, `monorepo-update`, `tdd`, `integration-tests` and `commit`, and the agents `test-writer`, `implementer`, `check-runner`, `functional-reviewer`, `code-reviewer` and `ux-reviewer`. Check that each `~/.claude/skills/<name>` and `~/.claude/agents/<name>.md` exists and resolves into the pack. If any is missing, offer to run the pack's `install.sh`.

### 2. Global file

Show the effective personal defaults (`language`, `branch-owner`, `push`, `ux-review`) from `~/.config/enterprise-engineering-skills/workflow.md` merged over the built-in defaults. Offer to create or edit that file; write only the keys the user confirms, in the format from `config.md`.

### 3. Project deviations

Show the detected tracker and monorepo layout and the effective configuration (resolved per `config.md`). Ask which settings should differ for this project. Write `docs/agents/config/workflow.md` with only the keys whose value differs from what the global file and the built-in defaults or detection would give anyway. If nothing differs, do not create the file.

Do not stage or commit `docs/agents/`; versioning it is the project's choice.

### 4. Agent skills block

Optional; only offer it, skills do not read it. Upsert only the `## Agent skills` section of `AGENTS.md` (create the file if missing, preserve all other sections, never duplicate):

```markdown
## Agent skills

This repo uses the enterprise-engineering-skills pipeline (`/analyze` → `/implement` → `/verify`).
Project deviations: `docs/agents/config/workflow.md`.
```

### Done

Report what was written, and whether the global install resolves. State that the pack itself was not updated; update it with `git pull` in its checkout.
