# EXP-057: Gold Mention Span vs Whole-Question Semantic Ranking

## Research question

Is EXP-056's semantic entity error caused by weak entity semantics, or by embedding the entire question instead of the entity mention?

## Controlled change

Keep fixed:

- graph,
- entity profiles,
- MiniLM model,
- cosine similarity,
- ranking procedure.

Change only:

```text
semantic query = full question
```

to:

```text
semantic query = gold entity mention span
```

## Examples

```text
full question:
"What is the backup cadence of the customer-profile storage platform?"

gold mention:
"customer-profile storage platform"
```

and:

```text
full question:
"Which service is maintained by the infrastructure reliability group?"

gold mention:
"infrastructure reliability group"
```

## Metrics

- FullQuestionHit@1
- GoldMentionHit@1
- per-task gold rank

## Interpretation

If gold mention ranking fixes the Platform Reliability error, the problem is mention localization / entity role.

If it still fails, the entity profiles or embedding model are insufficient.

## Important limitation

The mention span is oracle-provided in this experiment.

Success would not solve entity linking end to end.

It would isolate the next missing capability:

```text
question → entity mention detection
```
