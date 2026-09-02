---
name: ux-review
description: >-
  Browser UX/a11y walkthrough after Functional verify — Critical/Major hard gate,
  then re-check local tooling. Phase 2 of /verify when ux-review is enabled, or
  run /ux-review directly after implementation.
disable-model-invocation: true
---

# UX review

Phase 2 of `/verify` when `workflow.md` has `ux-review: enabled`. Functional gate must already be green (or you are resuming after UX fixes). Do **not** Ship from this skill — return to `/verify` for Ship.

Read `docs/agents/workflow.md`. Skills root: parent of this file. Checklist: [checklist.md](checklist.md). Commit via `{skills-root}/commit/SKILL.md`.

If the repo has an overlay, read it after this skill: `.cursor/skills/development/ux-review/SKILL.md`.

## When to skip

Auto-green (no browser) when the fixed-point diff has **no UI/frontend** changes (e.g. only backend/API/docs). Tell `/verify` UX is skipped → Ship.

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

3 UX failures → **stop**. Leave `in-progress`. Return to `/verify` **Fail** (do not Ship; do not comment Minors).

## Scope

1. Screens from PRD `## Acceptance criteria` + frontend files in `git diff <fixed-point>...HEAD`
2. Short happy-path to reach those screens
3. Viewports: desktop `1440x900`; mobile `390x844x3,mobile,touch` via Chrome DevTools MCP `emulate`

**Base URL** — from `AGENTS.md` / `docs/agents/domain.md`; else ask. Chrome DevTools MCP unavailable → hard fail: do not Ship.

## One cycle

Walkthrough and A11y+Visual sub-agents **in parallel** (`Task`, `generalPurpose`). Parent synthesizes; Minor never fails the gate.

**Walkthrough prompt** — base URL, scope screens, happy-path, checklist path, both viewports:

> Act as a first-time user. Use Chrome DevTools MCP (`navigate_page`, `take_snapshot`, `click`, `take_screenshot`, `emulate`). Desktop then mobile. At each screen: is the next step obvious? Is the primary action clear? Are dangerous actions guarded? Screenshot friction points. Report Critical/Major/Minor with screen + issue. Under 400 words.

**A11y + Visual prompt** — same scope, [checklist.md](checklist.md):

> Check affected screens against the checklist. Focus on contrast, tap targets, focus visibility, form labels, accessible names, horizontal overflow; hierarchy; loading/empty/error/success; AI-slop anti-patterns. Cite checklist item or WCAG where useful. Critical/Major/Minor with screen + issue. Under 400 words.

**Outcome:** any Critical/Major → fail. Only Minor (or none) → green; hand back to `/verify` for Ship.

Fail and cycles < 3 → Fix, then **Re-check**, then repeat this cycle (re-walk **changed screens only**).

## Fix

Parent: trivial one-file CSS/copy. Else one `Task` per cluster. No push/PR, no container-root commits, no scope creep vs PRD Out of Scope.

Commit: `fix(ui): <what> (#<PRD>)`.

### Re-check (mandatory after any UX fix)

Hand control to parent `/verify`: re-run **Local pipeline** (tests + tooling from `AGENTS.md`) on affected delivery roots.

- Red → Functional Fix; counts toward Functional cycles (max 3). Then re-run Local pipeline.
- Green → resume UX gate (re-walk affected screens only).

Full Spec/Standards again **only** if the UX fix changes behaviour vs AC (new flow, AC copy, new screen). Otherwise skip Spec/Standards.

## Green output

Tell `/verify` UX is green. Do **not** comment Minors on the PRD or the PR.

## Rules

- Max **3** UX cycles; Functional max **3** stays owned by `/verify`
- Parent commits; fix sub-agents write code
- No commits on the monorepo container root
- No Ship from this skill
