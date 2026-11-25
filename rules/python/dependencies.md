# Python: dependencies

Scope: `PY-DEP`.

| ID | Title | Level |
|---|---|---|
| [PY-DEP-001](#py-dep-001--keep-sqlalchemy-below-21) | Keep SQLAlchemy below 2.1 | MUST |
| [PY-DEP-002](#py-dep-002--build-images-from-the-lock-file) | Build images from the lock file | MUST |

### PY-DEP-001 — Keep SQLAlchemy below 2.1

- **Level:** MUST
- **Applies to:** Python services using SQLAlchemy
- **Enforced by:** version constraint in `pyproject.toml`; Dependabot ignore rule
- **Why:** `opentelemetry-instrumentation-sqlalchemy` only instruments SQLAlchemy `< 2.1.0` (it silently skips 2.1, so queries lose their spans); 2.1 also changed the default `postgresql://` driver to psycopg v3 and stopped installing `greenlet`, which turned CI red in one service and took another down in a development environment. Lift the rule when the instrumentation supports 2.1.
- **Source:** Internal observability standard; internal CI/CD standard.

Correct:
```toml
[tool.poetry.dependencies]
sqlalchemy = ">=2.0,<2.1"
```

Incorrect:
```toml
[tool.poetry.dependencies]
sqlalchemy = "*"
```

### PY-DEP-002 — Build images from the lock file

- **Level:** MUST
- **Applies to:** Dockerfiles and CI workflows of Python repos
- **Enforced by:** `grep -R "poetry update" .github Dockerfile* *.Dockerfile` must return nothing; CI build stage
- **Why:** `poetry update` builds the latest versions allowed by the ranges, not what Dependabot updated and tests validated.
- **Source:** Internal CI/CD standard.

Correct:
```dockerfile
FROM python:3.13 AS requirements-stage
RUN poetry export --only main --without-hashes -o /tmp/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
```

Incorrect:
```dockerfile
RUN poetry update && poetry export -o /tmp/requirements.txt
```
