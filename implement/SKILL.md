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

Fetch the analysis per `docs/agents/issue-tracker.md` — by `#N` on GitHub, or as `/implement 001`, `#1` or `<slug>` resolving to `.scratch/analysis/NNN-<slug>.md` locally.

**Stop** when the GitHub issue already has `ready-to-review`, or the only local match sits under `.scratch/analysis/done/`.

When the user invoked `/implement`, just proceed — `ready-for-agent` is not required. Auto-start without the user is allowed only when the issue has `ready-for-agent` or is already `in-progress`.

Then set `in-progress` and remove `ready-for-agent` (it has done its job) and `needs-attention` (this is the resume path after a human acted), so the issue carries `analysis` + `in-progress` and nothing else. The user may pass `human` or `agent` to override branch-owner for this session.

If `## FAQ` is still open, do **not** invent answers. Implement the decided parts and skip anything that depends on an open question, or leave the whole session for later.

## 2. Branch

Branch name from analysis `## Delivery`; branch-owner from `workflow.md`, unless the user overrode it for this session. **human:** stay on HEAD. Never commit on a monorepo container root.

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

Product code always goes through **sub-agents**, even when the Architecture is flat.

A **part** is one unchecked `- [ ]` in `## Acceptance`, meaning one observable behaviour. Map each part to an Architecture `###`, which gives you its path and delivery root — the `###` maps units, it is not the size of an agent. A part spanning two units is a bad Acceptance item; implement the decided seam only.

A **cluster** is consecutive unchecked parts that map to the same `###` and share files: same module, same endpoint or test class. That is the size of one agent. A part with no overlap is a cluster of one. Cap a cluster at roughly **8** parts and push the leftovers into the next sequential cluster after the commit.

Without `###` subsections, cluster by shared paths anyway, and treat a lone part as one agent. Go parallel only when the Change and Architecture paths are clearly disjoint.

`## Acceptance` is a constraint for verify and TDD, not a work breakdown. Print the plan **by cluster** — items, unit, path, wave — rather than one sequential wave per overlapping part. When resuming, skip work already in the branch or already checked off.

Group into **waves**:

- **Same wave (parallel):** disjoint clusters, neither depends on the other's output. Typical: different delivery roots, or different modules with disjoint directories.
- **Next wave after commit:** next overlapping cluster (same module / shared files), or leftover parts past the ~8 cap.
- **Unclear / overlapping / single unit:** one sequential cluster. Do not guess.

Same worktree — safety is disjoint paths, not isolated checkouts.

## 4. Execute

Independent clusters in a wave: spawn them in **one parent turn**, one sub-agent per cluster. Overlapping clusters: one at a time, then commit, then the next.

**Sub-agent:** one sub-agent per cluster. It writes code and tests only — no commit, push, PR, branch change, nested agents, or container-root commits. Prompt: **all** Acceptance items in this cluster (the list, not one item); analysis Change / Architecture (relevant `###`) / API Contracts as constraints; open FAQ to skip; skill paths (`tdd`, and `integration-tests` for PHP HTTP); `AGENTS.md` commands; delivery-root paths; no scope creep (stay inside Change/Architecture).

The sub-agent finishes every item in its prompt and then returns. If it gets stuck on one item, it returns what is done and what remains, and the parent checks off only the done ones. For **each** item, cover the seams that apply (see `tdd/SKILL.md`):

- HTTP contract → `integration-tests`
- Decision logic in handler / domain / VO → unit test (HTTP does not replace it)
- Pure wiring, no branches → skip unit
- No HTTP → unit only

Order: highest seam first (HTTP when the item is HTTP-shaped), then unit for the same decision. Writing the tests for the whole cluster first, then implementing, is allowed. One-test-at-a-time is also fine — not required.

**Parent** does not write product code except a one-file follow-up after the agent (import, typo).

Once the wave joins, review the diff and run the relevant tests per cluster. Fix a small failure yourself when it is one file; hand a large one to another sub-agent scoped to that cluster and that failure. Non-overlapping fixes in the same wave may run in parallel, overlapping files stay sequential.

Commit in each affected delivery root per `commit/SKILL.md` — `feat(scope): <acceptance title> (#<N>)` for a single item, `feat(scope): <shared theme> (#<N>)` for a cluster of several. Check off every completed `## Acceptance` item in the cluster, and do not comment on the ticket after each one. Commit messages stay English. Then move to the next wave.

## 5. Verify

When the decided parts are done — all parts, if no FAQ blocks anything — read and follow `{skills-root}/verify/SKILL.md` in this session.

If an open FAQ left work behind, set `needs-attention` in place of `in-progress`, comment what remains in `language`, and do not run verify as if the analysis were complete.

If the session dies first, leave `in-progress`: that state is resumable and needs no human. Comment what remains in `language`; re-running `/implement` picks it up.
