#!/usr/bin/env python3
"""Minimal Claude Code status line used by bingo-skills setup.

Reads Claude Code status JSON from stdin and prints one compact line.
All optional fields are tolerated; no credentials or network access are used.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import subprocess
import sys


def get(obj, *path, default=None):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur if cur is not None else default


def branch_for(cwd: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "branch", "--show-current"],
            check=False,
            capture_output=True,
            text=True,
            timeout=0.2,
        )
        branch = result.stdout.strip()
        if branch:
            return branch
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            timeout=0.2,
        )
        sha = result.stdout.strip()
        return sha or None
    except Exception:
        return None


def pct_left(used):
    try:
        value = float(used)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    return max(0.0, min(100.0, 100.0 - value))


def fmt_pct(value) -> str | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return f"{max(0.0, min(100.0, number)):.0f}%"


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    pieces: list[str] = []

    model = get(data, "model", "display_name") or get(data, "model", "id")
    effort = get(data, "effort", "level")
    if model:
        pieces.append(f"{model}{(' ' + str(effort)) if effort else ''}")

    remaining = get(data, "context_window", "remaining_percentage")
    if remaining is None:
        used = get(data, "context_window", "used_percentage")
        remaining = pct_left(used)
    remaining_text = fmt_pct(remaining)
    if remaining_text:
        pieces.append(f"ctx {remaining_text} left")

    cwd = (
        get(data, "workspace", "current_dir")
        or get(data, "cwd")
        or os.getcwd()
    )
    cwd_path = Path(str(cwd)).expanduser()
    pieces.append(cwd_path.name or str(cwd_path))
    branch = branch_for(str(cwd_path))
    if branch:
        pieces.append(branch)

    # Not currently guaranteed by Claude's statusline payload. Never infer
    # live permissions from settings defaults or the process environment.
    permissions = get(data, "permission_mode")
    if isinstance(permissions, str) and permissions.strip():
        pieces.append(f"permissions {permissions.strip()}")

    if pieces:
        print(" · ".join(pieces))


if __name__ == "__main__":
    main()
