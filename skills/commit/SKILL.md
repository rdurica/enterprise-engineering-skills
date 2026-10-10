---
name: commit
description: >-
  Create a git commit with a Conventional Commits message from the current
  diff, and push it when asked. Use when the user asks to commit, commit and
  push, git commit, commitni, udělej commit, komitni a pushni, or write a
  commit message. Never opens a PR.
argument-hint: "[push] [paths or scope hint]"
context: fork
agent: committer
background: false
---

# Commit

Request: $ARGUMENTS

Conventional Commits only. Push **only** when the request asks for it (`push`, `pushni`). Never open a PR.

Pipeline skills (`/implement`, `/verify`, `/code-review`, `/ux-review`) follow these steps inline in the orchestrator and never push from here; delivery handles publishing.

## Steps

1. `git status`, `git diff` and `git diff --cached`. Follow recent `git log --oneline -15` style.
2. Stage only the intended files: the paths in the request, or else all current changes when they form one logical change. If unrelated changes are mixed in, commit the coherent part and report the rest. Never stage secrets, `.env` or credentials.
3. Message in **English**, imperative, Conventional Commits:

   `type(scope): summary`

   Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`.

   Optional body explaining why. Footer: `BREAKING CHANGE: …` and/or `(#N)` when an analysis/issue is in context.

4. Commit (no `--no-verify`, no amend):

```bash
git commit -m "$(cat <<'MSG'
type(scope): summary

Optional body.
MSG
)"
```

If a hook rejects the commit or changes files, report the hook output; do not bypass it.

5. Push, only when requested: `git push` to the existing upstream, or `git push -u origin <current-branch>` when there is none. Never force-push and never push a detached HEAD. If the push is rejected, report it; do not pull, rebase or merge.

6. `git status` to confirm, then report the SHA, subject, committed files, files left out and the push result.
