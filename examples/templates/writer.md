# Overlay: Codex gpt-6-astra

<!-- model_identity: {"kind":"hosted","provider":"openai","model_id":"gpt-6-astra","provider_version":null,"pinned":false,"confidence":"reduced"} -->

Loop only. Do not use for Sol or Terra.

- Goal, Context, Constraints, Done when (implement, focused tests, inspect, fix, handoff).
- Persist until that bar. Do not stop at a first patch or a plan.
- Name `$skill` explicitly when a product skill applies.
- Point to docs only for this change. Do not dump a doc stack.
- If the model pauses, quote the blocking instruction on resume.
- Effort: `xhigh`.

# Writer: #<ISSUE> <TITLE>

You are Codex (`gpt-6-astra`, `xhigh`). Implement only GitHub issue #<ISSUE>.
Do not commit. Do not push. Do not start any other issue.

HEAD `<HEAD>`. Do not edit loop-seat files (`CLAUDE.md`, Cursor rules).
No pull request unless the human said so.

Issue: https://github.com/<OWNER>/<REPO>/issues/<ISSUE>
Body: `.devloop/issue-<ISSUE>-body.md`
The GitHub issue body is the closed contract. The checker will judge
the diff against that issue. Do not reopen it from another notes file.

## Goal

Match the closed issue body.

## Context

The pick is decided. Restate the closed binding. No new skill unless
the issue says so.

## Binding (do not re-derive, do not stop on this fork)

Repeat every mechanical pin from the issue body.

## Constraints

- Proof as in the issue done-list.
- Docs + changelog.

## Done when

Implement, focused tests, inspect, fix, handoff
`.devloop/<ISSUE>-handoff.md`.
Persist until that bar.
Stop.
