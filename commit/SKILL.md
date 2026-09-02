---
name: commit
description: >-
  Create a git commit with a Conventional Commits message from the current
  diff. Use when the user asks to commit, git commit, commitni, udělej commit,
  or write a commit message. Does not push or open a PR.
---

# Commit

Conventional Commits only. Do **not** push or open a PR.

## Steps

1. `git status` and `git diff` (and `git diff --cached`). Follow recent `git log` style.
2. Stage only the intended files. Never stage secrets, `.env`, or credentials.
3. Message in **English**, imperative, Conventional Commits:

   `type(scope): summary`

   Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`.

   Optional body. Footer: `BREAKING CHANGE: …` and/or `(#N)` when an analysis/issue is in context.

4. Commit (no `--no-verify`, no amend, no force):

```bash
git commit -m "$(cat <<'EOF'
type(scope): summary

Optional body.

EOF
)"
```

5. `git status` to confirm. Stop — no `git push`, no `gh pr create`.
