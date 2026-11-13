# EXP-112 — Result: Reward Validity and Termination Audit

## Validation
- 282 tests passed
- Ruff all checks passed

## Frozen Cirrus ranking
```text
1. kbv2-doc-cirrus-contradiction (pending, non-effective revision)
2. kbv2-doc-cirrus-manual (authoritative current policy)
```

## Trajectories
```text
A early STOP:         reward=-1.10 coverage=0.0 conflict_exposure=1
B complete STOP:      reward=+2.80 coverage=1.0 conflict_exposure=1
C forced timeout:     reward=-0.10 coverage=0.0 conflict_exposure=1
D explicit early STOP: reward=-1.10 coverage=0.0 conflict_exposure=1
```

## Conclusions
- V1 reward correctly measures gold evidence coverage and retrieval cost.
- V1 reward allows an incomplete timeout to avoid the early-STOP penalty.
- The high-reward complete trajectory includes an exposed pending, conflicting revision; evidence presence alone is not correct answer interpretation.
- Conflict exposure is a diagnostic, **not** proof that the agent answered incorrectly.
- Hidden gold labels used in scoring are never policy-visible.

## Decision
Introduce opt-in reward v2, preserving v1 semantics for reproducibility. Penalize incomplete forced termination at the same rate as an explicit premature STOP. Do not automatically penalize conflicting document retrieval until evidence resolution is evaluated.
