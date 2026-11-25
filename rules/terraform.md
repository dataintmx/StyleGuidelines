# Terraform rules

Scope: `TF-*`. Modules, Kubernetes resources (probes, lifecycle), secrets and formatting.

| ID | Title | Level |
|---|---|---|
| [TF-K8S-001](#tf-k8s-001--http-deployments-declare-startup-readiness-and-liveness-probes) | HTTP deployments declare startup, readiness and liveness probes | MUST |
| [TF-K8S-002](#tf-k8s-002--probe-celery-workers-with-the-heartbeat-file) | Probe Celery workers with the heartbeat file | MUST |
| [TF-K8S-003](#tf-k8s-003--roll-out-with-max_unavailable--0-and-max_surge--1) | Roll out with `max_unavailable = 0` and `max_surge = 1` | MUST |

### TF-K8S-001 — HTTP deployments declare startup, readiness and liveness probes

- **Level:** MUST
- **Applies to:** Terraform modules with HTTP deployments
- **Enforced by:** code review; post-deploy verification (`Ready` and no restarts)
- **Why:** without readiness a pod that crashes on start is marked ready and replaces the healthy one. A tolerant liveness (≈30 s) avoids restarting a service whose workers are only recycling: with a 3 s period and 1 s timeout, a service restarted when both workers reached `max_requests` at once and stopped answering for about 7 s.
- **Source:** Internal runtime standard; internal incident, 2026.

Correct:
```hcl
startup_probe {
  period_seconds    = 2
  timeout_seconds   = 3
  failure_threshold = 60
  http_get {
    path = "/"
    port = 8000
  }
}
readiness_probe {
  period_seconds = 3
  http_get {
    path = "/"
    port = 8000
  }
}
liveness_probe {
  period_seconds    = 10
  timeout_seconds   = 3
  failure_threshold = 3
  http_get {
    path = "/"
    port = 8000
  }
}
```

Incorrect:
```hcl
liveness_probe {
  initial_delay_seconds = 30
  period_seconds        = 3
  timeout_seconds       = 1
  http_get {
    path = "/"
    port = 8000
  }
}
```

### TF-K8S-002 — Probe Celery workers with the heartbeat file

- **Level:** MUST
- **Applies to:** Terraform modules with Celery worker deployments
- **Enforced by:** code review; post-deploy verification (`Ready` and no restarts)
- **Why:** Kubernetes does not use the Docker `HEALTHCHECK`. The liveness probe checks that the file written by `PY-CEL-003` is recent. Ship the image with the heartbeat first and the probe after: without the file Kubernetes restarts the worker in a loop. A broker outage longer than about 3–4 minutes restarts the workers. Beat has no probe, and workers scaled to zero by KEDA have none while no pods exist. `celery inspect ping` is not used: each run imports Celery and the app, costs 3–5 s of CPU and pushed workers to scale up.
- **Source:** Internal runtime standard.

Correct:
```hcl
liveness_probe {
  initial_delay_seconds = 60
  period_seconds        = 30
  timeout_seconds       = 5
  failure_threshold     = 3
  exec {
    command = ["sh", "-c", "test $(( $(date +%s) - $(stat -c %Y /tmp/celery_worker_heartbeat) )) -lt 120"]
  }
}
```

Incorrect:
```hcl
liveness_probe {
  period_seconds = 30
  exec {
    command = ["celery", "-A", "src.celery.app", "inspect", "ping"]
  }
}
```

### TF-K8S-003 — Roll out with `max_unavailable = 0` and `max_surge = 1`

- **Level:** MUST
- **Applies to:** Terraform modules with HTTP deployments
- **Enforced by:** code review
- **Why:** the replacement pod must be ready before the old one leaves, so a rollout does not reduce serving capacity.
- **Source:** Internal runtime standard.

Correct:
```hcl
strategy {
  type = "RollingUpdate"
  rolling_update {
    max_unavailable = "0"
    max_surge       = "1"
  }
}
```

Incorrect:
```hcl
strategy {
  type = "Recreate"
}
```
