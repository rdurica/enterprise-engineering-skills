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

Skills repo (`~/.cursor/skills`) is shared across machines. Per-repo differences live in `docs/agents/workflow.md`.

## Process

### 1. Explore

Read what already exists — do not assume:

- `git remote -v` — GitHub? No remote?
- `CLAUDE.md` or `AGENTS.md` — existing `## Agent skills` block?
- `docs/adr/` — existing ADRs?
- `docs/agents/` — prior setup output?
- `.cursor/skills/` — project-vendored pipeline skills already present?
- **Monorepo:** nested git repos — run `git submodule status` and/or find nested `.git` dirs (excluding `.git/modules/`). If found, note paths and remotes for the `## Monorepo` section in `workflow.md`.

If `CLAUDE.md` exists → often indicates human-owned workflow; recommend preset **human-owned**. For agent-managed branches and push after verify → **full-agentic**.

See [workflow-presets.md](./workflow-presets.md) for preset values.

### 2. Interview (preset + language + UX review)

Offer a preset first; user may confirm or customize.

**Always ask** (presets do not set these):

- **Language:** English (`en`) / Czech (`cs`) — published analysis prose and ticket comments
- **UX/UI review before PR?** Enabled (browser walkthrough + hard gate) / Disabled

Then, unless a preset already answered them:

| # | Question | Options |
|---|----------|---------|
| 1 | **Issue tracker** | GitHub / Local / Both |
| 2 | **Branch owner** | Agent (agent creates/checkouts branch) / Human (user creates branch, agent stays on HEAD) |
| 3 | **Push policy** | finalize / never |

**Presets:**

- `full-agentic` — github, agent, finalize
- `human-owned` — github, human, never

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

Fill template placeholders: `{{PRESET}}`, `{{BRANCH_OWNER}}`, `{{PUSH}}`, `{{TRACKER_ACTIVE}}`, `{{LANGUAGE}}`, `{{UX_REVIEW}}`, `{{MONOREPO_SECTION}}`.

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

**Edit target:** `CLAUDE.md` if it exists, else `AGENTS.md`. Never create both.

**CLAUDE.md safe merge:**

1. If `CLAUDE.md` exists → upsert `## Agent skills` block only; do **not** touch other sections
2. If block missing → append to end of `CLAUDE.md`
3. If neither `CLAUDE.md` nor `AGENTS.md` exists → create **AGENTS.md** (do not create `CLAUDE.md`)
4. Never overwrite the full file; never duplicate the block

```markdown
## Agent skills

Issue tracker: [GitHub | local markdown]. See `docs/agents/issue-tracker.md`.
Domain docs: `docs/adr/`. See `docs/agents/domain.md`.
Workflow defaults: `docs/agents/workflow.md` (branch-owner, push, language, work types).
Pipeline: `/align` → `/analyze` → `/implement` → `/verify` (functional [→ ux] → ship).
Project skills: `.cursor/skills/` (vendored by `/setup` if missing).
```

#### issue-tracker.md

Write using templates:

- [issue-tracker-github.md](./issue-tracker-github.md) — active or reference copy
- [issue-tracker-local.md](./issue-tracker-local.md) — active or reference copy
- [domain.md](./domain.md)

First line must identify backend: `# Issue tracker: GitHub` or `# Issue tracker: Local Markdown`.

### 5. Vendor pipeline skills

Copy pipeline skills into the **target repo** at `.cursor/skills/` (one folder per skill, no nesting) so the pipeline is in git and works for Cursor and Claude Code.

**Skip this step** when the current working directory **is** the skills pack itself (cwd contains `setup/SKILL.md` at the repo root).

**Source (prefer shared pack):** `$HOME/.cursor/skills` when it contains `setup/SKILL.md`. Else parent of this skill file (so a fresh checkout of the skills repo still works). Never copy from `~/.cursor/skills-cursor/` or from the target’s already-vendored tree as the preferred source — that tree is often stale and missing new skills like `analyze`. Do **not** copy `images/`.

**Destination:** `<target-repo>/.cursor/skills/` at the container root (not inside delivery roots).

**Copy only these directories** (pipeline + commit format + helpers implement/verify read):

```
align  analyze  implement  verify  ux-review  tdd  integration-tests  setup  git-release  monorepo-update  commit
```

**If missing only:** if `$DEST/<name>/SKILL.md` already exists, skip that skill (keep project overlays). Re-running `/setup` after updating the shared pack therefore vendors **new** pipeline skills without overwriting project overlays.

```bash
SOURCE="$HOME/.cursor/skills"
if [ ! -f "$SOURCE/setup/SKILL.md" ]; then
  SOURCE="<pack-root>"   # parent of this setup/SKILL.md
fi
DEST=".cursor/skills"
mkdir -p "$DEST"
for name in align analyze implement verify ux-review tdd integration-tests setup git-release monorepo-update commit; do
  if [ -f "$DEST/$name/SKILL.md" ]; then
    echo "skip $name (already vendored)"
    continue
  fi
  if [ ! -d "$SOURCE/$name" ]; then
    echo "warn $name missing in source" >&2
    continue
  fi
  cp -a "$SOURCE/$name" "$DEST/$name"
done
```

Do not add `.cursor/skills` to `.gitignore` — these files should be committed with the repo.

In a monorepo, vendor once at the container root. Do not copy into each delivery root.

### 6. Done

Setup complete. Pipeline: `/align` → `/analyze` → `/implement` → `/verify` (functional [→ ux] → ship).

Report which skills were copied and which were skipped as already present.

User can edit `docs/agents/*.md` directly later. Re-run `/setup` to update workflow without touching the rest of `CLAUDE.md`. Re-run also copies any still-missing skills; it does not overwrite existing `.cursor/skills/*`.
