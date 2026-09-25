#!/usr/bin/env bash

set -euo pipefail

select_python() {
  local candidate
  local -a candidates

  if [[ -n "${PYTHON_BIN:-}" ]]; then
    candidates=("${PYTHON_BIN}")
  else
    candidates=(python3.12 python3.13 python3.11 python3)
  fi

  for candidate in "${candidates[@]}"; do
    if command -v "${candidate}" >/dev/null 2>&1 \
      && "${candidate}" -c 'import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)'
    then
      printf '%s\n' "${candidate}"
      return 0
    fi
  done

  printf '%s\n' "Python 3.11, 3.12, or 3.13 is required." >&2
  return 1
}

python_bin="$(select_python)"

if [[ ! -d .venv ]]; then
  if ! "${python_bin}" -m venv .venv; then
    printf '%s\n' \
      "Unable to create .venv. On Debian, Ubuntu, or WSL, install the matching python3-venv package." \
      >&2
    exit 1
  fi
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

printf '%s\n' "Bootstrap complete."
printf '%s\n' "Next: make doctor && make check"
