# Terraform rules

Scope: `TF-*`. Modules, Kubernetes resources (probes, lifecycle), secrets and formatting.

| ID | Title | Level |
|---|---|---|
| [TF-K8S-001](#tf-k8s-001--http-deployments-declare-startup-readiness-and-liveness-probes) | HTTP deployments declare startup, readiness and liveness probes | MUST |
| [TF-K8S-002](#tf-k8s-002--probe-celery-workers-with-the-heartbeat-file) | Probe Celery workers with the heartbeat file | MUST |
| [TF-K8S-003](#tf-k8s-003--roll-out-with-max_unavailable--0-and-max_surge--1) | Roll out with `max_unavailable = 0` and `max_surge = 1` | MUST |
| [TF-K8S-004](#tf-k8s-004--add-a-short-prestop-wait-to-http-deployments) | Add a short `preStop` wait to HTTP deployments | MUST |
| [TF-K8S-005](#tf-k8s-005--ignore-image-and-env-changes-when-the-cicd-pipeline-owns-them) | Ignore image and env changes when the CI/CD pipeline owns them | MUST |
| [TF-SEC-001](#tf-sec-001--deliver-secrets-through-external-secrets) | Deliver secrets through External Secrets | MUST |
| [TF-LNT-001](#tf-lnt-001--run-terraform-fmt-validate-tflint-and-checkov-in-ci) | Run `terraform fmt`, `validate`, `tflint` and `checkov` in CI | MUST |
| [TF-MOD-001](#tf-mod-001--declare-a-moved-block-when-renaming-a-module-or-adding-count) | Declare a `moved` block when renaming a module or adding `count` | MUST |

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

### TF-K8S-004 — Add a short `preStop` wait to HTTP deployments

- **Level:** MUST
- **Applies to:** Terraform modules with HTTP deployments
- **Enforced by:** code review
- **Why:** endpoint removal and the `SIGTERM` reach the pod at the same time, so a pod that stops at once can still receive requests routed by components that have not yet seen the change. A short `sleep` in `preStop` lets traffic drain first. The wait must be shorter than `termination_grace_period_seconds`, together with `graceful_timeout` (see `PY-RUN-003`), or the pod is killed with `SIGKILL`.
- **Source:** Internal runtime standard.

Correct:
```hcl
lifecycle {
  pre_stop {
    exec {
      command = ["/bin/sh", "-c", "sleep 10"]
    }
  }
}
```

Incorrect:
```hcl
container {
  name  = var.container_name
  image = var.image
}
```

### TF-K8S-005 — Ignore image and env changes when the CI/CD pipeline owns them

- **Level:** MUST
- **Applies to:** Terraform modules whose deployments are updated by a CI/CD pipeline
- **Enforced by:** code review; `terraform plan` shows no image or env diff after a deploy
- **Why:** when the pipeline sets the image tag and environment values, Terraform would revert them to the stored values on its next apply and roll back a release. `ignore_changes` makes the pipeline the single owner of those fields.
- **Source:** Internal CI/CD standard.

Correct:
```hcl
lifecycle {
  ignore_changes = [
    spec[0].template[0].spec[0].container[0].image,
    spec[0].template[0].spec[0].container[0].env,
  ]
}
```

Incorrect:
```hcl
resource "kubernetes_deployment_v1" "this" {
  metadata {
    name = var.name
  }
}
```
with no `lifecycle` block while the pipeline deploys by image tag.

### TF-SEC-001 — Deliver secrets through External Secrets

- **Level:** MUST
- **Applies to:** all Terraform modules that give secrets to workloads
- **Enforced by:** `checkov`; secret scanning; code review
- **Why:** secrets in `.tf` files or in plain variables end up in the repository, the state and the plan output. An `ExternalSecret` references the secret in the secrets manager and the workload consumes the resulting Kubernetes Secret. See also `GEN-SEC-001`.
- **Source:** Internal security standard.

Correct:
```hcl
resource "kubernetes_manifest" "database" {
  manifest = {
    apiVersion = "external-secrets.io/v1"
    kind       = "ExternalSecret"
    metadata = {
      name      = "database"
      namespace = var.namespace
    }
    spec = {
      secretStoreRef = {
        name = var.secret_store
        kind = "ClusterSecretStore"
      }
      target = {
        name = "database"
      }
      dataFrom = [{
        extract = {
          key = var.database_secret_key
        }
      }]
    }
  }
}
```

Incorrect:
```hcl
variable "database_password" {
  type = string
}

resource "kubernetes_secret_v1" "database" {
  metadata {
    name = "database"
  }
  data = {
    password = var.database_password
  }
}
```

### TF-LNT-001 — Run `terraform fmt`, `validate`, `tflint` and `checkov` in CI

- **Level:** MUST
- **Applies to:** all Terraform repositories
- **Enforced by:** CI lint stage
- **Why:** formatting, validation, linting and policy checks catch syntax errors, deprecated arguments and insecure settings before a plan is reviewed.
- **Source:** Internal CI/CD standard.

Correct:
```bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
tflint --recursive
checkov --directory .
```

Incorrect:
```bash
terraform validate
```

### TF-MOD-001 — Declare a `moved` block when renaming a module or adding `count`

- **Level:** MUST
- **Applies to:** all Terraform repositories
- **Enforced by:** code review; the plan shows moves and no destroy/create pair
- **Why:** renaming a module call or adding `count` or `for_each` changes resource addresses, and Terraform plans to destroy and recreate everything under it. A `moved` block maps the old address to the new one and keeps the existing resources.
- **Source:** Internal infrastructure standard.

Correct:
```hcl
moved {
  from = module.api
  to   = module.api[0]
}

module "api" {
  count  = var.enabled ? 1 : 0
  source = "./modules/api"
}
```

Incorrect:
```hcl
module "api" {
  count  = var.enabled ? 1 : 0
  source = "./modules/api"
}
```
