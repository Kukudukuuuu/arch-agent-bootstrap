"""TDD seam tests: CLI verbs only, never internals. Independent literals, no tautologies."""
import json

from typer.testing import CliRunner

from aab.cli import app

runner = CliRunner()


def test_check_lists_tools():
    res = runner.invoke(app, ["check"])
    assert res.exit_code == 0
    for name in ["python", "node", "go", "gh", "git"]:
        assert name in res.output


def test_check_json_parses():
    res = runner.invoke(app, ["check", "--json"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert isinstance(data, list)
    names = {d["name"] for d in data}
    assert {"python", "node", "go", "gh", "git"} <= names
    for d in data:
        assert set(d) >= {"name", "found", "ok", "fix_hint"}


def test_plan_prints_without_mutating():
    res = runner.invoke(app, ["plan"])
    assert res.exit_code == 0
    assert "skip" in res.output or "todo" in res.output


def test_plan_only_filters():
    res = runner.invoke(app, ["plan", "--only", "go"])
    assert res.exit_code == 0
    assert "go" in res.output
    assert "python" not in res.output


def test_plan_only_unknown_fails():
    res = runner.invoke(app, ["plan", "--only", "nope"])
    assert res.exit_code == 2


def test_bootstrap_dry_run_changes_nothing():
    plan = runner.invoke(app, ["plan"])
    boot = runner.invoke(app, ["bootstrap"])
    assert boot.exit_code == 0
    assert boot.output == plan.output


def test_bootstrap_execute_requires_only():
    res = runner.invoke(app, ["bootstrap", "--execute"])
    assert res.exit_code == 2
