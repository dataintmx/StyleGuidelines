# Python: configuration

Scope: `PY-CFG`.

| ID | Title | Level |
|---|---|---|
| [PY-CFG-001](#py-cfg-001--read-the-environment-only-in-a-cached-basesettings-class) | Read the environment only in a cached `BaseSettings` class | MUST |
| [PY-CFG-002](#py-cfg-002--fail-at-startup-when-a-required-value-is-missing) | Fail at startup when a required value is missing | MUST |

### PY-CFG-001 — Read the environment only in a cached `BaseSettings` class

- **Level:** MUST
- **Applies to:** Python services and workers
- **Enforced by:** code review; search for `os.getenv` and `os.environ` outside the settings module (the Gunicorn config, which runs before the application, is the exception)
- **Why:** one typed class is the only place that knows the names, types and defaults of the environment, so values are validated once and tests override them in one spot. Caching avoids re-parsing the environment on every call.
- **Source:** Internal architecture contracts.

Correct:
```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    redis_url: str
    request_timeout_seconds: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Incorrect:
```python
import os

database_url = os.getenv("DATABASE_URL")
timeout = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "30"))
```

### PY-CFG-002 — Fail at startup when a required value is missing

- **Level:** MUST
- **Applies to:** Python services and workers
- **Enforced by:** CI smoke test that imports the application; code review
- **Why:** a required field without a default makes pydantic raise a validation error when the settings are built, so the process stops at startup instead of failing later on the first request that needs the value. Defaults are only for values that are safe in every environment.
- **Source:** Internal architecture contracts.

Correct:
```python
class Settings(BaseSettings):
    database_url: str
    redis_url: str
```

Incorrect:
```python
class Settings(BaseSettings):
    database_url: str = ""
    redis_url: str | None = None
```
