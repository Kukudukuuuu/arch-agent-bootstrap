"""CLI: thin adapter over Checks + Plan + Bootstrap executor."""
from __future__ import annotations

import json

import typer

from .checks import run_checks
from .executor import execute_step
from .plan import build_plan, render_plan

app = typer.Typer(help="Arch -> agent-ready dev setup")


def _load_steps(only: str | None) -> list[dict]:
    try:
        return build_plan(run_checks(), only=only)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2)


@app.command()
def check(
    as_json: bool = typer.Option(False, "--json", help="Machine-readable output"),
) -> None:
    """Report Host state. Read-only."""
    results = run_checks()
    if as_json:
        typer.echo(json.dumps(results, indent=2))
        return
    for r in results:
        mark = "✓" if r["ok"] else "✗"
        extra = r["version"] or r["fix_hint"]
        typer.echo(f"{mark} {r['name']}: {extra}")


@app.command()
def plan(
    only: str | None = typer.Option(None, "--only", help="Only one step"),
    dry_run: bool = typer.Option(True, "--dry-run/--execute", help="Plan never mutates; flag kept for spec parity"),
) -> None:
    """Print ordered Plan. Never mutates."""
    _ = dry_run  # plan is always a preview
    typer.echo(render_plan(_load_steps(only)))


@app.command()
def bootstrap(
    only: str | None = typer.Option(None, "--only", help="Only one step"),
    dry_run: bool = typer.Option(True, "--dry-run/--execute"),
) -> None:
    """Preview Plan (default) or execute one Step with --only X --execute."""
    steps = _load_steps(only)
    if dry_run:
        typer.echo(render_plan(steps))
        return
    if only is None:
        typer.echo("refusing full execute without --only in v1; use --only <step> --execute", err=True)
        raise typer.Exit(2)
    target = steps[0]
    if target["status"] == "skip":
        typer.echo(f"✓ skip {target['name']}: already ready")
        return
    typer.echo(f"run: {target['fix_hint']}")
    rc, out = execute_step(target)
    typer.echo(out)
    if rc != 0:
        typer.echo(f"step failed (exit {rc}); re-run `aab check` after fixing manually", err=True)
        raise typer.Exit(rc)
    rechecked = {c["name"]: c for c in run_checks()}
    now = rechecked.get(target["name"], {})
    if now.get("ok"):
        typer.echo(f"✓ verified {target['name']}: {now.get('version')}")
    else:
        typer.echo(f"! unverified {target['name']}: re-run `aab check`", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
