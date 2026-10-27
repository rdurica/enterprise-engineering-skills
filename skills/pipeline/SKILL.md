---
name: pipeline
description: Shared configuration and tracker reference for the pipeline skills; not invoked directly.
user-invocable: false
disable-model-invocation: true
---

# Pipeline

Shared reference read by the pipeline skills; there is nothing to run. Files live next to this one at `{skills-root}/pipeline/`.

- [config.md](./config.md) — settings, built-in defaults, resolution order, tracker and monorepo detection, file format.
- [tracker-github.md](./tracker-github.md) — issue operations when the resolved `tracker` is `github`.
- [tracker-local.md](./tracker-local.md) — file operations when the resolved `tracker` is `local`.
