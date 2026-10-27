---
name: idea
description: >-
  Write down a planned change as a short idea (Goal, Change, optional
  Depends on) to be analyzed later with /analyze #N. Use when the user wants
  to note, plan or queue a change without a full analysis, or to rewrite an
  existing idea.
argument-hint: "[#N]"
disable-model-invocation: true
model: sonnet
effort: medium
---

# Idea

Write down a change that is not due yet: why it exists and what changes, in a few sentences. The detailed analysis comes later with `/analyze #N`, against the code as it is then. Do not analyze, design or implement here.

Resolve configuration per `{skills-root}/pipeline/config.md` (skills root is the parent of this skill's directory) and tracker operations per `{skills-root}/pipeline/tracker-<tracker>.md`. Take `language` from the resolved config; if unset, use the language of the conversation and do not ask. Prose goes in that language; headings, identifiers and paths stay English. Branch slugs are ASCII and hyphenated.

## `/idea` — new idea

1. **Talk it through.** A short conversation, a few questions at most, only about the Goal (why the change exists, what holds at the end) and the Change (the intent, how behaviour changes). No decision tree, spikes or checkpoint.
2. **Look around.** Read the open ideas and analyses (active ones locally). Propose `Depends on` for each one this change builds on or touches the same area as, and warn about a duplicate or overlap before creating anything. Read code only to get module and concept names right; do not settle architecture.
3. **Confirm.** Show the draft and the proposed `Depends on`; the user confirms or corrects. If an open idea already has the same intent, ask whether to create anyway or use `/idea #N` on it.
4. **Create** per the tracker file: title `Idea: <title>`, label `idea` on GitHub, `docs/agents/analysis/ideas/NNN-<slug>.md` locally. The ID is shared across `ideas/`, active and `done/`.

## `/idea #N` — rewrite

Fetch the idea and rewrite Goal, Change or `Depends on` in place; keep the number, the branch and the rest of `## Delivery`. If the issue or file is already an analysis (label `analysis`, or a file outside `ideas/`), refuse and point to `/analyze-modify #N`.

## Body

```markdown
## Delivery

- Ticket: [#<N>](<issue url>)        (or the external ticket; locally NNN)
- Kind: feature | chore
- Branch: `feature/<ticket>-<short-slug>`
- Depends on: #41, #42               (optional)

## Goal

{1–3 sentences: why the change exists and what should hold at the end}

## Change

{2–4 sentences: the intent and how behaviour changes; no classes, paths or contracts}
```

Nothing else: no Current State, Affected Areas, Architecture, API Contracts, Acceptance or Further Notes. `Ticket` and `Branch` follow the rules in `/analyze` step 3 of Phase B; on GitHub the issue number is known only after creating, so add `## Delivery` by editing the body right after.

## Finish

Say that the next step is `/analyze #N` when the change is due. A `Depends on` that is still open will be flagged then.
