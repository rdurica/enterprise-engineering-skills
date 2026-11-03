---
name: ees-pipeline
description: Shared configuration, delivery and tracker reference for the pipeline skills; not invoked directly.
user-invocable: false
disable-model-invocation: true
---

# Pipeline

Shared reference read by the pipeline skills; there is nothing to run. Files live next to this one at `{skills-root}/ees-pipeline/`.

- [config.md](./config.md) — settings (`language`), resolution order, tracker and monorepo detection, file format.
- [delivery.md](./delivery.md) — branch, push, CI and PR handling; read only by the main session at the start of `/ees-implement` and at the end of `/ees-verify`.
- [tracker-github.md](./tracker-github.md) — issue operations when the resolved `tracker` is `github`.
- [tracker-local.md](./tracker-local.md) — file operations when the resolved `tracker` is `local`.
