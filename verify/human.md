# Verify — human

Stay on **HEAD**. Do not checkout, create, fetch, push, watch CI, or open a PR.

If `## Monorepo`, read [monorepo.md](monorepo.md) — still no checkout; diff current HEAD only. The user can run `/monorepo-update #N` first to put delivery roots on the analysis Delivery branch.

Unrelated dirty files → stop and ask. Intentional verify diffs may proceed.

Run the **Gate** in [SKILL.md](SKILL.md). Skip CI.

Never comment on a PR. Green and fail notes go on the **analysis only** (`language` from `workflow.md`; headings in English). GitHub: `gh issue comment`. Local: append under `## Comments`.

## Ship (gate green)

Comment on the analysis: local verify is green; the user should push and open the PR.

- GitHub: do **not** add `ready-to-review` (no PR yet). Leave `in-progress`.
- Local: `mkdir -p .scratch/analysis/done` and `mv` to `.scratch/analysis/done/NNN-<slug>.md`. Leave `Status: in-progress`.

## Fail (gate red after 3 cycles or hard stop)

Comment on the analysis: what failed, what was tried, what remains. Set `needs-attention` (GitHub: `--remove-label in-progress --add-label needs-attention`; local: `Status: needs-attention`). Do not add `ready-to-review`. Do not move to `done/`. Do not open a PR.
