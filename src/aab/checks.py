"""Checks: read-only Host probes. Never mutates."""
from __future__ import annotations

import shutil
import subprocess

WANTED = [
    ("python", "python3 --version", "sudo pacman -S --needed python"),
    ("node", "node --version", "sudo pacman -S --needed nodejs"),
    ("go", "go version", "sudo pacman -S --needed go"),
    ("gh", "gh --version", "sudo pacman -S --needed github-cli"),
    ("opencode", "opencode --version", "see https://opencode.ai/docs"),
    ("git", "git --version", "sudo pacman -S --needed git base-devel"),
]


def _version(cmd: str) -> str | None:
    try:
        out = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        if out.returncode != 0:
            return None
        line = (out.stdout or out.stderr).strip().splitlines()
        return line[0].strip() if line else "installed"
    except Exception:
        return None


def run_checks() -> list[dict]:
    results = []
    for name, probe, fix in WANTED:
        binary = name if name != "python" else "python3"
        found = shutil.which(binary) is not None
        version = _version(probe) if found else None
        ok = found and version is not None
        results.append(
            {
                "name": name,
                "wanted": probe,
                "found": found,
                "version": version,
                "ok": bool(ok),
                "fix_hint": "" if ok else fix,
            }
        )
    return results
