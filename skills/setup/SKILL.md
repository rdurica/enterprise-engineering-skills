---
name: setup
description: >-
  Configure a repo for the engineering skills pipeline — issue tracker and git
  workflow (branch-owner, push), and checks the globally installed skills and
  agents.
  Run before analyze or implement, or again to refresh configuration.
disable-model-invocation: true
model: sonnet
effort: high
---

# Setup

Configure or refresh a repo. Run inside the **target project** (not the skills repo).

The shared pack is one git checkout with `skills/` (one folder per skill), `agents/` (one subagent per file) and `generated/` (agents built per provider from `agents/` and `agents.toml`). Its `install.sh` links skills into `~/.claude/skills/` and agents from `generated/claude/agents/` into `~/.claude/agents/`. Pack root is the parent of the `skills/` directory containing this skill. Per-repo differences live in `docs/agents/config/workflow.md`.

Skills carry their own `model` and `effort` in frontmatter, agents in the pack's `agents.toml`: the orchestrating skills run on Opus, delegated work on Sonnet, check running on Haiku.

## Process

### 1. Explore

Read what already exists — do not assume:

- `git remote -v` — GitHub? No remote?
- `AGENTS.md` — existing `## Agent skills` block?
- `docs/agents/config/` — prior setup output? Also inspect any legacy configuration directly under `docs/agents/` to recover saved settings on refresh.
- **Old project copies** — the pack is only used globally. Look for pipeline copies left by older vendored setups: `skills-dir` and `agents-dir` in an existing `workflow.md`, `.claude/skills/` and `.claude/agents/`, and legacy `.agents/skills/`, `.codex/skills/` or `.cursor/skills/`. Record their paths for step 5.
- **Monorepo:** nested git repos — run `git submodule status` and/or find nested `.git` dirs (excluding `.git/modules/`). If found, note paths and remotes for the `## Monorepo` section in `workflow.md`.

The normal entry point is the user running the pipeline locally. Recommend **human-owned** when the user wants to keep their current branch and manage PRs; recommend **full-agentic** when the agent should manage branches and PRs. Do not infer branch ownership from editor files or the tracker.

See [workflow-presets.md](./workflow-presets.md) for preset values.

### 2. Interview (preset + language + UX review)

Ask one question at a time with a recommended option using `AskUserQuestion`, with a text fallback if the tool is unavailable or does not permit the request.

Reuse settings already established in the session or existing `workflow.md`; show the resulting draft for review. For missing settings, offer a preset or ask only the unanswered questions.

**Resolve when unknown** (presets do not set these):

- **Language:** English (`en`) / Czech (`cs`) — published analysis prose and ticket comments
- **UX/UI review before finalization?** Enabled (browser walkthrough + hard gate) / Disabled

Then resolve any settings not already answered by the session, repo or preset:

| # | Question | Options |
|---|----------|---------|
| 1 | **Issue tracker** | GitHub / Local / Both |
| 2 | **Branch owner** | Agent (agent creates/checkouts branch) / Human (user creates branch, agent stays on HEAD) |
| 3 | **Push policy** | finalize / never |

**Presets:**

- `full-agentic` — github, agent, finalize
- `human-owned` — github (or local), human, finalize

Branch ownership controls checkout and PR management. Push policy is independent: `finalize` allows the parent orchestrator to push after verification and check CI; `never` disables pushing. A session instruction such as “do not push” overrides either preset. Working subagents never commit or push.

If tracker is **Both**: write active backend to `issue-tracker.md` and reference copies as `issue-tracker.github.md` + `issue-tracker.local.md`.

### 3. Auto-detect

- **Agent trigger:** GitHub `ready-for-agent` (optional auto-start). Happy path: human reviews the analysis, then runs `/implement`. User-invoked `/implement` does not require the label.
- **Monorepo:** if nested git repos were found in Explore, include `## Monorepo` in the workflow draft (see below). Otherwise omit the section.

### 4. Confirm and write

Show draft of:

- `docs/agents/config/workflow.md` (from [workflow.md.template](./workflow.md.template))
- `docs/agents/config/issue-tracker.md` (+ reference copies if Both)
- `## Agent skills` block patch

Let the user edit, then write.

On re-runs, refresh these managed outputs using the current templates and confirmed settings. Preserve project-specific documentation and additions in `docs/agents/config/`; merge existing content rather than blindly replacing it. Leave unrelated files untouched.

Keep configuration and project-specific instruction overlays in `docs/agents/config/`, active local analyses in `docs/agents/analysis/`, and completed analyses in `docs/agents/analysis/done/`. Refresh only configuration; never overwrite, move or delete analyses during setup. When refreshing a legacy project, read its old configuration to preserve settings and additions, then write the current configuration under `config/`; leave legacy files untouched and report their paths.

