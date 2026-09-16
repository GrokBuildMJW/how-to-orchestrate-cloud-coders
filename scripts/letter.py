#!/usr/bin/env python3
"""Assemble a live letter from an overlay plus a template.

No tokens. No home paths. The template must already start with the
overlay bytes, or you pass --overlay and --body to concatenate.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from pipe import (  # noqa: E402
    UTF8,
    ascii_punct,
    load_overlay,
    overlay_name,
    require_letterhead,
    write_utf8,
)


def _die(message: str, code: int = 2) -> None:
    sys.stderr.write(message + "\n")
    raise SystemExit(code)


def _read(path: Path) -> str:
    if not path.is_file():
        _die(f"letter: missing file {path}")
    text = ascii_punct(path.read_text(encoding=UTF8))
    return text.replace("\r\n", "\n").replace("\r", "\n")


def assemble(overlay: str, body: str) -> str:
    overlay = overlay.rstrip()
    body = body.lstrip("\n")
    if body.startswith(overlay):
        return body if body.endswith("\n") else body + "\n"
    return overlay + "\n\n" + body.lstrip() + (
        "" if body.endswith("\n") else "\n"
    )


def fill(text: str, replacements: list[str]) -> str:
    for item in replacements:
        if "=" not in item:
            _die(f"letter: --set needs NAME=value, got {item!r}")
        name, value = item.split("=", 1)
        if not name or any(ch in name for ch in "/\\"):
            _die("letter: bad placeholder name")
        text = text.replace("<" + name + ">", value)
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Assemble or check a letter (overlay + template)."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_new = sub.add_parser("new", help="Write OUT from overlay + template.")
    p_new.add_argument("--harness", required=True, choices=("codex", "claude", "grok", "kimi"))
    p_new.add_argument("--model", required=True)
    p_new.add_argument("--role")
    p_new.add_argument("--template", required=True, help="Template path (may already include overlay).")
    p_new.add_argument("--out", required=True)
    p_new.add_argument("--set", dest="replacements", action="append", default=[])
    p_check = sub.add_parser("check", help="Refuse unless IN starts with the overlay.")
    p_check.add_argument("--harness", required=True, choices=("codex", "claude", "grok", "kimi"))
    p_check.add_argument("--model", required=True)
    p_check.add_argument("--role")
    p_check.add_argument("--seat")
    p_check.add_argument("infile")
    args = parser.parse_args(argv)

    if args.cmd == "new":
        overlay = load_overlay(args.harness, args.model, args.role)
        body = fill(_read(Path(args.template)), args.replacements)
        letter = assemble(overlay, body)
        require_letterhead(letter, args.harness, args.model, args.role)
        write_utf8(Path(args.out), letter)
        print(overlay_name(args.harness, args.model, args.role), "->", args.out)
        return 0
    require_letterhead(
        _read(Path(args.infile)),
        args.harness,
        args.model,
        args.role,
        args.seat,
    )
    print("ok", overlay_name(args.harness, args.model, args.role))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
