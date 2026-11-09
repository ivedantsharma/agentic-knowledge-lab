# EXP-063 Result: End-to-End Explicit-Entity Claim-Graph QA

## Reported aggregate

```text
tasks=4
EntityLinkAccuracy=1.0000
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
ProvenanceCoverage=1.0000
```

All four explicit-name tasks resolved the correct start entity, selected the intended claim path, returned the expected answer, and preserved evidence provenance.

## Interpretation

This validates composition of:

```text
natural-language question
→ lexical entity linking
→ branching graph path selection
→ answer
→ provenance
```

on the existing four synthetic Phase 6 tasks.

## Version note

The user-reported output came from an older local runner revision and did not print the newer path-margin and EndToEndSuccessRate fields present in the current committed script.

The correctness metrics are still valid, but the latest runner should be used for final closeout reporting.

## Limitation

EXP-063 still requires an explicit registered entity surface in the question. EXP-064 tests a hybrid semantic fallback and abstention without supplying a gold mention span.
