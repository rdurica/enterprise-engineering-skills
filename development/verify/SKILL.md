---
name: verify
description: >-
  Gate before human review — Spec vs PRD, Standards, tests, AGENTS.md tooling.
  Then ship: agent opens a PR; human stays on HEAD. Use at the end of
  /implement, or when the user runs /verify after implementation.
disable-model-invocation: true
---

# Verify

Nothing ships until this gate is green. `/implement` runs this skill after all PRD acceptance criteria. `/verify` may be invoked directly if that session died.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` — run `/setup` if missing. If the repo has a verify overlay, read it after this skill: `.cursor/skills/development/verify/SKILL.md`, else `.cursor/skills/verify/SKILL.md`.

**branch-owner** from PRD `## Delivery`, else `workflow.md`. Read the matching file **now** (agent syncs before the diff):

| branch-owner | File |
|--------------|------|
| `human` | [human.md](human.md) |
| `agent` | [github.md](github.md) |

If `workflow.md` has `## Monorepo` (or nested git repos exist), also read [monorepo.md](monorepo.md).

Do **not** open a PR, set `ready-to-review`, or move to `.scratch/prd/done/` on a red gate.

## Gate (max 3 cycles)

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
4. Ask; if none, Spec sub-agent reports "no spec available" — hard failure, do not ship

From the PRD, read **`## Delivery` → branch name** when present.

### Fixed point

Default: `origin/main` (or repo default) in each affected delivery root. Session may already have a merge-base.

```bash
git -C <path> rev-parse <fixed-point>
git -C <path> diff <fixed-point>...HEAD
git -C <path> log <fixed-point>..HEAD --oneline
```

Single-repo: same in cwd. Need a non-empty diff before review sub-agents.

### Standards sources

`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `docs/adr/`, module `AGENTS.md`. Monorepo: per affected delivery root.

### One cycle

Spec and Standards sub-agents **in parallel** (`Task`, `generalPurpose`), then local tooling.

**Standards prompt** — per-root diff commands, commit lists, standards files:

> Review each affected delivery root separately. For each root run `git -C <path> diff <fixed-point>...HEAD`. Skip empty diffs. Never review container root. Report every documented-standard violation. Cite file + rule. Hard vs judgement. Skip what tooling enforces. Under 400 words.

**Spec prompt** — per-root diffs, commits, full PRD (`## Acceptance criteria`, `## Out of Scope`):

> Review each affected delivery root separately. For each root run `git -C <path> diff <fixed-point>...HEAD`. Skip empty diffs. Report: (a) missing or partial AC; (b) scope creep vs Out of Scope; (c) requirements that look wrong. Quote the spec line. Under 400 words.

**Local pipeline** — each affected root's `AGENTS.md` (and repo-root `AGENTS.md` if commands live there): full relevant tests, cs-fix / phpstan / typecheck as documented. Fail → fix → re-run. Do not push while local gates are red.

**Outcome:** hard Spec/Standards misses, red tests/tooling → fail. Judgement calls → record, do not fail.

Green → **Ship** in the path file already read.

Fail and cycles < 3 → fix, repeat this cycle.

3 failures → **stop**. Leave `in-progress`. Comment problems in `prd-language`. Do not ship.

### Fix

One `Task` (`generalPurpose`) per independent failure cluster (sequential if same files). Prompt: PRD Out of Scope, failing output, `tdd` / `integration-tests` when changing tests, no scope creep, no push/PR, no container-root commits.

Parent re-runs failed commands, then **commits** per `commit/SKILL.md`: `fix(scope): <what failed> (#<PRD>)`. Trivial one-file fixes: parent, no sub-agent.

## Rules

- Max **3** gate cycles
- Parent commits; fix sub-agents write code
- No commits on the monorepo container root
