---
name: setup
description: >-
  Configure a repo for the engineering skills pipeline — issue tracker, git
  workflow (branch-owner, push), and domain doc layout. Run once per repo before
  align, to-prd, or to-issues.
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
- `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`
- `docs/agents/` — prior setup output?

If `CLAUDE.md` exists → often indicates human-owned workflow; recommend preset **human-owned**. For agent-managed branches and push handoff → **full-agentic**.

See [workflow-presets.md](./workflow-presets.md) for preset values.

### 2. Interview (preset or three questions)

Offer a preset first; user may confirm or customize.

| # | Question | Options |
|---|----------|---------|
| 1 | **Issue tracker** | GitHub / Local / Both |
| 2 | **Branch owner** | Agent (agent creates/checkouts branch) / Human (user creates branch, agent stays on HEAD) |
| 3 | **Push policy** | each-slice / finalize / never |

**Presets:**

- `full-agentic` — github, agent, each-slice
- `human-owned` — github, human, never

If tracker is **Both**: write active backend to `issue-tracker.md` and reference copies as `issue-tracker.github.md` + `issue-tracker.local.md`.

### 3. Auto-detect

- **Domain layout:** `single-context` unless `CONTEXT-MAP.md` exists → `multi-context`
- **Agent trigger:** `ready-for-implementation` on PRD only (documented in issue-tracker templates)

### 4. Confirm and write

Show draft of:

- `docs/agents/workflow.md` (from [workflow.md.template](./workflow.md.template))
- `docs/agents/issue-tracker.md` (+ reference copies if Both)
- `docs/agents/domain.md`
- `## Agent skills` block patch

Let the user edit, then write.

#### workflow.md

Fill template placeholders: `{{PRESET}}`, `{{BRANCH_OWNER}}`, `{{PUSH}}`, `{{TRACKER_ACTIVE}}`.

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
Domain docs: [single-context | multi-context]. See `docs/agents/domain.md`.
Workflow defaults: `docs/agents/workflow.md` (branch-owner, push, work types).
Pipeline: `/align` → `/to-prd` → `/to-issues` → `/implement` → `/to-review`.
```

#### issue-tracker.md

Write using templates:

- [issue-tracker-github.md](./issue-tracker-github.md) — active or reference copy
- [issue-tracker-local.md](./issue-tracker-local.md) — active or reference copy
- [domain.md](./domain.md)

First line must identify backend: `# Issue tracker: GitHub` or `# Issue tracker: Local Markdown`.

### 5. Done

Setup complete. Pipeline: `/align` → `/to-prd` → `/to-issues` → `/implement` → `/to-review`.

User can edit `docs/agents/*.md` directly later. Re-run `/setup` to update workflow without touching the rest of `CLAUDE.md`.
