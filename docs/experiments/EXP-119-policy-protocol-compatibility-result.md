# EXP-119 Result — Phase 11 / Phase 12 Compatibility Audit

## Configuration
Join 12 real routing tasks to their Phase 11 SFT source-task records, verify exact question matches, compute minimal BM25 support budgets using existing `BM25Retriever` on the same 22 documents, and compare **budget labels** and split metadata. This is NOT trained SFT model inference.

## Validated
GitHub CI on merged EXP-119: **380 tests passed**, Ruff passed, and the full audit driver was exercised by a real-file smoke test in pytest. The separate full user-local audit stdout has not yet been supplied.

## Observed protocol differences
- Phase 11: supervised Qwen/LoRA, `SEARCH_HYBRID_K1/2/3/5` and `REFORMULATE`, exact action accuracy, Phase 11 heldout Meridian.
- Phase 12: sequential tabular REINFORCE, `SEARCH_K1/2/3/5` and `STOP`, discounted trajectory reward, EXP-118 BM25 heldout **all non-Cirrus** families.
- The four K action labels can be mapped by *name*, not by ranking or semantic equivalence; STOP and REFORMULATE have no counterparts.
- Cirrus route-003 has Phase 11 Hybrid target K2 but BM25 minimal K1. Solstice route-006 has Phase 11 Hybrid target K2 but BM25 minimal K3.

## Conclusion
Direct LoRA-versus-REINFORCE score comparisons are **invalid** without a common retriever, action/state protocol, data splits, same evaluation reward and actual saved-model inference. This is a compatibility audit; neither model's superiority was established.

## Reproduce
```bash
uv run python scripts/run_phase12_policy_protocol_audit.py
```
The full command output remains to be archived in addition to passing driver smoke tests.
