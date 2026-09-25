from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path


def command_succeeds(command: Sequence[str]) -> bool:
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    return True


def main() -> int:
    required_checks = [
        ("Python 3.11-3.13", (3, 11) <= sys.version_info[:2] < (3, 14)),
        ("Git", command_succeeds(["git", "--version"])),
        ("Docker daemon", command_succeeds(["docker", "info"])),
        ("Docker Compose", command_succeeds(["docker", "compose", "version"])),
        (".env", Path(".env").is_file()),
    ]
    later_checks = [
        ("GitHub CLI authentication", 3, command_succeeds(["gh", "auth", "status"])),
        ("Ollama", 6, command_succeeds(["ollama", "--version"])),
    ]

    failed = False
    for name, passed in required_checks:
        status = "ok" if passed else "missing"
        print(f"[{status}] {name}")
        failed = failed or not passed

    for name, session, passed in later_checks:
        status = "ok" if passed else "later"
        print(f"[{status}] {name} (required by Session {session})")

    if failed:
        print("Resolve missing core requirements before Session 1.")
        return 1

    print("Core environment is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
