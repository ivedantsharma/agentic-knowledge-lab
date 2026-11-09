# Phase 6 Failure Taxonomy

## 1. Whole-question entity-linking leakage

### Symptom

The semantic entity ranker selected the answer entity rather than the entity mention.

Example:

```text
"Which service is maintained by the infrastructure reliability group?"
```

Whole-question ranking:

```text
1. Borealis
2. Platform Reliability
```

Gold linked entity:

```text
Platform Reliability
```

### Cause

The embedding mixed:

- entity mention semantics,
- requested answer type,
- relation semantics.

### Lesson

Entity linking and answer retrieval are different objectives.

Mention-focused representations improved this failure.

---

## 2. Related-node type confusion

### Symptom

A team mention ranked a related service above the team.

Examples:

```text
team → Atlas service
team → Solstice service
```

### Cause

Semantic similarity captured graph neighborhood relevance but ignored semantic role.

### Repair

Type-constrained candidate ranking.

### Lesson

Structured retrieval benefits from:

```text
semantic similarity
+ symbolic compatibility constraints
```

---

## 3. Mixed lexical type cues

### Symptom

The original lexical type inferer abstained on:

```text
team ... service
group ... cache
```

### Cause

It treated any multiple type categories in the same phrase as ambiguity.

### Repair diagnostic

A first-cue heuristic improved type inference:

```text
0.6667 → 1.0000
```

### Limitation

The heuristic is not a general syntactic parser.

---

## 4. Confidence-threshold false abstention

### Symptom

The correct entity ranked first within the correct type, but its score fell below the fixed threshold.

Example:

```text
Identity Foundations
score=0.372357
threshold=0.39
```

### Cause

Raw cosine thresholds are not calibrated probabilities and vary by phrasing/entity type.

### Lesson

Do not interpret one global cosine threshold as calibrated confidence.

---

## 5. False-positive semantic entry into graph

### Symptom

An unrelated team question entered the graph and returned a valid but irrelevant answer.

Example category:

```text
employee travel reimbursements
```

The system linked to:

```text
Platform Reliability
```

and then returned a valid graph answer.

### Cause

Once a wrong entity is accepted, graph traversal can remain internally consistent.

### Lesson

Graph structure cannot repair a bad entry point.

Abstention quality is part of graph QA quality.

---

## 6. Near-distractor path margin

### Symptom

The correct Atlas path ranked first, but only narrowly:

```text
correct path ≈ 0.782214
legacy path  ≈ 0.755725
margin       ≈ 0.0265
```

### Cause

Both paths share:

- the same start entity,
- similar relation structure,
- semantically related storage evidence.

### Lesson

Perfect top-1 accuracy can hide weak separation.

Path-score margin should be tracked alongside accuracy.

---

## 7. Downstream metric collapse from upstream abstention

### Symptom

In EXP-064:

```text
PathSelectionAccuracy=0.5000
AnswerAccuracy=0.5000
```

### Correct diagnosis

The two failed answerable tasks never reached path search.

Therefore the drop is not evidence that path ranking regressed.

Conditioned on successful entity resolution:

```text
path success = 2/2
answer success = 2/2
```

### Lesson

End-to-end metrics must be decomposed by stage.

---

## 8. Ambiguous graph edges

The deterministic traversal layer intentionally rejects multiple claims with the same:

```text
(subject, relation)
```

instead of guessing.

This is not yet solved.

Future work should introduce:

- qualifiers,
- environments,
- temporal scopes,
- claim selection policy.

This failure mode is deferred rather than hidden.

---

## Summary

The dominant Phase 6 bottleneck is not graph traversal.

It is:

```text
semantic entity entry
+ confidence / abstention
```

The graph layer itself behaved strongly on the controlled branching benchmark.
