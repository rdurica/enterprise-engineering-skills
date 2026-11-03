---
name: ees-code-review
description: >-
  Code review of a diff — a read-only reviewer finds correctness, security,
  design, best-practice, performance, test and readability issues, a fresh
  implementer fixes them. Phase 2 of /ees-verify, the review step of
  /ees-change, or run /ees-code-review directly on the current changes after
  an ordinary prompt.
argument-hint: "[base ref | paths]"
disable-model-invocation: true
model: opus
effort: medium
---

# Code review

Phase 2 of `/ees-verify`, always on, and the review step of `ees-change`. In verify the Functional gate must already be green, or you are resuming after code-review fixes. Do **not** Ship from this skill — hand back to the caller.

**Direct use** (`/ees-code-review` without a pipeline around it): review the changes of the current conversation.

- **Base:** an explicit base ref from the argument; otherwise `HEAD` when there are uncommitted changes, else the merge-base with the default branch. Limit to the paths in the argument when given. An empty diff → say so and stop.
- **Contract:** the conversation — what the user asked for and decided. Without an analysis, a finding that would change requested behaviour is Blocked and goes to the user.
- Run the cycles below. Commit only when the user asks for it, through `ees-commit`; otherwise leave the fixes uncommitted, and a next cycle reviews the diff since the previous review instead of since the last commit.
- When the diff contains frontend files, offer the UX review at the end; do not run it unasked.

Functional asks whether the diff matches the analysis and the documented standards. This phase asks whether the code is any good.

**Find, then fix — by different agents.** `ees-code-reviewer` is read-only and only reports findings; a fresh `ees-implementer` fixes them. The reviewer does not have to weigh what a fix costs, so it reports everything it sees.

Skills root is the parent of this skill directory (two levels above `SKILL.md`); resolve configuration per `{skills-root}/ees-pipeline/config.md`; commit via `{skills-root}/ees-commit/SKILL.md`. If the repo has an overlay, read it after this skill: `docs/agents/config/code-review.md`. Follow [Execution contract](../ees-pipeline/execution.md) for delegation, resource isolation and test-baseline changes.

## What the reviewer looks for

The areas and severities are defined in the `ees-code-reviewer` agent: correctness, security, design, best practices of the stack, performance, tests and readability, each with a verdict. It reads the code around the diff and the project's manifests, not only the diff.

An endpoint whose authorization contradicts the analysis is a finding to fix, not Blocked: every block in `## API Contracts` carries a mandatory Authorization line, so the rule is specified and the code has to match it. Only an endpoint the analysis never described is Blocked.

## One cycle

1. **Review.** Start a new `ees-code-reviewer` with fresh, scoped context: the fixed review base, the intended diff including untracked files, the analysis reference (or the brief), the committed tests and the delivery roots. Cycle 1 reviews the whole diff from the review base. Cycles 2 and 3 review only the delta since the previous cycle's last commit, with the previous report.
2. **Select.** The parent reads the report and picks what gets fixed: every Critical and Major; a Minor when its fix is local and cheap. Drop a finding only when it is wrong, and say why in one line. A report without verdicts for every area goes back to a new reviewer once.
3. **Fix.** Start a fresh `ees-implementer` per independent cluster of selected findings, with the findings verbatim, the allowed paths and the guardrails below. A finding about a test goes to `ees-test-writer` under the Execution contract (reviewed reason, separate test commit, no weakened assertions).
4. **Check and commit.** Rerun tests and tooling for the affected paths through `ees-check-runner`; red → repair within this review's cycle limit. Commit per delivery root:
   - `refactor(scope): <what> (#<N>)` when the fixes were design, readability or structure only
   - `fix(scope): <what> (#<N>)` when broken behaviour was repaired

Revisit Spec/Standards when externally observable behaviour changes.

## Guardrails for fixes

- Stay within the intended fixed review-base diff. A directly necessary regression test or adjacent repair is allowed when justified against the analysis; avoid unrelated cleanup.
- No renaming of public API fields, DB columns or symbols used outside the diff.
- Preserve the agreed analysis contract. Repairing behaviour that violates it is allowed; changing the contract is Blocked.
- No scope creep past the analysis Change and Architecture.
- No push, no PR, no commits on a monorepo container root, no comments anywhere.

## Outcome

- No Critical or Major left, nothing Blocked and the re-check green → gate green, hand back for UX or Ship.
- Fixes landed → next cycle on the delta, up to 3 in total. A cycle whose report has no Critical or Major ends the review.
- Anything Blocked, or Critical/Major still open after 3 cycles → stop and return to `/ees-verify` **Fail**, which sets `needs-attention` and puts the Blocked items in the fail note. In `/ees-change` and direct use, Blocked items go to the user. Do not Ship.

Every selected finding ends as a commit or as a Blocked item — never as a comment.
