---
name: to-prd
description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user — just synthesize what you already know.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` — run `/setup` in the target repo if missing.

Read `prd-language` from `workflow.md` (`en` | `cs`). If missing, ask (same as missing `/setup`). Write PRD **prose** (title, problem, stories, AC text, notes) in that language. Keep the template **section headings in English**. Branch slug: ASCII, hyphenated; transliterate if the title is not English.

All publish operations follow `docs/agents/issue-tracker.md` (GitHub or local `.scratch/` — do not hardcode `gh` only).

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. If `docs/adr/` exists, respect those decisions in the PRD.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can.

Check with the user that these seams match their expectations.

3. Write the PRD using the template below, then publish (GitHub: label `prd` only; local: `.scratch/prd/NNN-<slug>.md`, no Status). Do not add `ready-for-agent`.

4. After publish, prepend `## Delivery` (GitHub: edit issue body; local: update PRD.md):

```markdown
## Delivery

- Branch: `feature/prd-<number>-<short-slug>` (local: `NNN` from next ID, three digits; GitHub: issue number. Slug from title, lowercase, max ~30 chars)
- Branch owner: agent | human   # from docs/agents/workflow.md unless user overrides
- Push: finalize | never
```

For **bugs**, set `Kind: bug` and use the shorter bug template sections where appropriate.

<prd-template>

## Kind

feature | bug | chore

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

For **bug** PRDs, replace with: Problem, Repro steps, Root cause hypothesis, Fix scope.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Acceptance criteria

Required. `/implement` plans internal increments from this list.

- [ ] Criterion 1

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>

### Local tracker publish

When `docs/agents/issue-tracker.md` is Local Markdown, follow `issue-tracker-local.md`:

1. Compute next `NNN` per issue-tracker-local.md (scan `.scratch/prd/` and `.scratch/prd/done/`; never reuse).
2. Choose `<slug>` from the PRD title (lowercase, hyphenated, ASCII; transliterate if needed).
3. Create `.scratch/prd/NNN-<slug>.md` with Kind, Delivery (`feature/prd-NNN-<short-slug>`), and PRD body. No Status line.

Bug fast-path (ticket with AC, not a full PRD): same path and ID scan, `Kind: bug`.

### GitHub publish

When backend is GitHub, follow issue-tracker-github.md `/to-prd` operations.

After publish, tell the user the next step is `/implement` on this PRD.
