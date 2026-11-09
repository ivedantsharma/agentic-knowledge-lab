# Phase 7 Final Review

## Status

Complete.

Phase 7 is closed as a benchmark-design, hard-retrieval-evaluation, and failure-analysis phase.

## Central question

> Can we design a hard, typed, reproducible evaluation suite that distinguishes retrieval failures, ambiguity, contradiction, staleness, multi-hop incompleteness, and unanswerable behavior?

For the controlled synthetic benchmark:

> Yes. KnowledgeBench v2 now separates evidence roles, challenge types, candidate-budget effects, and benchmark-integrity failures that ordinary Recall@K/MRR would hide.

## What was built

### Typed task schema

`KnowledgeBenchV2Task` with:

- explicit challenge labels,
- answerability,
- supporting evidence,
- ordered evidence chains,
- distractors,
- contradictory evidence,
- stale evidence,
- ambiguity candidates.

### Typed document schema

`KnowledgeBenchV2Document` with:

- ID,
- title,
- text,
- source type,
- optional effective date,
- metadata.

### Challenge-aware evaluator

Metrics:

- Supporting Recall@K,
- MRR,
- Evidence-Chain Coverage,
- Distractor Hit Rate,
- Contradiction Hit Rate,
- Stale Hit Rate,
- Ambiguity Candidate Coverage,
- Unanswerable Retrieval Rate.

### Per-challenge slices

Tasks can contribute to multiple slices.

This makes mixed challenge tasks measurable without forcing one exclusive category.

### Candidate-budget evaluation

Tested:

```text
k=1
k=3
k=5
```

### Benchmark integrity audit

Checks:

- ID uniqueness,
- reference integrity,
- temporal evidence consistency,
- ambiguity structure,
- challenge distribution.

## Experiment progression

### EXP-065

Defined KnowledgeBench v2 taxonomy and schema.

Validated explicit evidence roles and versioned benchmark representation.

### EXP-066

BM25 vs Dense seed baseline.

BM25:

```text
SupportingRecall@3=0.6667
MRR=1.0000
ChainCoverage=0.6667
```

Dense:

```text
SupportingRecall@3=0.5833
MRR=0.7500
ChainCoverage=0.5833
```

### EXP-067

Full-corpus role-rank diagnostic.

Found stale and contradiction cases were initially too weak.

### EXP-068

Strengthened stale and contradictory evidence without changing support evidence or retrievers.

Adversarial ranks moved into realistic candidate budgets.

### EXP-069

Challenge-aware evaluation on strengthened corpus.

Exposed different BM25 and Dense tradeoffs.

### EXP-070

Added ambiguity as a first-class task property.

Both retrievers achieved:

```text
AmbiguityCandidateCoverage=1.0000
```

on the seed ambiguity task.

### EXP-071

Expanded to hard-v0:

```text
22 documents
10 tasks
```

Per-challenge slices became meaningfully different.

BM25 contradiction slice:

```text
SupportRecall=1.0000
ContradictionHitRate=0.0000
```

Dense contradiction slice:

```text
SupportRecall=0.7500
ContradictionHitRate=1.0000
```

BM25 stale slice:

```text
SupportRecall=0.5556
StaleHitRate=1.0000
```

Dense stale slice:

```text
SupportRecall=0.6667
StaleHitRate=0.6667
```

### EXP-072

Candidate-budget sensitivity.

BM25:

```text
support recall:
0.4444 → 0.7778 → 0.7778

chain coverage:
0.4167 → 0.6667 → 0.6667

k:
1 → 3 → 5
```

BM25 support gains saturated at k=3 while adversarial exposure continued to increase.

Dense:

```text
support recall:
0.5000 → 0.7500 → 0.8611

chain coverage:
0.2500 → 0.6250 → 0.7917
```

Dense continued gaining useful evidence at k=5 but also reached maximal annotated adversarial exposure.

### EXP-073

Integrity audit initially failed.

The failure was caused by an overly strict audit rule, not broken benchmark data.

### EXP-074

Repaired temporal audit semantics.

Final validation:

```text
205 tests passed
ruff passed
audit_rule_version=temporal-v2
missing_document_references=[]
duplicate_document_ids=[]
duplicate_task_ids=[]
temporal_tasks_without_dated_evidence=[]
ambiguity_tasks_with_too_few_candidates=[]
passed=True
```

## Main research lessons

### 1. Hardness should be explicit

A task should say whether it tests:

- distractors,
- contradiction,
- ambiguity,
- stale knowledge,
- multi-hop evidence,
- unanswerability.

### 2. Evidence roles matter

Supporting and misleading documents should not share one relevance label.

### 3. MRR is not enough

High first-hit quality can coexist with incomplete multi-hop evidence.

### 4. Retrieval exposure is not belief

Retrieving a contradiction may be necessary.

The downstream system must decide what to trust.

### 5. Temporal validity is separate from lexical/semantic relevance

Retrievers can rank stale evidence highly even when it is no longer authoritative.

### 6. Ambiguity should be represented, not hidden

An ambiguous query may require multiple candidate interpretations.

### 7. Fixed top-k retrieval cannot solve abstention

Nearest-neighbor retrieval returns something even when no answer exists.

### 8. Candidate budget is an experimental variable

Changing k changes both support and risk.

### 9. Benchmarks need integrity tests

Evaluation code can create false conclusions just like model code can.

### 10. Negative results improve the benchmark

EXP-067 and EXP-073 both exposed benchmark/evaluator weaknesses that were more valuable than a clean pass.

## Why Phase 7 stops here

The phase now contains:

- explicit challenge taxonomy,
- typed task/document schemas,
- evidence-role separation,
- seed benchmark,
- adversarial hardening,
- ambiguity representation,
- mixed hard benchmark,
- challenge-aware metrics,
- per-challenge slices,
- candidate-budget sensitivity,
- structural integrity audit,
- negative-result documentation,
- reusable evaluation code.

Further expansion would mainly increase benchmark scale rather than teach a new mechanism.

That is appropriate later during the full research campaign.

## What Phase 7 deliberately does not solve

- agent trace quality,
- tool-selection correctness,
- stopping-policy quality,
- answer groundedness,
- model-based grading,
- hallucination evaluation,
- production-scale benchmark construction,
- inter-annotator agreement,
- natural-corpus benchmark generation.

Those belong to later phases.

## Next phase

Phase 8:

# Agent Evaluation & Graders

The focus shifts from:

```text
What did retrieval return?
```

to:

```text
What did the agent do with the retrieved evidence?
```

Phase 8 will evaluate:

- tool use,
- search traces,
- stopping,
- retrieval paths,
- groundedness,
- deterministic graders,
- eventually model-based graders.
