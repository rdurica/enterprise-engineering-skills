# Development skills

Feature pipeline and helpers. `/setup` copies this folder into a target repo at `.cursor/skills/development/` (does not overwrite existing skills).

```
setup/              — per-repo tracker, git workflow, domain doc layout
align/              — alignment interview; no PRD here
to-prd/             — conversation → published PRD
implement/          — plan from PRD; parent for small work, sub-agents for large increments, then verify
verify/             — Closer: Functional (Spec + Standards + tests) [→ UX] → Ship; agent: ready PR if green, draft PR if fail; notes on PRD; human: HEAD
ux-review/          — Phase 2 of /verify (if enabled); browser UX/a11y; re-check tooling after fixes
commit/             — Conventional Commits (English); used by implement/verify
tdd/                — red-green-refactor (parent and implement sub-agents)
integration-tests/  — Symfony HTTP integration tests (parent and implement sub-agents)
git-release/        — semver tag + GitHub release; user must confirm version
monorepo-update/    — no args: sync delivery roots to main + bump pointers; with PRD: every delivery root → Delivery branch
```

Helpers during implement/verify: `tdd`, `integration-tests`, `commit`, `ux-review`. Outside the feature loop: `git-release`, `monorepo-update`.
