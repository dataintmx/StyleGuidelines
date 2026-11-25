# Scripts

Checks that enforce rules no linter covers.

| Script | Verifies |
|---|---|
| `check-no-comments.py` | `GEN-CMT-001`: no comments other than an allow-list of directives |

## check-no-comments.py

Python 3.11+, standard library only.

```
check-no-comments.py [--warn-only] [--format text|github] [--exclude GLOB]... [PATH...]
```

- Without `PATH`, it checks the files from `git ls-files`. A directory `PATH` is walked recursively.
- Output is `path:line: comment found`. With `--format github` it emits `::error file=…,line=…::…` (`::warning` with
  `--warn-only`).
- Exit code: `1` with findings, `0` without findings or with `--warn-only`, `2` on usage errors.
- `--exclude` takes an `fnmatch` glob matched against the full path and the file name.
- Unreadable files or files that do not tokenize are reported on stderr and skipped.

Supported files: `.py` (`tokenize`; docstrings are not comments), `.ts .tsx .js .jsx .mjs .cjs`, `.css .scss`
(`//` only in scss), `.tf .tfvars .hcl`, `.sh .bash`, `.yml .yaml`, `Dockerfile*` and `*.Dockerfile`. Other files are
ignored. Strings, template literals, regular expression literals, heredocs and YAML block scalars are not comments.

Allowed directives (`ALLOWED_DIRECTIVES` in the script, the authoritative list): shebang, encoding, `noqa`,
`type: ignore`, `pragma`, `pylint:`, `fmt: off|on|skip`, `isort:`, `ruff:`, `mypy:`, `eslint-…`, `prettier-ignore`,
`@ts-expect-error`, `@ts-ignore`, `@ts-nocheck`, `/// <reference`, `tflint-ignore`, `checkov:skip`, `shellcheck`,
`yamllint`, `hadolint`, Docker `syntax=`/`escape=`/`check=`, `@license`, `Copyright`, `SPDX-License-Identifier`,
`istanbul|c8|v8 ignore`, `webpackChunkName`, `sourceMappingURL`.

Tests: `python -m pytest scripts/test_check_no_comments.py`.

It runs as a step of `python-ci.yml` in `ci-templates` (T14) and as a pre-commit hook. Per P5 it starts as
informational for one week and then becomes blocking.
