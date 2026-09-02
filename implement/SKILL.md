---
name: implement
description: >-
  Implement a published analysis — one TDD sub-agent per cluster of
  overlapping Acceptance items (HTTP + unit where there is decision
  logic), parallel when paths are disjoint; parent commits, then runs
  verify. Use when picking up an analysis issue or /implement #N.
disable-model-invocation: true
---

# Implement

Fetch the analysis, set `in-progress`, follow `docs/agents/workflow.md` for branch and monorepo. Sub-agents write product code and tests. Parent orchestrates, commits, checks off `## Acceptance`, then runs verify. Do not push or open a PR.

Source of truth is the analysis body. Run `/setup` if `docs/agents/` is missing.

Skills root: parent of this file. Read `{skills-root}/tdd/SKILL.md` (and `integration-tests/SKILL.md` for PHP HTTP). Pass those paths in any sub-agent prompt. When committing, follow `{skills-root}/commit/SKILL.md`.

Read `language` from `workflow.md`.

## 1. Preflight

Fetch the analysis per `docs/agents/issue-tracker.md`. GitHub: `#N`. Local: `/implement 001`, `#1`, or `<slug>` → `.scratch/analysis/NNN-<slug>.md`. **Stop** if GitHub has `ready-to-review`, or the only local match is under `.scratch/analysis/done/`. User invoked `/implement` → proceed (do not require `ready-for-agent`). Auto-start without the user → only if `ready-for-agent` or already `in-progress`; **never** when `needs-attention` is set. Set `in-progress` (removing `needs-attention` if present — this is the resume path after a human acted). User may pass `human` or `agent` to override branch-owner for this session.

Open `## FAQ`: do **not** invent answers. Implement decided parts only; skip parts that depend on open FAQ, or leave the session for later.

## 2. Branch

From analysis `## Delivery`, else `workflow.md`. **human:** stay on HEAD. Never commit on a monorepo container root.

**agent:** in each delivery root (not the container root):

1. `git status` — creating a new branch and the tree is dirty → **stop**. Existing branch: unrelated dirty files → **stop**.
2. `git fetch origin` — missing `origin` or fetch fails → **stop**.
3. Default base: `origin/HEAD`, else `origin/main`, else `origin/master`.
4. `<branch>` exists locally or on origin → checkout; if `origin/<branch>` exists, `git pull --rebase`. Do not reset onto origin/default.
5. `<branch>` does not exist → create from origin, never from HEAD:

```bash
git checkout --no-track -b <branch> origin/<default>
```

`--no-track` so the new branch does not track `origin/main`.

## 3. Plan

Product code always goes through **sub-agents**. A flat Architecture does not skip agents.

**Part** = one unchecked `- [ ]` in `## Acceptance` (one observable behaviour). Architecture `###` maps units and paths — it is not the size of an agent. Map each part to a `###` (path / delivery root). An item that spans two units is a bad Acceptance item — implement the decided seam only.

**Cluster** = consecutive unchecked parts that map to the same Architecture `###` / delivery root and share files (same module, same endpoint / test class). That is the size of one agent. A single part with no overlap is a cluster of one. Cap **~8** parts per cluster; leftover overlapping parts become the next sequential cluster after commit.

No `###`: still cluster by shared paths; a lone part is one agent. Parallel only when Change/Architecture paths are clearly disjoint.

`## Acceptance` is verify + TDD constraint, not a WBS. Print the plan **by cluster** (items, unit, path, wave) — not one sequential wave per overlapping part. Resume: skip work already in the branch / checked Acceptance.

Group into **waves**:

- **Same wave (parallel):** disjoint clusters, neither depends on the other's output. Typical: different delivery roots, or different modules with disjoint directories.
- **Next wave after commit:** next overlapping cluster (same module / shared files), or leftover parts past the ~8 cap.
- **Unclear / overlapping / single unit:** one sequential cluster. Do not guess.

Same worktree — safety is disjoint paths, not isolated checkouts.

## 4. Execute

Independent clusters in a wave: spawn them in **one parent turn** with multiple `Task` calls. Overlapping clusters: one at a time, then commit, then the next.

**Sub-agent:** one `generalPurpose` `Task` per cluster. It writes code and tests only — no commit, push, PR, branch change, nested agents, or container-root commits. Prompt: **all** Acceptance items in this cluster (the list, not one item); analysis Change / Architecture (relevant `###`) / API Contracts as constraints; open FAQ to skip; skill paths (`tdd`, and `integration-tests` for PHP HTTP); `AGENTS.md` commands; delivery-root paths; no scope creep (stay inside Change/Architecture).

Finish every item in the prompt, then return. Stuck on one item: return done vs remaining — parent checks off only the done. For **each** item, cover both seams that apply (see `tdd/SKILL.md`):

- HTTP contract → `integration-tests`
- Decision logic in handler / domain / VO → unit test (HTTP does not replace it)
- Pure wiring, no branches → skip unit
- No HTTP → unit only

Order: highest seam first (HTTP when the item is HTTP-shaped), then unit for the same decision. Writing the tests for the whole cluster first, then implementing, is allowed. One-test-at-a-time is also fine — not required.

**Parent** does not write product code except a one-file follow-up after the agent (import, typo).

After the wave joins: per cluster, diff and relevant tests. Small failures: fix yourself (one file). Large: another sub-agent with the error (still this cluster / this fail). Non-overlapping fixes in the same wave may run in parallel; overlapping files sequential.

Commit in each affected delivery root per `commit/SKILL.md`. One item: `feat(scope): <acceptance title> (#<N>)`. Cluster of several: `feat(scope): <shared theme> (#<N>)`. Check off every completed `## Acceptance` item in the cluster. Do not comment on the ticket after each cluster. Commit messages stay English. Then the next wave.

## 5. Verify

Decided parts done (or all parts if no blocking FAQ) → read and follow `{skills-root}/verify/SKILL.md` in this session. If FAQ skipped work remains: set `needs-attention` (replacing `in-progress`), comment what remains in `language`; do not run verify as if the analysis were complete. If the session dies first: leave `in-progress` — that state is resumable and needs no human — comment what remains in `language`; re-run `/implement` to resume.
