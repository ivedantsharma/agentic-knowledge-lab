# EXP-057: Mention-Span Semantic Entity Ranking

## Research question

Does embedding only the entity-reference span improve semantic entity linking compared with embedding the full question?

## Motivation

EXP-056 found:

```text
SemanticHit@1=0.5000
SemanticHit@3=1.0000
```

The failure was:

```text
question:
"Which service is maintained by the infrastructure reliability group?"

whole-question top-1:
Borealis

gold start entity:
Platform Reliability
```

The whole question describes both the entity mention and the requested answer.

## Controlled change

Keep fixed:

- graph,
- entity profiles,
- embedding model,
- cosine similarity,
- positive/negative task concepts.

Change only the text embedded for entity linking:

```text
full question
→ gold entity-mention span
```

## Oracle caveat

The mention span is supplied manually.

Therefore EXP-057 does not solve mention extraction.

It isolates whether mention-focused semantic representation fixes the ranking problem.

## Metrics

- WholeQuestionHit@1
- MentionSpanHit@1
- MentionSpanHit@3
- positive mention top scores
- negative mention top scores

## Interpretation

If mention-span Hit@1 improves substantially, the primary failure is query representation / mention isolation.

If the intended entity still ranks poorly, the entity profiles or embedding model are the more likely bottleneck.
