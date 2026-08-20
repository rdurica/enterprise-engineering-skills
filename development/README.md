# Development skills

Feature pipeline and helpers. `/setup` copies this folder into a target repo at `.cursor/skills/development/` (does not overwrite existing skills).

```
setup/              — per-repo tracker, git workflow, domain doc layout
align/              — alignment interview; no PRD here
to-prd/             — conversation → published PRD
implement/          — plan from PRD; parent for small work, sub-agents for large increments, then verify
verify/             — Spec + Standards + tests; agent: CI + PR; human: HEAD
commit/             — Conventional Commits (English); used by implement/verify
tdd/                — red-green-refactor (parent and implement sub-agents)
integration-tests/  — Symfony HTTP integration tests (parent and implement sub-agents)
git-release/        — semver tag + GitHub release; user must confirm version
monorepo-update/    — sync delivery roots to main; bump + push submodule pointers on container root
```

Helpers during implement/verify: `tdd`, `integration-tests`, `commit`. Outside the feature loop: `git-release`, `monorepo-update`.
