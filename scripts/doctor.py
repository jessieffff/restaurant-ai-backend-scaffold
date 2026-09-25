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
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return True


def main() -> int:
    checks = [
        ("Python 3.11-3.13", (3, 11) <= sys.version_info[:2] < (3, 14)),
        ("Git", command_succeeds(["git", "--version"])),
        ("Docker", command_succeeds(["docker", "--version"])),
        ("Docker Compose", command_succeeds(["docker", "compose", "version"])),
        ("Ollama", command_succeeds(["ollama", "--version"])),
        (".env", Path(".env").is_file()),
    ]

    failed = False
    for name, passed in checks:
        status = "ok" if passed else "missing"
        print(f"[{status}] {name}")
        failed = failed or not passed

    if failed:
        print("Resolve missing requirements before Session 1.")
        return 1

    print("Environment is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
