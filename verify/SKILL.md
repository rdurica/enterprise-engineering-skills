---
name: verify
description: >-
  Closer after implementation — Spec vs PRD, Standards, tests, AGENTS.md tooling;
  optional UX; then ship. Agent: ready PR if green, draft PR if the gate fails;
  human stays on HEAD. Comments only on the PRD, never on the PR. Use at the
  end of /implement, or when the user runs /verify after implementation.
disable-model-invocation: true
---

# Verify

Close the work; do not review it. Hard findings become commits. The human arrives at a finished PR (agent) or green HEAD (human). `/implement` runs this skill after all PRD acceptance criteria. `/verify` may be invoked directly if that session died.

Never post findings on a PR (`gh pr review` / `gh pr comment`). Green and fail notes go on the **PRD only**.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` — run `/setup` if missing. If the repo has a verify overlay, read it after this skill: `.cursor/skills/development/verify/SKILL.md`, else `.cursor/skills/verify/SKILL.md`.

**branch-owner** from PRD `## Delivery`, else `workflow.md`. Read the matching file **now** (agent syncs before the diff):

| branch-owner | File |
|--------------|------|
| `human` | [human.md](human.md) |
| `agent` | [github.md](github.md) |

If `workflow.md` has `## Monorepo` (or nested git repos exist), also read [monorepo.md](monorepo.md).

Do **not** set `ready-to-review` or move to `.scratch/prd/done/` on a red gate. Agent still opens or keeps a **draft** PR — **Fail** in [github.md](github.md).

## Phases

1. **Functional** — Spec vs PRD, Standards, local tests + tooling (below)
2. **UX** — if `workflow.md` has `ux-review: enabled`; else skip
3. **Ship** or **Fail** — path file already read (`human.md` / `github.md`)

## Functional gate (max 3 cycles)

Copy and track:

```
Verify cycle: 1 / 3
- [ ] Spec vs PRD
- [ ] Standards
- [ ] Local tests + AGENTS.md tooling
- [ ] Fixes committed (if any)
```

CI, push, and PR are **not** in this gate — they live in [github.md](github.md).

### Spec source

1. Issue refs (`#123`) via `docs/agents/issue-tracker.md`
2. Path the user passed
3. `.scratch/prd/NNN-<slug>.md` (not `prd/done/`), else `docs/` / `specs/`
4. Ask; if none, Spec sub-agent reports "no spec available" — hard failure → **Fail**

From the PRD, read **`## Delivery` → branch name** when present.

### Fixed point

Default: `origin/main` (or repo default) in each affected delivery root. Session may already have a merge-base.

```bash
git -C <path> rev-parse <fixed-point>
git -C <path> diff <fixed-point>...HEAD
git -C <path> log <fixed-point>..HEAD --oneline
```

Single-repo: same in cwd. Need a non-empty diff before Spec/Standards sub-agents.

### Standards sources

`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `docs/adr/`, module `AGENTS.md`. Monorepo: per affected delivery root.

### One cycle

Spec and Standards sub-agents **in parallel** (`Task`, `generalPurpose`), then local tooling.

**Standards prompt** — per-root diff commands, commit lists, standards files:

> Return a fix-list, not a review. For each affected delivery root run `git -C <path> diff <fixed-point>...HEAD`. Skip empty diffs. Never review the container root. Hard documented-standard violations only. Cite file + rule. Skip judgement and what tooling enforces. Format: `- path: <file> — <rule> — change: <what>`. Empty list = green. Do not post comments. Under 400 words.

**Spec prompt** — per-root diffs, commits, full PRD (`## Acceptance criteria`, `## Out of Scope`):

> Return a fix-list, not a review. For each affected delivery root run `git -C <path> diff <fixed-point>...HEAD`. Skip empty diffs. Hard items only: (a) missing or partial AC; (b) scope creep vs Out of Scope. Format: `- path: <file> — <AC or Out of Scope line> — change: <what>`. Empty list = green. Do not post comments. Under 400 words.

**Local pipeline** — each affected root's `AGENTS.md` (and repo-root `AGENTS.md` if commands live there): full relevant tests, cs-fix / phpstan / typecheck as documented. Fail → fix → re-run. Do not push while local gates are red.

**Outcome:** hard Spec/Standards misses, red tests/tooling → fail. Judgement → ignore; do not fail; do not post.

Fail and cycles < 3 → fix, repeat this cycle.

3 Functional failures → **Fail** in the path file already read.

### Fix

One `Task` (`generalPurpose`) per independent failure cluster (sequential if same files). Prompt: PRD Out of Scope, failing output, `tdd` / `integration-tests` when changing tests, no scope creep, no push/PR, no container-root commits.

Parent re-runs failed commands, then **commits** per `commit/SKILL.md`: `fix(scope): <what failed> (#<PRD>)`. Trivial one-file fixes: parent, no sub-agent.

## After Functional green

Check off remaining satisfied AC on the PRD. Then read `ux-review` from `workflow.md`:

- `disabled` or missing → **Ship** in the path file already read
- `enabled` → read and follow `{skills-root}/ux-review/SKILL.md` in this session (`skills-root` = parent of this file’s directory, i.e. `development/`)

### Re-check after UX fixes

When UX review commits fixes, re-run **Local pipeline** on affected roots (same commands as Functional).

- Red → Fix (Functional rules); counts toward Functional cycles (max 3). Do not Ship.
- Green → resume UX gate (re-walk affected screens only per ux-review skill)
- Full Spec/Standards again **only** if the UX fix changes behaviour vs AC; otherwise skip

UX gate green (or skipped / auto-skipped for non-UI diffs) → **Ship** in the path file already read.

UX gate stops after 3 failures → **Fail** in the path file already read.

## Rules

- Max **3** Functional cycles; max **3** UX cycles (owned by ux-review)
- Parent commits; fix sub-agents write code
- No commits on the monorepo container root
- No comments, reviews, or inline notes on a PR — PRD only
