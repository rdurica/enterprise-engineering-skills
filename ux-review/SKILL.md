---
name: ux-review
description: >-
  Browser UX/a11y walkthrough after code review — Critical/Major hard gate,
  then re-check local tooling. Phase 3 of /verify when ux-review is enabled, or
  run /ux-review directly after implementation.
disable-model-invocation: true
---

# UX review

Phase 3 of `/verify` when `workflow.md` has `ux-review: enabled`. The Functional and code review gates must already be green, or you are resuming after UX fixes. Do **not** Ship from this skill — return to `/verify` for Ship.

Read `docs/agents/workflow.md`. Skills root: parent of this skill directory (two levels above `SKILL.md`). Checklist: [checklist.md](checklist.md). Commit via `{skills-root}/commit/SKILL.md`.

If the repo has an overlay, read it after this skill: `docs/agents/ux-review.md`. Follow [implement’s Execution contract](../implement/SKILL.md#execution-contract) for fixes, resources, and test-baseline changes, including direct `/ux-review` use.

## When to skip

Auto-green (no browser) when the intended fixed review-base diff has **no UI/frontend** changes (e.g. only backend/API/docs). Tell `/verify` UX is skipped → Ship.

`ux-review: disabled` or missing → `/verify` never calls this skill.

## Gate (max 3 cycles)

```
UX review cycle: 1 / 3
- [ ] Scope (affected screens + happy-path)
- [ ] Walkthrough (desktop + mobile)
- [ ] Findings triaged
- [ ] Critical/Major fixes committed (if any)
- [ ] Re-check local tooling green (after any fix)
```

| Severity | Examples | Gate |
|----------|----------|------|
| **Critical** | Unreadable text, broken layout, missing input label, dead primary CTA, horizontal overflow | **fail** |
| **Major** | Weak hierarchy, contrast below AA, tap target < 44px, missing loading/error/empty, confusing nav | **fail** |
| **Minor** | Off-grid spacing, polish, AI-slop aesthetics | ignore; do not post |

3 UX failures → **stop**. Return to `/verify` **Fail**, which sets `needs-attention` (do not Ship; do not comment Minors).

## Scope

1. Screens from analysis `## Acceptance` + frontend files in `git diff <review-base-SHA> -- <intended-paths>` plus intended untracked files
2. Short happy-path to reach those screens
3. Viewports: desktop `1440x900`; mobile `390x844`, with mobile/touch emulation when the available browser tool supports it

**Base URL** — from `AGENTS.md` / `docs/agents/domain.md`; else ask. Use any available browser automation tool capable of navigation, interaction, viewport control, screenshots, and accessible UI inspection. If the required walkthrough cannot be performed, report the missing capability and hard fail; do not claim green.

## One cycle

Use Walkthrough and A11y+Visual sub-agents with fresh, scoped context: relevant analysis, review-base, screens, URL, checklist and browser instructions. Parallel walkthroughs require independent browser sessions and isolated application state; otherwise run sequentially. Parent synthesizes; Minor never fails the gate.

**Walkthrough prompt** — base URL, scope screens, happy-path, checklist path, both viewports:

> Act as a first-time user. Use the available browser automation tool and its documented APIs. Desktop then mobile. At each screen: is the next step obvious? Is the primary action clear? Are dangerous actions guarded? Screenshot friction points. Report Critical/Major/Minor with screen + issue. Under 400 words.

**A11y + Visual prompt** — same scope, [checklist.md](checklist.md):

> Check affected screens against the checklist. Focus on contrast, tap targets, focus visibility, form labels, accessible names, horizontal overflow; hierarchy; loading/empty/error/success; AI-slop anti-patterns. Cite checklist item or WCAG where useful. Critical/Major/Minor with screen + issue. Under 400 words.

**Outcome:** any Critical/Major → fail. Only Minor (or none) → green; hand back to `/verify` for Ship.

Fail and cycles < 3 → Fix, then **Re-check**, then repeat this cycle (re-walk **changed screens only**).

## Fix

Parent may handle trivial one-file CSS/copy follow-ups; delegate substantial fixes by independent cluster under the Execution contract. Preserve the agreed analysis contract, test-first coverage and stable test baseline. Commit justified test changes separately; production commit: `fix(ui): <what> (#<N>)`. No push/PR, container-root commits, or scope creep.

### Re-check (mandatory after any UX fix)

Hand control to parent `/verify`: re-run the local tests/tooling from `AGENTS.md` on affected delivery roots.

- Red → repair and rerun within this UX gate’s cycle limit; no separate re-check counter.
- Green → resume UX gate (re-walk affected screens only).

Full Spec/Standards again **only** if the UX fix changes behaviour vs Acceptance (new flow, Acceptance copy, new screen). Otherwise skip Spec/Standards.

## Green output

Tell `/verify` UX is green. Do **not** comment Minors on the analysis or the PR.

## Rules

- Max **3** UX cycles; Functional max **3** stays owned by `/verify`
- Parent orchestrates and commits; sub-agents handle substantial fixes
- No commits on the monorepo container root
- No Ship from this skill
