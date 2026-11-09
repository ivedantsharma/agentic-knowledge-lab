# EXP-070: Ambiguity as a First-Class Retrieval Challenge

## Research question

When a question is genuinely under-specified, can KnowledgeBench v2 represent the competing plausible interpretations and measure whether retrieval exposes them?

## Motivation

The Phase 7 benchmark already covers:

- multi-hop,
- distractors,
- stale knowledge,
- contradictions,
- unanswerable questions.

The remaining major taxonomy gap is ambiguity.

A plain unanswerable label is insufficient because it does not distinguish:

```text
no relevant evidence exists
```

from:

```text
multiple incompatible interpretations are plausible
```

## Schema change

Add:

```text
ambiguity_candidate_document_ids
```

These are documents corresponding to plausible competing interpretations of the same under-specified question.

## New metric

```text
AmbiguityCandidateCoverage@K
```

For an ambiguous task:

```text
retrieved ambiguity candidates
/
all annotated ambiguity candidates
```

This metric does not reward answering.

It measures whether retrieval exposes the ambiguity to a downstream verifier or agent.

## Seed ambiguity case

Question:

```text
What cache duration does Nimbus use?
```

Two equally plausible services exist:

```text
Nimbus Session Cache   → ten minutes
Nimbus Analytics Cache → thirty minutes
```

The question does not specify which Nimbus service is intended.

Therefore:

```text
should_answer=False
challenge_types={ambiguity, unanswerable}
```

## Versioning

Reported datasets remain unchanged.

New versions:

```text
knowledgebench_v2_seed_documents_v2.json
knowledgebench_v2_seed_tasks_v1.json
```

## Interpretation

High ambiguity-candidate coverage is useful because a downstream system can see the competing interpretations.

Returning only one plausible candidate may encourage unjustified confident answering.

EXP-070 evaluates retrieval exposure only; clarification/answer policy belongs to later phases.
