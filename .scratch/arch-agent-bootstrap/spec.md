## Problem Statement

Fresh Arch installs take hours to become agent-ready: python/node/go/gh/opencode, auth, editor config, fonts, Docker. Steps are scattered across wiki pages and dotfiles. Repros fail on a second machine.

## Solution

`aab` CLI with three verbs: `check` (read-only Host report), `plan` (ordered Plan with `--dry-run` default), `bootstrap` (execute missing Steps, verify each). Idempotent: re-running on an agent-ready Host is a no-op.

## User Stories

1. As an Arch user, I want `check` to report installed/missing tools with versions, so that I know what blocks agent work.
2. As an Arch user, I want `plan --dry-run` to print the ordered Steps without changing my Host, so that I can review before running.
3. As an Arch user, I want `bootstrap` to install only missing Steps and verify each, so that re-runs are safe.
4. As an Arch user, I want `bootstrap --only <step>` to run one Step, so that I can fix incrementally.
5. As a newcomer, I want a README with 60-second demo, so that I can evaluate in one minute.
6. As a contributor, I want `check --json` machine output, so that scripts can consume it.

## Implementation Decisions

- Modules: Checks (probes), Plan (ordering + filtering), Bootstrap (executor + verifier). CLI is thin adapter over them.
- Checks never mutate; Bootstrap never probes directly — it consumes Check results.
- Step model: `name`, `wanted`, `found`, `ok`, `fix_hint`. Executor maps Step → shell action; verifier re-runs Check.
- Seam under test: CLI verbs (`check`, `plan`, `bootstrap --dry-run`). Internals untested directly.
- Out-of-box Steps: python, node, go, gh-auth, opencode-config, base-devel+git, fonts/terminal (advisory only).

## Testing Decisions

- Good test = invoke CLI via runner, assert exit code + user-visible output, never internals.
- Prior art: Typer `CliRunner` tests.
- Coverage: check reports missing tool; plan lists steps in order; bootstrap dry-run changes nothing; `--only` filters; `--json` parses.

## Out of Scope

- Real installs touching the Host in tests (mocked); actual `pacman -S` execution only via explicit `bootstrap` without `--dry-run` on real Host; TUI; daemon; network version checks; multi-distro support.

## Further Notes

- Niche: Arch + AI-agent setup. Dogfood on author's own Host.
