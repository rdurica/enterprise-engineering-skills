# Verify — human

Stay on the current branch. Do not checkout or create branches and do not create, edit, mark ready/draft, or otherwise manage PRs. Branch ownership is separate from publishing: `push: finalize` allows the parent to push after local gates and check CI. `push: never` or a session no-push instruction disables publishing and CI watches entirely.

If `## Monorepo`, read [monorepo.md](monorepo.md); still no checkout. The user can run `/monorepo-update #N` first to select delivery branches. Preserve the fixed review-base SHA(s) from implement or the first verify invocation.

Inspect status before work; preserve unrelated changes without staging them. If their overlap makes the intended scope unsafe, stop and ask. Intentional verify changes may proceed, including staged/unstaged and untracked files.

Run every local gate in [SKILL.md](SKILL.md). Parent delegates code/test fixes and owns commits.

Never comment on a PR. Green and fail notes go on the **analysis only** (`language` from `workflow.md`; headings in English). GitHub: `gh issue comment`. Local: append under `## Comments`.

## Ship (local gates green)

1. If publishing is allowed and a remote exists, push the current branch in each affected delivery root using an explicit branch ref. Inspect the destination first; never force-push or silently redirect to another branch. An unpublished current branch may be pushed explicitly to the configured origin without an existing upstream. If HEAD is detached, the destination is ambiguous, or protection rejects the push, retain local work and report the publication blocker.
2. For a GitHub remote after a successful push, follow **CI** in [github.md](github.md), without changing or creating a PR. CI failures use delegated fixes, local re-checks and a new pushed SHA. If required CI needs a PR the human has not opened, mark verification pending and explain the blocker; do not open it yourself.
3. When all applicable gates are green (or publishing is disabled by configuration/session), finalize analysis as `ready-to-review` regardless of whether a PR exists:
   - GitHub: remove `in-progress`, `needs-attention` and `ready-for-agent`; add `ready-to-review`.
   - Local: write `Status: ready-to-review`, then move to `.scratch/analysis/done/NNN-<slug>.md`.
4. Comment with local verification evidence, current commit SHA(s), publication/CI outcome or “not run: publishing disabled”, and any remaining human PR step. `ready-to-review` means verified work is ready for the human, not that a PR exists.

## Fail (gate red after budget or hard stop)

Set `needs-attention` (GitHub: remove `in-progress` and `ready-to-review`; add `needs-attention`; local: `Status: needs-attention`). Do not move to `done/`. Retain local commits; do not publish failed local gates or manage a PR. Comment on the analysis: the failing gate, attempted fixes, what remains, SHA(s), and any publication/CI blocker. Respect session no-push on every path.
