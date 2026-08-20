# Verify — monorepo

Read only when `docs/agents/workflow.md` has `## Monorepo`, or nested git repos exist (`git submodule status` / nested `.git`, excluding `.git/modules/`).

| Role | Path | Agent may |
|------|------|-----------|
| **Container root** | wrapper (`.`) | `gh issue …`, `make …` from cwd; **stays on `main`** |
| **Delivery roots** | nested repos (`backend/`, …) | checkout, pull, diff, commit, push, PR |

Container root is **never** a delivery root — no delivery-branch checkout, commit, push, PR, or review diff. Submodule pointer bumps are out of scope (`/monorepo-update` after sub-repo PRs merge).

Delivery roots: `workflow.md` `delivery-roots`, repo overlay, or `git submodule status`. Do not add `.` to that list.

Without `## Monorepo`, cwd is the only delivery root.
