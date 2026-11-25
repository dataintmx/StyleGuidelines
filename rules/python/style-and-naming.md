# Python: formatting and naming

Scope: `PY-STY`, `PY-NAM`.

| ID | Title | Level |
|---|---|---|
| [PY-STY-001](#py-sty-001--format-and-sort-imports-with-ruff-at-100-columns) | Format and sort imports with Ruff at 100 columns | MUST |
| [PY-STY-002](#py-sty-002--enable-the-minimum-ruff-rule-set) | Enable the minimum Ruff rule set | SHOULD |
| [PY-NAM-001](#py-nam-001--use-snake_case-pascalcase-and-upper_snake_case) | Use `snake_case`, `PascalCase` and `UPPER_SNAKE_CASE` | MUST |

### PY-STY-001 — Format and sort imports with Ruff at 100 columns

- **Level:** MUST
- **Applies to:** all Python repos
- **Enforced by:** `ruff format --check .`; `ruff check --select I .`
- **Why:** one formatter and one import order remove style noise from reviews. Ruff replaces separate formatter and import-sorting tools and reads a single configuration in `pyproject.toml`.
- **Source:** Internal code style standard.

Correct:
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["I"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Incorrect:
```toml
[tool.ruff]
line-length = 79
```

### PY-STY-002 — Enable the minimum Ruff rule set

- **Level:** SHOULD
- **Applies to:** all Python repos
- **Enforced by:** `ruff check .`
- **Why:** pycodestyle, pyflakes, import order, bugbear, pyupgrade, bandit and async checks catch the defects that most often reach production. `S101` (use of `assert`) is ignored in tests, where `assert` is the idiom. Teams may add rules; they should not drop these without a justified exception.
- **Source:** Internal code style standard.

Correct:
```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "S", "ASYNC"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]
```

Incorrect:
```toml
[tool.ruff.lint]
select = ["E", "F"]
```

### PY-NAM-001 — Use `snake_case`, `PascalCase` and `UPPER_SNAKE_CASE`

- **Level:** MUST
- **Applies to:** all Python repos
- **Enforced by:** `ruff N` (pep8-naming); code review
- **Why:** PEP 8 names let readers tell modules, functions, classes and constants apart at a glance. Modules, functions and variables use `snake_case`, classes use `PascalCase` and constants use `UPPER_SNAKE_CASE`.
- **Source:** PEP 8.

Correct:
```python
MAX_PAGE_SIZE = 100


class EventRepository:
    def list_events(self, page_size: int = MAX_PAGE_SIZE) -> list[Event]: ...
```

Incorrect:
```python
maxPageSize = 100


class event_repository:
    def listEvents(self, pageSize: int = maxPageSize) -> list[Event]: ...
```
