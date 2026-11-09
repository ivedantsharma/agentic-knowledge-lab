# Phase 7 High-Level Design

## Goal

Build a hard, typed, reproducible retrieval benchmark that can distinguish different knowledge-system failure modes instead of collapsing them into one retrieval score.

The central Phase 7 question is:

> Can we design an evaluation suite that separates missing support, distractor exposure, stale knowledge, contradiction exposure, ambiguity, multi-hop incompleteness, and unanswerable behavior?

## Final benchmark architecture

```text
Benchmark Documents
    ↓
Typed Task Schema
    ├── supporting evidence
    ├── evidence chain
    ├── distractors
    ├── contradictions
    ├── stale evidence
    └── ambiguity candidates
            ↓
Retriever
(BM25 / Dense baseline)
            ↓
Top-k Candidate Set
            ↓
Challenge-Aware Evaluator
    ├── supporting recall
    ├── MRR
    ├── evidence-chain coverage
    ├── distractor hit rate
    ├── contradiction hit rate
    ├── stale hit rate
    ├── ambiguity candidate coverage
    └── unanswerable retrieval rate
            ↓
Per-Challenge Slices
            ↓
Candidate-Budget Sensitivity
            ↓
Integrity Audit
```

## Core task model

`KnowledgeBenchV2Task` represents hard retrieval tasks with explicit evidence roles.

Main fields:

- `task_id`
- `question`
- `challenge_types`
- `should_answer`
- `expected_answer`
- `supporting_document_ids`
- `evidence_chain`
- `distractor_document_ids`
- `contradicting_document_ids`
- `stale_document_ids`
- `ambiguity_candidate_document_ids`

This separates task semantics from system behavior.

A retriever does not define what counts as stale, contradictory, ambiguous, or supporting evidence.

The benchmark does.

## Challenge taxonomy

Phase 7 defines six main challenge types:

- multi-hop,
- distractor,
- ambiguity,
- contradiction,
- stale knowledge,
- unanswerable.

Tasks may belong to multiple challenge types.

Example:

```text
multi_hop + stale_knowledge + distractor
```

This allows one task to contribute to several evaluation slices.

## Evidence-role separation

The benchmark distinguishes:

```text
supporting evidence
plausible distractor
contradicting evidence
stale evidence
ambiguity candidates
```

This matters because ordinary Recall@K cannot tell whether a candidate set contains both useful and harmful evidence.

## Retrieval metrics

### Supporting Recall@K

Measures how much annotated supporting evidence enters the candidate set.

### MRR

Measures how early the first supporting document appears.

MRR alone is insufficient for multi-hop tasks because one early support document can hide missing chain evidence.

### Evidence-Chain Coverage

Measures the fraction of annotated chain documents retrieved.

It evaluates evidence availability, not reasoning order.

### Distractor Hit Rate

Measures whether plausible but irrelevant evidence enters top-k.

### Contradiction Hit Rate

Measures whether contradictory evidence enters top-k.

Retrieving contradiction is not automatically an error; it is exposure that a downstream verifier must resolve.

### Stale Hit Rate

Measures whether stale evidence enters top-k.

### Ambiguity Candidate Coverage

Measures whether retrieval exposes the competing interpretations of an under-specified query.

### Unanswerable Retrieval Rate

Measures whether fixed-top-k retrieval still returns documents for unanswerable questions.

For nearest-neighbor retrieval this is expected to remain high without explicit abstention.

## Per-challenge evaluation

The evaluator can report metrics over each challenge subset.

This exposed different BM25 and Dense failure profiles that aggregate metrics hid.

## Candidate-budget sensitivity

Phase 7 treats `top_k` as part of the experimental condition.

Tested:

```text
k ∈ {1, 3, 5}
```

Main lesson:

```text
larger candidate budget
→ more support
→ more adversarial evidence
```

Candidate-set quality is therefore a Pareto tradeoff rather than a one-dimensional accuracy problem.

## Integrity audit

The benchmark includes a structural audit that checks:

- missing document references,
- duplicate document IDs,
- duplicate task IDs,
- temporal evidence consistency,
- ambiguity candidate count,
- challenge distribution,
- answerable/unanswerable balance.

The temporal audit deliberately allows undated relationship bridge documents while requiring dated current/stale temporal evidence.

## Hard-v0 benchmark

Current hard benchmark:

```text
documents=22
tasks=10
answerable=6
unanswerable=4
```

Challenge counts:

```text
multi_hop=4
distractor=2
ambiguity=2
contradiction=2
stale_knowledge=3
unanswerable=4
```

## Baseline observations

### BM25 at k=3

```text
SupportingRecall=0.7778
MRR=0.9167
EvidenceChainCoverage=0.6667
DistractorHitRate=0.5000
ContradictionHitRate=0.0000
StaleHitRate=1.0000
AmbiguityCoverage=1.0000
UnanswerableRetrievalRate=1.0000
```

### Dense MiniLM at k=3

```text
SupportingRecall=0.7500
MRR=0.8333
EvidenceChainCoverage=0.6250
DistractorHitRate=0.5000
ContradictionHitRate=1.0000
StaleHitRate=0.6667
AmbiguityCoverage=1.0000
UnanswerableRetrievalRate=1.0000
```

## Main architectural lesson

A hard retrieval benchmark should measure two dimensions simultaneously:

```text
Did useful evidence enter the candidate set?
What risky or misleading evidence entered with it?
```

Phase 7 demonstrates that those dimensions can move independently.

## Limitations

- synthetic corpus,
- 10 tasks,
- small challenge slices,
- no human annotation study,
- no natural production corpus,
- no model-based graders,
- no answer-generation evaluation,
- no trace evaluation,
- no calibrated abstention policy,
- no confidence intervals across multiple random seeds or datasets.

The phase validates benchmark design mechanisms and failure diagnostics, not benchmark maturity at production scale.
