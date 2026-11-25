# Agent instructions snippet

Paste or link this block from `CLAUDE.md`, `AGENTS.md` and `.github/copilot-instructions.md` in each repository.

```markdown
## Style guide

- Follow the DataInt style guide: https://github.com/dataintmx/StyleGuidelines
- Rules are identified by ID (for example `PY-LOG-001`). Cite the ID when you justify a change and in commit messages.
- MUST rules are blocking. SHOULD rules need a justified exception in the pull request.
- Precedence: language rules, then `GEN-*` rules, then auxiliary guides (PEP 8, Google style guides).
- Do not add comments to code except allowed directives (`noqa`, `type: ignore`, `pragma`, `tflint-ignore`,
  `checkov:skip`, `eslint-disable`, `prettier-ignore`). See `GEN-CMT-001`.
- Branches, commits and pull requests follow the organization-wide `CONTRIBUTING.md`.
```

The list of allowed directives is authoritative in [`scripts/README.md`](scripts/README.md).
