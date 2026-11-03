---
name: ees-verify
description: >-
  Closer after implementation — Functional review against the analysis and
  documented standards, code review, UX review when the diff touches the
  frontend, then delivery: ready PR when green, draft PR and needs-attention
  when a gate fails. Comments only on the analysis, never on the PR. Followed
  automatically at the end of /ees-implement; not a command of its own.
user-invocable: false
disable-model-invocation: true
model: opus
effort: medium
---

# Verify

Finish implementation through Functional → code review → UX (frontend only) → Ship/Fail. `/ees-implement` follows this file automatically in the same session; a run interrupted or failed here is resumed with `/ees-implement #N`. Fix actionable findings within the analysis scope; report blockers needing a human decision.

Resolve configuration per `{skills-root}/ees-pipeline/config.md` (`language`, monorepo) and tracker operations per `{skills-root}/ees-pipeline/tracker-<tracker>.md`, plus `docs/agents/config/verify.md` if present. Skills root is the parent of this skill's directory. Follow sibling `ees-implement/SKILL.md` → **Execution contract** for delegation and stable test rules; parent may handle trivial one-file follow-ups. Branches, pushing, CI and PRs follow `{skills-root}/ees-pipeline/delivery.md`; no other part of this file deals with them.

Comments go on the analysis, never the PR, in the resolved `language`. Status changes use the `/ees-verify` operations of the tracker file.

## Scope

Use the analysis from implement. Missing spec or unclear scope is a blocker; obtain it before reviewing.

Keep implement’s review base. When resuming without it, take the Delivery branch per **Start** in `delivery.md` and use its merge-base with the default or explicit base. Keep that base fixed for this run; never derive it from an unrelated current branch.

Review committed and intended staged/unstaged changes, and inspect intended untracked files too:

```bash
git -C <root> diff <review-base> -- <intended-paths>
git -C <root> status --short
```

Exclude unrelated work. Review delivery roots only, never a monorepo container root.

## 1. Functional

Run one `ees-functional-reviewer` agent with fresh scoped context, alongside the full documented suite through `ees-check-runner`. Read-only review can run in parallel with checks; checks sharing mutable test resources need isolation or sequential execution.

- **Spec:** full relevant analysis and diff. Check Acceptance completeness, scope vs Change/Architecture, API contracts, invented FAQ answers and test coverage. Existing unchanged tests are valid coverage. Non-trivial handler/domain decision logic needs unit tests; HTTP coverage alone is insufficient.
- **Standards:** diff plus `AGENTS.md` and contributor standards. Report documented violations with file, rule and required change. Skip subjective style and violations already handled by tooling.
- **Local checks:** documented tests, lint/type checks and other relevant commands from each affected root’s `AGENTS.md`.

The reviewer returns a concise fix list, not comments. Delegate repairs to `ees-implementer` (or `ees-test-writer` for justified test corrections), review and commit them, then re-run checks for the affected paths. A repair cycle starts a new `ees-functional-reviewer` on the delta since the previous cycle's last commit, with the previous fix list; the code review that follows covers the whole diff again. Follow the Execution contract for justified test corrections and separate test commits. Max 3 Functional repair cycles; unresolved failures → Fail.

## 2. Code review

After Functional is green, check off satisfied Acceptance and follow sibling `ees-code-review/SKILL.md`. A read-only reviewer finds correctness, security, design, best-practice and readability issues; implementers fix them, preserving the agreed contract. Blocked findings or exhausted review cycles → Fail.

## 3. UX

Follow sibling `ees-ux-review/SKILL.md` when the review-base diff contains frontend files as defined there under **When it runs**; otherwise skip this step. Critical/Major findings must be fixed; a blocked or exhausted UX gate → Fail.

After review or UX fixes, rerun checks for the affected paths before continuing. Repair failed checks within the current gate’s cycle limit; there is no separate re-check counter. Revisit Spec/Standards when the fix changes externally observable behaviour; re-walk affected UI when needed.

## 4. Finalize

Ensure the intended verified work is committed before Ship, including correct uncommitted work on resume. Stage only that scope. If code changed since the last full suite run, run the full suite once more through `ees-check-runner`. If hooks change files, inspect and rerun affected checks. Do not claim historical tests-first evidence when tests and code arrived together.

Then follow **Finish** in `{skills-root}/ees-pipeline/delivery.md`: **Green** when every gate passed, **Fail** when a gate is red after its budget or a hard stop occurred. CI fixes go through the same delegated repair and local-check loop; do not reset exhausted gate budgets. Retain local work on every path.
