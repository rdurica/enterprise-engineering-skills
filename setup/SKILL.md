---
name: setup
description: >-
  Configure a repo for the engineering skills pipeline — issue tracker, git
  workflow (branch-owner, push), and docs/adr. Run once per repo before
  align, analyze, or implement.
disable-model-invocation: true
---

# Setup

One-time per-repo configuration. Run inside the **target project** (not the skills repo).

The shared skills pack (`~/.codex/skills`, `~/.cursor/skills`, `~/.claude/skills` or `~/.agents/skills`) is shared across machines. Per-repo differences live in `docs/agents/workflow.md`.

## Process

### 1. Explore

Read what already exists — do not assume:

- `git remote -v` — GitHub? No remote?
- `AGENTS.md` — existing `## Agent skills` block?
- `docs/adr/` — existing ADRs?
- `docs/agents/` — prior setup output?
- **Skills dir** — reuse `skills-dir` from the session or existing `workflow.md`. Otherwise look for an existing vendored pipeline (for example in `.agents/skills/`, `.codex/skills/`, `.cursor/skills/` or `.claude/skills/`; custom paths are valid too). Reuse a single unambiguous installation; if none or several are found, ask which project path the user wants. Do not infer the active harness from unrelated config folders or use an editor-specific fallback.
- **Monorepo:** nested git repos — run `git submodule status` and/or find nested `.git` dirs (excluding `.git/modules/`). If found, note paths and remotes for the `## Monorepo` section in `workflow.md`.

The normal entry point is the user running the pipeline locally. Recommend **human-owned** when the user wants to keep their current branch and manage PRs; recommend **full-agentic** when the agent should manage branches and PRs. Do not infer branch ownership from editor files or the tracker.

See [workflow-presets.md](./workflow-presets.md) for preset values.

### 2. Interview (preset + language + UX review)

Reuse settings already established in the session or existing `workflow.md`; show the resulting draft for review. For missing settings, offer a preset or ask only the unanswered questions.

**Resolve when unknown** (presets do not set these):

- **Language:** English (`en`) / Czech (`cs`) — published analysis prose and ticket comments
- **UX/UI review before finalization?** Enabled (browser walkthrough + hard gate) / Disabled
- **Skills dir:** reuse the configured or unambiguous existing path; otherwise ask for the project path used by the user’s harness. Multiple harnesses may share a skills directory when supported; do not assume a path is discoverable by every runner.

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

- `docs/agents/workflow.md` (from [workflow.md.template](./workflow.md.template))
- `docs/agents/issue-tracker.md` (+ reference copies if Both)
- `docs/agents/domain.md`
- `## Agent skills` block patch

Let the user edit, then write.

#### workflow.md

Fill template placeholders: `{{PRESET}}`, `{{BRANCH_OWNER}}`, `{{PUSH}}`, `{{TRACKER_ACTIVE}}`, `{{LANGUAGE}}`, `{{UX_REVIEW}}`, `{{SKILLS_DIR}}`, `{{MONOREPO_SECTION}}`.

**`{{UX_REVIEW}}`** — `enabled` or `disabled` from the UX/UI review interview answer.

**`{{SKILLS_DIR}}`** — the skills dir confirmed in the interview, without a trailing slash.

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

Issue tracker: [GitHub | local markdown]. See `docs/agents/issue-tracker.md`.
Domain docs: `docs/adr/`. See `docs/agents/domain.md`.
Workflow defaults: `docs/agents/workflow.md` (branch-owner, push, language, work types).
Pipeline: `/align` → `/analyze` → `/implement` → `/verify` (functional → code review [→ ux] → finalize).
`/implement` orchestrates fresh test subagents → parent test commit → fresh implementation subagents → automatic `/verify`; see the skill for detailed rules.
Project skills: `<skills-dir>/` (vendored by `/setup`; re-running `/setup` overwrites them). Repo-specific additions belong in `docs/agents/`, not in the vendored files.
```

Substitute `<skills-dir>` with the confirmed path.

#### issue-tracker.md

Write using templates:

- [issue-tracker-github.md](./issue-tracker-github.md) — active or reference copy
- [issue-tracker-local.md](./issue-tracker-local.md) — active or reference copy
- [domain.md](./domain.md)

First line must identify backend: `# Issue tracker: GitHub` or `# Issue tracker: Local Markdown`.

### 5. Vendor pipeline skills

Copy pipeline skills into the **target repo** at the confirmed skills dir (one folder per skill, no nesting) so the pipeline is in git and available to the user’s configured harness.

**Skip this step** when the current working directory **is** the skills pack itself (cwd contains `setup/SKILL.md` at the repo root).

**Source:** use the shared pack containing this invoked `setup/SKILL.md` (pack root is the parent of `setup/`), or the source explicitly selected by the user. If this is a stale/vendored copy rather than the maintained pack, resolve the maintained source before refreshing; do not select another harness’s pack merely because its directory exists. Do **not** copy `personal/`.

**Destination:** `<target-repo>/<skills-dir>/` at the container root (not inside delivery roots).

**Copy only these directories** (pipeline + commit format + helpers implement/verify read):

```
align  analyze  implement  verify  code-review  ux-review  tdd  integration-tests  commit
```

`setup`, `git-release` and `monorepo-update` stay in the shared pack — they are global tools, not part of the per-repo pipeline.

**Refresh every required skill:** validate that the source contains all listed skills and the confirmed destination stays inside the target repo, without source overlap or symlinked destination paths. Stage complete copies before replacing anything. Replace only the listed folders, retaining the old copies until the new install is checked so a failed refresh can be restored. Leave unrelated folders untouched; repo-specific deviations belong in `docs/agents/`.

**Stale folders:** if `<skills-dir>/setup`, `<skills-dir>/git-release` or `<skills-dir>/monorepo-update` exist from an older run, report them and offer to remove them. Never delete without confirmation.

Do not add the skills dir to `.gitignore` — these files should be committed with the repo.

In a monorepo, vendor once at the container root. Do not copy into each delivery root.

### 6. Done

Setup complete. Pipeline: `/align` → `/analyze` → `/implement` → `/verify` (functional → code review [→ ux] → ship).

Report which skills were vendored or updated and which stale folders were found.

User can edit `docs/agents/*.md` directly later. Re-run `/setup` to update workflow without touching the rest of `AGENTS.md`. Re-running is also how the repo picks up an updated shared pack — every vendored skill is overwritten.
