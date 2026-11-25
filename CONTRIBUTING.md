# Contributing

Contribution workflow (branches, commits, pull requests, review) is defined in the organization-wide `CONTRIBUTING.md`
in `dataintmx/.github` (T23) and is not repeated here. This file only covers what is specific to this repository.

## Proposing a rule

1. Copy [`rules/TEMPLATE.md`](rules/TEMPLATE.md) into the file of the matching area.
2. Pick the next free ID for the scope and topic. Never reuse an ID.
3. Set the level to MUST only if CI enforces it or a reviewer can block on it; otherwise use SHOULD.
4. Name the enforcing tool or check in `Enforced by`, and add its configuration to [`config/`](config/README.md) or
   [`scripts/`](scripts/README.md).
5. Keep explanations out of code blocks.
6. Update the index table in the area file and in the root [`README.md`](README.md), and add an entry to
   [`CHANGELOG.md`](CHANGELOG.md).

## Changing or retiring a rule

Change the text in place and record it in the changelog. To retire a rule, keep its heading and set
`Status: withdrawn` with the reason.

## Review

Reviewers comment by rule ID. A rule without agreement becomes SHOULD or is left out.
