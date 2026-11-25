# Python rules

Index of the Python rules (`PY-*`). Each topic has its own file in this directory; see the
[directory README](python/README.md).

| Topic | IDs | File |
|---|---|---|
| Formatting and naming | `PY-STY`, `PY-NAM` | [`python/style-and-naming.md`](python/style-and-naming.md) |
| Configuration | `PY-CFG` | [`python/config.md`](python/config.md) |
| Logging and observability | `PY-LOG`, `PY-OBS` | [`python/logging-observability.md`](python/logging-observability.md) |
| Runtime (Gunicorn) | `PY-RUN` | [`python/runtime-gunicorn.md`](python/runtime-gunicorn.md) |
| Celery | `PY-CEL` | [`python/celery.md`](python/celery.md) |
| Dependencies | `PY-DEP` | [`python/dependencies.md`](python/dependencies.md) |
| Testing | `PY-TST` | [`python/testing.md`](python/testing.md) |

Rules (full text in each topic file):

| ID | Title | Level |
|---|---|---|
| [PY-LOG-001](python/logging-observability.md#py-log-001--use-the-standard-logging-configuration-and-never-log-credentials) | Use the standard logging configuration and never log credentials | MUST |
| [PY-LOG-002](python/logging-observability.md#py-log-002--use-one-log-format-with-trace-and-span-ids) | Use one log format with trace and span IDs | MUST |
| [PY-LOG-003](python/logging-observability.md#py-log-003--configure-logging-before-telemetry-and-silence-the-server-access-loggers) | Configure logging before telemetry and silence the server access loggers | MUST |
| [PY-LOG-004](python/logging-observability.md#py-log-004--include-the-authenticated-user-and-organization-in-log-lines) | Include the authenticated user and organization in log lines | MUST |
| [PY-OBS-001](python/logging-observability.md#py-obs-001--do-not-put-basehttpmiddleware-between-the-access-log-and-the-app) | Do not put `BaseHTTPMiddleware` between the access log and the app | MUST |
| [PY-OBS-002](python/logging-observability.md#py-obs-002--exclude-health-probes-and-the-metrics-route-from-the-access-log-and-traces) | Exclude health probes and the metrics route from the access log and traces | MUST |
| [PY-OBS-003](python/logging-observability.md#py-obs-003--bind-the-authenticated-user-in-an-async-dependency) | Bind the authenticated user in an async dependency | MUST |
| [PY-OBS-004](python/logging-observability.md#py-obs-004--propagate-w3c-trace-context-on-every-outbound-http-client) | Propagate W3C trace context on every outbound HTTP client | MUST |
| [PY-RUN-001](python/runtime-gunicorn.md#py-run-001--run-apis-with-gunicorn-and-gunicorn_configpy-migrate-outside-the-web-process) | Run APIs with Gunicorn and `gunicorn_config.py`; migrate outside the web process | MUST |
| [PY-RUN-002](python/runtime-gunicorn.md#py-run-002--recreate-connections-per-worker-and-close-them-on-exit) | Recreate connections per worker and close them on exit | MUST |
| [PY-RUN-003](python/runtime-gunicorn.md#py-run-003--keep-graceful_timeout-below-the-pod-termination-grace-period) | Keep `graceful_timeout` below the pod termination grace period | MUST |
| [PY-CEL-001](python/celery.md#py-cel-001--do-nothing-heavy-in-worker_process_init) | Do nothing heavy in `worker_process_init` | MUST |
| [PY-CEL-002](python/celery.md#py-cel-002--configure-acknowledgement-limits-and-recycling-on-every-celery-app) | Configure acknowledgement, limits and recycling on every Celery app | MUST |
| [PY-CEL-003](python/celery.md#py-cel-003--write-a-heartbeat-file-from-a-consumer-bootstep) | Write a heartbeat file from a consumer bootstep | MUST |
| [PY-DEP-001](python/dependencies.md#py-dep-001--keep-sqlalchemy-below-21) | Keep SQLAlchemy below 2.1 | MUST |
| [PY-DEP-002](python/dependencies.md#py-dep-002--build-images-from-the-lock-file) | Build images from the lock file | MUST |
| [PY-TST-001](python/testing.md#py-tst-001--run-pytest-with-coverage-and-junit-reports-in-ci) | Run pytest with coverage and JUnit reports in CI | MUST |
| [PY-TST-002](python/testing.md#py-tst-002--test-against-ephemeral-services-and-fixtures-never-shared-databases) | Test against ephemeral services and fixtures, never shared databases | MUST |
