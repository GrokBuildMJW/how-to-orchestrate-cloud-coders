# Copy-paste pack

Read the [iron rules](../README.md#iron-rules) first. The orchestrator
session never implements coding. It never writes a review verdict.
Cursor mini-agents are never the writer or the checker. If a template
or a call would break those rules, do not paste it.

This folder is the practical half of the guide. The root README is the
story: which cloud coder does which job, how Cursor steers them, and
how a fallback works. These files are what you copy.

There are no secrets here. There are no personal home paths. Each
overlay is the first page of a letter. If a letter does not start with
the overlay for the model you are about to call, the helper will
refuse to start the program.

Read this page once. After that, you mostly copy an overlay, fill a
template, and paste a call from [`dispatch.md`](dispatch.md).

## What each path is for

| Path | What it is | What you do |
|---|---|---|
| `overlays/overlay-<program>-<model>.md` | Letterhead for the default job | Copy into the product as `.devloop/` with the **same** file names |
| `overlays/overlay-<program>-<model>-<role>.md` | Letterhead for architecture or hunt | Call with `--role architecture` or `--role hunt`. Missing file = refuse |
| `templates/issue-body.md` | GitHub ticket shape | One closed decision. No leftover “A or B”. Every checker rule is a checkbox |
| `templates/writer.md` | Astra writer letter | Overlay already at the top. Swap overlay + flags for Sol or Terra |
| `templates/checker.md` | Fable checker letter | Paste the **whole** closed ticket under Pin |
| `templates/second-look.md` | Grok 4.6 second look | CONFIRM or CHALLENGE only |
| `templates/architecture-writer.md` | Astra architecture letter | `--role architecture`. Does not implement |
| `templates/architecture-checker.md` | Fable architecture letter | No PASS/BLOCK. Fill IDs |
| `templates/hunt-writer.md` | Astra hunt letter | Example catalog + class table — rewrite for **this** product; `--role hunt` |
| `templates/hunt-confirm.md` | Fable on hunt **files** | Checker overlay, no `--role hunt`. Default confirmer |
| `templates/hunt-checker.md` | Fable as **second hunter** | Hunt overlay. Only if the ticket names `Second-voice: fable hunt` |
| `dispatch.md` | Live call lines | Fill `IN` / `OUT`. Always name the model. Role jobs name `--role` |

`scripts/pipe.py` lives one folder up. It is the teaching helper. It
refuses a letter that does not start with the matching overlay
(including `--role` files), then writes a JSON stamp as the first
line of the output. That stamp is what the call asked for. Who
actually ran is the transcript header under it.

`scripts/letter.py` copies overlay + template to a live letter and
checks the first page. No tokens. Placeholders look like `<ISSUE>`.

Do not copy product API keys, `gh` tokens, or machine-specific config
into this pack.

## How a first round is assembled

You do not start with the call. You start with the ticket.

1. Write the GitHub issue from `templates/issue-body.md` until the
   decision is closed. If a done-box still says “A vs B”, stop.
2. Copy `templates/writer.md`. Keep the Astra overlay at the top unless
   this round is a Sol or Terra fallback. Fill the issue number and
   the HEAD. Point at the issue body on disk.
3. Copy `templates/checker.md`. Keep the Fable overlay at the top.
   Under Pin, paste the ticket **verbatim**, including every checkbox.
4. When you need a second look, copy `templates/second-look.md`. Keep
   the Grok 4.6 overlay. Point it at the checker output file, not at a
   summary of the checker.
5. Call through `pipe.py` using the matching block in `dispatch.md`.

A fallback is the same assembly with a different overlay, a different
letter path, and a different call. It is not a search-and-replace on
the model flag.

## Overlays you must not mix

Each overlay file is one identity. The filename is
`overlay-<program>-<model>.md`. The `model_identity` comment inside
must match the `--model` (or Codex `-c model=`) on the call.

- Codex Astra, Sol, and Terra are three files.
- Claude Fable 5.1, the short `fable` alias, and Opus are three files.
  The `fable` alias is a different name and needs `overlay-claude-fable.md`,
  not the Fable 5.1 file.
- Grok 4.6 and Grok 4.5 are two files.
- Kimi k3 and Kimi k2.5 are two files.

If you are not sure which page to use, do not guess. Open the overlay
folder and pick the file whose model id is the one on the call line.
