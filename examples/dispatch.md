# Live call shapes

The [iron rules](../README.md#iron-rules) still apply here. These calls
are how the *other* seats work. They are not how the Cursor
orchestrator session writes code or issues PASS/BLOCK.

This page is the call book. The root README explains why each cloud
coder has its job. Here you copy the line that starts that job.

Copy these. Fill `IN` / `OUT` / the ticket number. Run from the product
repo root. Always name the model. Always put the matching overlay at
the top of `IN`.

Helper: `python scripts/pipe.py` (copy from this repo). Overlay folder:
`.devloop/` or `LOOP_OVERLAY_DIR`.

A fallback is a different call: different prompt file, different
overlay, different flags. Do not keep the default letter and only
change `--model`.

The helper stamp on the first line of `OUT` is what this call asked
for. Who actually ran is the program’s transcript header under that
stamp. If those disagree, throw the round away.

---

## Writer, default (Astra)

Astra is the usual writer. High effort (`xhigh`). It should stay until
the ticket’s done-list is met. The trailing `-` means Codex reads the
letter from stdin, which is what `pipe.py` feeds.

```
python scripts/pipe.py pipe --seat coding IN OUT -- \
  codex exec -c model="gpt-6-astra" -c model_reasoning_effort="xhigh" \
  -c sandbox_mode="danger-full-access" -c approval_policy="never" -
```

Resume only this same Astra session. Flags are not inherited. If you
omit sandbox or effort on resume, the writer wakes up somewhere it
cannot run tests.

```
python scripts/pipe.py pipe --seat coding IN OUT -- \
  codex exec resume <session-id> -c model="gpt-6-astra" -c model_reasoning_effort="xhigh" \
  -c sandbox_mode="danger-full-access" -c approval_policy="never" -
```

A broken Codex models-cache load can silently answer as Terra at
medium effort. If the transcript header is not Astra, throw the round
away and start a new letter.

---

## Writer fallback (own letter, own effort)

Use these only for mechanical work: re-render something already
defined, a rename with no behavior change, formatting. New logic, a
semantic proof, architecture *implementation*, and every fix after
BLOCK or CHALLENGE stay on Astra.

Sol and Terra each need their own overlay at the top of `IN-sol` /
`IN-terra`. Do not reuse Astra’s “stay until done” page. Sol effort
is `high`. Terra effort is `medium`.

```
python scripts/pipe.py pipe --seat coding IN-sol OUT-sol -- \
  codex exec -c model="gpt-5.6-sol" -c model_reasoning_effort="high" \
  -c sandbox_mode="danger-full-access" -c approval_policy="never" -

python scripts/pipe.py pipe --seat coding IN-terra OUT-terra -- \
  codex exec -c model="gpt-5.6-terra" -c model_reasoning_effort="medium" \
  -c sandbox_mode="danger-full-access" -c approval_policy="never" -
```

Resume only a session for the same model, with that model’s letter and
the complete flags above. A model switch is a fresh call.

---

## Checker (Fable)

Fable is the checker. One checker. PASS or BLOCK only. Paste the whole
closed GitHub ticket into the letter.

```
python scripts/pipe.py pipe --seat review IN OUT -- \
  claude -p --model claude-fable-5-1 --effort xhigh
```

### Last resort: Opus

Only when Fable cannot run. Own overlay, own letter, own output file.
Never start on Opus.

```
python scripts/pipe.py pipe --seat review IN-opus OUT-opus -- \
  claude -p --model opus --effort xhigh
```

The `fable` alias is a different name and needs its own overlay file
`overlay-claude-fable.md`, not the Fable 5.1 file.

### Local exception: two Claude wallets

This is not a second checker. On our machine we have two Claude
subscriptions, so the binary is sometimes `sub1` or `sub2` instead of
`claude` (still Fable, still the same overlay). Use that only when one
wallet is empty. Do not jump to Opus because one wallet is empty.
`pipe.py` accepts those names. One login: keep `claude`.

```
python scripts/pipe.py pipe --seat review IN OUT -- sub1 -p --model claude-fable-5-1 --effort xhigh
python scripts/pipe.py pipe --seat review IN OUT -- sub2 -p --model claude-fable-5-1 --effort xhigh
```

---

## Second look

Grok 4.6 re-reads the checker against the same round and the same
ticket. CONFIRM or CHALLENGE only. It does not fix product code.

Run it after a genuine coding review, and on every BLOCK, *before* the
next writer letter. Skip it only on a fact-only PASS, and write
`RoR: skipped (fact-only round)` on the close comment. When unsure,
run it.

```
python scripts/pipe.py grok-file --seat review_of_review --model grok-4.6 IN OUT
```

Optional third voice. Each letter must say the other is running
independently in parallel, so neither waits.

```
python scripts/pipe.py kimi-p --seat review_of_review --model kimi-k3 IN OUT
```

Grok 4.5 and Kimi k2.5 are separate letters (`overlay-grok-grok-4.5.md`,
`overlay-kimi-kimi-k2.5.md`). Do not keep a 4.6 letter and only change
`--model`.

---

## Ticket body from a file

The helper also posts UTF-8 issue text so a ticket does not pick up
the wrong encoding from the shell.

```
python scripts/pipe.py gh-comment <issue> PATH
python scripts/pipe.py gh-edit <issue> PATH
```

Close the ticket body **before** the writer starts. Do not dispatch a
done-list that still contains a “vs”.

---

## Architecture (not the writer page)

Fable and Astra in parallel. Each letter starts with the **architecture**
overlay. `--role architecture`. Do not send the writer overlay.

Assemble:

```
python scripts/letter.py new --harness claude --model claude-fable-5-1 --role architecture \
  --template examples/templates/architecture-checker.md --out IN-arch-fable \
  --set ISSUE=N --set TITLE=topic --set OWNER=org --set REPO=name

python scripts/letter.py new --harness codex --model gpt-6-astra --role architecture \
  --template examples/templates/architecture-writer.md --out IN-arch-astra \
  --set ISSUE=N --set TITLE=topic --set OWNER=org --set REPO=name
```

```
python scripts/pipe.py pipe --seat review --role architecture IN-arch-fable OUT-arch-fable -- \
  claude -p --model claude-fable-5-1 --effort xhigh

python scripts/pipe.py pipe --seat coding --role architecture IN-arch-astra OUT-arch-astra -- \
  codex exec -c model="gpt-6-astra" -c model_reasoning_effort="xhigh" \
  -c sandbox_mode="read-only" -c approval_policy="never" -
```

If the architecture voice must write a handoff file, give Codex write
access in a **new** letter. Do not keep the architecture overlay and
only change sandbox.

---

## Hunt (one hunter, then Fable on the artifacts)

This is how a hunt round is run: **Astra hunts once**. Fable does
**not** walk the tree again. Fable checks the hunt handoff against
the closed ticket (PASS or BLOCK), using the **checker** letterhead,
not the hunt letterhead.

Architecture still uses two independent voices. Hunt does not, unless
the ticket explicitly says `Second-voice: fable hunt`.

The catalog and class tables in `hunt-writer.md` are **one real
product’s example**. Rewrite both tables for the tree you are hunting
before the first hunt letter. Then the ticket may Omit/Focus areas
and Class-Omit/Class-Focus classes. Silence is not omit. Empty class
fields mean every **default** class, not only fail-closed wiring.
Opt-in classes (idempotency, races, secrets) stay out unless named.

Effort stays `xhigh`. Do not invent `ultra`.

Assemble and run the hunter:

```
python scripts/letter.py new --harness codex --model gpt-6-astra --role hunt \
  --template examples/templates/hunt-writer.md --out IN-hunt-astra \
  --set ISSUE=N --set TITLE=topic --set OWNER=org --set REPO=name

python scripts/pipe.py pipe --seat coding --role hunt IN-hunt-astra OUT-hunt-astra -- \
  codex exec -c model="gpt-6-astra" -c model_reasoning_effort="xhigh" \
  -c sandbox_mode="danger-full-access" -c approval_policy="never" -
```

When `.devloop/N-hunt-coding.md` and `-hunt-coding-table.md` exist,
confirm (no `--role hunt`):

```
python scripts/letter.py new --harness claude --model claude-fable-5-1 \
  --template examples/templates/hunt-confirm.md --out IN-hunt-confirm \
  --set ISSUE=N --set TITLE=topic --set OWNER=org --set REPO=name

python scripts/pipe.py pipe --seat review IN-hunt-confirm OUT-hunt-confirm -- \
  claude -p --model claude-fable-5-1 --effort xhigh
```

Skip the Grok second look on a hunt confirm unless Fable BLOCKed.
The hunter does not confirm its own hunt.

Optional second hunter (only if the ticket names it):
`examples/templates/hunt-checker.md`, `--seat review --role hunt`,
then a cross-check AGREE/DISAGREE on findings — not the default.

---

## After yes

Commit product files only. Tick every done-box on the ticket. Comment
the snapshot id. Close. Do not leave landed boxes unchecked. Do not
mix loop files or Cursor settings into that commit.

If the transcript header under the stamp disagrees with the model on
the call, there is no yes. Throw the round away. New letter. New
overlay. New call.
