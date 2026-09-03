# Enterprise Engineering Skills

Agent skills for delivering features in an existing codebase: architecture and contracts are the spec, agents write the code and the tests, and every change arrives as a reviewable PR.

## Why

Agents are already good at implementation. They read the surrounding code, follow its idioms and rarely need to be told how to write a class — so spelling out the how is effort spent on something that goes stale the moment the code moves.

What an agent cannot take over is **responsibility**. I stay accountable for the project, so I own the boundaries: architecture, seams, contracts. Everything inside them is the agents' work.

The point is understanding, not just working code. Because I define the inputs and outputs myself, I know what crosses every seam, I can explain the whole flow, and I can answer to the business without first re-reading the diff — which in enterprise work matters more than raw speed. That is where this differs from spec-driven development: the goal is not "it does what I asked for", it is "I understand what it does and can stand behind it".

## What this is

`/analyze` fixes only the decisions that are expensive to reverse — layers, data flow, API contracts — plus a testable `## Acceptance`. How the code gets written is left to the implementing agents. You decide at the start and approve at the end.

Built for **brownfield, incremental work** in a repository that has tests, CI and documented conventions. Aligning, publishing an analysis and gating the result costs real time; it pays off when a change crosses more than one seam or package, and when someone other than the author has to review it.

**Not for** vibe coding, greenfield prototypes and spikes, one-off scripts, or trivial fixes.

## Pipeline

| Phase | Skill | Output |
|-------|-------|--------|
| 0 | `/setup` | `docs/agents/workflow.md`, `issue-tracker.md`, `domain.md`; vendors pipeline skills into the repo's skills dir (`.cursor/skills`, `.claude/skills`, …) |
| 1 | `/align` | Shared understanding; `docs/adr/` when a decision has real trade-offs |
| 2 | `/analyze` | Published analysis (architecture, API contracts, Acceptance) + `## Delivery` |
| 3 | `/implement #N` | Sub-agents write code and tests from the analysis; parent commits; then runs verify |
| 4 | `/verify` | Acceptance, standards, tests, tooling, code review, CI; findings fixed in code; PR opened |

You work at the start (align, review the published analysis) and at the end (review the PR). In between agents implement, test, run tooling and leave a clean tree.

| Work type | `/align` | `/analyze` | `/implement` |
|-----------|----------|------------|--------------|
| New feature | recommended | analysis | agents + verify |
| Complex bug | if root cause unclear | analysis (`Kind: bug`) | yes |
| Simple bug | skip | ticket with Acceptance | yes |
| Trivial fix | — | — | direct fix, outside the pipeline |

## Analysis lifecycle

```mermaid
stateDiagram-v2
    analysisPublished: analysis
    inProgress: in_progress
    needsAttention: needs_attention
    readyToReview: ready_to_review

    analysisPublished --> inProgress: implement_starts
    inProgress --> readyToReview: verify_green
    inProgress --> needsAttention: verify_fail_or_open_faq
    needsAttention --> inProgress: user_calls_implement
```

`ready-to-review` appears only after a green verify that opened a ready PR. `needs-attention` means the agent stopped and cannot continue alone — verify red after three cycles, a hard stop, or work blocked by an open `## FAQ`; it replaces `in-progress` so auto-start leaves it alone. Answer what the comment asks and re-run `/implement`. A dead session keeps `in-progress`, because re-running `/implement` is enough.

Notes always go on the analysis, never on the PR. On GitHub these states are labels; locally they are the `Status:` line in `.scratch/analysis/NNN-<slug>.md`.

## Configuration

`/setup` writes per-repo config to `docs/agents/workflow.md` and offers a preset:

| Preset | Tracker | branch-owner | push |
|--------|---------|--------------|------|
| `full-agentic` | github | agent | finalize |
| `human-owned` | github | human | never |
| `custom` | user choice | user choice | user choice |

It always asks for **language** (`en` \| `cs`) — analysis prose and ticket comments use it, section headings stay English. Issue tracker is GitHub (`gh`), local (`.scratch/`), or both. UX review is an optional hard gate inside `/verify`.

## Skills

One folder per skill at the pack root — Claude Code does not load nested category folders. `/setup` vendors the pipeline ones into the target repo.

```
setup/              — per-repo tracker, git workflow, domain doc layout
align/              — alignment interview; no analysis here
analyze/            — conversation to published analysis
implement/          — sub-agents implement from the analysis; parent commits
verify/             — Acceptance, standards, tests, tooling, code review, UX, CI, then ship
code-review/        — fix-first code review, phase 2 of /verify
ux-review/          — browser UX gate, phase 3 of /verify
tdd/                — red-green-refactor
integration-tests/  — Symfony HTTP integration tests
commit/             — Conventional Commits (English)
git-release/        — semver tag + GitHub release
monorepo-update/    — sync delivery roots / checkout an analysis branch
```

`tdd`, `integration-tests`, `commit`, `code-review` and `ux-review` are helpers called during implement and verify. `setup`, `git-release` and `monorepo-update` sit outside the feature loop and stay in the shared pack — they are not vendored into repos.

## Sub-agents

The skills say "sub-agent" and never name a tool, so the same text works in both runners. Whichever you use, the general-purpose sub-agent is the one meant: Cursor spawns it with the `Task` tool and `subagent_type: generalPurpose`, Claude Code with the `Task` tool and `general-purpose`. Which model runs behind it does not matter — nothing in the pack depends on a specific one.

## Installation

Clone or symlink into `~/.cursor/skills/` (Cursor) or `~/.claude/skills/` (Claude Code):

```bash
git clone git@github.com:rdurica/enterprise-engineering-skills.git ~/.cursor/skills
```

Both tools load `SKILL.md` from each immediate child of that directory and of the project skills dir. Which one a repo uses is detected by `/setup` — an already vendored dir wins, then `.claude/skills` when the repo has `CLAUDE.md` or `.claude/`, otherwise `.cursor/skills` — and recorded as `skills-dir` in `docs/agents/workflow.md`. A gitignored `personal/` folder is the place for local-only skills — Cursor loads them, git never sees them.
