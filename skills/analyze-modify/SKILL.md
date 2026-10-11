---
name: analyze-modify
description: >-
  Modify an existing analysis — before or after /implement — so it stays one
  consistent current state: explore the analysis, ADRs and code, name the risks
  the modification brings and agree them with the user, then rewrite the
  analysis in place. Use when a published analysis needs to change.
disable-model-invocation: true
---

# Analyze modify

Take a published analysis and the user's description of what should be different, and leave behind an analysis that reads as if it had been written that way from the start. Do not write a changelog into the body — history goes only in `## Revisions`. Do not implement — that is `/implement`.

Read `docs/agents/config/issue-tracker.md` and `docs/agents/config/workflow.md`; run `/setup` if they are missing. Write prose in the workflow `language`, as `/analyze` does.

## Process

### 1. Load

Resolve the analysis number or path through the tracker — on the local tracker also look in `done/`. Ask for the modification if the user did not describe it.

Decide the phase:

- **Not implemented** — the Delivery branch does not exist or has no commits past its merge-base, and the analysis carries no pipeline label. Only the document changes.
- **In progress or delivered** — the branch has commits, the issue is `in-progress`, `needs-attention` or `ready-to-review`, or the file is in `done/`. Read the branch diff against its merge-base too: committed tests and code are part of what must stay consistent.

### 2. Find inconsistencies

Walk every section — Current State, Change, Affected Areas, Architecture, API Contracts, Acceptance, Further Notes — and list what the modification contradicts, makes obsolete or leaves missing. Check it against `docs/adr/` and, when implemented, against the committed tests and code. Delegate broad searches to the built-in `Explore` agent and keep only its conclusions.

If the modification rewrites most of Change and Acceptance or changes the goal, stop and recommend a fresh `/align` and `/analyze` instead.

### 3. Agree the risks

Name each concrete risk the modification brings: a broken API contract or client compatibility, data or migration impact, committed tests or code that stop matching, a conflict with an ADR, scope growth. Put them to the user one at a time with `AskUserQuestion` and a recommended answer, as in `/align` step 2 — accept, mitigate, or change the modification. Ask the open decisions the modification creates the same way. Explore instead of asking whenever the code can answer.

Do not rewrite anything until every risk is agreed or parked in FAQ.

### 4. Rewrite in place

Follow [analysis-template.md](../analyze/analysis-template.md) for every section you touch.

- Rewrite the affected sections so the whole analysis describes one current state. No "new", "changed", "originally" or strikethrough in the body.
- An accepted risk with its mitigation is a decision: put it in Architecture or Further Notes, or write an ADR — superseding the old one when it conflicts — using the buckets from `/align` step 4.
- Acceptance: changed and new items become `- [ ]`, dropped items are deleted, untouched completed items stay `- [x]`.
- Unresolved questions go to `## FAQ` under Affected Areas.
- Append one bullet to `## Revisions`, the last section: date, the modification in one sentence, the risks the user accepted and, when tests are already committed, the tests that must change. `/implement` treats those tests as an agreed contract change.
- Keep `## Delivery` unchanged — same ticket, same branch.

Before publishing, reread the whole analysis once: no section contradicts another, nothing was invented beyond the session.

### 5. Publish

Follow the `/analyze-modify` operations in `docs/agents/config/issue-tracker.md`.

- **GitHub:** update the body, add a short comment summarising the revision. A `ready-to-review` issue no longer matches its delivery: replace that label with `needs-attention`. Never add `ready-for-agent`.
- **Local:** update the file. When it is in `done/`, move it back to `docs/agents/analysis/` and note the revision under `## Comments`.

Tell the user the next step is `/implement` on the same analysis, which continues on the existing branch.
