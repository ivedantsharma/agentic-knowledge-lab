# ADR-015: Retrieval Policy SFT Requires Measured Labels, Leakage Control, and Class Balance

## Status

Accepted.

## Context

Phase 11 attempted to learn retrieval actions using Qwen2.5-0.5B-Instruct with LoRA.

Early experiments showed three distinct failure modes:

1. frozen-model default-action bias,
2. invalid inherited paraphrase labels,
3. majority-class collapse during SFT.

## Evidence

### Frozen baseline

EXP-101:

```text
format compliance=1.0000
action accuracy=0.0000
```

The model understood the protocol but not the policy.

### Paraphrase instability

EXP-107 showed:

```text
Cirrus:
  lexical  -> K2
  semantic -> K1

Solstice:
  lexical  -> K1
  semantic -> K2
```

Therefore labels are query-specific.

### Leakage control

EXP-108 constructed evidence-family-disjoint splits.

### Majority-class collapse

EXP-109:

```text
after SFT:
all train/dev/heldout predictions -> K1
heldout accuracy=0.0000
```

### Balanced sampling

EXP-110:

```text
train accuracy=0.9091
dev accuracy=1.0000
heldout accuracy=0.6667
```

with multi-action predictions restored.

## Decision

Future retrieval-policy SFT experiments must:

1. independently measure oracle labels for each query,
2. keep shared evidence families within one split,
3. report class distribution,
4. prevent dominant-class shortcuts through balanced sampling or an equivalent controlled method,
5. evaluate prediction distribution in addition to accuracy and loss.

## Rejected alternatives

### Inherit labels across paraphrases

Rejected because query wording changes retrieval ranking and minimal useful k.

### Random example-level splitting

Rejected because near-duplicate queries and shared evidence can leak across splits.

### Judge SFT by training loss alone

Rejected because EXP-109 achieved lower loss while learning a degenerate all-K1 policy.

### Continue hyperparameter tuning on the tiny dataset

Rejected because data coverage remains the dominant limitation.

## Consequence

Phase 12 should treat the learned policy as a baseline and optimize trajectory-level utility with explicit rewards rather than continue static-label tuning alone.
