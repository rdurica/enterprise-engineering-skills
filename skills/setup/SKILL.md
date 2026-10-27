---
name: setup
description: >-
  Optional configuration helper for the engineering skills pipeline — checks the
  global install, manages the personal defaults file and project deviations, and
  cleans up old project copies.
  The pipeline works without it.
disable-model-invocation: true
model: sonnet
effort: high
---

# Setup

Optional. The pipeline works with no configuration: tracker and monorepo are detected and every other setting has a built-in default (see `{skills-root}/pipeline/config.md`, the single description of settings, resolution order and detection). Run `/setup` inside the **target project** (not the skills repo) to check the install, change defaults or clean up old copies.

The shared pack is one git checkout with `skills/` (one folder per skill), `agents/` (one subagent per file) and `generated/` (agents built per provider). Its `install.sh` links skills into `~/.claude/skills/` and `~/.agents/skills/` and agents into `~/.claude/agents/`. Pack root is the parent of the `skills/` directory containing this skill. `/setup` never pulls or updates the pack.

Every step shows a preview and waits for confirmation before writing or deleting anything. Ask one question at a time with a recommended option using `AskUserQuestion`, with a text fallback.

## Process

### 1. Global install

Skip when the current working directory **is** the pack (it contains `skills/setup/SKILL.md` and `agents/`).

The pipeline is the skills `pipeline`, `analyze`, `analyze-modify`, `implement`, `change`, `verify`, `code-review`, `ux-review`, `complete`, `monorepo-update`, `tdd`, `integration-tests` and `commit`, and the agents `test-writer`, `implementer`, `check-runner`, `functional-reviewer`, `code-reviewer` and `ux-reviewer`. Check that each `~/.claude/skills/<name>` and `~/.claude/agents/<name>.md` exists and resolves into the pack. If any is missing, offer to run the pack's `install.sh`.

### 2. Global file

Show the effective personal defaults (`language`, `branch-owner`, `push`, `ux-review`) from `~/.config/enterprise-engineering-skills/workflow.md` merged over the built-in defaults. Offer to create or edit that file; write only the keys the user confirms, in the format from `config.md`.

### 3. Project deviations

Show the detected tracker and monorepo layout and the effective configuration (resolved per `config.md`). Ask which settings should differ for this project. Write `docs/agents/config/workflow.md` with only the keys whose value differs from what the global file and the built-in defaults or detection would give anyway. If nothing differs, do not create the file.

Do not stage or commit `docs/agents/`; versioning it is the project's choice.

### 4. Migrate an old project

Look for files left by the earlier setup:

- `docs/agents/config/issue-tracker.md`, `issue-tracker.github.md`, `issue-tracker.local.md` and `domain.md` — offer to delete them. When a copy differs from the pack's `{skills-root}/pipeline/tracker-<tracker>.md`, show the difference first and offer to move the project-specific content into `AGENTS.md` or an overlay (`verify.md`, `code-review.md`, `ux-review.md`) before deleting.
- An old `docs/agents/config/workflow.md` — offer to reduce it to deviations: read the keys, rename `active` to `tracker` and keep it only if it differs from detection, drop every key equal to the global or built-in value, drop `Preset:`, prose and the legacy `## Skills` section. Delete the file when nothing remains.
- A long `## Agent skills` block in `AGENTS.md` — offer to replace it with the short block from step 5.

Never modify, move or delete anything in `docs/agents/analysis/`. Leave a project's `docs/adr/` in place.

### 5. Agent skills block

Optional; only offer it, skills do not read it. Upsert only the `## Agent skills` section of `AGENTS.md` (create the file if missing, preserve all other sections, never duplicate):

```markdown
## Agent skills

This repo uses the enterprise-engineering-skills pipeline (`/analyze` → `/implement` → `/verify`).
Project deviations: `docs/agents/config/workflow.md`.
```

### 6. Old pack copies

Skip when the current working directory is the pack itself.

Project definitions take precedence over user ones with the same name, so old project copies shadow the global pack. Look for them: `skills-dir` and `agents-dir` in an existing `workflow.md`, `.claude/skills/` and `.claude/agents/`, and legacy `.agents/skills/`, `.codex/skills/` or `.cursor/skills/`. List the exact folders and files found for the skills and agents named in step 1, plus copies of `setup`, `git-release`, the retired skill `align` and retired agents (`analyst`, `committer`, `correctness-reviewer`, `craft-reviewer`, `spec-reviewer`, `standards-reviewer`), and offer their removal. Never delete without confirmation, never remove a whole skills directory or unrelated skills, and validate that every path stays inside the target repo without symlinked parents. If removal is declined, warn that the copies still shadow the global pack.

### Done

Report what was written, deleted or retained, and whether the global install resolves. State that the pack itself was not updated; update it with `git pull` in its checkout.
