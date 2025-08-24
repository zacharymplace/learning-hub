# Contributing Guide

## Workflow
- Create a feature branch from `dev` (e.g., `feat/short-description`).
- Open a PR to `dev`. Squash and merge when approved.
- Periodically promote `dev` -> `main` with a version bump.

## Standards
- Add/Update README sections when you change behavior.
- Include lightweight tests in `tests/` when possible.
- Keep scripts idempotent and safe (dry-run flags, backups).

## Release
- Semantic versioning: MAJOR.MINOR.PATCH
- Update CHANGELOG.md with notable changes.
