# Scripts

Checks that enforce rules no linter covers.

Planned (added in phase 2):

| Script | Verifies |
|---|---|
| `check-no-comments.py` | `GEN-CMT-001`: no comments other than an allow-list of directives |

`check-no-comments.py` is based on `tokenize` for Python. Allowed directives: `noqa`, `type: ignore`, `pragma`,
`tflint-ignore`, `checkov:skip`, `eslint-disable`, `prettier-ignore`, shebang, and license or encoding headers. The same
pattern is extended to TypeScript, HCL, YAML and shell. It runs as a step of `python-ci.yml` in `ci-templates` (T14) and
as a pre-commit hook. Per P5 it starts as informational for one week and then becomes blocking.
