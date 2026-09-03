# Verify — agent

Always push and open a **PR**. Green gate → ready PR. Failed gate → draft PR. Do not skip the PR.

Never comment on the PR (`gh pr review`, `gh pr comment` forbidden). Green and fail notes go on the **analysis only**.

If `## Monorepo`, read [monorepo.md](monorepo.md) before sync.

## Sync (before the gate)

Single-repo: cwd is the delivery root. Fetch, checkout the Delivery branch, `pull --rebase` if it exists.

Monorepo: container root stays on `main`. For each **delivery root**:

1. `git -C <path> status --short` — unrelated dirty files → **stop**. Intentional verify diffs may proceed.
2. `git -C <path> fetch origin`
3. Affected if `origin/<branch>` exists, a PR exists for `<branch>`, or the branch has commits vs `origin/main`. Else skip.
4. `git -C <path> checkout <branch>` && `git -C <path> pull origin <branch>`
5. Record path, branch, `rev-parse --short HEAD`

Diff the local checkout — not `git show origin/<branch>:path`. Never diff the container root.

Then run the **Gate** in [SKILL.md](SKILL.md).

## Analysis comments

GitHub: `gh issue comment` on the analysis issue (`-R` container-root in a monorepo). Local: append under `## Comments`. Body in `language` from `workflow.md`. Headings stay English.

## PR body

Title references analysis `#N`. Pass this `--body` (overrides a repo `PULL_REQUEST_TEMPLATE`). Copy `## Acceptance` from the analysis — **never** invent a separate `## Test plan`. Check `- [x]` only items whose tests actually ran and passed in this verify; leave skipped (FAQ) and untested items `- [ ]`.

```markdown
Implements #<N>.

## Summary

- {1–3 bullets from Change / commits}

## Acceptance

- [x] {item whose tests ran and passed}
- [ ] {skipped or not tested}
```

## Ship (gate green)

1. `git push -u origin <branch>` in **each affected delivery root** (skip container root; skip if no remote).
2. CI, if a GitHub remote exists:
   ```bash
   gh run list --limit 5
   gh run watch {RUN_ID} --exit-status
   ```
   No workflows → treat CI as green. Red CI → **Fix** in SKILL.md, then a new gate cycle (do not count the cycle complete until CI is re-watched).
3. **Ready PR** in each delivery root with commits vs default branch. **Never** on the container root.
   - no PR → `gh pr create` (no `--draft`) with the PR body above
   - draft PR → `gh pr ready` (do not add a Test plan; refresh Acceptance checkboxes if tests changed)
   - already ready → leave it
   Collect PR URLs.
4. Finalize analysis. The final state carries exactly two labels, `analysis` and `ready-to-review` — nothing else:
   - GitHub: `gh issue edit <N> [-R …] --remove-label in-progress --remove-label needs-attention --remove-label ready-for-agent --add-label ready-to-review` (removing a label that is not set is fine)
   - Local: write `Status: ready-to-review`, then `mkdir -p .scratch/analysis/done` and `mv` to `.scratch/analysis/done/NNN-<slug>.md`.

```markdown
Verify gate green.

## Pull requests

- **{repo}** ({path}): {url}

## Monorepo (if applicable)

Submodule pointer bumps on the container root are for the user after sub-repo PRs merge.
```

## Fail (gate red after 3 cycles or hard stop)

Set `needs-attention` (GitHub: `--remove-label in-progress --add-label needs-attention`; local: `Status: needs-attention`). Do not add `ready-to-review`. Do not move to `done/`.

1. `git push -u origin <branch>` in **each affected delivery root** (skip container root; skip if no remote). Do not watch CI.
2. **Draft PR** in each delivery root with commits vs default branch. **Never** on the container root.
   - no PR → `gh pr create --draft` with the PR body above
   - ready PR → `gh pr ready --undo`
   - already draft → leave it
   Collect PR URLs.
3. Comment on the analysis: which gate ran out of cycles, what failed (Spec, Standards, tests, code review, UX), what was tried, what remains — Blocked code review items go here verbatim. Include draft PR URLs.

```markdown
Verify failed at the {Functional | code review | UX | re-check} gate. Marked needs-attention. Draft PR(s) open.

## What failed

- …

## What was tried

- …

## What remains

- …

## Pull requests (draft)

- **{repo}** ({path}): {url}
```
