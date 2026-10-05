# 01: CLI skeleton + check verb

**What to build:** `aab check` reports Host state (each wanted tool: found/missing + version + fix hint) in human and `--json` form.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] `aab check` exits 0 and lists python/node/go/gh/opencode with ok/missing
- [ ] `aab check --json` outputs parseable JSON with same data
- [ ] Checks never mutate the Host
