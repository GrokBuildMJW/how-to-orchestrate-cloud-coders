# Overlay: Grok grok-4.6

<!-- model_identity: {"kind":"hosted","provider":"xai","model_id":"grok-4.6","provider_version":null,"pinned":false,"confidence":"reduced"} -->

Loop review-of-review. Do not use for grok-4.5.

- Headless. No mid-run questions. Complete CONFIRM or CHALLENGE.
- Goal: check the Fable verdict against the same round diff and evidence.
- Do not fix product code.
- `pipe.py grok-file` with this model's default unless the header says otherwise.

# Second look: #<ISSUE> <TITLE>

You check the checker. Verdict must be CONFIRM or CHALLENGE only.
Do not fix anything. Do not re-run the test suite.

Writer gpt-6-astra, session `<SESSION>`.
Uncommitted on HEAD `<HEAD>`.
No pull request. Do not start the next ticket.

Issue: https://github.com/<OWNER>/<REPO>/issues/<ISSUE>
Body: `.devloop/issue-<ISSUE>-body.md` (closed; GitHub matches)
Checker output: `.devloop/review-<ISSUE>-claude-fable-5-1-out.txt`
Handoff: `.devloop/<ISSUE>-handoff.md`
Independent verify: `.devloop/verify-<ISSUE>-independent.txt`

Re-check the checker's verdict against the same round and the closed
issue body. Do not start a second product review. Do not reopen a fork
the human already closed.

## Pin (do not weaken)

<PASTE THE WHOLE CLOSED ISSUE BODY, including every done checkbox.>

Stop.
