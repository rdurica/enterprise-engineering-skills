---
name: tdd
description: >-
  Test-driven development with red-green-refactor vertical slices. Use when
  building features or fixes test-first, or when implement delegates testing.
  For PHP backend, routes HTTP work to integration-tests and handler/domain
  work to PHPUnit unit tests.
---

# Test-Driven Development

## Philosophy

Tests verify behaviour through **public interfaces**, not implementation details. Good tests survive refactors; bad tests break when you rename an internal function.

See [tests.md](tests.md), [mocking.md](mocking.md), [refactoring.md](refactoring.md).

## Anti-pattern: horizontal slices

Do NOT write all tests first, then all code.

```
WRONG:  RED test1..5  →  GREEN impl1..5
RIGHT:  RED test1 → GREEN impl1 → RED test2 → GREEN impl2 → …
```

## Workflow

### 1. Planning

Read `CONTEXT.md` and relevant ADRs if they exist.

Before writing code:

- Confirm interface changes and behaviours to test (prioritized)
- List behaviours, not implementation steps
- Get user approval on the plan

### 2. Tracer bullet

```
RED:   One test for one behaviour → fails
GREEN: Minimal code to pass → passes
```

### 3. Incremental loop

One test at a time. Only enough code to pass the current test. No speculative features.

### 4. Refactor

After all tests pass, apply [refactoring.md](refactoring.md). **Never refactor while RED.**

## Choosing the test layer (PHP backend)

| Seam | Skill / approach |
|------|------------------|
| HTTP API endpoint | `integration-tests` — full-stack contract via KernelBrowser |
| Command/Query handler, domain service, value object | PHPUnit **unit tests** — read paths and conventions from target repo `AGENTS.md` |
| Both in one slice | TDD cycle at the highest seam first (usually HTTP); unit tests only where HTTP cannot reach the logic cleanly |

Run one test file per red-green cycle. Project-specific PHPUnit commands live in `AGENTS.md`.

## Checklist per cycle

- [ ] Test describes behaviour, not implementation
- [ ] Test uses public interface only
- [ ] Code is minimal for this test
- [ ] No speculative features added
