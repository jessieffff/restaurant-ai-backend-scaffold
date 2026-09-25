from collections.abc import Sequence
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from scripts import doctor


def test_later_tools_do_not_block_session_one(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("", encoding="utf-8")

    def command_succeeds(command: Sequence[str]) -> bool:
        return command[0] not in {"gh", "ollama"}

    monkeypatch.setattr(doctor, "command_succeeds", command_succeeds)

    assert doctor.main() == 0
    output = capsys.readouterr().out
    assert "[later] GitHub CLI authentication (required by Session 3)" in output
    assert "[later] Ollama (required by Session 6)" in output
    assert "Core environment is ready." in output


def test_missing_docker_blocks_session_one(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("", encoding="utf-8")

    def command_succeeds(command: Sequence[str]) -> bool:
        return command[:2] != ["docker", "info"]

    monkeypatch.setattr(doctor, "command_succeeds", command_succeeds)

    assert doctor.main() == 1
    output = capsys.readouterr().out
    assert "[missing] Docker daemon" in output
    assert "Resolve missing core requirements before Session 1." in output
