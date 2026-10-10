---
name: setup
description: >-
  Configure a repo for the engineering skills pipeline — issue tracker, git
  workflow (branch-owner, push), docs/adr, and global or project skills
  and agents.
  Run before align, analyze, or implement, or again to refresh configuration.
disable-model-invocation: true
model: sonnet
effort: high
---

# Setup

Configure or refresh a repo. Run inside the **target project** (not the skills repo).

The shared pack is one git checkout with two folders: `skills/` (one folder per skill) and `agents/` (one subagent definition per file). Its `install.sh` links them into `~/.claude/skills/` and `~/.claude/agents/`. Pack root is the parent of the `skills/` directory containing this skill. Per-repo differences live in `docs/agents/config/workflow.md`.

Skills and agents carry their own `model` and `effort` in frontmatter: the orchestrating skills run on Opus, delegated work on Sonnet, check running on Haiku. Never rewrite those values while copying; a project that needs different models changes its vendored copies deliberately.

## Process

### 1. Explore

Read what already exists — do not assume:

- `git remote -v` — GitHub? No remote?
- `AGENTS.md` — existing `## Agent skills` block?
- `docs/adr/` — existing ADRs?
- `docs/agents/config/` — prior setup output? Also inspect any legacy configuration directly under `docs/agents/` to recover saved settings on refresh.
- **Skills mode and existing copies** — read `skills-mode` and `skills-dir` from existing `workflow.md` and inspect any configured project skills directory. Read `agents-dir` too. Look for existing pipeline copies in `.claude/skills/` and `.claude/agents/`, plus legacy copies in `.agents/skills/`, `.codex/skills/` or `.cursor/skills/` from older Codex/Cursor setups; custom paths are valid too. Record existing paths for refresh or cleanup, but do not ask for a destination until copying is selected.
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

### 3. Choose skills mode

On every run, offer **Copy pipeline skills and agents into this project?** unless the user has already explicitly chosen for this run:

- **No — global** (`skills-mode: global`): use the shared pack installed in `~/.claude/`; do not copy skills or agents or ask for a destination. `/setup` does not download or update the shared pack.
- **Yes — project copies** (`skills-mode: vendored`): keep the pipeline in the project's git history and refresh it from the maintained shared pack on every `/setup`.

Preselect the saved `skills-mode`. For legacy configuration with `skills-dir` but no mode, preselect `vendored` to preserve existing behavior. Otherwise recommend `global`. Presets do not choose the mode; the user can change it on every run.

For `vendored`, reuse the configured or single unambiguous existing project paths; otherwise default to `.claude/skills` and `.claude/agents`, which Claude Code loads from the project root.

