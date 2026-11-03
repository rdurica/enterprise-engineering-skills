# Delivery

The only description of branches, pushing, CI and PRs. Only the main session reads it, at two points: **Start** in `/ees-implement` step 2 and **Finish** in `/ees-verify` Finalize. Every other skill and agent leaves git delivery alone: workers never commit, push, switch branches or touch PRs; the main session makes the commits.

## Publishing

Publishing is on by default: the main session pushes the Delivery branch, watches CI and opens the PR.

- **"Do not push"** (or an equivalent instruction) in the session turns publishing off for that session: local commits only, no push, CI watch, PR creation or PR state change. Tracker updates on the analysis still happen.
- **No PR-capable remote** — no `origin`, or an `origin` that is not GitHub — push only when a remote exists and open no PR. Report it as local or push-only delivery; that is not a failure.

## Start

In each delivery root (in a monorepo every affected one, never the container root):

1. `git fetch origin`.
2. Take the branch from the analysis `## Delivery`. If it exists locally or on the remote, reuse it; otherwise create it from the remote default branch with `--no-track`.
3. Switch only with a clean worktree. Pull the matching remote branch only when clean. Preserve unfinished local work on resume: no automatic stash, reset or rebase.
4. A direct `/ees-verify` uses the same branch: stay on it when current, otherwise switch in a clean worktree, fetching it when it exists only on the remote. Report a missing or ambiguous branch or a divergent remote history instead of rewriting it.

## Finish

Runs after every local gate of `/ees-verify` is decided, per delivery root with changes. Never force-push, never push the container root, never comment on a PR (`gh pr review`, `gh pr comment` are forbidden); notes go on the analysis only.

### Green

When publishing is off, skip to step 5 and report "publication/CI skipped by the session".

1. Check the remote, then push explicitly: `git push -u origin <branch>`. A rejected push or a missing remote is a publication blocker: keep the local results and report it.
2. Create a **draft** PR if none exists, or update the existing PR's title and Summary to the final scope (see PR body).
3. Watch CI (see CI). Red or unresolved → repair, or Fail.
4. After green CI mark the draft ready; a ready PR stays ready. Collect the URLs.
5. Apply the tracker's Green operation and comment on the analysis: gate evidence, the published or local SHA(s), the CI outcome and the PR URLs, or the explicit local-only outcome.

### Fail

A gate red after its budget, or a hard stop.

1. When publishing is on, push the committed work to the Delivery branch and create or keep a **draft** PR (a ready PR goes back to draft). Do not publish unverified repair commits after an earlier CI failure and do not watch CI for a failed local gate. Report an unavailable remote, a rejected push or a PR failure honestly; they never excuse losing local results.
2. When publishing is off, keep the local commits and change no PR.
3. Apply the tracker's Fail operation and comment on the analysis: the gate that failed (Functional, code review, UX, CI) or the publication blocker, what was tried, what remains, the full SHA(s), Blocked review items verbatim and draft PR URLs when one was opened. Never claim a draft that was not opened.

## PR body

Title in English Conventional Commits like the commits (`type(scope): … (#N)`), referencing the analysis `#N`. Supply the body explicitly (it overrides a repository PR template) through `--body-file` or a structured argument: the analysis link and `## Summary` (English heading, content in the resolved `language`). No Acceptance or Test plan in the PR; Acceptance is checked off only in the analysis.

```markdown
Implements #<N>.

## Summary

- {1–3 bullets describing the final change}
```

## CI

Check the push and PR workflows for the commit just published, not an older or unrelated run. Create the draft PR first so PR-triggered checks can run. No applicable workflow means CI is skipped; missing expected, pending or inconclusive checks are not green. Respect repository timeouts and avoid indefinite waits.

Delegate CI fixes, rerun the affected local gates, commit, push and check the new commit. Stop after 3 unsuccessful CI repairs, or when the checks cannot finish, and report the blocker instead of claiming success.

## Monorepo

Start and Finish run per affected delivery root; the container root stays on its branch and gets no checkout, commit, push or PR. Submodule pointer bumps are left to `/ees-monorepo-update` after the delivery PRs merge.
