# Glossary — arch-agent-bootstrap

Single-context. Use these terms everywhere (spec, tickets, code, tests).

- **Host**: the Arch Linux machine being set up.
- **Check**: read-only probe that reports state (installed / missing / version). Never mutates.
- **Plan**: ordered list of Steps derived from Checks + user selection.
- **Step**: one install/config action with `name`, `check`, `run`, `verify`.
- **Bootstrap**: turning a fresh Host into an agent-ready Host via a Plan.
- **Dry-run**: print the Plan without executing it.
- **Agent-ready**: Host has python, node, go, gh CLI (authed), opencode config, base dev tools.
