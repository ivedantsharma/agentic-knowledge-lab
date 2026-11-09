# Phase 7 Foundations: KnowledgeBench v2

## Goal

Build a benchmark that can answer a more useful question than:

> Did the system retrieve the answer?

KnowledgeBench v2 should help answer:

> What kind of knowledge failure occurred, and under what adversarial condition?

## Benchmark design principles

### 1. Difficulty must be explicit

Hardness is represented through challenge labels rather than inferred after a model fails.

### 2. Evidence roles must be separated

Relevant, stale, contradictory, and distracting documents are not interchangeable.

### 3. Multi-hop ground truth needs structure

A set of relevant documents does not express dependency order.

KnowledgeBench v2 therefore supports an ordered evidence chain.

### 4. Unanswerable is a first-class task type

Retrieving something for every query is not success.

A benchmark must reward correct abstention.

### 5. Do not build the benchmark around one model

Tasks should describe knowledge properties, not known weaknesses of MiniLM, BM25, Qwen, or one prompt.

### 6. Preserve versioning

The Phase 7 seed is versioned separately.

Later hard sets should not silently mutate earlier reported results.

## Initial scope

Phase 7 will build toward:

```text
single-hop control
multi-hop
lexical distractor
semantic distractor
ambiguity
contradiction
stale/current evidence
unanswerable
combinations of the above
```

## Evaluation progression

Planned sequence:

```text
EXP-065 taxonomy + schema
→ seed dataset validation
→ baseline retrieval runs
→ per-challenge metrics
→ evidence-chain metrics
→ stale/contradiction diagnostics
→ ambiguity/unanswerable diagnostics
→ harder mixed challenge set
→ benchmark closeout
```

Model-based graders are intentionally deferred to Phase 8.
