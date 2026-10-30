---
name: ees-change
description: >-
  Implements a code change asked for in conversation — a feature, bug fix,
  refactor, new endpoint or behaviour change — outside a published analysis.
  Use whenever the user asks to implement, add, fix, change or refactor code
  and the change adds behaviour or touches more than one file: tests go to
  ees-test-writer, code to ees-implementer, checks to ees-check-runner and review to
  ees-code-reviewer. Not for /ees-implement #N analyses, trivial one-line edits or
  questions.
argument-hint: "[what to change]"
---

# Change

Request: $ARGUMENTS

The main session scopes, delegates, reviews and reports; agents write the tests and code. No analysis, no tracker, no branch or PR management. Skills root is the parent of this skill's directory.

## 1. Triage

- **An analysis covers it** (a number, slug or path is named) → use `ees-implement` instead.
- **Below the threshold** — a typo, an import, a one-line fix, a rename inside one file, with no new behaviour → edit directly, run the affected test and stop.
- **A decision is missing** that the code cannot answer, such as an API shape, a data model or user-visible behaviour → ask one short question with a recommended answer.
- **Large or open-ended** — several units, open design questions, a migration → suggest `/ees-analyze` and wait for the user's choice.

Everything else continues below.

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

Run `ees-code-reviewer` on the diff with the brief in place of an analysis. Rerun only the affected tests after its fixes. A second cycle reviews only the delta since the first and runs only when the first changed behaviour. Blocked items go to the user.

## 7. Report

Summarize in a few lines: what changed, the tests added, check results, and anything left for the user. Commit only when the user asked for it, through the `ees-commit` skill, tests before code.
