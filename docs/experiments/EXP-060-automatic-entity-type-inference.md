# EXP-060: Automatic Lexical Entity-Type Inference

## Research question

Can explicit type cues in the mention replace the oracle entity-type label from EXP-059 while preserving semantic entity-link accuracy and abstention?

## Controlled change

EXP-059:

```text
gold entity type
→ type-constrained semantic ranking
→ threshold
```

EXP-060:

```text
lexically inferred entity type
→ type-constrained semantic ranking
→ same threshold
```

Keep fixed:

- MiniLM,
- entity profiles,
- mention-focused semantic ranking,
- threshold = 0.39,
- graph.

## Type cues

Examples:

```text
team / group / squad
→ team

service / system / platform / application
→ service
```

Ambiguous or missing type cues cause abstention.

## Metrics

- TypeInferenceAccuracy
- ResolvableEntityAccuracy
- AbstentionAccuracy
- FalsePositiveResolutionRate

## Why deterministic type inference first?

The graph currently uses only two coarse entity types.

A small explicit cue system is easier to diagnose than introducing another model.

If this baseline fails on paraphrased type language, semantic or learned type inference can be justified later.
