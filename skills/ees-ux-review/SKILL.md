---
name: ees-ux-review
description: >-
  UX and accessibility review of a frontend diff — consistency with the
  project's design system, WCAG 2.2 AA, usability heuristics and frontend best
  practices, statically in the code and, when the app runs, in a browser.
  Critical/Major hard gate. Runs automatically in /ees-verify and the
  `ees-change` skill whenever the diff touches the frontend; not a command of
  its own.
user-invocable: false
disable-model-invocation: true
model: sonnet
effort: high
---

# UX review

Phase 3 of `/ees-verify` and the last review step of `ees-change`. The Functional and code review gates must already be green, or you are resuming after UX fixes. Do **not** Ship from this skill — hand back to the caller.

Skills root: parent of this skill directory (two levels above `SKILL.md`); resolve configuration per `{skills-root}/ees-pipeline/config.md`. Checklist: [checklist.md](checklist.md). Commit via `{skills-root}/ees-commit/SKILL.md`. If the repo has an overlay, read it after this skill: `docs/agents/config/ux-review.md`. Follow [Execution contract](../ees-pipeline/execution.md) for fixes, resources and test-baseline changes.

## When it runs

There is no switch. It runs when the fixed review-base diff, including intended untracked files, contains frontend files:

- components and pages: `.tsx`, `.jsx`, `.vue`, `.svelte`, `.astro`, `.html`
- styles: `.css`, `.scss`, `.sass`, `.less`, Tailwind or theme configuration
- server-side templates: `.twig`, `.blade.php`, `.erb`, `.jinja`, `.hbs` and other view templates
- or an Acceptance item (or brief outcome) that describes a screen or what the user sees.

Anything else — backend, API, docs, tests only — skips the review. Tell the caller "UX skipped: no frontend changes".

## Two parts, one reviewer

Each cycle runs one `ees-ux-reviewer` agent with fresh, scoped context: the analysis reference (or brief), the review base, the affected screens, the base URL when there is one, the viewports and [checklist.md](checklist.md).

1. **Static — always.** In the code: consistency with the project's design system (existing components, tokens for colour, spacing and typography, established patterns for forms, tables, dialogs and states), accessibility in the markup (labels, roles, names, alt, focus handling), and best practices of the frontend framework at the version in the manifest.
2. **Browser — when the app runs.** Take the base URL from `AGENTS.md`; when it is missing or the app does not answer, try the documented dev command once. Walk the affected screens and their happy path as a first-time user, desktop `1440x900` then mobile `390x844` (with touch emulation when the tool supports it), against the browser items of the checklist.

When no browser tool is available, or the app cannot be started, run the static part only. This does not fail the gate and asks no one: the report says "browser walkthrough not run" with the reason, and the caller puts that line into the analysis comment or the report.

## Gate (max 3 cycles)

| Severity | Examples | Gate |
|----------|----------|------|
| **Critical** | Unreadable text, broken layout, missing input label, dead primary action, horizontal overflow, keyboard trap, contrast far below AA | **fail** |
| **Major** | Contrast below AA, tap target < 24px, missing loading/error/empty state, a new component or style duplicating an existing one, hard-coded colours or spacing where tokens exist, confusing navigation or unguarded destructive action | **fail** |
| **Minor** | Polish, small spacing or copy improvements | report only; never fails the gate |

Any Critical/Major → fail, then Fix and Re-check and repeat (re-review **changed screens and files only**). Only Minor or nothing → green. 3 failed cycles → **stop** and return to the caller as **Fail** (`/ees-verify` sets `needs-attention`).

## Fix

The parent selects Critical and Major findings and delegates the fixes to a fresh `ees-implementer` per independent cluster under the Execution contract; a trivial one-file CSS or copy fix may be done directly. Preserve the agreed analysis contract, test-first coverage and stable test baseline. Commit justified test changes separately; production commit: `fix(ui): <what> (#<N>)`. No push/PR, container-root commits or scope creep.

### Re-check (mandatory after any UX fix)

Re-run the local tests/tooling from `AGENTS.md` on the affected delivery roots through `ees-check-runner`.

- Red → repair and rerun within this UX gate’s cycle limit; no separate re-check counter.
- Green → resume the UX gate.

Full Spec/Standards again **only** if the UX fix changes behaviour vs Acceptance (new flow, Acceptance copy, new screen).

## Green output

Tell the caller UX is green, and whether the browser walkthrough ran. Do **not** comment Minors on the analysis or the PR.

## Rules

- Max **3** UX cycles; Functional max **3** stays owned by `/ees-verify`
- The reviewer only reports; implementers fix; the parent orchestrates and commits
- No commits on the monorepo container root
- No Ship from this skill
