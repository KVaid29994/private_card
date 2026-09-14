---
name: ruff
description: 'Lint and format Python code with Ruff. Use when the user asks to lint, format, auto-fix, or check style/quality of Python files, or mentions "ruff", "flake8", "black formatting", or Python linting errors.'
argument-hint: '[path] (optional, defaults to current directory)'
---

# Ruff (Python Linter & Formatter)

Ruff is a fast, all-in-one Python linter and formatter (replaces flake8, isort, black,
and pyupgrade in a single tool). This skill wraps the common workflows so they can be
run consistently.

## When to Use

- User asks to "lint this Python file/project"
- User asks to "format" Python code
- User wants auto-fixable issues (unused imports, import order, etc.) resolved
- User is debugging a `ruff` error/warning code (e.g. `E501`, `F401`, `I001`)

## Prerequisites

Ruff must be installed. Check first, then install if missing:

```powershell
ruff --version
# if missing:
pip install ruff
# or, if the project uses uv:
uv add --dev ruff
```

## Procedure

1. **Check for a config.** Look for `[tool.ruff]` in `pyproject.toml`, or a
   standalone `ruff.toml` / `.ruff.toml`. If none exists, Ruff uses sane defaults —
   don't invent a config file unless the user asks for one.
2. **Lint (no changes).** Run [scripts/lint.ps1](./scripts/lint.ps1) or:
   ```powershell
   ruff check <path>
   ```
3. **Auto-fix safe issues.**
   ```powershell
   ruff check <path> --fix
   ```
4. **Format code** (Black-compatible style):
   ```powershell
   ruff format <path>
   ```
5. **Explain a specific rule code** (e.g. what `F401` means and how to resolve it):
   see [references/rules.md](./references/rules.md) for the common codes, or run
   ```powershell
   ruff rule F401
   ```

## Notes

- Prefer `ruff check --fix` before manually editing style issues by hand.
- Never run `--fix` with `--unsafe-fixes` unless the user explicitly asks for it —
  unsafe fixes can change program behavior.
- This is a demo skill included for reference; this repo (`wedding-card-demo`) is a
  static HTML/CSS/JS project with no Python code, so there's nothing to actually lint
  here yet.
