# Docker rules

Scope: `DKR-*`. Dockerfile conventions, images built from the lock file, smoke tests.

| ID | Title | Level |
|---|---|---|
| [DKR-IMG-001](#dkr-img-001--build-in-several-stages-and-keep-build-tools-out-of-the-final-image) | Build in several stages and keep build tools out of the final image | MUST |
| [DKR-IMG-002](#dkr-img-002--pin-the-exact-base-image-version) | Pin the exact base image version | MUST |
| [DKR-USR-001](#dkr-usr-001--run-as-an-unprivileged-user) | Run as an unprivileged user | SHOULD |
| [DKR-IGN-001](#dkr-ign-001--exclude-git-metadata-env-files-dependencies-and-artifacts-with-dockerignore) | Exclude Git metadata, env files, dependencies and artifacts with `.dockerignore` | MUST |
| [DKR-SEC-001](#dkr-sec-001--never-pass-secrets-through-arg-or-env) | Never pass secrets through `ARG` or `ENV` | MUST |

Lock-file builds and the image smoke test are covered by [`PY-DEP-002`](python/dependencies.md#py-dep-002--build-images-from-the-lock-file) and [`CI-PIP-003`](ci.md#ci-pip-003--smoke-test-the-image-before-pushing-it).

### DKR-IMG-001 — Build in several stages and keep build tools out of the final image

- **Level:** MUST
- **Applies to:** all Dockerfiles
- **Enforced by:** code review
- **Why:** compilers, package managers and source trees in the final image enlarge it and widen the attack surface. Dependencies are installed and the application is built in earlier stages; the final stage copies only the result.
- **Source:** Common practice for container images.

Correct:
```dockerfile
FROM node:22.11.0-slim AS deps
WORKDIR /srv/app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS builder
COPY . .
RUN npm run build

FROM node:22.11.0-slim AS runner
WORKDIR /srv/app
COPY --from=builder /srv/app/dist ./dist
COPY --from=deps /srv/app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

Incorrect:
```dockerfile
FROM node:22.11.0
WORKDIR /srv/app
COPY . .
RUN npm ci && npm run build
CMD ["node", "dist/server.js"]
```

### DKR-IMG-002 — Pin the exact base image version

- **Level:** MUST
- **Applies to:** all Dockerfiles
- **Enforced by:** code review; `hadolint DL3007`
- **Why:** a moving tag changes the image between builds without a code change, which makes builds irreproducible and upgrades unreviewed. Use the full version tag, never `latest`.
- **Source:** Common practice for container images.

Correct:
```dockerfile
FROM python:3.12.7-slim-bookworm
```

Incorrect:
```dockerfile
FROM python:latest
```

### DKR-USR-001 — Run as an unprivileged user

- **Level:** SHOULD
- **Applies to:** all Dockerfiles for services and workers
- **Enforced by:** `hadolint DL3002`; code review
- **Why:** a process that runs as root turns a code-execution flaw into control of the container. Create a system user in the final stage, own only the files it needs and switch with `USER`. An image that needs root for a documented reason states it in the pull request.
- **Source:** Common practice for container images.

Correct:
```dockerfile
RUN groupadd --system --gid 1001 app && useradd --system --uid 1001 --gid app --no-create-home app
COPY --from=builder --chown=app:app /srv/app/dist ./dist
USER app
```

Incorrect:
```dockerfile
COPY --from=builder /srv/app/dist ./dist
CMD ["node", "dist/server.js"]
```

### DKR-IGN-001 — Exclude Git metadata, env files, dependencies and artifacts with `.dockerignore`

- **Level:** MUST
- **Applies to:** all repositories with a Dockerfile
- **Enforced by:** code review; CI check that `.dockerignore` exists
- **Why:** without it `COPY . .` sends `.git`, local `.env*` files and installed dependencies into the build context and possibly into the image, slowing the build, breaking layer caching and leaking local files.
- **Source:** Common practice for container images.

Correct:
```
.git
.env*
node_modules
.venv
__pycache__
dist
.next
coverage.xml
junit.xml
```

Incorrect: a repository with a Dockerfile and no `.dockerignore`, or one that lists only `node_modules`.

### DKR-SEC-001 — Never pass secrets through `ARG` or `ENV`

- **Level:** MUST
- **Applies to:** all Dockerfiles
- **Enforced by:** `hadolint`; code review; secret scanning of images
- **Why:** values passed through `ARG` and `ENV` are stored in the image layers and its metadata, where anyone with the image can read them. A build that needs a secret mounts it with `--mount=type=secret`, which is available during one `RUN` and never persisted.
- **Source:** Common practice for container images.

Correct:
```dockerfile
RUN --mount=type=secret,id=registry_token \
    REGISTRY_TOKEN="$(cat /run/secrets/registry_token)" npm ci
```
```bash
docker build --secret id=registry_token,env=REGISTRY_TOKEN .
```

Incorrect:
```dockerfile
ARG REGISTRY_TOKEN
ENV REGISTRY_TOKEN=${REGISTRY_TOKEN}
RUN npm ci
```
