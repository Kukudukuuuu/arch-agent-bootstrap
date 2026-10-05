# 02: Plan verb with dry-run

**What to build:** `aab plan` turns Check results into an ordered Plan; default prints without executing; `--only` filters to one Step.

**Blocked by:** 01: CLI skeleton + check verb

**Status:** ready-for-agent

- [ ] `aab plan` prints ordered Steps with [skip]/[todo] based on Checks
- [ ] `aab plan --only go` prints only that Step
- [ ] `aab plan` changes nothing on the Host
