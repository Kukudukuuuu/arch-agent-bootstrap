"""Bootstrap executor: runs one Step's fix command, then re-verifies via Checks."""
from __future__ import annotations

import subprocess


def execute_step(step: dict) -> tuple[int, str]:
    """Run step['fix_hint'] unless manual/advisory. Returns (returncode, output)."""
    fix = step.get("fix_hint", "")
    if not fix or fix.startswith("see ") or "advisory" in fix:
        return 2, f"manual step: {fix or 'no fix recorded'}"
    try:
        out = subprocess.run(fix, shell=True, capture_output=True, text=True, timeout=300)
        tail = (out.stdout or "") + (out.stderr or "")
        return out.returncode, tail.strip()[-2000:] or f"exit {out.returncode}"
    except Exception as e:  # noqa: BLE001 — report, don't raise, at CLI seam
        return 1, str(e)
