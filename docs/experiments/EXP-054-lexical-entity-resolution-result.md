# EXP-054 Result: Lexical Entity Resolution + Gold Relation Path

## Aggregate

```text
EntityLinkAccuracy=1.0000
EntityResolutionFailureRate=0.0000
AnswerAccuracy=1.0000
PathAccuracy=1.0000
ProvenanceCoverage=1.0000
```

## Interpretation

All four Phase 3-derived questions contain the intended start entity explicitly by canonical name.

The lexical resolver correctly links all four and the downstream deterministic graph traversal remains perfect.

## What this establishes

The graph can now be accessed from natural-language questions when the start entity appears as an exact registered surface.

## What this does not establish

The benchmark does not yet test:

- aliases,
- overlapping entity names,
- implicit entity references,
- unregistered paraphrases,
- misspellings,
- ambiguous mentions.

EXP-055 therefore stress-tests the resolver before introducing semantic entity linking.
