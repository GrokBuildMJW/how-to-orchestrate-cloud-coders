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
