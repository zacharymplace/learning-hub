# Conventions

## Repo layout
- `docs/` – published site content
- `docs/how-to/`, `docs/snippets/`, `docs/reference/`, `docs/examples/`
- `scripts/python/` – generators & utilities
- `.github/` – workflows, templates

## Filenames & headings
- Kebab-case for docs: `power-query-handoff.md`
- One H1 per page; short H2/H3s; verbs for How-Tos (“Export…”, “Validate…”)

## Code style
- **Python:** ruff/black defaults, pure functions, JSONL logs, `pyarrow` dtypes
- **SQL:** UPPER keywords, snake_case identifiers, idempotent staging/merge
- **Markdown:** copy-paste blocks first; minimal prose; use admonitions for tips/pitfalls

## Data types (cross-tool)
- Dates: store/export ISO `YYYY-MM-DD`, strip TZ for Excel hand-offs
- IDs: keep as text if leading zeros matter
- Booleans: pandas `boolean`; Excel/PQ logical

## Commits
- `docs(how-to): …`, `docs(snippets): …`, `chore(examples): …`
- Use `closes #123` to auto-close issues

## Links & paths
- From top-level pages → `examples/<file>`
- From `how-to/*` pages → `../examples/<file>`

## Quality checks
- MkDocs build with `--strict` must be green
- Add examples for anything users copy/paste
