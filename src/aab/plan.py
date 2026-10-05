"""Plan: ordered Steps derived from Checks. Pure, no I/O."""
from __future__ import annotations


def build_plan(checks: list[dict], only: str | None = None) -> list[dict]:
    steps = []
    for c in checks:
        if only and c["name"] != only:
            continue
        steps.append(
            {
                "name": c["name"],
                "status": "skip" if c["ok"] else "todo",
                "detail": c["version"] or c["fix_hint"],
                "fix_hint": c["fix_hint"],
            }
        )
    if only and not steps:
        raise ValueError(f"unknown step: {only}")
    return steps


def render_plan(steps: list[dict]) -> str:
    lines = []
    for s in steps:
        mark = "✓ skip" if s["status"] == "skip" else "→ todo"
        lines.append(f"{mark} {s['name']}: {s['detail']}")
    return "\n".join(lines)
