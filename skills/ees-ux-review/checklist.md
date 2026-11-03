# UX review checklist

Used by `ees-ux-reviewer`. Sources: the project's own design system first, then [WCAG 2.2](https://www.w3.org/TR/WCAG22/) level AA and [Nielsen's usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/). Severity hints: **C** = Critical, **M** = Major, **m** = Minor. **S** = checkable statically in the code, **B** = needs the browser.

## Design system consistency

1. **Reuse components** — The change uses the project's existing components (buttons, inputs, dialogs, tables, alerts) instead of a new one or raw elements styled by hand. (**M**, S)
2. **Tokens, not literals** — Colours, spacing, radii, shadows and typography come from the project's tokens, theme or utility classes; no hard-coded values where a token exists. (**M**, S)
3. **Established patterns** — Forms, validation messages, empty/loading/error states, confirmations and navigation follow the patterns already used on comparable screens. (**M**, S/B)
4. **Visual consistency** — Spacing, alignment and hierarchy match neighbouring screens; no near-miss misalignment. (**m**, B)

## Accessibility (WCAG 2.2 AA)

5. **Labels** — Every input has a programmatic, visible label; placeholder alone is not a label (1.3.1, 3.3.2). (**C**, S)
6. **Names and roles** — Icon-only buttons and custom controls have accessible names and correct roles; semantic elements (`button`, `a`, headings, landmarks) instead of clickable `div`s (4.1.2). (**M**, S)
7. **Alt text** — Informative images have alt; decorative ones are hidden from assistive tech (1.1.1). (**M**, S)
8. **Contrast** — Text ≥ 4.5:1, large text and UI components ≥ 3:1 (1.4.3, 1.4.11). (**C** far below, **M** below, B)
9. **Keyboard** — The core path works with Tab, Enter, Space and Escape; no keyboard trap; logical focus order (2.1.1, 2.1.2, 2.4.3). (**C** trap, **M** otherwise, B)
10. **Focus visible and not obscured** — Focus indicator is visible and not hidden by sticky headers or overlays (2.4.7, 2.4.11). (**C**, B)
11. **Dialogs** — Focus moves into a dialog, stays there and returns on close. (**M**, S/B)
12. **Target size** — Interactive targets at least 24×24 CSS px or sufficiently spaced (2.5.8). (**M**, B)
13. **Errors** — Errors are identified in text near the field and say how to fix them; status messages are announced (3.3.1, 3.3.3, 4.1.3). (**M**, S/B)

## Usability (Nielsen heuristics)

14. **Visibility of system status** — Slow actions show progress; completed actions confirm success. (**M**, B)
15. **Match with the real world** — Copy uses the user's words; actions describe the outcome ("Save draft", not "Submit"). (**m**, S)
16. **User control** — Cancel, back or undo exists where the user might get stuck. (**M**, B)
17. **Error prevention** — Destructive actions need a confirmation or undo; inputs constrain invalid values. (**C** unguarded delete, **M** otherwise, S/B)
18. **Recognition over recall** — The next step and the primary action are obvious without hunting. (**M**, B)
19. **Empty, loading and error states** — Each affected list or screen has them, explains the state and offers a next action. (**M**, S/B)

## Responsive

20. **Mobile layout** — At 390px content reflows; no clipped primary UI and no horizontal scroll on the happy path (`scrollWidth` ≤ viewport) (1.4.10). (**C**, B)
21. **Readable size** — Body text stays readable on mobile (about 16px). (**M**, B)

## Frontend best practices

22. **Framework idiom** — State, effects, data fetching and forms follow the framework's conventions at the version in the manifest; no deprecated APIs. (**M**, S)
23. **Rendering cost** — No obvious needless re-renders, layout thrashing or unbounded lists without virtualization or pagination on the affected screens. (**M**, S)
24. **Assets** — Images have dimensions and an appropriate format and size; no layout shift on load. (**m**, S/B)
