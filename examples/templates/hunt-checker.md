# Overlay: Claude claude-fable-5-1 (hunt)

<!-- model_identity: {"kind":"hosted","provider":"anthropic","model_id":"claude-fable-5-1","provider_version":null,"pinned":false,"confidence":"reduced"} -->

Hunt seat only. Do not use for Opus.

- Use the coverage catalog in the hunt template (adapted to this product; the shipped table is one real-world example). Ticket may Omit or Focus rows.
- Lead with the outcome (count + highest severity). Numbered findings: ID, severity, `file:line`, evidence, suggested follow-up as a later writer ticket.
- Finding blocks, not PASS/BLOCK or CONFIRM/CHALLENGE. Do not explain inner reasoning.
- Do not implement. Do not write product code or tests. Do not start a test suite.
- Persist a hunt handoff and a finding table on disk.
- Effort: `xhigh`.
- The model that hunted a round does not review that round.
- Default hunt confirmer uses the **checker** overlay, not this file.
  Dispatch this hunt overlay only when the ticket names
  `Second-voice: fable hunt`.

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

## Constraints

Follow the hunt overlay. Work independently of the other hunt voice.
Do not implement. Do not emit PASS or BLOCK.

## Done when

Handoff lists every catalog ID with one status. Table columns:
ID | Severity | Location | Evidence | Suggested follow-up.
Lead with count and highest severity. Stop.
