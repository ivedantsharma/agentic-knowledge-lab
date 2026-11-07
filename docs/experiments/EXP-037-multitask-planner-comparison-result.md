# EXP-037 Result: Multi-Task Planner Comparison

## Aggregate results

| Metric | Rule-based | Semantic | Hybrid |
|---|---:|---:|---:|
| Answer Accuracy | 0.8000 | 0.8000 | 0.4000 |
| Planner Failure Rate | 0.2000 | 0.0000 | 0.0000 |
| Stopped Rate | 0.8000 | 1.0000 | 0.6000 |
| Stop Precision | 1.0000 | 0.8000 | 0.6667 |
| Premature Stop Rate | 0.0000 | 0.0000 | 0.2000 |
| Search Success Rate | 0.8000 | 1.0000 | 0.4000 |
| Average Search Steps | 2.0000 | 2.4000 | 3.6000 |
| Max-Step Exhaustion Rate | 0.0000 | 0.0000 | 0.4000 |

## Main conclusion

The hybrid planner is not yet the strongest overall planner.

It expands capability to the unseen dead-letter relation, but it regresses on multiple known-intent tasks.

Therefore the correct conclusion is:

```text
hybrid increases open-ended capability
but decreases trajectory reliability
```

not:

```text
hybrid is generally superior
```

## Failure analysis

### mh-001 — backup

After retrieving `org_atlas`, structured state contained:

```text
entity = Platform Reliability
```

The generative planner ignored that intermediate entity and asked directly about Atlas backup cadence.

It then became trapped on the Atlas deployment-snapshot distractor.

Result:

```text
max-step exhaustion
final evidence not retrieved
```

### mh-002 — retry count

After retrieving `org_dev_productivity`:

```text
entity = Cirrus
qualifier = production
```

The generated query became only:

```text
Cirrus worker platform
```

This repeatedly retrieved the same organization document rather than the production manual.

Result:

```text
retrieval loop
max-step exhaustion
```

### mh-003 — cache duration

The generated query successfully jumped to the Solstice manual.

Result:

```text
correct
```

### mh-004 — signing rotation

Structured state contained:

```text
entity = Meridian
qualifier = production
```

The generated query:

```text
Meridian rotating signing keys
```

dropped the production qualifier.

The development manual ranked first and the verifier correctly judged the answer relation, but could not know that the retrieved environment was wrong.

Result:

```text
premature STOP on wrong environment
```

### ood-001 — unseen dead-letter relation

The hybrid planner succeeded.

This is the key positive capability result.

## Diagnosis

The main hybrid weakness is not relation verification.

It is **continuation-query state preservation**.

The planner receives the original question and raw evidence, but the query-generation prompt does not explicitly include:

- current entity,
- qualifiers,
- structured intermediate state.

This recreates the information-loss problem identified in Phase 3.

## Next experiment

Preserve structured state explicitly in the generative continuation prompt while changing no other component.
