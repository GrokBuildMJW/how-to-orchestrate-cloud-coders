#!/usr/bin/env python3
"""UTF-8 dispatch helper for Cursor as the assigner, not the writer.

No product imports. No tokens. Looks up grok/kimi on PATH only.
Refuses a letter whose first page is not the selected model's overlay
(with --role: overlay-<program>-<model>-<role>.md).
Writes a JSON stamp, then the program's output, to the outfile.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

UTF8 = "utf-8"
LOOP_ROLES = (
    "coding",
    "review",
    "review_of_review",
    "bundle_review",
    "architecture",
    "kreuz",
    "hunt",
)
SEATS = ("coding", "review", "review_of_review", "bundle_review")
UTF16_LE_BOM = b"\xff\xfe"
UTF16_BE_BOM = b"\xfe\xff"
UTF8_BOM = b"\xef\xbb\xbf"

PUNCT = {
    "\u2014": "-",
    "\u2013": "-",
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
    "\u2192": "->",
    "\u00a0": " ",
}


def _die(message: str, code: int = 2) -> None:
    sys.stderr.write(message + "\n")
    raise SystemExit(code)


def decode_bytes(raw: bytes, origin: str) -> str:
    if raw.startswith(UTF16_LE_BOM) or raw.startswith(UTF16_BE_BOM):
        return raw.decode("utf-16")
    if raw.startswith(UTF8_BOM):
        raw = raw[len(UTF8_BOM) :]
    try:
        return raw.decode(UTF8)
    except UnicodeDecodeError as exc:
        _die(f"pipe: {origin} is not UTF-8 or UTF-16: {exc}")
    raise AssertionError("unreachable")


def ascii_punct(text: str) -> str:
    for src, dst in PUNCT.items():
        text = text.replace(src, dst)
    return text


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        ascii_punct(text).replace("\r\n", "\n").replace("\r", "\n"),
        encoding=UTF8,
        newline="\n",
    )


def ensure_file(path: Path) -> str:
    if not path.is_file():
        _die(f"pipe: missing file {path}")
    text = decode_bytes(path.read_bytes(), str(path))
    write_utf8(path, text)
    return path.read_text(encoding=UTF8)


def env_utf8() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def overlay_dirs() -> list[Path]:
    named = os.environ.get("LOOP_OVERLAY_DIR")
    dirs = []
    if named:
        dirs.append(Path(named))
    dirs.append(Path.cwd() / ".devloop")
    here = Path(__file__).resolve().parents[1] / "examples" / "overlays"
    dirs.append(here)
    return dirs


def overlay_name(harness: str, model: str, role: str | None = None) -> str:
    suffix = f"-{role}" if role else ""
    return f"overlay-{harness}-{model}{suffix}.md"


def load_overlay(harness: str, model: str, role: str | None = None) -> str:
    name = overlay_name(harness, model, role)
    for folder in overlay_dirs():
        path = folder / name
        if path.is_file():
            return ascii_punct(path.read_text(encoding=UTF8)).replace("\r\n", "\n").rstrip()
    _die(
        f"pipe: no overlay file {name} "
        "(set LOOP_OVERLAY_DIR or copy examples/overlays)"
    )
    raise AssertionError("unreachable")


def check_loop_seats(overlay: str, seat: str | None) -> None:
    if not seat:
        return
    found = re.findall(r"<!-- loop_seats:\s*(.+?)\s*-->", overlay)
    if not found:
        return
    if len(found) != 1:
        _die("pipe: overlay needs at most one loop_seats comment")
    try:
        seats = json.loads(found[0])
    except json.JSONDecodeError as error:
        _die(f"pipe: loop_seats is not JSON: {error}")
    if not isinstance(seats, list) or seat not in seats:
        _die(f"pipe: seat {seat} is not in overlay loop_seats; use --role")


def require_letterhead(
    text: str,
    harness: str,
    model: str,
    role: str | None = None,
    seat: str | None = None,
) -> None:
    overlay = load_overlay(harness, model, role)
    if not text.startswith(overlay + "\n") and text.rstrip() != overlay:
        _die("pipe: letter does not start with this model's overlay")
    matches = re.findall(r"<!-- model_identity: (.+?) -->", overlay)
    if len(matches) != 1:
        _die("pipe: overlay needs exactly one model_identity comment")
    try:
        identity = json.loads(matches[0])
    except json.JSONDecodeError as error:
        _die(f"pipe: overlay identity is not JSON: {error}")
    if identity.get("model_id") != model:
        _die("pipe: overlay model_id does not match the call line")
    if role is None:
        check_loop_seats(overlay, seat)


def pipe_selection(argv: list[str]) -> tuple[str, str]:
    if not argv:
        _die("pipe: dispatch command is missing")
    executable = Path(argv[0]).stem.lower()
    harness = {"sub1": "claude", "sub2": "claude"}.get(executable, executable)
    if harness not in {"codex", "claude", "grok", "kimi"}:
        _die("pipe: first program must be codex, claude, grok, kimi, sub1, or sub2")
    models: list[str] = []
    for index, arg in enumerate(argv[1:], 1):
        if arg in {"--model", "-m"} and index + 1 < len(argv):
            models.append(argv[index + 1])
        elif arg.startswith("--model="):
            models.append(arg.split("=", 1)[1])
        elif arg in {"-c", "--config"} and index + 1 < len(argv):
            config = argv[index + 1]
            if config.startswith("model="):
                models.append(config.split("=", 1)[1].strip("\"'"))
    if len(models) != 1 or not models[0]:
        _die("pipe: exactly one explicit model selection is required")
    if harness == "codex" and argv[-1] != "-":
        _die("pipe: Codex must consume the letter on stdin (trailing -)")
    return harness, models[0]


def stamp(seat: str | None, harness: str, model: str, role: str | None = None) -> str:
    profile = seat or os.environ.get("LOOP_SEAT") or ""
    if role:
        profile = f"{profile}:{role}" if profile else role
    payload = {
        "seat": seat or os.environ.get("LOOP_SEAT") or "",
        "role": role or "",
        "harness": harness,
        "model": model,
        "model_profile": profile,
    }
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":")) + "\n"


def run_cmd(
    argv: list[str],
    infile: Path,
    outfile: Path,
    seat: str | None,
    role: str | None = None,
) -> int:
    text = ensure_file(infile)
    harness, model = pipe_selection(argv)
    require_letterhead(text, harness, model, role, seat)
    header = stamp(seat, harness, model, role)
    write_utf8(outfile, header)
    completed = subprocess.run(
        argv,
        input=text.encode(UTF8),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=str(Path.cwd()),
        env=env_utf8(),
        check=False,
    )
    write_utf8(outfile, header + decode_bytes(completed.stdout, " ".join(argv)))
    return completed.returncode


def which_exe(name: str) -> Path:
    found = shutil.which(name)
    if not found:
        _die(f"pipe: {name} is not on PATH")
    return Path(found)


def grok_file(
    infile: Path,
    outfile: Path,
    model: str | None,
    seat: str | None,
    role: str | None = None,
) -> int:
    text = ensure_file(infile)
    model = model or ""
    if not model:
        _die("pipe: grok-file needs --model")
    require_letterhead(text, "grok", model, role, seat)
    header = stamp(seat, "grok", model, role)
    argv = [
        str(which_exe("grok")),
        "--model",
        model,
        "--prompt-file",
        str(infile.resolve()),
        "--always-approve",
        "--cwd",
        str(Path.cwd()),
    ]
    completed = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=str(Path.cwd()),
        env=env_utf8(),
        check=False,
    )
    write_utf8(outfile, header + decode_bytes(completed.stdout, "grok"))
    return completed.returncode


def kimi_p(
    infile: Path,
    outfile: Path,
    model: str | None,
    seat: str | None,
    role: str | None = None,
) -> int:
    text = ensure_file(infile)
    model = model or ""
    if not model:
        _die("pipe: kimi-p needs --model")
    require_letterhead(text, "kimi", model, role, seat)
    header = stamp(seat, "kimi", model, role)
    completed = subprocess.run(
        [str(which_exe("kimi")), "--model", model, "-p", text],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=str(Path.cwd()),
        env=env_utf8(),
        check=False,
    )
    write_utf8(outfile, header + decode_bytes(completed.stdout, "kimi"))
    return completed.returncode


def gh_body(args: list[str], path: Path) -> None:
    ensure_file(path)
    completed = subprocess.run(
        ["gh", *args, "--body-file", str(path)],
        cwd=str(Path.cwd()),
        env=env_utf8(),
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UTF-8 dispatch for Cursor-assigned cloud jobs.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_pipe = sub.add_parser("pipe", help="Feed IN as UTF-8 stdin to CMD; write UTF-8 OUT.")
    p_pipe.add_argument("--seat", choices=SEATS)
    p_pipe.add_argument("--role", choices=LOOP_ROLES)
    p_pipe.add_argument("infile")
    p_pipe.add_argument("outfile")
    p_pipe.add_argument("argv", nargs=argparse.REMAINDER)
    p_grok = sub.add_parser("grok-file")
    p_grok.add_argument("--seat", choices=SEATS)
    p_grok.add_argument("--role", choices=LOOP_ROLES)
    p_grok.add_argument("--model")
    p_grok.add_argument("infile")
    p_grok.add_argument("outfile")
    p_kimi = sub.add_parser("kimi-p")
    p_kimi.add_argument("--seat", choices=SEATS)
    p_kimi.add_argument("--role", choices=LOOP_ROLES)
    p_kimi.add_argument("--model")
    p_kimi.add_argument("infile")
    p_kimi.add_argument("outfile")
    p_comment = sub.add_parser("gh-comment")
    p_comment.add_argument("issue")
    p_comment.add_argument("path")
    p_edit = sub.add_parser("gh-edit")
    p_edit.add_argument("issue")
    p_edit.add_argument("path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "pipe":
        rest = list(args.argv)
        if rest and rest[0] == "--":
            rest = rest[1:]
        if not rest:
            _die("pipe: missing command after outfile")
        return run_cmd(
            rest, Path(args.infile), Path(args.outfile), args.seat, args.role
        )
    if args.cmd == "grok-file":
        return grok_file(
            Path(args.infile), Path(args.outfile), args.model, args.seat, args.role
        )
    if args.cmd == "kimi-p":
        return kimi_p(
            Path(args.infile), Path(args.outfile), args.model, args.seat, args.role
        )
    if args.cmd == "gh-comment":
        gh_body(["issue", "comment", args.issue], Path(args.path))
        return 0
    if args.cmd == "gh-edit":
        gh_body(["issue", "edit", args.issue], Path(args.path))
        return 0
    _die(f"pipe: unknown command {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
