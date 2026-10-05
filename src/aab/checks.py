"""Checks: read-only Host probes. Never mutates."""
from __future__ import annotations

import os
import shutil
import subprocess

WANTED = [
    # (name, kind, probe, fix_hint)
    # kind: "binary" = which <binary> + version cmd; "command" = shell rc==0; "file" = path exists
    ("python", "binary:python3", "python3 --version", "sudo pacman -S --needed python"),
    ("node", "binary:node", "node --version", "sudo pacman -S --needed nodejs"),
    ("go", "binary:go", "go version", "sudo pacman -S --needed go"),
    ("gh", "binary:gh", "gh --version", "sudo pacman -S --needed github-cli"),
    ("opencode", "binary:opencode", "opencode --version", "see https://opencode.ai/docs"),
    ("git", "binary:git", "git --version", "sudo pacman -S --needed git"),
    ("base-devel", "command", "pacman -Qi base-devel", "sudo pacman -S --needed base-devel"),
    ("gh-auth", "command", "gh auth status", "gh auth login"),
    ("opencode-config", "file", "~/.config/opencode", "create ~/.config/opencode/ (manual; never auto-modified)"),
    ("fonts", "command", "fc-list", "install a Nerd Font (advisory only)"),
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
    for name, kind, probe, fix in WANTED:
        if kind.startswith("binary:"):
            binary = kind.split(":", 1)[1]
            found = shutil.which(binary) is not None
            version = _version(probe) if found else None
            ok = found and version is not None
        elif kind == "command":
            version = _version(probe)
            ok = version is not None
            found = True  # probe ran; readiness reported via ok
        elif kind == "file":
            path = os.path.expanduser(probe)
            found = os.path.exists(path)
            version = path if found else None
            ok = found
        else:
            raise ValueError(f"unknown probe kind: {kind}")
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
