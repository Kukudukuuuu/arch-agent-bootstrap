# arch-agent-bootstrap

One command to turn a fresh Arch Linux install into an AI-agent-ready dev machine.

`aab` probes your host, prints an ordered plan, and installs only what's missing — safely re-runnable, dry-run by default.

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Typer](https://img.shields.io/badge/cli-typer-green) ![Tests](https://img.shields.io/badge/tests-11%20passed-brightgreen) ![Arch](https://img.shields.io/badge/distro-arch-blue)

## Why this exists

Fresh Arch installs take hours to become agent-ready: `python` / `node` / `go` / `github-cli` / `base-devel`, `gh auth login`, opencode config, fonts. The steps are scattered across wiki pages and dotfiles, and re-running someone's install script on a second machine is a gamble.

`aab` fixes that with three verbs:

| Command | What it does | Mutates? |
|---|---|---|
| `aab check` | Reports 10 probes with versions | Never |
| `aab plan` | Prints ordered `skip`/`todo` plan | Never |
| `aab bootstrap` | Previews by default; `--only X --execute` runs one step and re-verifies | Only with `--execute` |

## 60-second demo

```bash
git clone https://github.com/Kukudukuuuu/arch-agent-bootstrap.git
cd arch-agent-bootstrap
python3 -m venv .venv && .venv/bin/pip install typer pytest
export PYTHONPATH=src

.venv/bin/python -m pytest -q            # 11 passed
.venv/bin/python -m aab.cli check        # host report
.venv/bin/python -m aab.cli plan         # dry-run plan, changes nothing
.venv/bin/python -m aab.cli bootstrap --only go --execute
```

Example output on a ready machine:

```text
✓ python: Python 3.14.7
✓ node: v22.23.2
✓ go: go version go1.27.1
✓ gh: gh version 2.100.0
✓ opencode: opencode v2.0.23
✓ git: git version 2.55.0
✓ base-devel: Installed From: core
✓ gh-auth: github.com
✓ opencode-config: /home/you/.config/opencode
✓ fonts: JetBrainsMono-ExtraBold.ttf ...
```

## What it checks

| Step | Probe | Fix (only run with `--execute`) |
|---|---|---|
| `python` | `python3 --version` | `sudo pacman -S --needed python` |
| `node` | `node --version` | `sudo pacman -S --needed nodejs` |
| `go` | `go version` | `sudo pacman -S --needed go` |
| `gh` | `gh --version` | `sudo pacman -S --needed github-cli` |
| `opencode` | `opencode --version` | manual (see https://opencode.ai/docs) |
| `git` | `git --version` | `sudo pacman -S --needed git` |
| `base-devel` | `pacman -Qi base-devel` | `sudo pacman -S --needed base-devel` |
| `gh-auth` | `gh auth status` | `gh auth login` (interactive) |
| `opencode-config` | `~/.config/opencode` exists | manual, never auto-modified |
| `fonts` | `fc-list` | advisory only |

## Usage

```bash
# Human-readable report
.venv/bin/python -m aab.cli check

# Machine-readable (for scripts)
.venv/bin/python -m aab.cli check --json | jq '.[] | select(.ok == false)'

# Plan everything, or just one step
.venv/bin/python -m aab.cli plan
.venv/bin/python -m aab.cli plan --only base-devel
.venv/bin/python -m aab.cli plan --only gh-auth

# Preview (default, safe) vs execute (one step at a time)
.venv/bin/python -m aab.cli bootstrap                  # same as plan
.venv/bin/python -m aab.cli bootstrap --only git --execute
```

Safety rules:

- `bootstrap` without flags is a dry-run — it prints and exits.
- Full `--execute` without `--only` is refused. One step at a time.
- Already-ready steps print `✓ skip <name>: already ready` and run nothing.
- Manual/advisory steps (`opencode`, `fonts`) are never auto-run — the tool tells you what to do instead.
- After each executed step, the probe re-runs to verify. Unverified → exit 1.

## Project structure

```text
src/aab/
├── checks.py    # read-only Host probes (the only place that touches the system)
├── plan.py      # pure ordering: Checks → Plan (no I/O)
├── executor.py  # runs one step's fix command, then re-verifies
└── cli.py       # thin Typer adapter: check / plan / bootstrap
tests/
└── test_cli.py  # 11 CLI-seam tests (no internals, no Host mutation)
```

## Development

```bash
export PYTHONPATH=src
.venv/bin/python -m pytest -q          # run tests
.venv/bin/python -m aab.cli check     # dogfood on your own host
```

Conventions: `GLOSSARY.md` defines the domain language (Host, Check, Plan, Step, Bootstrap, Dry-run, Agent-ready); decisions live in `docs/adr/`; the spec and tracer-bullet tickets live in `.scratch/arch-agent-bootstrap/`.

## Roadmap

- [ ] `install` non-interactive mode for containers (`--yes` + log file)
- [ ] `doctor --fix` for common drift (stale `gh` token, missing Nerd Font)
- [ ] AUR helper detection (`yay`/`paru`) for opencode updates
- [ ] Shell completions (`aab --install-completion`)

## Contributing

Issues and PRs welcome. Keep slices vertical (one CLI-visible behaviour per PR with a test), and update `GLOSSARY.md` when you add domain terms.
