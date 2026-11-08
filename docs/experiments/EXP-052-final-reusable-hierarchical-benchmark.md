# Phase 5 Final Integrated Benchmark

## Purpose

Verify that the accepted Phase 5 policy still works after moving it from experiment scripts into the reusable retrieval module.

## Component under test

```text
knowledge_engine/retrieval/coarse_to_fine.py
```

## Benchmark

```text
data/processed/phase5_long_section_documents_v0.json
data/processed/phase5_long_section_tasks_v0.json
```

## Result

```text
tasks=3
EvidenceRetentionRate=1.0000
AvgReturnedWindowWords=43.33
```

## Per-task behavior

### Atlas

Selected parents:

```text
distractor_atlas_long
manual_alpha_long
```

The final Atlas window contains:

```text
ATLAS-KV-104
```

Evidence retained: true.

### Borealis

Selected parents:

```text
distractor_borealis_long
manual_beta_long
```

The final Borealis window contains:

```text
every six hours
```

Evidence retained: true.

### Cirrus

Selected parents:

```text
distractor_cirrus_long
manual_gamma_long
```

The final Cirrus window contains:

```text
CIRRUS-DLQ
```

Evidence retained: true.

## Candidate accounting

Per query:

```text
parent candidates scored = 6
section candidates scored = 3
retained sections = 2
chunk candidates scored = 13, 13, 15
```

## Comparison to EXP-051

The reusable component reproduces the EXP-051 output:

```text
EvidenceRetentionRate=1.0000
AvgReturnedWindowWords=43.33
```

This is important because the final result is no longer dependent on experiment-specific retrieval logic.

## Conclusion

The Phase 5 research policy has successfully transitioned from experimental code into a reusable retrieval component without regression on the final stress benchmark.
