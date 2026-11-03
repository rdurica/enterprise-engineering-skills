---
name: ees-change
description: >-
  Implements a code change outside a published analysis through the full
  agent workflow — brief, tests first through ees-test-writer, code through
  ees-implementer, checks through ees-check-runner, then code review and, for
  frontend changes, UX review. Run only when the user invokes /ees-change;
  ordinary prompts are handled directly by the main session.
disable-model-invocation: true
argument-hint: "[what to change]"
---

# Change

Request: $ARGUMENTS

The main session scopes, delegates, reviews and reports; agents write the tests and code. No analysis, no tracker, no branch or PR management. Skills root is the parent of this skill's directory.

## 1. Triage

- **An analysis covers it** (a number, slug or path is named) → use `/ees-implement` instead.
- **A decision is missing** that the code cannot answer, such as an API shape, a data model or user-visible behaviour → ask one short question with a recommended answer.
- **Large or open-ended** — several units with open design questions, a migration → suggest `/ees-analyze` and wait for the user's choice.

Everything else continues below; the user asked for the workflow, so do not shortcut it for a small change.

## 2. Brief

Read `AGENTS.md` in each affected root for conventions and commands, and the code the change touches. Delegate broad searches to `Explore`. Then write the brief every worker gets:

- **Expected behaviour** as a short list of observable outcomes, each with a trigger and result. It plays the role of Acceptance.
- **Decisions** from the conversation. They are the contract.
- **Allowed paths** for tests and for production code.
- **Commands** for the targeted tests and the full checks.

Split the brief into clusters only when parts touch disjoint paths and resources; otherwise one cluster.

## 3. Tests

Run `ees-test-writer` per cluster with the brief. Review its report and `git diff --stat`; every expected outcome needs a test failing for the expected reason. A bug fix needs a regression test that reproduces the bug.

A pure refactor with existing coverage skips this step: run the full checks through `ees-check-runner` as the baseline instead.

## 4. Code

Run a fresh `ees-implementer` per cluster with the brief and the tests from step 3. Independent clusters run in parallel. Follow [Execution contract](../ees-pipeline/execution.md): workers never edit each other's tests, commit or push. A blocker in a report goes to the user, not into a guess.

## 5. Checks

Run the full documented checks through `ees-check-runner`. Failures go back to `ees-implementer` (or to `ees-test-writer` for a test defect it proves) with the excerpt, at most two repair rounds.

## 6. Review

Follow the cycle in [`ees-code-review`](../ees-code-review/SKILL.md#one-cycle) with the brief in place of an analysis: a read-only `ees-code-reviewer` returns findings, a fresh `ees-implementer` fixes the ones you select, then rerun the affected tests. A second cycle reviews only the delta and runs only when the fixes changed behaviour. Blocked items go to the user.

When the diff contains frontend files (see [`ees-ux-review`](../ees-ux-review/SKILL.md#when-it-runs)), follow `ees-ux-review` after the code review, with the brief or request as the contract.

## 7. Report

Summarize in a few lines: what changed, the tests added, check results, and anything left for the user. Commit only when the user asked for it, through the `ees-commit` skill, tests before code.
