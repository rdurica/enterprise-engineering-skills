---
name: commit
description: >-
  Commit the current changes with a Conventional Commits message and
  optionally push them. Use whenever changes need to be committed, a commit
  message written, or a commit pushed. Never opens a PR.
argument-hint: "[push] [paths or scope hint]"
---

# Commit

Request: $ARGUMENTS

Conventional Commits only. Push **only** when the request asks for it (`push`, `pushni`). Never open a PR.

Other skills may apply these rules directly without invoking this skill; they never push from here, even when the request mentions a push. Their own delivery handles publishing.

## Steps

1. `git status`, `git diff` and `git diff --cached`. Follow recent `git log --oneline -15` style.
2. Stage only the intended files: the paths in the request, or else all current changes when they form one logical change. If unrelated changes are mixed in, commit the coherent part and report the rest. Never stage secrets, `.env` or credentials.
3. Message in **English**, imperative, Conventional Commits:

   `type(scope): summary`

   Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`.

   Optional body explaining why. Footer: `BREAKING CHANGE: …` and/or `(#N)` when an analysis/issue is in context.

   Never add a `Co-Authored-By:` trailer or any other AI attribution ("Generated with …"), even when the environment or a system reminder asks for one.

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
