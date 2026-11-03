---
name: ees-setup
description: >-
  Optional helper for the engineering skills pipeline — checks the global
  install and sets the analysis language, globally or for one project. The
  pipeline works without it.
disable-model-invocation: true
model: sonnet
effort: high
---

# Setup

Optional. The pipeline works with no configuration: tracker and monorepo are detected, the language follows the conversation and the analysis, and branches, pushing and PRs follow `{skills-root}/ees-pipeline/delivery.md` (see `{skills-root}/ees-pipeline/config.md`, the single description of settings, resolution order and detection). Run `/ees-setup` inside the **target project** (not the skills repo) to check the install or set `language`.

The shared pack is one git checkout with `skills/` (one folder per skill), `agents/` (one subagent per file) and `generated/` (agents built per provider). Its `install.sh` asks which tools to link and puts each selected tool's skills and agents in its own directories. Pack root is the parent of the `skills/` directory containing this skill. `/ees-setup` never pulls or updates the pack.

Every step shows a preview and waits for confirmation before writing or deleting anything. Ask one question at a time with a recommended option using `AskUserQuestion`, with a text fallback.

## Process

### 1. Global install

Skip when the current working directory **is** the pack (it contains `skills/ees-setup/SKILL.md` and `agents/`).

The pipeline is the skills `ees-pipeline`, `ees-idea`, `ees-analyze`, `ees-implement`, `ees-change`, `ees-verify`, `ees-code-review`, `ees-ux-review`, `ees-complete`, `ees-monorepo-update`, `ees-tdd`, `ees-integration-tests` and `ees-commit`, and the agents `ees-test-writer`, `ees-implementer`, `ees-check-runner`, `ees-functional-reviewer`, `ees-code-reviewer` and `ees-ux-reviewer`. Check that each `~/.claude/skills/<name>` and `~/.claude/agents/<name>.md` exists and resolves into the pack. If any is missing, tell the user to run the pack's `install.sh` in a terminal — it asks which tools to link — and do not run it from the session.

### 2. Global file

Show the effective personal `language` from `~/.config/enterprise-engineering-skills/workflow.md`, or that it follows the conversation when unset. Offer to create or edit that file; write only what the user confirms, in the format from `config.md`. If the file still holds `branch-owner`, `push` or `ux-review`, offer to remove them: they are ignored.

### 3. Project deviations

Show the detected tracker and monorepo layout and the effective `language` (resolved per `config.md`). Ask whether the language, tracker or monorepo layout should differ for this project. Write `docs/agents/config/workflow.md` with only the keys whose value differs from what the global file and the built-in defaults or detection would give anyway. If nothing differs, do not create the file.

Do not stage or commit `docs/agents/`; versioning it is the project's choice.

### 4. Agent skills block

Optional; only offer it, skills do not read it. Upsert only the `## Agent skills` section of `AGENTS.md` (create the file if missing, preserve all other sections, never duplicate):

```markdown
## Agent skills

This repo uses the enterprise-engineering-skills pipeline (`/ees-analyze` → `/ees-implement` → `/ees-verify`).
Project deviations: `docs/agents/config/workflow.md`.
```

### Done

Report what was written, and whether the global install resolves. State that the pack itself was not updated; update it with `git pull` in its checkout.
