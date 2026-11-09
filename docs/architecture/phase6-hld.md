# Phase 6 High-Level Design

## Goal

Build a provenance-aware claim-graph retrieval system that can answer relationship-heavy questions by combining:

- explicit entities,
- typed relations,
- claim-level evidence,
- entity resolution,
- bounded graph-path search,
- semantic path ranking,
- abstention.

The central Phase 6 question is:

> Can explicit entity, relation, and claim structure improve retrieval when the answer depends on relationships rather than only textual similarity?

## Final architecture

```text
User Question
    ↓
Entity Resolution
    ├── lexical name / alias
    └── typed semantic fallback
            ↓
Claim Graph
(entity → relation → entity/value)
            ↓
Bounded Literal-Path Enumeration
            ↓
Semantic Path Ranking
(MiniLM)
            ↓
Top Claim Path
            ↓
Answer + Claim IDs + Evidence Provenance
```

## Core data model

### GraphEntity

Represents a canonical node:

- entity_id,
- name,
- entity_type,
- aliases,
- metadata.

### KnowledgeClaim

Represents one typed edge or literal fact:

```text
subject_entity_id
+ relation
+ exactly one of:
  - object_entity_id
  - object_value
+ evidence
```

### EvidenceReference

Carries provenance:

- document_id,
- evidence_text,
- optional section title,
- metadata.

A graph edge is therefore not self-justifying.

Every claim must retain source evidence.

## Deterministic traversal

`ClaimGraphIndex` validates basic graph mechanics.

Given:

- start entity,
- relation path,

it traverses exactly one matching claim per hop and accumulates:

- claim IDs,
- evidence,
- final value.

Ambiguous duplicate edges intentionally raise rather than silently guess.

## Entity resolution stack

### Lexical resolver

Preferred when the question explicitly contains a registered entity surface.

It supports:

- canonical names,
- aliases,
- longest-match behavior,
- abstention when no surface exists.

### Semantic fallback

When lexical linking fails:

1. infer a coarse entity type,
2. rank only entities of that type,
3. apply a fixed cosine threshold,
4. otherwise abstain.

The semantic fallback is useful but imperfect.

Phase 6 hard stress showed false abstentions and one false positive under the fixed threshold policy.

## Path search

`GraphPathEnumerator` enumerates simple structurally valid paths from the chosen start entity.

Candidate paths terminate at literal values.

Each path profile includes:

- relation sequence,
- supporting evidence,
- final value.

`SemanticGraphPathRanker` embeds:

- the user question,
- each path profile,

and ranks candidates with cosine similarity.

This converts relation selection into constrained retrieval over graph-valid paths instead of free-form path generation.

## Reusable end-to-end component

The main integration component is:

```text
knowledge_engine/graph/qa.py
```

Main class:

```text
ClaimGraphQAEngine
```

Responsibilities:

- resolve start entity,
- enumerate paths,
- rank paths,
- return answer,
- preserve evidence,
- report path-score diagnostics.

It supports injectable entity resolvers.

This allows the same graph QA engine to run with:

- lexical-only entity linking,
- hybrid entity linking.

## Key experiment results

### Deterministic graph traversal

```text
AnswerAccuracy=1.0000
PathAccuracy=1.0000
ProvenanceCoverage=1.0000
```

### Lexical entity resolution stress

```text
OverallAccuracy=1.0000
ResolvableEntityAccuracy=1.0000
AbstentionAccuracy=1.0000
FalsePositiveResolutionRate=0.0000
```

### Mention-focused semantic entity ranking

```text
WholeQuestionHit@1=0.5000
MentionSpanHit@1=1.0000
```

### Oracle type-constrained entity ranking

```text
UnconstrainedResolvableAccuracy=0.5000
TypedResolvableAccuracy=1.0000
TypedAbstentionAccuracy=1.0000
```

### Semantic relation-path selection

```text
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
AvgCandidatePaths=2.00
```

### Explicit-entity end-to-end QA

```text
EntityLinkAccuracy=1.0000
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
ProvenanceCoverage=1.0000
```

### Hard hybrid end-to-end stress

```text
AnswerableEndToEndSuccessRate=0.5000
EntityResolutionAccuracy=0.5000
PathSelectionAccuracy=0.5000
AnswerAccuracy=0.5000
ProvenanceCoverage=0.5000
AbstentionAccuracy=0.5000
FalsePositiveAnswerRate=0.5000
```

The apparent path/answer drop is downstream of entity-resolution failures.

Conditioned on the two answerable tasks where a start entity was successfully resolved, both selected paths and answers were correct.

## Main architectural lesson

Graph reasoning quality depends on two distinct problems:

```text
1. entering the graph correctly
2. navigating the graph correctly
```

Phase 6 path navigation was strong on the synthetic branching benchmark.

The dominant remaining weakness was deciding whether and where to enter the graph for implicit semantic references.

## Limitations

- small synthetic graph,
- shallow bounded paths,
- no learned relation planner,
- no large-scale graph index,
- no qualifier-aware multi-edge disambiguation,
- no temporal graph reasoning,
- no calibrated entity confidence,
- fixed threshold,
- coarse entity types,
- no automatic mention-span extractor,
- no independent large held-out benchmark.

The phase validates mechanisms and failure modes, not production-scale generalization.
