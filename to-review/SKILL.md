---
name: to-review
description: >-
  Review changes since a fixed point along two axes — Standards (repo coding
  conventions) and Spec (originating issue/PRD). Runs parallel sub-agents.
  In monorepos, syncs delivery-root feature branches (checkout + pull) before
  review so the user can validate locally. Use when running `/to-review` on a
  branch, PR, PRD issue, or WIP changes.
disable-model-invocation: true
---

# To Review

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code follow this repo's documented conventions?
- **Spec** — does the code match the originating issue / PRD?

Both axes run as **parallel sub-agents**, then this skill aggregates findings.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` if present — run `/setup` if missing.

If the repo has a monorepo overlay (e.g. `.cursor/skills/to-review/SKILL.md`), read it after this skill.

## Monorepo roles

When `docs/agents/workflow.md` has `## Monorepo` (or nested git repos exist):

| Role | Typical path | Agent may |
|------|--------------|-----------|
| **Container root** | monorepo wrapper (`.`) | `gh issue …`, `make …` from cwd; **stays on `main`** |
| **Delivery roots** | nested git repos (`backend/`, …) | checkout delivery branch, pull, diff for review |

**Container root is never a delivery root** — no delivery-branch checkout, no commit, no push, no PR, no diff for review (submodule pointer bumps are out of scope).

Delivery roots come from `workflow.md` `delivery-roots`, repo overlay, or `git submodule status`. Do not add the container root to that list.

## Process

### 1. Identify the spec source

1. Issue refs from the user (`#123`) or commit messages — fetch via `docs/agents/issue-tracker.md`
2. Path the user passed
3. PRD under `docs/`, `specs/`, or `.scratch/` matching the branch or feature
4. Ask the user; if none, Spec sub-agent reports "no spec available"

From the PRD (or slice parent), read **`## Delivery` → branch name** when present.

### 2. Sync delivery roots (monorepo only)

Skip this step in a single-repo project (no nested delivery roots).

**Container root:** do nothing — remain on current branch (typically `main`).

For each **delivery root** listed in workflow/overlay:

1. `git -C <path> status --short` — if dirty, **STOP** and ask user to stash or commit
2. `git -C <path> fetch origin`
3. Root is **affected** if `origin/<branch>` exists, or a PR exists for `<branch>`, or the branch has commits vs `origin/main`
4. If not affected → skip this root
5. Otherwise:
   ```bash
   git -C <path> checkout <branch>
   git -C <path> pull origin <branch>
   ```
6. Record: path, branch, `git -C <path> rev-parse --short HEAD`

Sync is **independent of `branch-owner`** — review always checks out so the user can inspect locally.

Do **not** use `git show origin/<branch>:path` after sync — review from the local checkout.

Report synced roots in the final aggregate under **## Lokální stav**.

### 3. Pin the fixed point

Default fixed point: `origin/main` (or repo default branch) in **each affected delivery root**.

User may override with commit SHA, branch, tag, `HEAD~N`. Ask if unclear.

Per affected delivery root:

```bash
git -C <path> rev-parse <fixed-point>
git -C <path> diff <fixed-point>...HEAD
git -C <path> log <fixed-point>..HEAD --oneline
```

Single-repo (no monorepo): run the same commands in cwd.

Confirm at least one delivery root has a non-empty diff before spawning sub-agents. Skip roots with empty diff.

**Never** diff the container root.

### 4. Identify standards sources

`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, ADRs, module `AGENTS.md` files. In monorepos, read standards from each affected delivery root.

### 5. Spawn both sub-agents in parallel

One message, two `Task` calls with `subagent_type: generalPurpose`.

**Standards prompt** — include per-root diff commands, commit lists, standards file list:

> Review each affected delivery root separately. For each root run `git -C <path> diff <fixed-point>...HEAD`. Skip roots with empty diff. Never review container root. Report every place the diff violates a documented standard. Cite file + rule. Distinguish hard violations from judgement calls. Skip what tooling enforces. Under 400 words.

**Spec prompt** — include per-root diff commands, commit lists, spec contents:

> Review each affected delivery root separately. For each root run `git -C <path> diff <fixed-point>...HEAD`. Skip roots with empty diff. Report: (a) missing or partial requirements; (b) scope creep; (c) requirements that look wrong. Quote the spec line per finding. Under 400 words.

Skip Spec sub-agent if no spec exists.

### 6. Aggregate

Present under:

- **## Lokální stav** — synced delivery roots (path, branch, SHA); note container root unchanged on `main`
- **## Standards**
- **## Spec**

Do not merge or rerank findings across axes.

End with one line: finding count per axis and worst issue within each axis (if any).

## Why two axes

- Standards pass, Spec fail → correct style, wrong behaviour
- Spec pass, Standards fail → correct feature, wrong conventions

Reporting separately stops one axis masking the other.
