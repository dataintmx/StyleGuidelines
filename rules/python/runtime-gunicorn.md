# Python: runtime (Gunicorn)

Scope: `PY-RUN`.

| ID | Title | Level |
|---|---|---|
| [PY-RUN-001](#py-run-001--run-apis-with-gunicorn-and-gunicorn_configpy-migrate-outside-the-web-process) | Run APIs with Gunicorn and `gunicorn_config.py`; migrate outside the web process | MUST |
| [PY-RUN-002](#py-run-002--recreate-connections-per-worker-and-close-them-on-exit) | Recreate connections per worker and close them on exit | MUST |
| [PY-RUN-003](#py-run-003--keep-graceful_timeout-below-the-pod-termination-grace-period) | Keep `graceful_timeout` below the pod termination grace period | MUST |

### PY-RUN-001 — Run APIs with Gunicorn and `gunicorn_config.py`; migrate outside the web process

- **Level:** MUST
- **Applies to:** FastAPI services
- **Enforced by:** CI smoke test (`import src.asgi`); comparing the deployed `/gunicorn_config.py` with the template
- **Why:** a single config gives uniform workers, recycling and logging; with `preload_app = True` every socket opened at import must be recreated per worker; running Alembic at the startup of each worker causes races. Migrations run in an init container or a Job.
- **Source:** Internal runtime standard.

Correct:
```python
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 1000
max_requests_jitter = 100
timeout = 120
graceful_timeout = 30
preload_app = True
accesslog = None
bind = "0.0.0.0:8000"


def post_worker_init(worker):
    database.reinitialize()
    redis_client.reinitialize()
```

Incorrect:
```dockerfile
CMD ["uvicorn", "src.asgi:app", "--host", "0.0.0.0", "--port", "8000"]
```
```python
@app.on_event("startup")
async def run_migrations():
    command.upgrade(alembic_config, "head")
```

### PY-RUN-002 — Recreate connections per worker and close them on exit

- **Level:** MUST
- **Applies to:** FastAPI services with `preload_app = True`
- **Enforced by:** code review
- **Why:** pools and clients opened at import, before the fork, are shared between workers and fail intermittently. `post_worker_init` recreates every pool or client opened at import (SQLAlchemy/asyncpg engines, Redis, Mongo, pooled `httpx` clients); `worker_abort` and `worker_exit` close the same ones so a managed database with a connection limit is not left with dangling connections. A service that opens no network connection at import omits the hooks.
- **Source:** Internal runtime standard.

Correct:
```python
def post_worker_init(worker):
    database.reinitialize()
    redis_client.reinitialize()


def worker_abort(worker):
    database.close()
    redis_client.close()


def worker_exit(server, worker):
    database.close()
    redis_client.close()
```

Incorrect:
```python
preload_app = True
workers = 2
```
with `database` and `redis_client` created at import and no worker hooks.

### PY-RUN-003 — Keep `graceful_timeout` below the pod termination grace period

- **Level:** MUST
- **Applies to:** FastAPI services deployed on Kubernetes
- **Enforced by:** code review
- **Why:** if Gunicorn is allowed to drain longer than Kubernetes waits, the pod is killed with `SIGKILL` in the middle of in-flight requests. The standard value is `graceful_timeout = 30`.
- **Source:** Internal runtime standard.

Correct:
```python
graceful_timeout = 30
```
```hcl
termination_grace_period_seconds = 60
```

Incorrect:
```python
graceful_timeout = 120
```
```hcl
termination_grace_period_seconds = 30
```
