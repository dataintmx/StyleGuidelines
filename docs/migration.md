# Migration from the monolithic README

The previous guide (Spanish, one file) is preserved in [`../legacy/README.md`](../legacy/README.md). Its sections are
distributed across the new structure as follows. The "Rule IDs" column is filled in as rules are written in later phases;
this table then becomes the old section number → new ID lookup.

| Old section | Topic | New location | Rule IDs | Notes |
|---|---|---|---|---|
| 1 | Introduction | [`README.md`](../README.md) | n/a | Rewritten: how to read a rule, precedence, how to propose changes |
| 2, 2.1 | Auxiliary guides | [`README.md`](../README.md) (precedence) and each language file | n/a | PHP/WordPress removed (P4) |
| 3 | General guidelines (preface) | [`rules/general.md`](../rules/general.md) | `GEN-*` | |
| 3.1 | Project structure | [`rules/general.md`](../rules/general.md) | `GEN-FIL-*` | |
| 3.2 | Version control workflow | `CONTRIBUTING.md` (organization-wide, T23) | `GEN-GIT-001` pointer | Not duplicated here |
| 3.2.1 | Branch naming | `CONTRIBUTING.md` (T23) | `GEN-GIT-*` pointer | P2: no issue number in branch names; link with `Closes #N` in the PR |
| 3.2.2 | Versioning (CalVer) | `CONTRIBUTING.md` (T23) | `GEN-GIT-*` pointer | |
| 3.3.1–3.3.4 | Source files: encoding, name, structure, end of file | [`rules/general.md`](../rules/general.md) | `GEN-FIL-*` | |
| 3.4.1 | Maximum line length | [`rules/python/style-and-naming.md`](../rules/python/style-and-naming.md), [`rules/typescript.md`](../rules/typescript.md), [`config/`](../config/README.md) | `PY-STY-*`, `TS-*` | P3: Python 100 columns; the 80-column comment limit is dropped |
| 3.4.2 | Class size and structure | [`rules/python/style-and-naming.md`](../rules/python/style-and-naming.md) | `PY-STY-*` | |
| 3.4.3 | Blank lines | Formatter configuration in [`config/`](../config/README.md) | `PY-STY-*`, `TS-*` | Enforced by Ruff and Prettier |
| 3.4.4 | Indentation | [`config/`](../config/README.md) (`.editorconfig`) | `PY-STY-*`, `TS-*` | |
| 3.5.1, 3.5.2 | Non-ASCII and special characters | [`rules/general.md`](../rules/general.md) | `GEN-*` | |
| 3.5.3.1 | Comments | [`rules/general.md`](../rules/general.md) and [`scripts/`](../scripts/README.md) | `GEN-CMT-001` | Code has no comments; P5 rollout of the check |
| 3.5.3.2 | Docstrings | [`rules/general.md`](../rules/general.md) and [`rules/python/style-and-naming.md`](../rules/python/style-and-naming.md) | `GEN-CMT-*`, `PY-STY-*` | P1: public API of reusable libraries only |
| 3.5.4 | Naming | [`rules/general.md`](../rules/general.md) | `GEN-NAM-*` | |
| 3.5.4.1.1–3.5.4.1.7 | Naming by identifier type | [`rules/python/style-and-naming.md`](../rules/python/style-and-naming.md), [`rules/typescript.md`](../rules/typescript.md) | `PY-NAM-*`, `TS-*` | Per language; the old `UpperCamelCase` rule for modules is reviewed against PEP 8 |
| 3.5.5 | Spaces in expressions | Formatter configuration in [`config/`](../config/README.md) | `PY-STY-*`, `TS-*` | Enforced by Ruff and Prettier |
| 4, 4.1, 4.1.1 | Configuration files, Pylint | [`config/`](../config/README.md) | n/a | Pylint moves to [`config/legacy/.pylintrc`](../legacy/README.md) and is replaced by `config/ruff.toml` |

## Steps for each old section

1. Find the section in the table.
2. Write the rule in the target file using [`rules/TEMPLATE.md`](../rules/TEMPLATE.md), with a new ID.
3. Translate the text to English and apply decisions P1–P5.
4. Fill in the "Rule IDs" cell and add an entry to [`CHANGELOG.md`](../CHANGELOG.md).
5. When every section is migrated, remove `legacy/README.md` and `config/legacy/.pylintrc` one release later.
