---
name: code-review
description: >-
  Fix-first code review of the diff after Functional verify — correctness,
  security, duplication, seams, test quality and naming are fixed in code,
  not reported. Phase 2 of /verify, or run /code-review directly after
  implementation.
disable-model-invocation: true
---

# Code review

Phase 2 of `/verify`, always on. Functional gate must already be green, or you are resuming after code-review fixes. Do **not** Ship from this skill — hand back to `/verify`.

Functional asks whether the diff matches the analysis and the documented standards. This phase asks whether the code is any good — and then fixes it.

**Fix-first.** Anything you would have written as a review comment, you change in code instead. Naming and readability included. Nothing is reported and left behind, nothing is posted on the PR, nothing waits for the human except what genuinely needs a decision.

Read `docs/agents/workflow.md`. Skills root is the parent of this file; commit via `{skills-root}/commit/SKILL.md`. If the repo has an overlay, read it after this skill: `docs/agents/code-review.md`.

## Gate (max 3 cycles)

```
Code review cycle: 1 / 3
- [ ] Both sub-agents returned
- [ ] Fixes committed (if any)
- [ ] Local pipeline re-checked green after the fixes
- [ ] Blocked findings listed (if any)
```

## What to look for

Only things Spec and Standards do not already cover:

| Area | Examples |
|------|----------|
| Correctness | Unhandled error or edge path, missing validation on new input, wrong transaction or consistency boundary, new unbounded or N+1 query |
| Security | Missing authorization on a new endpoint or action, untrusted input reaching a query or a path, secrets in code, over-broad payload binding |
| Leftovers | TODO, dead or commented-out code, unused parameters, debug output |
| Duplication | New copy of logic that already exists in the repo |
| Seams | Business logic in a controller or a view, domain rule outside the domain layer |
| Test quality | Assertion-free test, test asserting mocks instead of behaviour, over-mocked unit under test |
| Readability | Misleading naming or naming against repo idiom, unclear signature, comment that restates the code, needless nesting |

## Two outcomes, both ending in code

- **Fix now** — everything in the table, naming and readability included. Whoever finds it, fixes it in the same pass.
- **Blocked** — the fix needs a human decision, or it would change behaviour against the analysis (for example an authorization rule nobody specified). Leave the code alone and report the item; it fails the gate.

## Guardrails

Fix-first is not a licence to rewrite the repo.

- Only files that appear in the fixed-point diff. Untouched code stays untouched, however ugly.
- No renaming of public API fields, DB columns, or symbols used outside the diff.
- Behaviour must not change. A fix that changes behaviour is Blocked, not a fix.
- No scope creep past the analysis Change and Architecture.
- No push, no PR, no commits on a monorepo container root, no comments anywhere.

## One cycle

Two sub-agents, each fixing what it finds and reporting what it had to leave. Give both the per-root diff commands (`git -C <path> diff <fixed-point>...HEAD`), the analysis Change and Architecture, and the guardrails above.

They share one worktree, so the same rule as `/implement` applies: run them in parallel only when you can scope them to disjoint delivery roots or directories. Otherwise run them one after the other, correctness and security first.

**Correctness and security prompt:**

> Review and fix the diff in each affected delivery root. Look for unhandled error and edge paths, missing validation on new input, wrong transaction or consistency boundaries, new unbounded or N+1 queries, missing authorization on new endpoints or actions, untrusted input reaching a query or path, secrets in code, over-broad payload binding. Fix what you can without changing behaviour against the analysis. Report anything that needs a human decision as Blocked with file and reason. Do not commit, push, or open a PR. Return: what you fixed (file plus one line each), then Blocked items. Under 400 words.

**Craft prompt:**

> Review and fix the diff in each affected delivery root. Look for duplication of logic that already exists in the repo, business logic in the wrong seam (controller or view instead of domain), leftovers (TODO, dead or commented-out code, unused parameters, debug output), weak tests (no assertions, asserting mocks instead of behaviour, over-mocked unit under test), and readability: misleading naming, naming against repo idiom, unclear signatures, comments that restate the code, needless nesting. Rename freely inside the diff, but never a public API field, a DB column, or a symbol used outside the diff. Behaviour must not change. Do not commit, push, or open a PR. Return: what you fixed (file plus one line each), then Blocked items. Under 400 words.

Parent synthesizes the two reports and commits per delivery root:

- `refactor(scope): <what> (#<N>)` when the pass was readability, naming or structure only
- `fix(scope): <what> (#<N>)` when broken behaviour was repaired

Then hand back to the `/verify` **Re-check after gate fixes** step: the local pipeline (tests and tooling from `AGENTS.md`) runs again on the affected roots. Red counts as a Functional failure and is fixed under Functional rules, not here.

## Outcome

- Nothing Blocked and the re-check green → gate green, hand back to `/verify` for Phase 3 (UX) or Ship.
- Fixes landed but the reviewers still have work → next cycle, up to 3.
- Anything Blocked, or still not clean after 3 cycles → stop and return to `/verify` **Fail**, which sets `needs-attention` and puts the Blocked items in the fail note. Do not Ship.

## Rules

- Max **3** code review cycles; Functional and UX keep their own three
- Parent commits; sub-agents write code
- Every finding ends as a commit or as a Blocked item — never as a comment
