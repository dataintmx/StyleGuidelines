# General rules

Scope: `GEN-*`. Rules that apply to every language: comments, configuration, names, secrets, files and
internationalization. Workflow rules (branches, commits, pull requests, versioning) are pointer rules such as
`GEN-GIT-001: follow CONTRIBUTING.md §2–5`; their text lives in the organization-wide `CONTRIBUTING.md`.

| ID | Title | Level |
|---|---|---|
| [GEN-CMT-001](#gen-cmt-001--do-not-write-comments-in-code) | Do not write comments in code | MUST |
| [GEN-CFG-001](#gen-cfg-001--keep-limits-timeouts-and-origins-in-a-dedicated-config-module) | Keep limits, timeouts and origins in a dedicated config module | MUST |

### GEN-CMT-001 — Do not write comments in code

- **Level:** MUST
- **Applies to:** all languages, all repositories
- **Enforced by:** `scripts/check-no-comments.py`; code review
- **Why:** comments rot; names, types, small functions and tests carry the meaning. The reason for a change goes in the commit and PR, design in the design docs.
- **Source:** Internal engineering decision, 2026.

Allowed only as tool directives, with the narrowest scope: `# noqa: E501`, `# type: ignore[attr-defined]`, `// eslint-disable-next-line no-console`, shebangs, and headers a tool requires.

Correct:
```python
SESSION_TTL_SECONDS = 900


def seconds_until(expires_at: datetime, now: datetime) -> int:
    return int((expires_at - now).total_seconds())
```

Incorrect:
```python
def seconds_until(expires_at, now):
    # .seconds ignores days
    return (expires_at - now).seconds
```
Fix the code (`total_seconds()`) and put the reason in the commit message.

### GEN-CFG-001 — Keep limits, timeouts and origins in a dedicated config module

- **Level:** MUST
- **Applies to:** Python services and workers, TypeScript apps
- **Enforced by:** code review; `ruff PLR2004` (magic values) as a guard
- **Why:** values scattered in code cannot be audited or changed per environment. An HTTP client had no timeout until connect and read timeouts were added to the shared configuration module; OpenTelemetry paths in a web app live in a single `config/otel.ts`.
- **Source:** Internal architecture contracts; internal observability standard.

Correct, in `src/configs/http.py`:
```python
API_CONNECT_TIMEOUT_SECONDS = 5
API_READ_TIMEOUT_SECONDS = 120
ALLOWED_ORIGINS = ("https://app.example.com",)
```

Correct, in `src/clients/catalog.py`:
```python
from src.configs.http import API_CONNECT_TIMEOUT_SECONDS, API_READ_TIMEOUT_SECONDS

timeout = httpx.Timeout(API_READ_TIMEOUT_SECONDS, connect=API_CONNECT_TIMEOUT_SECONDS)
```

Incorrect:
```python
response = httpx.get("https://api.example.com/v1/event", timeout=120)
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"])
```
