# 0001 — Python + Typer CLI, local-markdown tracker

Date: 2026-10-05
Status: accepted

## Context

Fresh Arch host, solo dev, empty Projects dir. Need shippable v1 in ~2 weeks that is portfolio + stars friendly. Host has python3.14, node22, go1.27.

## Decision

- Build `aab` as Python + Typer CLI (std lib + typer + pytest only).
- Vertical slices: Check → Plan (dry-run) → Bootstrap (execute).
- Checks are read-only; Bootstrap only runs what Checks mark missing unless `--force`.
- Issue tracker: local markdown under `.scratch/arch-agent-bootstrap/issues/`.
- Tests at CLI seam only (Typer runner), not internals.

## Consequences

- No daemon, no TUI, no network calls in v1.
- Easy to demo via `aab check` and `aab plan --dry-run`.
