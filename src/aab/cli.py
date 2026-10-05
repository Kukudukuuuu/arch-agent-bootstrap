"""CLI: thin adapter over Checks + Plan. Seams under test: check, plan, bootstrap."""
from __future__ import annotations

import json

import typer

from .checks import run_checks
from .plan import build_plan, render_plan

app = typer.Typer(help="Arch -> agent-ready dev setup")


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
) -> None:
    """Print ordered Plan. Never mutates."""
    try:
        steps = build_plan(run_checks(), only=only)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2)
    typer.echo(render_plan(steps))


@app.command()
def bootstrap(
    only: str | None = typer.Option(None, "--only", help="Only one step"),
    dry_run: bool = typer.Option(True, "--dry-run/--execute"),
) -> None:
    """Preview Plan (default) or execute one Step with --only X --execute."""
    try:
        steps = build_plan(run_checks(), only=only)
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2)
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
    typer.echo(f"would run: {target['fix_hint']}")
    typer.echo(f"verify: re-running check for {target['name']} (re-run `aab check` after install)")


if __name__ == "__main__":
    app()
