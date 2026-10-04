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

Read `docs/agents/workflow.md`. Skills root is the parent of this skill directory (two levels above `SKILL.md`); commit via `{skills-root}/commit/SKILL.md`. If the repo has an overlay, read it after this skill: `docs/agents/code-review.md`. Follow [implement’s Execution contract](../implement/SKILL.md#execution-contract) for delegation, resource isolation, and test-baseline changes, including direct `/code-review` use.

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
- **Blocked** — the fix needs a human decision, or it would change behaviour against the analysis. Leave the code alone and report the item; it fails the gate.

An endpoint whose authorization contradicts the analysis is a **Fix**: every block in `## API Contracts` carries a mandatory Authorization line, so the rule is specified and the code has to match it. Only an endpoint the analysis never described is Blocked.

## Guardrails

Fix-first is not a licence to rewrite the repo.

- Stay within the intended fixed review-base diff, including staged/unstaged and intended untracked files. A directly necessary regression test or adjacent repair is allowed when justified against the analysis; avoid unrelated cleanup.
- No renaming of public API fields, DB columns, or symbols used outside the diff.
- Preserve the agreed analysis contract. Repairing behaviour that violates it is allowed; changing the contract is Blocked.
- No scope creep past the analysis Change and Architecture.
- No push, no PR, no commits on a monorepo container root, no comments anywhere.

## One cycle

Use two sub-agents with fresh, scoped context: correctness/security and craft. Give them the fixed review-base, intended diff including untracked files, relevant analysis/contracts, committed tests and guardrails. Keep the same base across cycles.

Run in parallel only with disjoint write paths and isolated mutable resources; otherwise sequentially, correctness/security first.

Reviewers fix issues within their assigned paths using the areas above. Return changed files and brief reasons, plus any Blocked item with file and decision needed. Preserve the analysis contract and follow the Execution contract for test changes. Workers do not commit or publish.

Parent reviews reports and diffs, handles trivial one-file follow-up fixes when useful, runs checks, and commits per delivery root. Apply the Execution contract to test changes: reviewed reasons, separate test commits, no weakened assertions.

- `refactor(scope): <what> (#<N>)` when the pass was readability, naming or structure only
- `fix(scope): <what> (#<N>)` when broken behaviour was repaired

Rerun affected local tests/tooling after fixes. If red, repair within this review’s cycle limit before continuing; no separate re-check counter. Revisit Spec/Standards when externally observable behaviour changes.

## Outcome

- Nothing Blocked and the re-check green → gate green, hand back to `/verify` for Phase 3 (UX) or Ship.
- Fixes landed but the reviewers still have work → next cycle, up to 3.
- Anything Blocked, or still not clean after 3 cycles → stop and return to `/verify` **Fail**, which sets `needs-attention` and puts the Blocked items in the fail note. Do not Ship.

## Rules

- Max **3** code review cycles; Functional and UX keep their own three
- Parent orchestrates and commits; sub-agents handle substantial work
- Every finding ends as a commit or as a Blocked item — never as a comment
