# Overlay: Codex gpt-6-astra (hunt)

<!-- model_identity: {"kind":"hosted","provider":"openai","model_id":"gpt-6-astra","provider_version":null,"pinned":false,"confidence":"reduced"} -->

Hunt seat only. Do not use for Sol or Terra.

- Goal, Context, Constraints, Done when (map findings, persist handoff, stop).
- Use the coverage catalog in the hunt template (adapted to this product; the shipped table is one real-world example). Ticket may Omit or Focus rows.
- Produce numbered findings: ID, severity, `file:line`, evidence, suggested follow-up as a later writer ticket.
- Do not implement. Do not write product code or tests. Do not start a test suite.
- Use findings, not PASS/BLOCK or CONFIRM/CHALLENGE.
- Persist a hunt handoff and a finding table on disk.
- Effort: `xhigh`.
- The model that hunted a round does not review that round.
- Default round: this seat hunts; Fable then checks the handoff with
  the **checker** overlay (not this hunt overlay). A second hunter
  only if the ticket names `Second-voice: fable hunt`.

# Hunt: #<ISSUE> <TITLE>

English only. Fill Omit/Focus from the closed ticket. Silence is not omit.

Issue: https://github.com/<OWNER>/<REPO>/issues/<ISSUE>

## Goal

Map evidence-backed findings. Persist the hunt handoff and table, then stop.

## Default coverage (this is the boundary)

**This table is an example from one real product.** Copy the hunt
template into your repo, then rewrite every row so the IDs, areas,
and “what to examine” match **that** product. A catalog aimed at
another codebase is a defect. Do not hunt with this example list
unchanged.

The operator must not be the only source of scope **after** the
catalog is adapted. Hunt every row unless the ticket lists
`Omit: H-…` and/or `Focus: H-…`. Focus still records every
non-focused ID as `omitted-by-issue`. Unnamed rows stay in scope.

For each ID record exactly one status: `wired` | `missing-call` |
`logic-defect` | `omitted-by-issue` | `not-examined` (with `file:line`
why). Declared site versus consumer.

| ID | Area | What to examine |
|---|---|---|
| H-CLI | Command line and serve | entrypoints that start the product |
| H-HTTP | HTTP API | published routes versus server handlers versus clients |
| H-UI | UI or TUI commands | command names versus the HTTP or engine calls they should make |
| H-PROC | Process / workflow graph | steps, refusal, position |
| H-ORCH | Orchestration / dispatch | pipeline, scheduler, operate |
| H-DOM | Domain objects | lifecycle, store, agents |
| H-FND | Foundation | events, config, paths |
| H-EXEC | Execution | tools, sandbox |
| H-LLM | Model client | overlays, calibration |
| H-SKILL | Skills | registry versus install versus dispatch |
| H-MEM | Memory / learning | write versus read versus routing |
| H-AUTH | Auth / doctor / board | routes and callers |
| H-TEST | Tests that still assert a dead seam | read assertions only; do not start pytest |

Do not add installers/OS packs unless the ticket Focuses them.

Ticket may add declared paths under each ID. Empty path on the ticket
does not drop the ID.

## Default defect classes (example — rewrite with the catalog)

Same rule: this table is from one real product. Empty Class-Omit and
Class-Focus means every **default** class below, not only fail-closed
wiring. Opt-in classes stay out unless Class-Focus names them.

Default:

| ID | Class | Hunt looks for |
|---|---|---|
| D-MISS | missing-call | Declaration without consumer |
| D-FC | fail-closed invert | Refusal that cannot run, or error path that proceeds |
| D-STALE | stale assertion | Test or docs that still assert a removed seam |
| D-SPEC | spec drift | Published API, handler, and client disagree |
| D-ORPHAN | emit/consume orphan | Event emitted with no reader, or reader with no emit |
| D-JOIN | missing join | Two writes for one fact, no join |
| D-GATE | missing sibling gate | Path open; a sibling has a lock this one lacks |
| D-DEFAULT | default-open | Missing check means allow |

Opt-in (Class-Focus only): D-IDEM idempotency, D-RACE shared mutable
without lock, D-SECRET secret in the tree.

Coverage account: `H-ID | D-ID | Status | Evidence`.
Status: `wired` | `finding` | `omitted-by-issue` | `not-examined`.
`wired` means a consumer exists, not “correct”.

## Constraints

Follow the hunt overlay. Do not implement. Do not invent an operator pick.
Suggested writer tickets are recommendations only.

## Done when

Handoff lists every catalog ID with one status. Table columns:
ID | Severity | Location | Evidence | Suggested follow-up.
Zero findings is valid only if every non-omitted ID is `wired` or
`not-examined` with evidence. Stop.
