# Common Ruff Rule Codes

Reference loaded only when a specific rule needs explaining.

| Code | Category | Meaning |
|------|----------|---------|
| `E501` | pycodestyle | Line too long |
| `F401` | Pyflakes | Module imported but unused |
| `F841` | Pyflakes | Local variable assigned but never used |
| `I001` | isort | Import block is un-sorted or un-formatted |
| `UP` | pyupgrade | Suggests newer Python syntax (e.g. f-strings, `list` over `List`) |
| `B` | flake8-bugbear | Likely bugs / design smells (e.g. mutable default args) |
| `C4` | flake8-comprehensions | Unnecessary list/dict/set comprehension patterns |

## Resolving Common Issues

- **F401 (unused import)**: remove the import, or add `# noqa: F401` if it's
  intentionally re-exported.
- **E501 (line too long)**: let `ruff format` wrap it, or manually break the line;
  default limit is 88 chars (Black-compatible).
- **F841 (unused variable)**: prefix with `_` (e.g. `_result = ...`) if intentional,
  otherwise delete the assignment.

Full rule list: https://docs.astral.sh/ruff/rules/
