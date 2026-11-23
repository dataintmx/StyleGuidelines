# Tool configuration

One file per tool, identical to what CI runs (T14). Rules that a tool enforces cite the tool and rule code in their
`Enforced by` field.

Planned files (added in phase 2):

| File | Tool |
|---|---|
| `ruff.toml` | Ruff (line length 100) |
| `mypy.ini` | mypy |
| `.pre-commit-config.yaml` | pre-commit hooks |
| `.editorconfig` | Editors |
| `eslint.config.mjs` | ESLint |
| `.prettierrc.json` | Prettier |
| `tsconfig.base.json` | TypeScript |
| `.tflint.hcl` | tflint |
| `.checkov.yaml` | Checkov |

The previous Pylint configuration is in [`../legacy/.pylintrc`](../legacy/README.md) and is removed one release after
the new configuration ships.
