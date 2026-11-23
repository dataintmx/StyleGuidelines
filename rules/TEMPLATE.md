### PY-XXX-NNN — Imperative title

- **Level:** MUST | SHOULD
- **Applies to:** services | workers | libraries | all Python repos
- **Enforced by:** `ruff B006` | `scripts/check-no-comments.py` | code review
- **Why:** one or two sentences, with the incident or standard that justifies it.
- **Source:** `docs/standards/…` (T-number) or incident date.

Correct:
```python
…
```

Incorrect:
```python
…
```

## Notes for authors

- Replace `PY-XXX-NNN` with the real ID. The heading must be exactly `### <ID> — title`.
- IDs are immutable and never reused. A retired rule keeps its heading and gets `Status: withdrawn` plus the reason.
- Explanations never go inside code blocks (`GEN-CMT-001` also applies to examples). The only exception is the
  `Incorrect` block of `GEN-CMT-001`.
- Adjust the code fence language (`python`, `typescript`, `hcl`, `dockerfile`, `bash`, `css`, `yaml`).
- Add the rule to the index of its file and to the root `README.md`, and record it in `CHANGELOG.md`.
