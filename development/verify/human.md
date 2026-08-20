# Verify — human

Stay on **HEAD**. Do not checkout, create, fetch, push, watch CI, or open a PR.

If `## Monorepo`, read [monorepo.md](monorepo.md) — still no checkout; diff current HEAD only.

Unrelated dirty files → stop and ask. Intentional verify diffs may proceed.

Run the **Gate** in [SKILL.md](SKILL.md). Skip CI.

## Ship (gate green)

Comment on the PRD in `prd-language` from `workflow.md`: local verify is green; the user should push and open the PR.

- GitHub: do **not** add `ready-to-review` (no PR yet). Leave `in-progress`.
- Local: `mkdir -p .scratch/prd/done` and `mv` the file to `.scratch/prd/done/NNN-<slug>.md` (assign next `NNN` if unnumbered). Leave `Status: in-progress`.
