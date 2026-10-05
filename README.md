# arch-agent-bootstrap

One-command Arch → agent-ready dev setup. Niche: Arch Linux + AI coding agents.

## 60-second demo

```bash
python3 -m venv .venv && .venv/bin/pip install typer pytest
PYTHONPATH=src .venv/bin/python -m pytest -q        # 7 passed
PYTHONPATH=src .venv/bin/python -m aab.cli check    # host report
PYTHONPATH=src .venv/bin/python -m aab.cli plan     # dry-run plan, changes nothing
PYTHONPATH=src .venv/bin/python -m aab.cli bootstrap --only go --execute
```

## Skills used (mattpack)

grill-with-docs → to-spec → to-tickets → implement (tdd) → code-review → pr → retro. Spec in `.scratch/arch-agent-bootstrap/spec.md`, tickets in `.scratch/arch-agent-bootstrap/issues/`.
