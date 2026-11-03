# EXP-019: Context-Preserving Query Repair

## Goal

Test whether restoring the missing production qualifier repairs the hard-distractor failure.

## Before

Ambiguous query:

```text
What is the incremental backup cadence for Borealis?
```

Ranking:

```text
manual_borealis_staging  0.665681
manual_borealis          0.650305
```

Result:

```text
AnswerCorrect = 0.0000
```

## After

Context-preserving query:

```text
What is the incremental backup cadence for the production Borealis service?
```

Ranking:

```text
manual_borealis          0.716131
manual_borealis_staging  0.675785
```

Result:

```text
HopAccuracy      = 1.0000
ExactChainMatch  = 1.0000
FactAccuracy     = 1.0000
AnswerCorrect    = 1.0000
```

## Interpretation

Adding the missing qualifier reversed the ranking.

This strongly supports the hypothesis that the previous failure was caused primarily by information loss between hops rather than insufficient dense retrieval recall.

## Limitation

The production qualifier was still manually written into the hop-3 query template.

The next experiment extracts that qualifier from hop-2 evidence and carries it forward in structured retrieval state.
