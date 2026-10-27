---
name: analyze
description: >-
  Structured alignment interview on a change, then a published analysis —
  current state, change, affected areas, architecture, API contracts,
  acceptance. Use when starting a feature, stress-testing a design, or when
  the user wants to create, write, or publish an analysis.
disable-model-invocation: true
model: opus
---

# Analyze

Reach shared understanding through an interview, then synthesize it and the codebase into a published analysis. Do not implement here — that is `/implement`.

Write for a human who was not in the interview. They should read the analysis once and be able to explain the change without opening the diff.

Resolve configuration per `{skills-root}/pipeline/config.md` (skills root is the parent of this skill's directory; no setup step is needed) and tracker operations per `{skills-root}/pipeline/tracker-<tracker>.md`. For a simple bug (see "Bug fast-path" in `{skills-root}/pipeline/config.md`) skip Phase A and write the shorter bug variant with `Kind: bug`.

Take `language` (`en` | `cs`) from the resolved config; if unset, use the language of the conversation and do not ask. Everything you write in prose goes in that language: the title, every section body, and the comments on the ticket. Section headings stay English, and so do identifiers, paths, HTTP contracts and commit messages. Branch slugs are always ASCII and hyphenated, transliterated when the title is not.

## Idea conversion

`/analyze #N` on an idea (label `idea`, locally a file in `ideas/`) converts it. First check its `Depends on` per the tracker doc: a dependency is satisfied when the GitHub issue is closed, locally when the file is in `done/`. For each unsatisfied one show number, title and state, explain that the analysis would be written against a state that is still going to change, and ask with `AskUserQuestion` whether to continue anyway (recommend waiting). On refusal stop; the issue or file stays unchanged.

Phase A then runs in full with the idea's Goal and Change as the starting point (Change may be refined). Phase B rewrites the same ticket instead of creating one — see "Converting an idea".

## Phase A — Align

If the conversation already settled some decisions, interview only for the gaps.

### 1. Explore

If a codebase is available, read relevant code, `AGENTS.md` and the Further Notes of related earlier analyses (active and `done/`), and respect the decisions recorded there.

If a question can be answered by exploring the codebase, explore instead of asking. Delegate broad searches across many files to the built-in `Explore` agent and keep only its conclusions; read the few files that decide a question yourself.

### 2. Interview

Use `AskUserQuestion` with a recommended option, falling back to a text question if the tool is unavailable or does not permit the request.

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

### 4. Checkpoint

List every decision the interview resolved and put each one in a bucket:

- **Further Notes** — an alternative was in play. It becomes a `## Further Notes` bullet naming the rejected alternative.
- **Obvious** — no alternative was ever in play. Nothing to record.

Further Notes is the only place decisions are recorded; do not let a decision leave the session in no bucket at all.

Show the bucketed list and ask once with `AskUserQuestion`:

- **Publish** (recommended) — continue with Phase B.
- **Refine** — return to the interview.
- **Stop without analysis** — leave the decision list in the conversation and end. Nothing is written.

Without a codebase, run steps 2–4 only — do not write local files.

## Phase B — Publish

All publish operations follow `{skills-root}/pipeline/tracker-<tracker>.md` — GitHub or local `docs/agents/analysis/`, never hardcoded `gh`.

Start the analysis with a `## Goal` of 1–3 sentences (why the change exists, what must hold at the end; no bug variant). Keep Current State and Change to one short paragraph of 2–4 sentences each: today's behaviour and the behaviour after the change. Affected Areas follows as a short bullet map of where the change lands, with the behaviour diagram. Put implementation details in Architecture and API Contracts. Every Mermaid diagram must highlight the affected parts in orange, as defined in the template.

Publish **even when `## FAQ` still has open questions**. The analysis has to be stored so the work can continue later. Each FAQ item names what it belongs to, and once it is answered you fold the answer into that section and delete the item. The ideal end state is no FAQ section at all.

1. Make sure the decisions are complete; explore the repo only to fill gaps Phase A left.

2. Before drafting, read [analysis-template.md](analysis-template.md) for writing rules, section structure, Acceptance examples and the shorter bug variant. Write the analysis yourself from that template — this conversation already holds the decisions, rejected alternatives and explored code. Before publishing, check the draft against the session: every decision present, nothing invented, Current State and Change 2–4 sentences each, Mermaid highlighting per the template. Then publish it. On GitHub the only label is `analysis` — create it if it does not exist, and never add `ready-for-agent`. Locally the analysis is `docs/agents/analysis/NNN-<slug>.md` with no Status line.

3. After publishing, prepend `## Delivery` — edit the issue body on GitHub, update the file locally:

```markdown
## Delivery

- Ticket: [AB#4821](https://dev.azure.com/org/project/_workitems/edit/4821)
- Kind: feature | bug | chore
- Branch: `feature/4821-group-pricing`
```

**Ticket** is the number this work is tracked under, as a clickable link whenever you have a URL. An external tracker wins — Azure DevOps, Jira, Redmine, whatever the project uses. Take the ID or link from the conversation, and ask for it when the work clearly came from a ticket but nobody named it. Without an external ticket, use the analysis's own number: on GitHub the issue itself, linked as `Ticket: [#<N>](<issue url>)`; locally the plain file number `NNN`.

**Branch** is `feature/<ticket>-<short-slug>` and reuses that same number, so branch and ticket never drift apart. The slug comes from the title: lowercase, hyphenated, ASCII, around 30 characters.

Commits and the PR keep referencing the GitHub analysis issue as `#N`, because that is the number GitHub autolinks. The external ticket travels in the `Ticket:` line.

For **bugs**, set `Kind: bug` and use the shorter bug sections.

## Converting an idea

Do not create a new ticket. Rewrite the body of the same one: title `Idea: …` becomes `Analysis: …`, label `idea` is replaced by `analysis`, `## Delivery` is kept as is including `Depends on` (Kind may be refined). Locally `mv` the file from `docs/agents/analysis/ideas/` to `docs/agents/analysis/` with the same `NNN` and slug. Operations are in `{skills-root}/pipeline/tracker-<tracker>.md`.

## Publishing

### Local tracker publish

When the active backend is Local Markdown, follow the `/analyze` operations in `{skills-root}/pipeline/tracker-local.md`:

1. Compute the next `NNN` as described there — scan `docs/agents/analysis/`, `docs/agents/analysis/ideas/` and `docs/agents/analysis/done/`, never reuse an ID.
2. Take `<slug>` from the analysis title: lowercase, hyphenated, ASCII, transliterated if needed.
3. Create `docs/agents/analysis/NNN-<slug>.md` with Kind, Delivery (branch `feature/<ticket>-<short-slug>`, where the ticket falls back to `NNN`) and the analysis body. No Status line.

Bug fast-path — a ticket with Acceptance rather than a full analysis — uses the same path and ID scan with `Kind: bug`.

### GitHub publish

When the backend is GitHub, follow the `/analyze` operations in `{skills-root}/pipeline/tracker-github.md`.

**Monorepo:** if the resolved config has a `## Monorepo` section (explicit or detected), create the analysis issue on the **container-root** repo only — `gh … -R <owner/container-repo>` from that remote. Never publish an analysis into a delivery-root repository.

After publishing, tell the user the next step is `/implement` on this analysis, once they have reviewed it.
