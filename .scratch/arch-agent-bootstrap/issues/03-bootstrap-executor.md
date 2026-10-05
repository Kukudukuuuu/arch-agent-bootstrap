# 03: Bootstrap executor + docs

**What to build:** `aab bootstrap --dry-run` previews; `aab bootstrap --only <step> --execute` runs one safe Step and re-verifies; README demo works end-to-end.

**Blocked by:** 02: Plan verb with dry-run

**Status:** ready-for-agent

- [ ] `aab bootstrap --dry-run` equals `plan` output, changes nothing
- [ ] `aab bootstrap --only base-devel --execute` runs only in explicit mode, verifier re-checks
- [ ] README 60-second demo + tests all pass
