---
name: ees-discuss
description: >-
  Open-ended discussion of a question or idea: explore the context, lay out
  the possible approaches with trade-offs and talk them through. Use when the
  user wants to weigh options, compare approaches or think a design question
  through without asking for a change yet ("what are our options for…",
  "should we…"). Changes no project code and creates no tickets or
  deliverables.
argument-hint: "[topic]"
model: opus
---

# Discuss

Topic: $ARGUMENTS

A conversation, not a pipeline. Do not change project code, create tickets or write deliverables. The only files you write are throwaway experiments in the scratchpad (step 3).

Be concise and to the point: short answers, no preamble, no restating the question, no padding. Say what matters and stop; the user asks for more when they want it.

Keep what you verified (code, docs, sources, a run) apart from what you assume or estimate, and label the latter.

1. **Understand.** If the topic is unclear, or the right answer depends on the goal or constraints you do not know, ask one short question. Otherwise go straight on.
2. **Explore.** Read what decides the question: relevant code, docs, the web when it is about tools or practices. Delegate broad searches to `Explore`. Say in a line or two what you found and what is uncertain.
3. **Experiment** when it settles a point faster than reasoning: a calculation, a benchmark, how a library or command behaves. Write a small throwaway script in the scratchpad, run it and report the result, not the script. Never touch the project for this.
4. **Options.** Consider more ideas privately than you show, drop the weak ones and lay out 2–4 genuinely different approaches; no filler options. For each, a few lines: how it works, what it costs, when it wins. Include "do nothing" when it is realistic. End with your recommendation and why.
5. **Discuss.** Follow the user's lead: go deeper into one option, challenge assumptions, combine approaches, revisit. Disagree when you have reason to. No fixed number of rounds.
6. **Close** when the user decides or stops. State the conclusion in a few lines and, if it leads to a change, suggest the next step (`/ees-analyze`, a direct edit, nothing).
