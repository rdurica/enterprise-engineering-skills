# UX review checklist

Use during `/ux-review`. Severity hints: **C** = Critical, **M** = Major, **m** = Minor.

## Navigation & flow

1. **Next step obvious** — Can a first-time user tell what to do next without hunting? (**M**)
2. **Primary action visible** — The main CTA is visually dominant and not buried. (**M**)
3. **Way back** — Escape, cancel, or back exists where the user might get stuck. (**M**)
4. **Context** — User knows where they are (title, breadcrumb, or equivalent). (**m**)

## Visual hierarchy

5. **Scanability** — Headings and grouping make the page scannable in seconds. (**M**)
6. **Spacing consistency** — Related items share spacing; unrelated groups are separated. (**m**)
7. **Alignment** — Columns/edges line up; no near-miss 1–6px misalignment. (**m**)
8. **No AI-slop defaults** — Avoid generic Inter/Roboto-only stacks, purple-on-white gradients, badge clutter on heroes. (**m**)

## Content & forms

9. **Real labels** — Inputs have visible labels (not placeholder-only). (**C**)
10. **Validation feedback** — Errors say what failed and how to fix; shown near the field. (**M**)
11. **Button copy** — Actions describe the outcome (“Save draft”), not vague “Submit”/“OK” where context is unclear. (**m**)
12. **Dangerous actions** — Delete/override needs confirm or undo. (**C**)

## States

13. **Loading** — Slow actions show progress or skeleton; no silent freeze. (**M**)
14. **Empty** — Empty lists/screens explain state and offer a next action. (**M**)
15. **Error** — Failures are readable; retry or recovery exists when useful. (**M**)
16. **Success** — Completing a task gives clear confirmation. (**m**)

## Accessibility

17. **Contrast** — Text meets WCAG 2.2 AA (~4.5:1 normal, ~3:1 large). (**C**)
18. **Tap targets** — Interactive controls ≥ 44×44 CSS px on mobile. (**M**)
19. **Focus visible** — Keyboard focus ring is visible on interactive elements. (**C**)
20. **Keyboard** — Core path works without a pointer (tab, enter, escape). (**M**)
21. **Alt / name** — Informative images have alt; icon-only buttons have accessible names. (**M**)

## Responsive

22. **Mobile layout** — At ~390px width, content reflows; no clipped primary UI. (**C**)
23. **No horizontal scroll** — `scrollWidth` does not exceed viewport for the happy path. (**C**)
24. **Touch-friendly** — Controls are spaced enough to tap without mis-hits. (**M**)
25. **Readable size** — Body text remains readable on mobile (roughly ≥ 16px). (**M**)
