# Learning hub 

[![Discussions](https://img.shields.io/badge/discussions-ask%20a%20question-5865f2)](../../discussions)
[![docs](https://github.com/zacharymplace/learning-hub/actions/workflows/docs.yml/badge.svg)](../../actions/workflows/docs.yml)
[![generate examples](https://github.com/zacharymplace/learning-hub/actions/workflows/generate-examples.yml/badge.svg)](../../actions/workflows/generate-examples.yml)
[![lint](https://github.com/zacharymplace/learning-hub/actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)
[![website](https://img.shields.io/badge/website-live-4c1)](https://zacharymplace.github.io/learning-hub/)

**Purpose**: Notes, exercises, and experiments for continuous learning.

## Getting Started
```bash
# Optional: create a virtual environment
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Repo Layout
```
learning-hub/
├─ README.md
├─ scripts/
│  ├─ python/
│  └─ js/
├─ data/
│  ├─ samples/
├─ docs/
├─ tests/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  └─ PULL_REQUEST_TEMPLATE.md
├─ .gitignore
├─ LICENSE
└─ CHANGELOG.md
```

## Governance
- Owner: Z$
- Review Cycle: Quarterly
- Version: v0.1.0
- Audit Notes: Track design decisions in `docs/decisions/` (ADR format).

## Roadmap
- [ ] Define first 2–3 scripts or notebooks
- [ ] Add data samples and tests
- [ ] Wire CI (ruff/black or flake8 + pytest)
