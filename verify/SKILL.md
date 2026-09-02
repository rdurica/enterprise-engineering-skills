---
name: verify
description: >-
  Closer after implementation — Spec vs analysis, Standards, tests, AGENTS.md
  tooling; optional UX; then ship. Agent: ready PR if green, draft PR if the
  gate fails; human stays on HEAD. Comments only on the analysis, never on the
  PR. Use at the end of /implement, or when the user runs /verify after
  implementation.
disable-model-invocation: true
---

# Verify

Close the work; do not review it. Hard findings become commits. The human arrives at a finished PR (agent) or green HEAD (human). `/implement` runs this skill after decided analysis parts. `/verify` may be invoked directly if that session died.

Never post findings on a PR (`gh pr review` / `gh pr comment`). Green and fail notes go on the **analysis only**.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` — run `/setup` if missing. If the repo has a verify overlay, read it after this skill: `.cursor/skills/verify/SKILL.md`.

Read `language` from `workflow.md`.

**branch-owner** from analysis `## Delivery`, else `workflow.md`. Read the matching file **now** (agent syncs before the diff):

| branch-owner | File |
|--------------|------|
| `human` | [human.md](human.md) |
| `agent` | [github.md](github.md) |

If `workflow.md` has `## Monorepo` (or nested git repos exist), also read [monorepo.md](monorepo.md).

Do **not** set `ready-to-review` or move to `.scratch/analysis/done/` on a red gate. A red gate ends in `needs-attention` (label on GitHub, `Status:` locally) — it replaces `in-progress`, so the analysis is visibly waiting on a human. Agent still opens or keeps a **draft** PR — **Fail** in [github.md](github.md).

## Phases

1. **Functional** — Spec vs analysis, Standards, local tests + tooling (below)
2. **UX** — if `workflow.md` has `ux-review: enabled`; else skip
3. **Ship** or **Fail** — path file already read (`human.md` / `github.md`)

## Functional gate (max 3 cycles)

Copy and track:

```
Verify cycle: 1 / 3
- [ ] Spec vs analysis
- [ ] Standards
- [ ] Local tests + AGENTS.md tooling
- [ ] Fixes committed (if any)
```

CI, push, and PR are **not** in this gate — they live in [github.md](github.md).

### Spec source

1. Issue refs (`#123`) via `docs/agents/issue-tracker.md`
2. Path the user passed
3. `.scratch/analysis/NNN-<slug>.md` (not `analysis/done/`), else `docs/` / `specs/`
4. Ask; if none, Spec sub-agent reports "no spec available" — hard failure → **Fail**

From the analysis, read **`## Delivery` → branch name** when present.

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

**Spec prompt** — per-root diffs, commits, full analysis (`## Acceptance`, `## Change`, `## API Contracts` if present, `## Architecture`, `## FAQ`):

> Return a fix-list, not a review. For each affected delivery root run `git -C <path> diff <fixed-point>...HEAD`. Skip empty diffs. Hard items only: (a) missing or partial `## Acceptance`; (b) scope creep vs `## Change` / `## Architecture`; (c) diff that invents an answer to an open `## FAQ` item; (d) `## Acceptance` behaviour with no test proving it in the diff; (e) non-trivial handler/domain/VO logic in the diff (branches, invariant, calculation, policy) with no unit test proving that logic — HTTP integration alone is not enough; skip (e) for pure wiring with no branches. Open FAQ by itself is not a failure. Format: `- path: <file> — <Acceptance, Change, Architecture, FAQ, or unit-test line> — change: <what>`. Empty list = green. Do not post comments. Under 400 words.

**Local pipeline** — each affected root's `AGENTS.md` (and repo-root `AGENTS.md` if commands live there): full relevant tests, cs-fix / phpstan / typecheck as documented. Fail → fix → re-run. Do not push while local gates are red.

**Outcome:** hard Spec/Standards misses, red tests/tooling → fail. Judgement → ignore; do not fail; do not post.

Fail and cycles < 3 → fix, repeat this cycle.

3 Functional failures → **Fail** in the path file already read.

### Fix

One `Task` (`generalPurpose`) per independent failure cluster (sequential if same files). Prompt: analysis Change/Architecture, failing output, `tdd` / `integration-tests` when changing tests, no scope creep, no push/PR, no container-root commits.

Parent re-runs failed commands, then **commits** per `commit/SKILL.md`: `fix(scope): <what failed> (#<N>)`. Trivial one-file fixes: parent, no sub-agent.

## After Functional green

Check off remaining satisfied Acceptance on the analysis. Then read `ux-review` from `workflow.md`:

- `disabled` or missing → **Ship** in the path file already read
- `enabled` → read and follow `{skills-root}/ux-review/SKILL.md` in this session (`skills-root` = parent of this file’s directory)

### Re-check after UX fixes

When UX review commits fixes, re-run **Local pipeline** on affected roots (same commands as Functional).

- Red → Fix (Functional rules); counts toward Functional cycles (max 3). Do not Ship.
- Green → resume UX gate (re-walk affected screens only per ux-review skill)
- Full Spec/Standards again **only** if the UX fix changes behaviour vs Acceptance; otherwise skip

UX gate green (or skipped / auto-skipped for non-UI diffs) → **Ship** in the path file already read.

UX gate stops after 3 failures → **Fail** in the path file already read.

## Rules

- Max **3** Functional cycles; max **3** UX cycles (owned by ux-review)
- Parent commits; fix sub-agents write code
- No commits on the monorepo container root
- No comments, reviews, or inline notes on a PR — analysis only