For `global`, verify that Claude Code discovers every required pipeline skill and agent from the shared pack independently of project copies before offering their removal. A checkout path or an `AGENTS.md` reference alone is not proof of discovery. Check that `~/.claude/skills/<name>` and `~/.claude/agents/<name>.md` exist and resolve into the pack (run the pack's `install.sh` if they do not), then confirm in a fresh session with `/skills` and `/agents`. Project definitions take precedence over user ones with the same name, so remaining copies shadow the global pack. If discovery cannot be verified or required skills are missing, retain project copies and report the missing global setup; do not offer cleanup yet.

Once global discovery is verified, if project copies exist, list the exact known pipeline directories and offer their removal with separate confirmation. Keep the old paths available for cleanup even though the new workflow omits `skills-dir`. If removal is declined, leave them untouched and warn that Claude Code still loads them and they shadow the global pack. Do not claim global-only loading while copies remain.

### 4. Auto-detect

- **Agent trigger:** GitHub `ready-for-agent` (optional auto-start). Happy path: human reviews the analysis, then runs `/implement`. User-invoked `/implement` does not require the label.
- **Monorepo:** if nested git repos were found in Explore, include `## Monorepo` in the workflow draft (see below). Otherwise omit the section.

### 5. Confirm and write

Show draft of:

- `docs/agents/config/workflow.md` (from [workflow.md.template](./workflow.md.template))
- `docs/agents/config/issue-tracker.md` (+ reference copies if Both)
- `docs/agents/config/domain.md`
- `## Agent skills` block patch

Let the user edit, then write.

On re-runs, refresh these managed outputs using the current templates and confirmed settings. Preserve project-specific documentation and additions in `docs/agents/config/`; merge existing content rather than blindly replacing it. Leave unrelated files untouched.

Keep configuration and project-specific instruction overlays in `docs/agents/config/`, active local analyses in `docs/agents/analysis/`, and completed analyses in `docs/agents/analysis/done/`. Refresh only configuration; never overwrite, move or delete analyses during setup. When refreshing a legacy project, read its old configuration to preserve settings and additions, then write the current configuration under `config/`; leave legacy files untouched and report their paths.

Do not automatically ignore, stage or commit `docs/agents/`. Versioning agent configuration and analyses is the project's choice.

#### workflow.md

Fill template placeholders: `{{PRESET}}`, `{{BRANCH_OWNER}}`, `{{PUSH}}`, `{{TRACKER_ACTIVE}}`, `{{LANGUAGE}}`, `{{UX_REVIEW}}`, `{{SKILLS_MODE}}`, `{{SKILLS_LOCATION}}`, `{{MONOREPO_SECTION}}`.

**`{{UX_REVIEW}}`** — `enabled` or `disabled` from the UX/UI review interview answer.

**`{{SKILLS_MODE}}`** — `global` or `vendored` from the skills-mode step.

**`{{SKILLS_LOCATION}}`** — for `vendored`, write `- skills-dir: <confirmed project path>` and `- agents-dir: <confirmed project path>` (without trailing slashes), then explain that every `/setup` refreshes the copies. For `global`, omit both and state that Claude Code uses the shared pack installed in `~/.claude/`, updated separately from `/setup` (`git pull` in the pack). In both modes, repo-specific additions belong in `docs/agents/config/`.

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
Domain docs: `docs/adr/`. See `docs/agents/config/domain.md`.
Workflow defaults: `docs/agents/config/workflow.md` (branch-owner, push, language, work types).
Pipeline: `/align` → `/analyze` → `/implement` → `/verify` (functional → code review [→ ux] → finalize).
`/implement` (Opus) orchestrates `test-writer` agents → parent test commit → `implementer` agents → automatic `/verify` with reviewer and `check-runner` agents (Sonnet/Haiku); see the skill for detailed rules.
Skills: <mode-specific location and refresh behavior>. Repo-specific additions belong in `docs/agents/config/`.
```

For `vendored`, substitute `project copies in <skills-dir>/ and <agents-dir>/; every /setup refreshes them from the maintained shared pack`. For `global`, substitute `the shared pack installed in ~/.claude/; /setup updates project configuration, not the global pack`. Do not put a machine-specific global path into project configuration. If copies remain in global mode, also record their paths and the possible loading conflict in this block.

#### issue-tracker.md

Write using templates:

- [issue-tracker-github.md](./issue-tracker-github.md) — active or reference copy
- [issue-tracker-local.md](./issue-tracker-local.md) — active or reference copy
- [domain.md](./domain.md)

First line must identify backend: `# Issue tracker: GitHub` or `# Issue tracker: Local Markdown`.

### 6. Apply skills mode

**Skip copying and cleanup** when the current working directory **is** the skills pack itself (cwd contains `skills/setup/SKILL.md` and `agents/`).

**Global mode:** do not create a project skills directory or copy files. Remove only the exact known pipeline directories separately confirmed in step 3; validate that each stays inside the target repo, without source overlap or symlinked paths. Never remove the whole skills directory or unrelated skills. Report copies left behind. The nine skill directories and the agent files listed below define the pipeline; legacy `setup`, `git-release` and `monorepo-update` copies may also be offered for removal, with explicit confirmation. Then proceed to Done; do not run the vendoring procedure.

**Vendored mode:** follow the refresh procedure below on every run.

Copy pipeline skills and agents into the **target repo** at the confirmed skills and agents dirs (one folder per skill, one file per agent, no nesting) so the pipeline is in git and available to Claude Code.

**Source:** use the shared pack containing this invoked `setup/SKILL.md` (pack root is the parent of `skills/`; resolve symlinks first), or the source explicitly selected by the user. If this is a stale/vendored copy rather than the maintained pack, resolve the maintained source before refreshing. Do **not** copy `personal/`.

**Destination:** `<target-repo>/<skills-dir>/` and `<target-repo>/<agents-dir>/` at the container root (not inside delivery roots).

**Copy only these directories** (pipeline + commit format + helpers implement/verify read):

```
skills/: align  analyze  implement  verify  code-review  ux-review  tdd  integration-tests  commit
agents/: test-writer  implementer  check-runner  spec-reviewer  standards-reviewer
         code-reviewer  ux-reviewer   (each <name>.md)
```

`setup`, `git-release` and `monorepo-update` stay in the shared pack — they are global tools, not part of the per-repo pipeline.

**Refresh every required skill:** validate that the source contains all listed skills and the confirmed destination stays inside the target repo, without source overlap or symlinked destination paths. Stage complete copies before replacing anything. Replace only the listed folders and agent files, retaining the old copies until the new install is checked so a failed refresh can be restored. Leave unrelated folders untouched; repo-specific deviations belong in `docs/agents/config/`.

**Stale folders:** if `<skills-dir>/setup`, `<skills-dir>/git-release` or `<skills-dir>/monorepo-update`, or the retired agents `analyst.md`, `committer.md`, `correctness-reviewer.md` and `craft-reviewer.md` in `<agents-dir>`, exist from an older run, report them and offer to remove them. Never delete without confirmation.

Do not add the skills or agents dir to `.gitignore` — these files should be committed with the repo.

In a monorepo, vendor once at the container root. Do not copy into each delivery root.

### 7. Done

Setup complete. Pipeline: `/align` → `/analyze` → `/implement` → `/verify` (functional → code review [→ ux] → ship).

Report the selected mode, configuration files updated, skills and agents copied/refreshed or removed, and any stale or retained project copies. In global mode, state that the shared pack was not updated.

User can edit `docs/agents/config/*.md` directly later. Re-run `/setup` to review or change the mode and refresh project configuration without touching the rest of `AGENTS.md`. In vendored mode, every pipeline skill and agent is refreshed from the maintained shared pack; in global mode, update that pack separately.
