# Shell rules

Scope: `SH-*`. `shellcheck` and `set -euo pipefail`.

| ID | Title | Level |
|---|---|---|
| [SH-SAF-001](#sh-saf-001--start-with-the-env-bash-shebang-and-set--euo-pipefail) | Start with the `env bash` shebang and `set -euo pipefail` | MUST |
| [SH-SAF-002](#sh-saf-002--quote-expansions-and-use-arrays-for-argument-lists) | Quote expansions and use arrays for argument lists | MUST |
| [SH-SEC-001](#sh-sec-001--pass-secrets-through-stdin-or-a-restricted-file-never-as-an-argument) | Pass secrets through stdin or a restricted file, never as an argument | MUST |
| [SH-LNT-001](#sh-lnt-001--pass-shellcheck) | Pass `shellcheck` | SHOULD |

### SH-SAF-001 — Start with the `env bash` shebang and `set -euo pipefail`

- **Level:** MUST
- **Applies to:** all Bash scripts
- **Enforced by:** `shellcheck`; code review
- **Why:** `env` finds Bash wherever it is installed. `-e` stops at the first failing command, `-u` turns an unset variable into an error and `pipefail` makes a failure inside a pipeline fail the whole pipeline, so a script does not continue after an error.
- **Source:** Common practice for shell scripts.

Correct:
```bash
#!/usr/bin/env bash
set -euo pipefail

./build.sh
./deploy.sh
```

Incorrect:
```bash
#!/bin/sh

./build.sh
./deploy.sh
```

### SH-SAF-002 — Quote expansions and use arrays for argument lists

- **Level:** MUST
- **Applies to:** all Bash scripts
- **Enforced by:** `shellcheck SC2086`, `SC2046`
- **Why:** an unquoted expansion is split on whitespace and expanded as a glob, so a value with a space becomes several arguments. A command whose arguments vary is built in an array, which keeps each argument intact.
- **Source:** Common practice for shell scripts.

Correct:
```bash
args=(--namespace "${NAMESPACE}" --output json)
if [[ -n "${SELECTOR:-}" ]]; then
    args+=(--selector "${SELECTOR}")
fi
kubectl get pods "${args[@]}"
```

Incorrect:
```bash
args="--namespace ${NAMESPACE} --output json"
kubectl get pods $args
```

### SH-SEC-001 — Pass secrets through stdin or a restricted file, never as an argument

- **Level:** MUST
- **Applies to:** all scripts that handle secrets
- **Enforced by:** code review
- **Why:** command arguments are visible to every user of the host through `ps` and in `/proc`. Standard input and files with restricted permissions are not.
- **Source:** Internal security standard.

Correct:
```bash
printf '%s' "${REGISTRY_TOKEN}" | docker login registry.example.com --username ci --password-stdin
```
```bash
umask 077
printf '%s' "${REGISTRY_TOKEN}" > "${token_file}"
```

Incorrect:
```bash
docker login registry.example.com --username ci --password "${REGISTRY_TOKEN}"
```

### SH-LNT-001 — Pass `shellcheck`

- **Level:** SHOULD
- **Applies to:** all Bash scripts
- **Enforced by:** `shellcheck` in pre-commit and CI
- **Why:** `shellcheck` finds quoting, portability and logic mistakes before they run. A warning that must stay is silenced with a narrow `# shellcheck disable=SCxxxx` directive and justified in the pull request.
- **Source:** Common practice for shell scripts.

Correct:
```bash
shellcheck scripts/*.sh
```

Incorrect:
```bash
bash scripts/deploy.sh
```
