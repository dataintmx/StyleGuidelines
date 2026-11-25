# Rules

One Markdown file per area. Rule IDs, levels and the rule template are described in the [root README](../README.md) and
in [`TEMPLATE.md`](TEMPLATE.md).

| File | Scope | Holds |
|---|---|---|
| [`general.md`](general.md) | `GEN-*` | Comments, configuration, names, secrets, files, i18n, and pointer rules to `CONTRIBUTING.md` |
| [`python.md`](python.md) | `PY-*` | Python index; each topic lives in [`python/`](python/README.md) |
| [`typescript.md`](typescript.md) | `TS-*` | React, Next.js and Vite: naming, configuration and OpenTelemetry, tests, lint |
| [`terraform.md`](terraform.md) | `TF-*` | Modules, Kubernetes (probes, lifecycle), secrets, formatting |
| [`docker.md`](docker.md) | `DKR-*` | Dockerfile, image built from the lock file, smoke test |
| [`shell.md`](shell.md) | `SH-*` | `shellcheck`, `set -euo pipefail` |
| [`html-css.md`](html-css.md) | `CSS-*` | HTML and CSS |
| [`ci.md`](ci.md) | `CI-*` | Pipeline stages, gates, post-deploy verification |

Each file starts with a short scope statement and an index table (ID, title, level), followed by the rules in ID order.
