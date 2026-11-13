# EXP-111 — Result: Retrieval Rewards and Trajectories

## Validation
- 278 tests passed
- Ruff checks passed
- MiniLM weights loaded; unauthenticated HF warning was nonfatal

## Actual corpus and ranking
```text
task=route-003
ranked_top5=[
  kbv2-doc-cirrus-contradiction,
  kbv2-doc-cirrus-manual,
  kbv2-doc-cumulus-retry,
  kbv2-doc-cirrus-org,
  kbv2-doc-borealis-stale
]
```

## Actual results
```text
SEARCH_K1 → STOP:
  rewards=[-0.10, -1.00]
  return=-1.10

SEARCH_K1 → SEARCH_K2 → STOP:
  rewards=[-0.10, +1.90, +1.00]
  return=+2.80
```

## Conclusion
The deterministic environment correctly rewards newly retrieved evidence, charges incrementally for documents, and penalizes a premature STOP on this controlled query. It does not demonstrate policy learning.

## Follow-up issue
At k=2 the retrieved context contains both the pending Cirrus revision and the authoritative current manual. The +2.80 reward verifies gold-document presence, not contradiction resolution or answer correctness. Reward validity needs separate adversarial/termination auditing before policy optimization.
