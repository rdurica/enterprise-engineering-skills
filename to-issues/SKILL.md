---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices.
disable-model-invocation: true
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` for tracker conventions — run `/setup` if missing.

All publish operations follow `docs/agents/issue-tracker.md` (GitHub or local `.scratch/` — do not hardcode `gh` only).

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes an issue reference (issue number, URL, or `.scratch/` path) as an argument, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Any prefactoring should be done first

</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the issues to the issue tracker

For each approved slice, publish per issue-tracker conventions. Apply epic grouping only — **never** add `ready-for-implementation` to slice issues.

Publish in dependency order (blockers first) so you can reference real identifiers in "Blocked by".

After all slices are published, update the parent PRD to `ready-for-implementation` (remove `needs-slicing`, add `sliced` on GitHub):

**GitHub** — see issue-tracker-github.md `/to-issues` section.

**Local** — create `.scratch/<feature-slug>/issues/<NN>-<slug>.md` for each slice; set PRD `Status: ready-for-implementation` in PRD.md.

This is the only step that adds `ready-for-implementation` on the PRD. The first agent session picks the first unblocked slice.

<issue-template>
## Parent

Reference to parent PRD (GitHub `#N` or `.scratch/<slug>/PRD.md`).

## Branch

The branch from the parent PRD `## Delivery` section (same for all slices). Branch owner from Delivery applies to `/implement`.

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

Do NOT close the parent PRD.
