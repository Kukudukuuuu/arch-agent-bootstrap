"""TDD seam tests: CLI verbs only (+ executor manual-step guard), never internals."""
import json

from typer.testing import CliRunner

from aab.cli import app
from aab.executor import execute_step

runner = CliRunner()


def test_check_lists_tools():
    res = runner.invoke(app, ["check"])
    assert res.exit_code == 0
    for name in ["python", "node", "go", "gh", "git", "base-devel", "gh-auth"]:
        assert name in res.output


def test_check_json_step_shape():
    res = runner.invoke(app, ["check", "--json"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert isinstance(data, list)
    names = {d["name"] for d in data}
    assert {"python", "node", "go", "gh", "git", "base-devel", "gh-auth", "opencode-config", "fonts"} <= names
    for d in data:
        assert set(d) >= {"name", "wanted", "found", "ok", "fix_hint"}


def test_plan_prints_without_mutating():
    res = runner.invoke(app, ["plan"])
    assert res.exit_code == 0
    assert "skip" in res.output or "todo" in res.output


def test_plan_dry_run_flag_parity():
    res = runner.invoke(app, ["plan", "--dry-run"])
    assert res.exit_code == 0
    assert "skip" in res.output or "todo" in res.output


def test_plan_only_filters():
    res = runner.invoke(app, ["plan", "--only", "go"])
    assert res.exit_code == 0
    assert "go" in res.output
    assert "python" not in res.output


def test_plan_only_base_devel():
    res = runner.invoke(app, ["plan", "--only", "base-devel"])
    assert res.exit_code == 0
    assert "base-devel" in res.output


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


def test_bootstrap_execute_ready_step_skips():
    # go is ready on this host: safe, no mutation
    res = runner.invoke(app, ["bootstrap", "--only", "go", "--execute"])
    assert res.exit_code == 0
    assert "skip go" in res.output or "already ready" in res.output


def test_executor_manual_step_does_not_run():
    rc, out = execute_step({"name": "opencode", "fix_hint": "see https://opencode.ai/docs"})
    assert rc == 2
    assert "manual" in out
