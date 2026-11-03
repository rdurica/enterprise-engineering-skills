---
name: ees-change
description: >-
  Implements a larger code change asked for in conversation — a new feature,
  endpoint or behaviour that spans several units — outside a published
  analysis, or any change the user explicitly wants done tests-first: tests go
  to ees-test-writer, code to ees-implementer, checks to ees-check-runner and
  review to ees-code-reviewer. Not for bug fixes and small adjustments up to
  about five files, which the main session edits directly, not for
  /ees-implement #N analyses and not for questions.
argument-hint: "[what to change]"
---

# Change

Request: $ARGUMENTS

The main session scopes, delegates, reviews and reports; agents write the tests and code. No analysis, no tracker, no branch or PR management. Skills root is the parent of this skill's directory.

## 1. Triage

Pick the level first; the user's explicit wish overrides it ("do it tests-first", "just fix it").

- **An analysis covers it** (a number, slug or path is named) → use `ees-implement` instead.
- **Direct** — a bug fix or a small adjustment within about five files, with no new public API, data model or user-visible flow → follow **Direct** below and stop.
- **A decision is missing** that the code cannot answer, such as an API shape, a data model or user-visible behaviour → ask one short question with a recommended answer.
- **Large or open-ended** — several units, open design questions, a migration → suggest `/ees-analyze` and wait for the user's choice.

Everything else — a new feature, endpoint or behaviour across several units, or an explicit tests-first request — continues with step 2.

### Direct

The main session edits the code itself; no brief and no test writer.

1. Make the change. A bug fix gets a regression test next to the fix.
2. Run the affected tests through `ees-check-runner`.
3. When the change touches more than one file, run one review per step 6 on the diff, with the request as the contract. Skip it for a one-file change.
4. Report in two or three lines. Commit only when the user asked for it.

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

Run a fresh `ees-implementer` per cluster with the brief and the tests from step 3. Independent clusters run in parallel. Follow [implement's Execution contract](../ees-implement/SKILL.md#execution-contract): workers never edit each other's tests, commit or push. A blocker in a report goes to the user, not into a guess.

## 5. Checks

Run the full documented checks through `ees-check-runner`. Failures go back to `ees-implementer` (or to `ees-test-writer` for a test defect it proves) with the excerpt, at most two repair rounds.

## 6. Review

Follow the cycle in [`ees-code-review`](../ees-code-review/SKILL.md#one-cycle) with the brief (or, on the Direct level, the request) in place of an analysis: a read-only `ees-code-reviewer` returns findings, a fresh `ees-implementer` fixes the ones you select, then rerun the affected tests. A second cycle reviews only the delta and runs only when the fixes changed behaviour. Blocked items go to the user.

When the diff contains frontend files (see [`ees-ux-review`](../ees-ux-review/SKILL.md#when-it-runs)), follow `ees-ux-review` after the code review, with the brief or request as the contract.

## 7. Report

Summarize in a few lines: what changed, the tests added, check results, and anything left for the user. Commit only when the user asked for it, through the `ees-commit` skill, tests before code.
