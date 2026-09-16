"""No network. No tokens. Overlay admit and letter assembly only."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPE = ROOT / "scripts" / "pipe.py"
LETTER = ROOT / "scripts" / "letter.py"
OVERLAYS = ROOT / "examples" / "overlays"
TEMPLATES = ROOT / "examples" / "templates"


def run(argv: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *argv],
        cwd=str(ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_writer_template_starts_with_astra_overlay() -> None:
    overlay = (OVERLAYS / "overlay-codex-gpt-6-astra.md").read_text(encoding="utf-8").rstrip()
    letter = (TEMPLATES / "writer.md").read_text(encoding="utf-8")
    assert letter.startswith(overlay + "\n")


def test_letter_check_writer() -> None:
    completed = run(
        [
            str(LETTER),
            "check",
            "--harness",
            "codex",
            "--model",
            "gpt-6-astra",
            str(TEMPLATES / "writer.md"),
        ]
    )
    assert completed.returncode == 0, completed.stderr


def test_letter_check_hunt_role() -> None:
    completed = run(
        [
            str(LETTER),
            "check",
            "--harness",
            "codex",
            "--model",
            "gpt-6-astra",
            "--role",
            "hunt",
            str(TEMPLATES / "hunt-writer.md"),
        ]
    )
    assert completed.returncode == 0, completed.stderr


def test_writer_letter_refuses_hunt_role() -> None:
    env = os.environ.copy()
    env["LOOP_OVERLAY_DIR"] = str(OVERLAYS)
    completed = run(
        [
            str(LETTER),
            "check",
            "--harness",
            "codex",
            "--model",
            "gpt-6-astra",
            "--role",
            "hunt",
            str(TEMPLATES / "writer.md"),
        ],
        env=env,
    )
    assert completed.returncode == 2
    assert "does not start with this model's overlay" in completed.stderr


def test_letter_new_fills_placeholder() -> None:
    with tempfile.TemporaryDirectory() as raw:
        out = Path(raw) / "live.md"
        completed = run(
            [
                str(LETTER),
                "new",
                "--harness",
                "codex",
                "--model",
                "gpt-6-astra",
                "--template",
                str(TEMPLATES / "writer.md"),
                "--out",
                str(out),
                "--set",
                "ISSUE=1",
                "--set",
                "TITLE=demo",
            ]
        )
        assert completed.returncode == 0, completed.stderr
        text = out.read_text(encoding="utf-8")
        assert "Implement only GitHub issue #1" in text
        assert "# Writer: #1 demo" in text


def test_hunt_confirm_uses_checker_overlay_not_hunt() -> None:
    checker = (OVERLAYS / "overlay-claude-claude-fable-5-1.md").read_text(
        encoding="utf-8"
    ).rstrip()
    hunt = (OVERLAYS / "overlay-claude-claude-fable-5-1-hunt.md").read_text(
        encoding="utf-8"
    ).rstrip()
    letter = (TEMPLATES / "hunt-confirm.md").read_text(encoding="utf-8")
    assert letter.startswith(checker + "\n")
    assert not letter.startswith(hunt + "\n")


def test_hunt_template_contains_catalog() -> None:
    text = (TEMPLATES / "hunt-writer.md").read_text(encoding="utf-8")
    assert "example from one real product" in text
    assert "D-MISS" in text
    assert "Class-Focus" in text or "Class-Omit" in text or "default class" in text
    for row in (
        "H-CLI",
        "H-HTTP",
        "H-UI",
        "H-PROC",
        "H-ORCH",
        "H-DOM",
        "H-FND",
        "H-EXEC",
        "H-LLM",
        "H-SKILL",
        "H-MEM",
        "H-AUTH",
        "H-TEST",
    ):
        assert row in text


def test_pipe_help() -> None:
    completed = run([str(PIPE), "pipe", "-h"])
    assert completed.returncode == 0
    assert "--role" in completed.stdout


if __name__ == "__main__":
    tests = [
        test_writer_template_starts_with_astra_overlay,
        test_letter_check_writer,
        test_letter_check_hunt_role,
        test_writer_letter_refuses_hunt_role,
        test_letter_new_fills_placeholder,
        test_hunt_confirm_uses_checker_overlay_not_hunt,
        test_hunt_template_contains_catalog,
        test_pipe_help,
    ]
    for fn in tests:
        fn()
        print("ok", fn.__name__)
    print("passed", len(tests))
