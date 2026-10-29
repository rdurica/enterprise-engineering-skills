---
name: implement
description: >-
  Implements a published analysis end to end. Use whenever the user asks to
  implement, build or continue an analysis by its number, slug or path
  (/implement #N, "implement analysis 003"): fresh sub-agents write tests,
  parent verifies RED and commits tests, then fresh sub-agents implement;
  parent commits and runs verify automatically. For a change with no
  analysis, use the change skill instead.
model: sonnet
effort: high
---

# Implement

The main window orchestrates: read the saved analysis, plan work, delegate, review results, commit, then run `/verify` automatically. Tests come first; new implementation sub-agents work against committed tests.

Resolve configuration per `{skills-root}/pipeline/config.md` and tracker operations per `{skills-root}/pipeline/tracker-<tracker>.md`. Skills root is the parent of this skill's directory. Use sibling `tdd`, `integration-tests` for PHP HTTP, and `commit` skills where relevant.

## 1. Start locally

Resolve the user’s analysis number or path through the configured tracker. Stop if already `ready-to-review` or archived in local `done/`.

Before setting `in-progress`, on every run including resume: an idea (label `idea`, locally a file in `ideas/`) → stop and point to `/analyze #N`; change no labels or branch. An analysis whose `Depends on` is unsatisfied (closed issue or local `done/` file is satisfied; `ready-to-review` while open is not) → stop and list the unsatisfied ones; no bypass.

On GitHub set `in-progress`, remove `needs-attention`, and preserve unrelated labels; the local tracker has no status. Take language and branch-owner from the resolved config; a session `human` or `agent` overrides ownership only. Current delivery instructions, including “do not push”, carry through verify.

Open FAQ: work only on decided scope; do not invent answers to unblock it.

## 2. Branch and scope

- **Human-owned:** stay on the current branch; the user owns checkout and PRs.
- **Agent-owned:** fetch origin and use the analysis Delivery branch. Create a new branch from the remote default with `--no-track`; reuse an existing branch. Switch only with a clean worktree. Pull the matching remote branch only when clean; preserve unfinished local work on resume without automatic stash or rebase.
- **Monorepo:** delivery work belongs in delivery roots, never the container root.

Inspect existing changes and keep unrelated work out of commits. Establish the review base from the branch’s merge-base with the default or explicit analysis base, once for this run. Include earlier feature commits when resuming. Ask only if the scope/base is genuinely unclear; no mandatory checkpoint file or tracker comment.

## 3. Plan and delegate

Group Acceptance items sharing code/tests into manageable **clusters**. Show the cluster, paths and dependencies. Parallelize independent clusters; sequence overlapping paths, dependent work and checks sharing a database, fixtures or other mutable resources unless isolated. Cover cross-unit behaviour completely.

Plan tests for the entire decided scope before production work.

**Revised analysis.** When the analysis has `## Revisions` and the branch already has work, plan only the unchecked Acceptance items; checked items stay done. Plan against all unchecked revisions, not just the last; a revision that changed no Acceptance item or test is planned from its own text. The tests those revisions name are an agreed contract change — correct them through `test-writer` in a separate test commit before phase B.

**Small scope.** One cluster touching a handful of files needs no plan display: run one `test-writer`, then one `implementer`. Gates and the tests-first order stay the same. On resume, inspect git and the tests already present; reuse completed work rather than trusting checkboxes alone.

### Execution contract

Give each worker a fresh, scoped context: its phase and Acceptance items, relevant Change/Architecture/API Contracts, allowed paths, dependencies, skill paths and project commands. Link source files rather than copying the whole conversation. Workers return changed files, test results, completed items and blockers; they do not commit, push, change branches or manage PRs.

The parent primarily coordinates and delegates code/test work. A trivial one-file follow-up such as an import or typo may be fixed directly; substantial work goes to workers.

**Keep the main window lean.** Every turn resends its whole context. Review worker results from their report and `git diff --stat`; read the full diff only for files where the report, the stat or a failing check gives reason to doubt it. Pass workers paths and bases, not pasted diffs or logs.

**Agents.** Delegate through the Agent tool with these `subagent_type` values. Each agent definition fixes its model and effort, so the expensive orchestrator model only plans, reviews and commits:

| Agent | Work | Model / effort |
|-------|------|----------------|
| `test-writer` | Phase A tests, justified test corrections | sonnet / high |
| `implementer` | Phase B production code, delegated repairs | sonnet / high |
| `check-runner` | Project tests, lint and type checks; compact summary | haiku / low |
| `functional-reviewer` | Functional review in `/verify` (spec and standards) | sonnet / medium |
| `code-reviewer` | `/code-review` pass | sonnet / medium |
| `ux-reviewer` | `/ux-review` passes | sonnet / medium |

The parent runs every test, lint and type check through `check-runner`, never directly, so logs stay out of the main window. Workers run their own cluster tests.

**Checks in tiers.** After a wave or a repair, run only the tests and tooling for the affected paths. Run the full documented suite once at the start of `/verify` Functional and once before Ship, the latter only when code changed since the last full run.

**Escalation.** When a worker returns the same cluster unfinished or wrong twice, start a new one with `model: "opus", effort: "low"` and a sharper brief (failure evidence, the decision it missed). If that also fails, take the cluster with `model: "opus"` at its default effort, or mark the cluster blocked when the cause is an undecided contract. Do not escalate on the first attempt. The same applies to `code-reviewer`: when a cycle misses an issue that a later check or cycle exposes, run the next cycle with `effort: "high"`.

Committed tests are the contract. Later corrections require a concrete test defect, missing regression coverage or an agreed contract change, parent review and a separate test commit. Never weaken assertions to make faulty code pass. These rules apply to verify and review too.

## 4. Tests, then implementation

### A. Test-only sub-agents

Delegate all decided clusters to `test-writer` agents. They write tests and necessary fixtures/helpers, without production changes. Follow `tdd` for layers and RED: PHP HTTP contracts use `integration-tests`; handler/domain decision logic also needs unit coverage; pure wiring does not.

Workers run relevant tests. Missing/new behaviour must show expected RED; existing-behaviour regression tests may pass. Environment/fixture failures are not behavioural RED. Missing new symbols can establish initial RED; assertions must still be checked once the code exists.

Parent reviews coverage and results, fixes test issues through workers, then commits tests separately as `test(scope): <contract coverage> (#<N>)`. Complete the decided scope’s test commits before phase B. If hooks reject intentional RED, resolve the repository-specific blocker without silently bypassing hooks or implementing early. Tests alone do not complete Acceptance.

### B. New implementation sub-agents

Start new `implementer` agents per cluster with contracts, committed tests, expected failures and permitted production paths. They implement against the stable tests. Schedule consumers after providers when needed.

When a wave joins, review changes and run relevant checks through `check-runner`; delegate substantial repairs. Commit production changes using the appropriate `feat`/`fix` type. Check off only Acceptance behaviour verified as complete, without per-cluster tracker comments. In the same step — before `/verify` — check off (`- [x]`) each revision whose work is done: the tests it names are committed, if any, and the Acceptance items it changed are checked, if any.

## 5. Verify and resume

Once decided work is complete, automatically follow sibling `verify/SKILL.md` in this session. Carry the analysis, review base, test baseline, results and current delivery restrictions; the main window keeps orchestrating.

If FAQ leaves work unfinished, mark `needs-attention` and briefly explain what needs a decision. Do not verify it as complete.

On interruption, keep `in-progress` on GitHub. When possible, leave a short analysis comment with what is done, what remains and any non-obvious run command or review base needed to resume. A new invocation reads the analysis and git state; no routine checkpoint protocol is required.
