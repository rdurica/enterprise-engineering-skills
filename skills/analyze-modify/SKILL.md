---
name: analyze-modify
description: >-
  Modify an existing analysis — before or after /implement — so it stays one
  consistent current state: explore the analysis, earlier decisions and code,
  name the risks the modification brings and agree them with the user, then
  rewrite the analysis in place. Use when a published analysis needs to change.
disable-model-invocation: true
model: opus
---

# Analyze modify

Take a published analysis and the user's description of what should be different, and leave behind an analysis that reads as if it had been written that way from the start. Do not write a changelog into the body — history goes only in `## Revisions`. Do not implement — that is `/implement`.

Resolve configuration per `{skills-root}/pipeline/config.md` (skills root is the parent of this skill's directory). Write prose in the resolved `language`, as `/analyze` does; if unset, use the language of the analysis being modified, without asking.

## Process

### 1. Load

Resolve the analysis number or path through the tracker — on the local tracker also look in `done/`. Ask for the modification if the user did not describe it.

An idea (label `idea`, locally a file in `ideas/`) is not an analysis: refuse and point to `/idea #N` to edit the intent or `/analyze #N` to convert it.

Decide the phase:

- **Not implemented** — the Delivery branch does not exist or has no commits past its merge-base, and the analysis carries no pipeline label. Only the document changes.
- **In progress or delivered** — the branch has commits, the issue is `in-progress`, `needs-attention` or `ready-to-review`, or the file is in `done/`. Read the branch diff against its merge-base too: committed tests and code are part of what must stay consistent.

### 2. Find inconsistencies

Walk every section — Goal, Current State, Change, Affected Areas, Architecture, API Contracts, Acceptance, Further Notes — and list what the modification contradicts, makes obsolete or leaves missing. Check it against the decisions in Further Notes of this and related analyses and, when implemented, against the committed tests and code. Delegate broad searches to the built-in `Explore` agent and keep only its conclusions.

If the modification rewrites most of Change and Acceptance or changes the goal, stop and recommend a fresh `/analyze` instead.

### 3. Agree the risks

Name each concrete risk the modification brings: a broken API contract or client compatibility, data or migration impact, committed tests or code that stop matching, a conflict with a decision in another analysis's Further Notes, scope growth. Put them to the user one at a time with `AskUserQuestion` and a recommended answer, as in the `/analyze` interview — accept, mitigate, or change the modification. Ask the open decisions the modification creates the same way. Explore instead of asking whenever the code can answer.

Do not rewrite anything until every risk is agreed or parked in FAQ.

### 4. Rewrite in place

Follow [analysis-template.md](../analyze/analysis-template.md) for every section you touch.

- Rewrite the affected sections so the whole analysis describes one current state. No "new", "changed", "originally" or strikethrough in the body.
- An accepted risk with its mitigation is a decision: put it in Further Notes with the rejected alternative, and in Architecture when it shapes the design. A conflict with a decision in another analysis is a risk to agree in step 3.
- Acceptance: changed and new items become `- [ ]`, dropped items are deleted, untouched completed items stay `- [x]`.
- Unresolved questions go to `## FAQ` under Affected Areas.
- `## Revisions`, the last section, records only modifications to work that is already implemented, as `- [ ] <YYYY-MM-DD> — <modification in one sentence>; risks accepted…; tests to change…` (tests only when already committed). `/implement` treats those tests as an agreed contract change and checks the entry `- [x]` when realized.
  - Not implemented: rewrite the analysis only; add no entry.
  - An unchecked entry exists: fold the modification into it — rewrite that entry with the new date and add no bullet.
  - Every entry is checked: add a new `- [ ]` entry.
- Keep `## Delivery` unchanged — same ticket, same branch.

Before publishing, reread the whole analysis once: no section contradicts another, nothing was invented beyond the session.

### 5. Publish

Follow the `/analyze-modify` operations in `{skills-root}/pipeline/tracker-<tracker>.md`.

- **GitHub:** update the body. Not implemented: no comment. Otherwise keep one comment per revision, headed `## Revision` (heading always English, content in the resolved `language`): add it for a new entry, or edit the comment of the unchecked entry in place instead of adding another. A `ready-to-review` issue no longer matches its delivery: replace that label with `needs-attention`.
- **Local:** update the file. When it is in `done/`, move it back to `docs/agents/analysis/`. For a revision, note it under `## Comments` as `## Revision`, updating the existing note when the entry is unchecked.

Tell the user the next step is `/implement` on the same analysis, which continues on the existing branch.
