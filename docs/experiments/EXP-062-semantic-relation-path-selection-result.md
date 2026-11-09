# EXP-062 Result: Semantic Relation-Path Selection

## Aggregate

```text
tasks=4
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
AvgCandidatePaths=2.00
```

## Main result

Semantic path ranking selected the correct structurally valid route for all four tasks.

The strongest stress case was Atlas:

```text
correct production-storage path: 0.782214
legacy-storage distractor:        0.755725
snapshot distractor:              0.673707
```

The correct path won, but its margin over the legacy-storage distractor was only approximately:

```text
0.0265
```

## Interpretation

Graph structure constrains the search space to valid paths, and semantic ranking can select among those paths on this synthetic benchmark.

However, the small Atlas margin shows that semantically similar neighboring routes remain a realistic failure mode.

## Caveat

The start entity remained oracle-provided in EXP-062.

EXP-063 integrates entity resolution with path selection and traversal.