Do not automatically ignore, stage or commit `docs/agents/`. Versioning agent configuration and analyses is the project's choice.

#### workflow.md

Fill template placeholders: `{{PRESET}}`, `{{BRANCH_OWNER}}`, `{{PUSH}}`, `{{TRACKER_ACTIVE}}`, `{{LANGUAGE}}`, `{{UX_REVIEW}}`, `{{MONOREPO_SECTION}}`. On refresh, drop the legacy `## Skills` section (`skills-mode`, `skills-dir`, `agents-dir`).

**`{{UX_REVIEW}}`** — `enabled` or `disabled` from the UX/UI review interview answer.

**`{{MONOREPO_SECTION}}`** — empty string when not a monorepo. When nested git repos exist, replace with:

```markdown
## Monorepo

- container-root: .
  remote: org/monorepo     <!-- GitHub issues/analyses live here; stays on main — no branch, commit, push, or PR during /implement or /verify -->
- delivery-roots:
  - path: backend
    remote: org/backend
  - path: frontend
    remote: org/frontend
```

Fill `path` and `remote` from detection (`git submodule status`, nested `.git`, `git remote -v` in each path). Include `remote` on `container-root` (from its `origin`) so `/analyze` and other `gh issue` ops target the monorepo, not delivery roots. Let the user confirm or edit before writing. Submodule pointer bumps on the container root are **not** part of the agent pipeline — document only, no automation.

#### Agent skills block

**Edit target:** `AGENTS.md`.

Upsert only the `## Agent skills` section; preserve all other sections. Append it if missing, or create `AGENTS.md` if the file does not exist. Never overwrite the full existing file or duplicate the section.

```markdown
## Agent skills

Issue tracker: [GitHub | local markdown]. See `docs/agents/config/issue-tracker.md`.
Workflow defaults: `docs/agents/config/workflow.md` (branch-owner, push, language, work types).
Pipeline: `/analyze` → `/implement` → `/verify` (functional → code review [→ ux] → finalize).
`/implement` (Opus) orchestrates `test-writer` agents → parent test commit → `implementer` agents → automatic `/verify` with reviewer and `check-runner` agents (Sonnet/Haiku); see the skill for detailed rules.
Decisions: recorded in `## Further Notes` of each analysis, with the rejected alternative; there are no ADRs.
Ad-hoc work outside an analysis goes through the `change` skill: tests by `test-writer`, code by `implementer`, checks by `check-runner`, review by `code-reviewer`. The main session reviews and commits; workers never commit or push.
Skills: the shared pack installed in `~/.claude/`; `/setup` updates project configuration, not the pack. Repo-specific additions belong in `docs/agents/config/`.
```

#### issue-tracker.md

Write using templates:

- [issue-tracker-github.md](./issue-tracker-github.md) — active or reference copy
- [issue-tracker-local.md](./issue-tracker-local.md) — active or reference copy

First line must identify backend: `# Issue tracker: GitHub` or `# Issue tracker: Local Markdown`.

### 5. Global pack and old copies

Skip this step when the current working directory **is** the pack itself (cwd contains `skills/setup/SKILL.md` and `agents/`).

The pipeline is the skills `analyze`, `implement`, `change`, `verify`, `code-review`, `ux-review`, `tdd`, `integration-tests` and `commit`, and the agents `test-writer`, `implementer`, `check-runner`, `functional-reviewer`, `code-reviewer` and `ux-reviewer`. Check that each `~/.claude/skills/<name>` and `~/.claude/agents/<name>.md` exists and resolves into the pack; run the pack's `install.sh` if not. `/setup` does not pull or update the pack.

Project definitions take precedence over user ones with the same name, so old project copies shadow the global pack. If step 1 found any, list the exact pipeline skill folders and agent files, plus copies of `setup`, `git-release`, `monorepo-update`, the retired skill `align` and retired agents (`analyst`, `committer`, `correctness-reviewer`, `craft-reviewer`, `spec-reviewer`, `standards-reviewer`), and offer their removal. Never delete without confirmation, never remove a whole skills directory or unrelated skills, and validate that every path stays inside the target repo without symlinked parents. If removal is declined, warn that the copies still shadow the global pack.

The pack no longer uses ADRs. If `docs/agents/config/domain.md` exists, offer its removal and drop any `Domain docs:` line from the `## Agent skills` block. Leave a project's `docs/adr/` in place; the pack simply does not read it.

### 6. Done

Setup complete. Pipeline: `/analyze` → `/implement` → `/verify` (functional → code review [→ ux] → ship).

Report the configuration files updated, whether the global pack resolves, and project copies removed or retained. State that the pack itself was not updated.

User can edit `docs/agents/config/*.md` directly later. Re-run `/setup` to refresh project configuration without touching the rest of `AGENTS.md`. Update the pack separately with `git pull` in its checkout.
