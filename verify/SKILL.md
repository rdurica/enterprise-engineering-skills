---
name: verify
description: >-
  Closer after implementation — Spec vs analysis, Standards, tests, AGENTS.md
  tooling, then code review and optional UX; then ship. Agent: ready PR if
  green, draft PR if a gate fails; human stays on HEAD. Comments only on the
  analysis, never on the PR. Use at the end of /implement, or when the user
  runs /verify after implementation.
disable-model-invocation: true
---

# Verify

Finish implementation through Functional → code review → optional UX → Ship/Fail. `/implement` invokes this automatically; the user may also run it directly. Fix actionable findings within the analysis scope; report blockers needing a human decision.

Read `docs/agents/issue-tracker.md` and `workflow.md`, plus `docs/agents/verify.md` if present. Run `/setup` if configuration is missing. Skills root is the parent of this skill's directory. Follow sibling `implement/SKILL.md` → **Execution contract** for delegation and stable test rules; parent may handle trivial one-file follow-ups.

Choose delivery instructions by branch-owner: [human.md](human.md) or [github.md](github.md). For a monorepo also read [monorepo.md](monorepo.md). Push policy is independent of branch ownership; session no-push overrides it in Ship and Fail. No-push skips git publication, CI watches and PR changes; tracker updates remain allowed unless separately restricted.

Comments go on the analysis, never the PR, in the workflow language. `ready-to-review` means verified work is ready for the human; it does not require a PR on human-owned or local-only delivery.

## Scope

Use the analysis from implement, the user’s number/path, or the configured local tracker. Missing spec or unclear scope is a blocker; obtain it before reviewing.

Keep implement’s review base. For direct verify, identify the intended branch first and use its merge-base with the default/explicit base. Keep that base fixed for this run; never derive it from an unrelated current branch. Continuing local implementation needs no repeated checkout, pull or rebase.

Review committed and intended staged/unstaged changes, and inspect intended untracked files too:

```bash
git -C <root> diff <review-base> -- <intended-paths>
git -C <root> status --short
```

Exclude unrelated work. Review delivery roots only, never a monorepo container root.

## 1. Functional

Run Spec and Standards reviewers in parallel with fresh scoped context, then relevant project tests/tooling. Read-only review can be parallel; checks sharing mutable test resources need isolation or sequential execution.

- **Spec:** full relevant analysis and diff. Check Acceptance completeness, scope vs Change/Architecture, API contracts, invented FAQ answers and test coverage. Existing unchanged tests are valid coverage. Non-trivial handler/domain decision logic needs unit tests; HTTP coverage alone is insufficient.
- **Standards:** diff plus `AGENTS.md`, contributor standards and ADRs. Report documented violations with file, rule and required change. Skip subjective style and violations already handled by tooling.
- **Local checks:** documented tests, lint/type checks and other relevant commands from each affected root’s `AGENTS.md`.

Reviewers return concise fix lists, not comments. Delegate repairs, review and commit them, then re-run affected checks. Follow the Execution contract for justified test corrections and separate test commits. Max 3 Functional repair cycles; unresolved failures → Fail.

## 2. Code review

After Functional is green, check off satisfied Acceptance and follow sibling `code-review/SKILL.md`. It fixes correctness, security, structure and readability, preserving the agreed contract. Blocked findings or exhausted review cycles → Fail.

## 3. UX

If `ux-review: enabled`, follow sibling `ux-review/SKILL.md`; otherwise skip. Its non-UI skip is valid. Critical/Major findings must be fixed; a blocked or exhausted UX gate → Fail.

After review or UX fixes, rerun affected local checks before continuing. Repair failed checks within the current gate’s cycle limit; there is no separate re-check counter. Revisit Spec/Standards when the fix changes externally observable behaviour; re-walk affected UI when needed.

## 4. Finalize

Ensure the intended verified work is committed before Ship, including correct uncommitted work from a direct verify invocation. Stage only that scope. If hooks change files, inspect and rerun affected checks. Do not claim historical tests-first evidence when tests and code arrived together.

Follow the selected delivery path for push, CI and PR handling. CI fixes go through the same delegated repair and local-check loop; do not create another tracking protocol or reset exhausted gate budgets. Stop after 3 unsuccessful CI repairs or when external checks/publication cannot complete, and report the blocker honestly.

- **Green:** mark `ready-to-review`; local tracker moves to `done/`. Preserve unrelated labels. Briefly record checks, current/published commit, CI outcome and PR URL when applicable. Explicitly state skipped publication/CI.
- **Fail:** replace `in-progress` with `needs-attention`, remove `ready-to-review`, retain local work and do not archive. Name the failing gate, attempted fixes and remaining blocker. Agent-owned may provide a draft PR if publishing is allowed; human-owned never manages PRs.
