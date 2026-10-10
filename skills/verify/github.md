# Verify — agent

Parent manages delivery branches and PRs when publishing is allowed. Read `push` from workflow: `finalize` permits Ship/Fail publishing; `never` or a session no-push instruction forbids push and all PR creation/state changes. In that case finish local gates, retain commits, and explicitly report git publication/CI skipped; analysis tracker updates remain allowed unless separately forbidden. Sub-agents never push or manage PRs.

Never comment on the PR (`gh pr review`, `gh pr comment` forbidden). Green and fail notes go on the **analysis only**.

If `## Monorepo`, read [monorepo.md](monorepo.md).

## Local branch handling

Continuing implement stays on its delivery branch without another pull/rebase. For direct verify, use the analysis Delivery branch: stay there if current; otherwise switch only in a clean worktree to the existing local/remote branch. Fetch remote-only branches when needed. Establish the review base from that intended branch, preserve unfinished work, and report missing/ambiguous branch or divergent publication history instead of rewriting it.

Monorepo: apply this per affected delivery root; never switch or publish the container root. Run the local gates in [SKILL.md](SKILL.md).

## Analysis comments

GitHub: `gh issue comment` on the analysis issue (`-R` container-root in a monorepo). Local: append under `## Comments`. Body in `language` from workflow; headings stay English.

## PR body

Title references analysis `#N`. Supply the body explicitly (overrides a repo PR template), using a structured tool argument or `--body-file`. Copy `## Acceptance` from the analysis; do not invent a separate Test plan. Check only items whose tests actually ran and passed here; skipped or untested items remain unchecked.

```markdown
Implements #<N>.

## Summary

- {1–3 bullets describing final Change / commits}

## Acceptance

- [x] {tested and passed item}
- [ ] {skipped or untested item}
```

## CI

Check applicable push/PR workflows for the commit just published, not an older or unrelated run. Agent-owned creates/updates the draft PR first so PR-triggered checks can run; human-owned only reads an existing PR. No applicable workflows means CI is skipped; missing expected, pending or inconclusive checks are not green. Respect repository timeouts and avoid indefinite waits.

Delegate CI fixes, rerun affected local gates, commit and push, then check the new commit. Use verify’s repair limit. If checks need an unavailable PR or cannot finish, report the blocker instead of claiming success.

## Ship (local gates green)

If publishing is disabled: finalize local analysis as below, report SHA(s) and “publication/CI skipped by configuration/session”; create no PR.

When publishing is allowed, per affected delivery root with changes:

1. Check remote destination, then push the Delivery branch explicitly (`git push -u origin <branch>`). Never force-push. If no remote or no PR-capable remote exists, preserve local results and report the publication blocker; do not claim published completion.
2. Create a **draft** PR if none exists; update an existing PR's body to reflect final scope and tested Acceptance. Never target the container root.
3. Check CI above, including PR-triggered checks. Red or unresolved → repair or Fail.
4. After green CI, mark the draft PR ready; an already ready PR remains ready. Collect URLs.

Finalize only after all applicable gates are green (or publishing explicitly disabled):

- GitHub analysis: remove `in-progress`, `needs-attention`, `ready-for-agent`; add `ready-to-review`, preserve the existing tracker kind label (`analysis` or bug).
- Local: write `Status: ready-to-review`, then move to `docs/agents/analysis/done/NNN-<slug>.md`.

Comment on the analysis with gate evidence, published SHA(s), CI outcome, PR URLs or explicit local-only outcome. Monorepo pointer bumps remain for the user after delivery PRs merge.

## Fail (gate red after budget or hard stop)

Set `needs-attention`; remove `in-progress` and `ready-to-review`. Do not move to `done/`.

Only when publishing is allowed, publish committed work to the intended delivery branch and create/keep a **draft** PR for review (ready PR → draft). Skip container root; never force-push. Do not publish unverified repair commits after an earlier CI failure. Report any unavailable remote, push rejection or PR failure honestly; these do not excuse losing the local results. Do not watch CI for a failed local gate.

When publishing is disabled, retain local commits and do not push, create a PR or change an existing PR's state.

Comment on the analysis: gate that exhausted its budget (Functional, code review, UX, CI) or publication blocker; what failed, attempted fixes, remaining work, full SHA(s), and draft PR URLs if available. Include Blocked review items verbatim. Never claim a draft was opened if publishing was skipped.
