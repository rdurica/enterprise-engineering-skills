# When to Mock

Mock at **system boundaries** only: external APIs, time, file system (sometimes).

Do not mock your own modules or internal collaborators.

Prefer dependency injection at boundaries. Prefer specific SDK-style functions over one generic fetcher with conditional mocks.
