# Overlay: Grok grok-4.5

<!-- model_identity: {"kind":"hosted","provider":"xai","model_id":"grok-4.5","provider_version":null,"pinned":false,"confidence":"reduced"} -->

Loop review-of-review fallback. Do not reuse the 4.6 overlay.

- Headless. No mid-run questions. Complete CONFIRM or CHALLENGE.
- More explicit rubric than 4.6: list AC, tests, docs, and whether the reviewer cited evidence.
- Do not fix product code.
- Pass `--model grok-4.5` (or the header's slug). Do not keep 4.6 flags.
