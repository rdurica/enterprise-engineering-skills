# Verify — monorepo

Read only when `docs/agents/config/workflow.md` has `## Monorepo`, or nested git repos exist (`git submodule status` / nested `.git`, excluding `.git/modules/`).

| Role | Path | Agent may |
|------|------|-----------|
| **Container root** | wrapper (`.`) | all `gh issue …` **`-R` container remote**; `make …` from cwd; **stays on its existing branch** |
| **Delivery roots** | nested repos (`backend/`, …) | diff, commit; branch/push/PR actions only as allowed by owner and publishing policy — **not** issue/analysis create |

Container root is **never** a delivery root — no delivery-branch checkout, commit, push, PR, or review diff. Submodule pointer bumps are out of scope for verify: `/monorepo-update` (no args) after sub-repo PRs merge; `/monorepo-update #N` checks out the analysis Delivery branch in **every** delivery root for human review and does **not** commit pointers. Issues and analyses always target the container-root GitHub repo (see `docs/agents/config/issue-tracker.md`), never a delivery-root remote.

Delivery roots: `workflow.md` `delivery-roots`, repo overlay, or `git submodule status`. Do not add `.` to that list.

Without `## Monorepo`, cwd is the only delivery root.

Human-owned delivery roots stay on their current branches and never manage PRs; `push: finalize` permits push after green local gates and CI for the published commit. Agent-owned continues an implement handoff without re-sync; direct verify follows safe branch handling in github.md. `push: never` and a session no-push instruction disable all publication paths. Review and delegate under the common verify scope and Execution contract.
