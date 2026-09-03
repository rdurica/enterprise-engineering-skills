---
name: align
description: >-
  Structured alignment interview on a plan or design — explore the codebase,
  resolve decision branches one by one, and write docs/adr/ when a decision
  has real trade-offs. Use when starting a feature, stress-testing a design,
  or before writing an analysis.
disable-model-invocation: true
---

# Align

Reach shared understanding before implementation. Do NOT write an analysis here — that is `/analyze`. Do NOT implement here — that is `/implement`.

Read `docs/agents/workflow.md` if present — skip align for simple bugs (bug fast-path in workflow.md). Use this skill only for new features or complex/unclear bugs.

## Process

### 1. Explore

If a codebase is available, read relevant code plus `docs/adr/` if it exists (see `docs/agents/domain.md` if configured).

If a question can be answered by exploring the codebase, explore instead of asking.

### 2. Interview

Walk the decision tree one branch at a time:

- One question at a time
- Provide a recommended answer with each question
- Resolve dependencies between decisions before moving on
- Stop when every branch is resolved

### 3. Runnable spikes (when needed)

If a question cannot be settled in conversation, build a **throwaway spike**:

- Minimal code, no tests, no polish
- One command to run
- State in memory only unless persistence is the question
- Capture the verdict, then continue aligning
- Delete or fold the decision into real code when done

### 4. Document

List every decision the interview resolved and put each one in a bucket:

- **ADR** — real trade-offs and a reversal cost. Write `docs/adr/NNNN-slug.md` (next number; Context / Decision / Consequences) and name the rejected alternative in Context.
- **Analysis** — shapes the change but is cheap to reverse. It travels to `/analyze` as a `## Further Notes` bullet naming the rejected alternative.
- **Obvious** — no alternative was ever in play. Nothing to record.

Do not write ADRs for obvious or easily reversed choices, and do not let a decision leave the session in no bucket at all.

Without a codebase, run steps 2–3 only — do not write local files.

### 5. Hand off

When aligned, tell the user the next step is `/analyze` to synthesize the session into a published analysis. Hand over the bucketed decision list with it: `/analyze` links the ADRs from `## Architecture` and folds the analysis bucket into `## Further Notes`.

For bug fast-path, hand off to lightweight issue creation or `/analyze` with `Kind: bug` instead.
