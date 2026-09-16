# Overlay: Grok grok-4.6

<!-- model_identity: {"kind":"hosted","provider":"xai","model_id":"grok-4.6","provider_version":null,"pinned":false,"confidence":"reduced"} -->

Loop review-of-review. Do not use for grok-4.5.

- Headless. No mid-run questions. Complete CONFIRM or CHALLENGE.
- Goal: check the Fable verdict against the same round diff and evidence.
- Do not fix product code.
- `pipe.py grok-file` with this model's default unless the header says otherwise.
