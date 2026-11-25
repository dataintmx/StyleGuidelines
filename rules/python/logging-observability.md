# Python: logging and observability

Scope: `PY-LOG`, `PY-OBS`.

| ID | Title | Level |
|---|---|---|
| [PY-LOG-001](#py-log-001--use-the-standard-logging-configuration-and-never-log-credentials) | Use the standard logging configuration and never log credentials | MUST |
| [PY-LOG-002](#py-log-002--use-one-log-format-with-trace-and-span-ids) | Use one log format with trace and span IDs | MUST |
| [PY-LOG-003](#py-log-003--configure-logging-before-telemetry-and-silence-the-server-access-loggers) | Configure logging before telemetry and silence the server access loggers | MUST |
| [PY-LOG-004](#py-log-004--include-the-authenticated-user-and-organization-in-log-lines) | Include the authenticated user and organization in log lines | MUST |
| [PY-OBS-001](#py-obs-001--do-not-put-basehttpmiddleware-between-the-access-log-and-the-app) | Do not put `BaseHTTPMiddleware` between the access log and the app | MUST |
| [PY-OBS-002](#py-obs-002--exclude-health-probes-and-the-metrics-route-from-the-access-log-and-traces) | Exclude health probes and the metrics route from the access log and traces | MUST |
| [PY-OBS-003](#py-obs-003--bind-the-authenticated-user-in-an-async-dependency) | Bind the authenticated user in an async dependency | MUST |
| [PY-OBS-004](#py-obs-004--propagate-w3c-trace-context-on-every-outbound-http-client) | Propagate W3C trace context on every outbound HTTP client | MUST |
| [PY-OBS-005](#py-obs-005--run-prometheus-metrics-in-multiprocess-mode-with-several-workers) | Run Prometheus metrics in multiprocess mode with several workers | MUST |
| [PY-OBS-006](#py-obs-006--label-metrics-by-route-template-not-by-url) | Label metrics by route template, not by URL | MUST |

### PY-LOG-001 — Use the standard logging configuration and never log credentials

- **Level:** MUST
- **Applies to:** all Python services and workers
- **Enforced by:** unit tests of formatter and access log; code review
- **Why:** one format with `trace_id`/`span_id` for every logger (root, gunicorn, uvicorn, `py.warnings`) lets the log and trace backends correlate; tokens in URLs and logs leak sessions.
- **Source:** Internal observability standard.

Correct:
```python
setup_logging()
setup_telemetry(service_name="billing-api")
logger = logging.getLogger(__name__)
logger.info("Session created for %s", organization)
```
```dockerfile
COPY logging_config.yaml /logging_config.yaml
CMD ["gunicorn", "src.asgi:app", "-c", "/gunicorn_config.py"]
```

Incorrect:
```python
setup_telemetry(service_name="billing-api")
print(f"login with token {access_token}")
logger.info("Session data %s", session.model_dump())
```
```dockerfile
CMD ["gunicorn", "src.asgi:app", "--log-config", "log.ini"]
```

### PY-LOG-002 — Use one log format with trace and span IDs

- **Level:** MUST
- **Applies to:** all Python services and workers
- **Enforced by:** unit test of the formatter; code review
- **Why:** a single line layout, with `trace_id` and `span_id` filled by the OpenTelemetry logging instrumentation, lets any log line be matched to its trace. The formatter is declared once in `logging_config.yaml` and applies to root, `gunicorn.error`, `uvicorn`, `uvicorn.error` and `py.warnings`.
- **Source:** Internal observability standard.

Correct:
```yaml
formatters:
  otel:
    (): src.configs.logger.OTelFormatter
    format: "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
```

Incorrect:
```yaml
formatters:
  plain:
    format: "%(levelname)s %(message)s"
```

### PY-LOG-003 — Configure logging before telemetry and silence the server access loggers

- **Level:** MUST
- **Applies to:** all Python services and workers
- **Enforced by:** unit tests of the logging setup; code review
- **Why:** `setup_logging()` runs before `setup_telemetry(...)` so every logger already has the standard formatter. `uvicorn.access` and `gunicorn.access` stay at WARNING because the application emits its own access log inside the span, and `logging.captureWarnings(True)` routes Python warnings through the same format.
- **Source:** Internal observability standard.

Correct:
```python
logging.captureWarnings(True)
setup_logging()
setup_telemetry(service_name="billing-api")
```
```yaml
loggers:
  uvicorn.access:
    level: WARNING
  gunicorn.access:
    level: WARNING
```

Incorrect:
```python
setup_telemetry(service_name="billing-api")
setup_logging()
```
```yaml
loggers:
  uvicorn.access:
    level: INFO
```

### PY-LOG-004 — Include the authenticated user and organization in log lines

- **Level:** MUST
- **Applies to:** services that authenticate users from a session
- **Enforced by:** unit tests of the formatter with and without a user; code review
- **Why:** investigating an error needs to know who triggered it. Two fields are appended to the OpenTelemetry block; the formatter reads them from the request context and prints `-` when there is no user (probes, workers, startup, unauthenticated requests). The organization is quoted because it can contain spaces. The full session is never logged at INFO; it goes to DEBUG and the level is raised temporarily to investigate a 403.
- **Source:** Internal observability standard.

Correct:
```yaml
formatters:
  otel:
    (): src.configs.logger.OTelFormatter
    format: "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s enduser.id=%(enduserId)s dataint.organization=%(enduserOrganization)s] - %(message)s"
```
```python
logger.debug("Session data %s", session.model_dump())
```

Incorrect:
```python
logger.info("Session data %s", session.model_dump())
```

### PY-OBS-001 — Do not put `BaseHTTPMiddleware` between the access log and the app

- **Level:** MUST
- **Applies to:** FastAPI/Starlette services
- **Enforced by:** `ruff` custom check or grep in CI (`BaseHTTPMiddleware`, `@app.middleware("http")`); unit test of the access log
- **Why:** it runs the rest of the request in another task with a copy of the context; the user bound by the authentication dependency does not propagate back, so the access log and the error log show `enduser.id=-` even though the span has the user. Use pure ASGI middlewares.
- **Source:** Internal observability standard.

Correct:
```python
class AccessLogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)


app.add_middleware(AccessLogMiddleware)
```

Incorrect:
```python
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    return await call_next(request)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await call_next(request)
```

### PY-OBS-002 — Exclude health probes and the metrics route from the access log and traces

- **Level:** MUST
- **Applies to:** FastAPI/Starlette services
- **Enforced by:** unit test: a health request produces no trace and no log line; a normal request produces one SERVER span and an access log line with the span's `trace_id` and no query string
- **Why:** probes and metric scrapes run every few seconds and would drown real traffic in logs and traces. The access log is a pure ASGI middleware inside the span and prints the client address, `"METHOD path"`, status and duration, never the query string.
- **Source:** Internal observability standard.

Correct:
```python
EXCLUDED_PATHS = frozenset({"/", "/metrics"})


class AccessLogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["path"] in EXCLUDED_PATHS:
            await self.app(scope, receive, send)
            return
        await self.log_and_forward(scope, receive, send)
```

Incorrect:
```python
class AccessLogMiddleware:
    async def __call__(self, scope, receive, send):
        logger.info("%s %s?%s", scope["method"], scope["path"], scope["query_string"])
        await self.app(scope, receive, send)
```

### PY-OBS-003 — Bind the authenticated user in an async dependency

- **Level:** MUST
- **Applies to:** FastAPI services that authenticate users from a session
- **Enforced by:** unit tests of the authentication dependency, isolation between requests (`contextvars.copy_context()`) and span attributes (`InMemorySpanExporter`)
- **Why:** `bind_enduser(session)` stores the email and organization in `contextvars` and sets them on the current span (`enduser.id`, `dataint.organization`). A synchronous dependency runs in the threadpool and whatever it puts in a `contextvar` does not leave that thread, so the dependency that reads the session, and the WebSocket one, must be `async`.
- **Source:** Internal observability standard.

Correct:
```python
async def current_session(request: Request) -> Session:
    session = await read_session(request)
    bind_enduser(session)
    return session
```

Incorrect:
```python
def current_session(request: Request) -> Session:
    session = read_session_sync(request)
    bind_enduser(session)
    return session
```

### PY-OBS-004 — Propagate W3C trace context on every outbound HTTP client

- **Level:** MUST
- **Applies to:** all Python services and workers
- **Enforced by:** unit test that an outbound call carries `traceparent`; code review
- **Why:** the propagator is W3C `tracecontext`. `httpx` and `requests` need separate instrumentors, so a service that uses both instruments both; otherwise calls made with the uninstrumented client break the trace.
- **Source:** Internal observability standard.

Correct:
```python
set_global_textmap(TraceContextTextMapPropagator())
HTTPXClientInstrumentor().instrument()
RequestsInstrumentor().instrument()
```

Incorrect:
```python
HTTPXClientInstrumentor().instrument()
response = requests.get("https://api.example.com/v1/items", timeout=10)
```

### PY-OBS-005 — Run Prometheus metrics in multiprocess mode with several workers

- **Level:** MUST
- **Applies to:** services that expose Prometheus metrics and run more than one worker
- **Enforced by:** code review; a scrape of `/metrics` under load that reflects the traffic of every worker
- **Why:** each Gunicorn worker keeps its own in-memory registry, so a scrape would see only the worker that answered. With `PROMETHEUS_MULTIPROC_DIR` set, workers write to shared files and the `/metrics` route aggregates them. The directory is emptied at startup and `child_exit` marks dead workers so their gauges do not linger.
- **Source:** Internal observability standard.

Correct:
```python
metrics_dir = os.environ.get("PROMETHEUS_MULTIPROC_DIR")
if metrics_dir:
    shutil.rmtree(metrics_dir, ignore_errors=True)
    os.makedirs(metrics_dir)


def child_exit(server, worker):
    if metrics_dir:
        multiprocess.mark_process_dead(worker.pid)
```
```python
def metrics_registry() -> CollectorRegistry:
    if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
    else:
        registry = REGISTRY
    return registry
```

Incorrect:
```python
@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
```
with `workers = 2` and no `PROMETHEUS_MULTIPROC_DIR`.

### PY-OBS-006 — Label metrics by route template, not by URL

- **Level:** MUST
- **Applies to:** all Python services that record request metrics
- **Enforced by:** code review; check that the number of distinct `handler` label values stays bounded
- **Why:** a label with the concrete URL creates one time series per identifier, which exhausts memory in the metrics backend. The route template (`/events/{event_id}`) has a fixed number of values.
- **Source:** Internal observability standard.

Correct:
```python
Instrumentator(should_group_untemplated=True).instrument(app)
```
```python
REQUESTS = Counter("http_requests_total", "Requests", ["method", "route"])
REQUESTS.labels(request.method, request.scope["route"].path).inc()
```

Incorrect:
```python
REQUESTS = Counter("http_requests_total", "Requests", ["method", "path"])
REQUESTS.labels(request.method, request.url.path).inc()
```
