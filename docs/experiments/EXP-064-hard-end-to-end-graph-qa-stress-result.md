# EXP-064 Result: Hard End-to-End Hybrid Claim-Graph QA Stress

## Aggregate

```text
tasks=6
AnswerableEndToEndSuccessRate=0.5000
EntityResolutionAccuracy=0.5000
PathSelectionAccuracy=0.5000
AnswerAccuracy=0.5000
ProvenanceCoverage=0.5000
AbstentionAccuracy=0.5000
FalsePositiveAnswerRate=0.5000
```

## Successful cases

### Explicit entity + branching path

Atlas resolved lexically and selected the intended Borealis production-storage path.

```text
path_score_margin=0.026488
```

### Implicit service

The production customer-profile storage description resolved semantically to Borealis and returned:

```text
every six hours
```

## Answerable failures

Two implicit team questions abstained before path search.

### Customer-profile storage team

```text
semantic entity score=0.356677
threshold=0.390000
```

### Asynchronous worker team

```text
semantic entity score=0.287011
threshold=0.390000
```

These are entity-confidence failures.

They are not path-selection failures.

## Abstention failures

The unrelated employee-travel team question produced:

```text
false_positive_entity=platform_reliability
false_positive_answer='every six hours'
```

This demonstrates that a semantically plausible but wrong graph entry can produce a fully coherent downstream answer.

## Conditional path interpretation

Among answerable tasks where an entity was successfully resolved:

```text
resolved answerable tasks=2
correct paths=2
correct answers=2
correct provenance=2
```

Therefore the aggregate 0.5000 path/answer metrics are downstream consequences of entity-resolution failures.

## Research conclusion

The current bottleneck is:

```text
implicit entity resolution
+ confidence / abstention
```

not graph traversal.

The fixed global cosine threshold is not robust enough across team/service paraphrases.

Do not retune the threshold on this benchmark.
