# Python: Celery

Scope: `PY-CEL`.

| ID | Title | Level |
|---|---|---|
| [PY-CEL-001](#py-cel-001--do-nothing-heavy-in-worker_process_init) | Do nothing heavy in `worker_process_init` | MUST |
| [PY-CEL-002](#py-cel-002--configure-acknowledgement-limits-and-recycling-on-every-celery-app) | Configure acknowledgement, limits and recycling on every Celery app | MUST |
| [PY-CEL-003](#py-cel-003--write-a-heartbeat-file-from-a-consumer-bootstep) | Write a heartbeat file from a consumer bootstep | MUST |

### PY-CEL-001 — Do nothing heavy in `worker_process_init`

- **Level:** MUST
- **Applies to:** Celery workers (prefork)
- **Enforced by:** code review; startup timing in CI smoke test
- **Why:** importing OpenTelemetry instrumentors and an LLM SDK inside `worker_process_init` made each child take 9–10 s at 0.5 CPU; Celery waits 4 s (`worker_proc_alive_timeout`), kills the child and respawns it in a loop. Heavy imports run once in the parent before the fork; the child only creates connections, clients and the `TracerProvider`.
- **Source:** Internal runtime standard; internal incident, 2026.

Correct:
```python
preload_instrumented_libraries()
app.conf.worker_proc_alive_timeout = 30


@worker_process_init.connect
def init_worker_process(**kwargs):
    database.reinitialize()
    setup_telemetry(service_name="orders-celery")
```

Incorrect:
```python
@worker_process_init.connect
def init_worker_process(**kwargs):
    from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
    import openai
    OpenAIInstrumentor().instrument()
    database.reinitialize()
```

### PY-CEL-002 — Configure acknowledgement, limits and recycling on every Celery app

- **Level:** MUST
- **Applies to:** Celery workers
- **Enforced by:** `celery inspect conf` check after deploy; code review
- **Why:** without `acks_late` a task is lost when the pod restarts; without time limits a task can run forever; without recycling, memory leaks accumulate.
- **Source:** Internal runtime standard.

Correct:
```python
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_time_limit = 300
app.conf.task_soft_time_limit = 240
```
```dockerfile
CMD ["celery", "-A", "src.celery.app", "worker", "--concurrency=2", "--max-tasks-per-child=50", "--max-memory-per-child=200000", "-Q", "orders_tasks"]
```

Incorrect:
```python
app.conf.task_acks_late = False
```
```dockerfile
CMD ["celery", "-A", "src.celery.app", "worker"]
```

### PY-CEL-003 — Write a heartbeat file from a consumer bootstep

- **Level:** MUST
- **Applies to:** Celery workers
- **Enforced by:** code review; liveness probe in `TF-K8S-002`
- **Why:** Kubernetes ignores the Docker `HEALTHCHECK`, so a worker needs a signal the cluster can read. The bootstep belongs to the consumer, not the worker: Celery restarts the consumer on every broker reconnection and any timer registered on the worker is lost, so the heartbeat never came back after a broker outage. The timer shares the event loop that consumes tasks, so a hung worker or a lost broker makes the file age; tasks run in child processes, so a long task does not stop it.
- **Source:** Internal runtime standard.

Correct:
```python
HEARTBEAT_FILE = Path("/tmp/celery_worker_heartbeat")
HEARTBEAT_INTERVAL_SECONDS = 10.0


class HeartbeatFile(bootsteps.StartStopStep):
    requires = {"celery.worker.consumer.connection:Connection"}

    def start(self, parent):
        self.touch()
        self.timer = parent.timer.call_repeatedly(HEARTBEAT_INTERVAL_SECONDS, self.touch, priority=10)

    def stop(self, parent):
        self.timer.cancel()

    def shutdown(self, parent):
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def touch(self):
        HEARTBEAT_FILE.touch()


app.steps["consumer"].add(HeartbeatFile)
```

Incorrect:
```python
app.steps["worker"].add(HeartbeatFile)
```
```dockerfile
HEALTHCHECK CMD celery -A src.celery.app inspect ping
```
