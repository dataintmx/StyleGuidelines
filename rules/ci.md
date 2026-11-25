# Continuous integration rules

Scope: `CI-*`. Pipeline stages, gates and post-deploy verification.

| ID | Title | Level |
|---|---|---|
| [CI-PIP-001](#ci-pip-001--run-the-pipeline-stages-in-order-each-gating-the-next) | Run the pipeline stages in order, each gating the next | MUST |
| [CI-PIP-002](#ci-pip-002--tests-gate-the-deploy) | Tests gate the deploy | MUST |
| [CI-PIP-003](#ci-pip-003--smoke-test-the-image-before-pushing-it) | Smoke-test the image before pushing it | MUST |
| [CI-PIP-004](#ci-pip-004--deploy-the-image-tagged-with-the-commit-sha) | Deploy the image tagged with the commit SHA | MUST |
| [CI-DPL-001](#ci-dpl-001--verify-the-rollout-after-deploy-and-roll-back-on-failure) | Verify the rollout after deploy and roll back on failure | MUST |

### CI-PIP-001 — Run the pipeline stages in order, each gating the next

- **Level:** MUST
- **Applies to:** all repositories that build and deploy an image
- **Enforced by:** `needs:` chain in the workflow; code review
- **Why:** each stage gates the next, so a broken change stops before it reaches the cluster. Stages: 1 lint and format (`ruff check` and `ruff format --check`; `eslint` and `prettier --check`), 2 types (`mypy`; `tsc --noEmit`), 3 tests and coverage, 4 build from the lock file, 5 image smoke test, 6 image push, 7 deploy and verification, 8 pipeline metrics. Pull requests run stages 1–5; pushes to the deploy branches run 1–8.
- **Source:** Internal CI/CD standard.

Correct:
```yaml
jobs:
  ci:
    uses: example-org/ci-templates/.github/workflows/python-ci.yml@v1
  build:
    needs: ci
    uses: example-org/ci-templates/.github/workflows/docker-build.yml@v1
  deploy:
    needs: build
    uses: example-org/ci-templates/.github/workflows/k8s-deploy.yml@v1
```

Incorrect:
```yaml
jobs:
  build:
    uses: example-org/ci-templates/.github/workflows/docker-build.yml@v1
  deploy:
    uses: example-org/ci-templates/.github/workflows/k8s-deploy.yml@v1
```

### CI-PIP-002 — Tests gate the deploy

- **Level:** MUST
- **Applies to:** workflows that deploy
- **Enforced by:** `needs:` from the test job to the deploy job; code review
- **Why:** a deploy that does not depend on the tests ships untested code. A repo without tests starts with the image smoke test and a health test. Pre-existing failures are marked `xfail` with a linked issue; the job is not ignored or allowed to fail.
- **Source:** Internal CI/CD standard.

Correct:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
  deploy:
    needs: test
    runs-on: ubuntu-latest
```

Incorrect:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - run: pytest
  deploy:
    runs-on: ubuntu-latest
```

### CI-PIP-003 — Smoke-test the image before pushing it

- **Level:** MUST
- **Applies to:** workflows that build a Python image
- **Enforced by:** CI image smoke-test stage
- **Why:** a broken import must fail in CI and never reach the cluster. Run the built image with fake environment variables: for an API, import the application; for Celery, run `celery -A src.celery.app inspect --help`.
- **Source:** Internal CI/CD standard.

Correct:
```yaml
- run: docker run --rm -e DATABASE_URL=postgresql://user:pass@localhost/db "$IMAGE" python -c "import src.asgi"
- run: docker push "$IMAGE"
```

Incorrect:
```yaml
- run: docker push "$IMAGE"
```

### CI-PIP-004 — Deploy the image tagged with the commit SHA

- **Level:** MUST
- **Applies to:** workflows that deploy images to Kubernetes
- **Enforced by:** code review
- **Why:** the pushed image carries a tag of the form `<env>_<sha7>` (`qa_` for the development branch, `prod_` for the production branch) and the deploy sets exactly that tag, so what runs is traceable to a commit. Floating tags such as `latest` are not deployed.
- **Source:** Internal CI/CD standard.

Correct:
```yaml
image: example/billing-api:${{ needs.build.outputs.tag }}
```

Incorrect:
```yaml
image: example/billing-api:latest
```

### CI-DPL-001 — Verify the rollout after deploy and roll back on failure

- **Level:** MUST
- **Applies to:** workflows that deploy Deployments to Kubernetes
- **Enforced by:** the deploy job; requires a readiness probe (`TF-K8S-001`)
- **Why:** `kubectl rollout status` alone reports success when the new pod has no readiness probe, so CI stayed green with the service crash-looping. After the rollout, check that the new pods are `Ready` and have no restarts; on failure run `kubectl rollout undo` and fail the job.
- **Source:** Internal CI/CD standard.

Correct:
```bash
set -euo pipefail
kubectl -n "$NS" set image deployment/"$DEP" "$CONTAINER"="$IMAGE"
if ! kubectl -n "$NS" rollout status deployment/"$DEP" --timeout=300s; then
  kubectl -n "$NS" rollout undo deployment/"$DEP"
  exit 1
fi
sleep 30
SELECTOR=$(kubectl -n "$NS" get deploy "$DEP" -o jsonpath='{.spec.selector.matchLabels}' | jq -r 'to_entries|map("\(.key)=\(.value)")|join(",")')
NOT_READY=$(kubectl -n "$NS" get pods -l "$SELECTOR" -o json | jq '[.items[] | select(.spec.containers[0].image=="'"$IMAGE"'") | select((.status.containerStatuses[0].ready|not) or .status.containerStatuses[0].restartCount>0)] | length')
if [ "$NOT_READY" != "0" ]; then
  kubectl -n "$NS" rollout undo deployment/"$DEP"
  exit 1
fi
```

Incorrect:
```bash
kubectl -n "$NS" set image deployment/"$DEP" "$CONTAINER"="$IMAGE"
kubectl -n "$NS" rollout status deployment/"$DEP"
```
