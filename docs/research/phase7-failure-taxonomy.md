# Phase 7 Failure Taxonomy

## 1. Single-metric blindness

### Symptom

One aggregate retrieval score suggests two retrievers behave similarly.

### Hidden behavior

One system may retrieve more support while also retrieving more stale or contradictory evidence.

### Lesson

Report both positive evidence coverage and adversarial evidence exposure.

---

## 2. High MRR with incomplete evidence chain

### Symptom

MRR is high because one useful document ranks first.

### Failure

Other required multi-hop evidence is absent.

### Lesson

MRR does not measure multi-hop completeness.

Use evidence-chain coverage.

---

## 3. Weak adversarial benchmark examples

### Symptom

```text
StaleHitRate=0
ContradictionHitRate=0
```

### Initial interpretation

Retriever appears robust.

### Actual diagnosis

Full-rank analysis showed stale/contradictory documents were too low in the corpus.

### Repair

Strengthen adversarial examples while preserving support evidence and retrievers.

### Lesson

A zero failure rate may reflect an easy benchmark rather than a strong system.

---

## 4. Distractor dominance

### Symptom

A plausible but wrong document ranks above supporting evidence.

Example:

```text
Aurora distractor
> Borealis current policy
```

for Dense retrieval.

### Lesson

Semantic similarity can strongly prefer a related but irrelevant document.

---

## 5. Stale evidence exposure

### Symptom

BM25 retrieved stale policy evidence aggressively.

At hard-v0, k=3:

```text
StaleHitRate=1.0000
```

### Lesson

Lexical overlap does not encode temporal validity.

---

## 6. Contradiction exposure

### Symptom

Dense retrieval surfaced pending contradictory policy documents.

At hard-v0, contradiction slice:

```text
ContradictionHitRate=1.0000
```

### Lesson

Semantic relevance and factual authority are different properties.

---

## 7. Ambiguous query collapse risk

### Symptom

An under-specified query could retrieve only one plausible interpretation.

### Benchmark response

Annotate all plausible ambiguity candidates.

### Metric

```text
AmbiguityCandidateCoverage@K
```

### Lesson

For ambiguous queries, exposing multiple interpretations can be better than confidently retrieving one.

---

## 8. Unanswerable nearest-neighbor behavior

### Symptom

```text
UnanswerableRetrievalRate=1.0000
```

for BM25 and Dense at all tested k.

### Cause

Fixed top-k retrieval always returns nearest candidates.

### Lesson

Retrieval ranking and abstention are separate capabilities.

---

## 9. Candidate-budget confounding

### Symptom

Larger k improves support coverage.

### Hidden cost

The same larger k increases:

- distractors,
- stale evidence,
- contradictions.

### Lesson

Always compare systems at matched candidate budgets.

---

## 10. Benchmark audit false positive

### Symptom

The integrity audit flagged valid multi-hop temporal tasks.

### Cause

The first audit rule required every supporting document to be temporally dated.

### Repair

Require:

- dated stale evidence,
- at least one dated current supporting document,
- allow undated non-temporal bridge facts.

### Lesson

Evaluation infrastructure itself can contain failure modes and should be experimentally validated.

---

## 11. Tiny-slice instability

### Symptom

One challenge example can define an entire metric.

### Repair

Move from seed tasks to a mixed hard benchmark with multiple examples per challenge.

### Remaining limitation

The hard-v0 slices are still small.

---

## Summary

The dominant Phase 7 insight is:

```text
retrieval quality
!=
support recall alone
```

A useful benchmark must expose:

```text
support completeness
+ adversarial exposure
+ ambiguity
+ answerability
+ candidate-budget effects
+ annotation integrity
```
