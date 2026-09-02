# Verify — human

Stay on **HEAD**. Do not checkout, create, fetch, push, watch CI, or open a PR.

If `## Monorepo`, read [monorepo.md](monorepo.md) — still no checkout; diff current HEAD only. The user can run `/monorepo-update #N` first to put delivery roots on the PRD branch.

Unrelated dirty files → stop and ask. Intentional verify diffs may proceed.

Run the **Gate** in [SKILL.md](SKILL.md). Skip CI.

Never comment on a PR. Green and fail notes go on the **PRD only** (`prd-language` from `workflow.md`; headings in English). GitHub: `gh issue comment`. Local: append under `## Comments`.

## Ship (gate green)

Comment on the PRD: local verify is green; the user should push and open the PR.

- GitHub: do **not** add `ready-to-review` (no PR yet). Leave `in-progress`.
- Local: `mkdir -p .scratch/prd/done` and `mv` the file to `.scratch/prd/done/NNN-<slug>.md` (assign next `NNN` if unnumbered). Leave `Status: in-progress`.

## Fail (gate red after 3 cycles or hard stop)

Comment on the PRD: what failed, what was tried, what remains. Leave `in-progress`. Do not add `ready-to-review`. Do not move to `.scratch/prd/done/`. Do not open a PR.
