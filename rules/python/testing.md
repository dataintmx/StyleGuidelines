# Python: testing

Scope: `PY-TST`.

| ID | Title | Level |
|---|---|---|
| [PY-TST-001](#py-tst-001--run-pytest-with-coverage-and-junit-reports-in-ci) | Run pytest with coverage and JUnit reports in CI | MUST |
| [PY-TST-002](#py-tst-002--test-against-ephemeral-services-and-fixtures-never-shared-databases) | Test against ephemeral services and fixtures, never shared databases | MUST |
| [PY-TST-003](#py-tst-003--do-not-lower-coverage-by-more-than-2-points-against-the-base-branch) | Do not lower coverage by more than 2 points against the base branch | SHOULD |

### PY-TST-001 — Run pytest with coverage and JUnit reports in CI

- **Level:** MUST
- **Applies to:** Python repos with a CI pipeline
- **Enforced by:** CI test stage; the `coverage.xml` artifact must exist
- **Why:** coverage and test results are published from `coverage.xml` and `junit.xml`; without them nothing measures coverage, even when `pytest-cov` is installed.
- **Source:** Internal testing and quality standard; internal CI/CD standard.

Correct:
```bash
pytest --cov=src --cov-report=xml --junitxml=junit.xml
```

Incorrect:
```bash
pytest
```

### PY-TST-002 — Test against ephemeral services and fixtures, never shared databases

- **Level:** MUST
- **Applies to:** Python services with database or cache tests
- **Enforced by:** code review; CI workflow with `services:` instead of database URL secrets
- **Why:** tests against shared databases depend on live data, are slow and flaky, and force the database to accept connections from CI runners. Use throwaway Postgres or Redis as job `services:`, with fixtures or factories for data.
- **Source:** Internal testing and quality standard.

Correct:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    env:
      DATABASE_URL: postgresql://postgres:test@localhost:5432/postgres
```

Incorrect:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.PUBLIC_DATABASE_URL }}
```

### PY-TST-003 — Do not lower coverage by more than 2 points against the base branch

- **Level:** SHOULD
- **Applies to:** Python repos with a CI pipeline
- **Enforced by:** coverage status check in CI
- **Why:** the comparison against the base branch catches changes that ship untested code without imposing an absolute threshold that encourages low-value tests. A drop above 2 points needs a justified exception in the pull request.
- **Source:** Internal testing and quality standard.

Correct:
```yaml
coverage:
  status:
    project:
      default:
        target: auto
        threshold: 2%
```

Incorrect:
```yaml
coverage:
  status:
    project:
      default:
        target: auto
        threshold: 20%
```
