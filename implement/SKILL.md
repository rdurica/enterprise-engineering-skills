---
name: implement
description: >-
  Orchestrate a published analysis locally: fresh sub-agents write tests,
  parent verifies RED and commits tests, then fresh sub-agents implement.
  Parallelize independent paths and resources; parent commits and runs
  verify automatically. Use for /implement #N or a local analysis.
disable-model-invocation: true
---

# Implement

The main window orchestrates: read the saved analysis, plan work, delegate, review results, commit, then run `/verify` automatically. Tests come first; new implementation sub-agents work against committed tests.

Read `docs/agents/issue-tracker.md` and `workflow.md`; run `/setup` if missing. Skills root is the parent of this skill's directory. Use sibling `tdd`, `integration-tests` for PHP HTTP, and `commit` skills where relevant.

## 1. Start locally

Resolve the user’s analysis number or path through the configured tracker. User-invoked `/implement` needs no `ready-for-agent` label. Stop if already `ready-to-review` or archived in local `done/`. Optional auto-start requires `ready-for-agent` or `in-progress`, and must not run while `needs-attention` is set.

Set `in-progress`, remove `ready-for-agent` and `needs-attention`, and preserve unrelated labels. Read language and branch-owner from workflow; a session `human` or `agent` overrides ownership only. Current delivery instructions, including “do not push”, carry through verify.

Open FAQ: work only on decided scope; do not invent answers to unblock it.

## 2. Branch and scope

- **Human-owned:** stay on the current branch; the user owns checkout and PRs.
- **Agent-owned:** fetch origin and use the analysis Delivery branch. Create a new branch from the remote default with `--no-track`; reuse an existing branch. Switch only with a clean worktree. Pull the matching remote branch only when clean; preserve unfinished local work on resume without automatic stash or rebase.
- **Monorepo:** delivery work belongs in delivery roots, never the container root.

Inspect existing changes and keep unrelated work out of commits. Establish the review base from the branch’s merge-base with the default or explicit analysis base, once for this run. Include earlier feature commits when resuming. Ask only if the scope/base is genuinely unclear; no mandatory checkpoint file or tracker comment.

## 3. Plan and delegate

Group Acceptance items sharing code/tests into manageable **clusters**. Show the cluster, paths and dependencies. Parallelize independent clusters; sequence overlapping paths, dependent work and checks sharing a database, fixtures or other mutable resources unless isolated. Cover cross-unit behaviour completely.

Plan tests for the entire decided scope before production work. On resume, inspect git and the tests already present; reuse completed work rather than trusting checkboxes alone.

### Execution contract

Give each worker a fresh, scoped context: its phase and Acceptance items, relevant Change/Architecture/API Contracts, allowed paths, dependencies, skill paths and project commands. Link source files rather than copying the whole conversation. Workers return changed files, test results, completed items and blockers; they do not commit, push, change branches or manage PRs.

The parent primarily coordinates and delegates code/test work. A trivial one-file follow-up such as an import or typo may be fixed directly; substantial work goes to workers.

Committed tests are the contract. Later corrections require a concrete test defect, missing regression coverage or an agreed contract change, parent review and a separate test commit. Never weaken assertions to make faulty code pass. These rules apply to verify and review too.

## 4. Tests, then implementation

### A. Test-only sub-agents

Delegate all decided clusters to test workers. They write tests and necessary fixtures/helpers, without production changes. Follow `tdd` for layers and RED: PHP HTTP contracts use `integration-tests`; handler/domain decision logic also needs unit coverage; pure wiring does not.

Workers run relevant tests. Missing/new behaviour must show expected RED; existing-behaviour regression tests may pass. Environment/fixture failures are not behavioural RED. Missing new symbols can establish initial RED; assertions must still be checked once the code exists.

Parent reviews coverage and results, fixes test issues through workers, then commits tests separately as `test(scope): <contract coverage> (#<N>)`. Complete the decided scope’s test commits before phase B. If hooks reject intentional RED, resolve the repository-specific blocker without silently bypassing hooks or implementing early. Tests alone do not complete Acceptance.

### B. New implementation sub-agents

Start new workers per cluster with contracts, committed tests, expected failures and permitted production paths. They implement against the stable tests. Schedule consumers after providers when needed.

When a wave joins, review changes and run relevant checks; delegate substantial repairs. Commit production changes using the appropriate `feat`/`fix` type. Check off only Acceptance behaviour verified as complete, without per-cluster tracker comments.

## 5. Verify and resume

Once decided work is complete, automatically follow sibling `verify/SKILL.md` in this session. Carry the analysis, review base, test baseline, results and current delivery restrictions; the main window keeps orchestrating.

If FAQ leaves work unfinished, mark `needs-attention` and briefly explain what needs a decision. Do not verify it as complete.

On interruption, keep `in-progress`. When possible, leave a short analysis comment with what is done, what remains and any non-obvious run command or review base needed to resume. A new invocation reads the analysis and git state; no routine checkpoint protocol is required.
