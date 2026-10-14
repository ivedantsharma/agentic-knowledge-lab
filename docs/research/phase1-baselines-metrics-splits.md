# Phase 1 — Baselines, Metrics, Splits, Leakage, and Fair Experiments

This module explains how to compare retrieval and agent systems fairly.

---

## 1. Baseline

A baseline is a simpler reference system that answers:

> Is the new system actually better than something reasonable?

Examples:

- BM25
- dense retrieval
- hybrid retrieval
- single-shot RAG
- prompt-only agent

A baseline does not need to be state of the art.

It needs to be:
- relevant,
- reproducible,
- strong enough to be meaningful.

### Why BM25 matters

BM25 is useful because it is:
- simple,
- widely understood,
- strong on exact lexical matches,
- cheap,
- deterministic.

If a complex system cannot outperform BM25 on tasks where BM25 is strong, the added complexity may not be justified.

Important correction:

BM25 is not automatically "high precision" in every task.

Its usefulness comes from being a strong lexical baseline, not from being universally precise.

---

## 2. One metric is not enough

Suppose:

```text
System A answer accuracy = 85%
System B answer accuracy = 82%
```

We still cannot immediately conclude that A is better.

Questions to ask:

- Did both systems use the same dataset?
- Were they evaluated on the same examples?
- Were prompts/models/configuration controlled?
- Is the 3-point difference stable across repeated runs?
- Did A retrieve better evidence?
- Did A use more tool calls?
- Was A much slower or more expensive?
- Did A succeed only by guessing from parametric memory?
- Is the difference statistically meaningful?

This is why we separate metrics into layers.

---

## 3. Retrieval metrics

### Recall@K

Question:

> Of all required relevant documents, how many were found in the top K?

Example:

Suppose there are 2 relevant documents.

Top-5 retrieved results contain both.

```text
Recall@5 = 2 / 2 = 1.0
```

If only one was found:

```text
Recall@5 = 1 / 2 = 0.5
```

### Precision@K

Question:

> Of the K retrieved documents, how many are relevant?

If top-5 contains 2 relevant documents:

```text
Precision@5 = 2 / 5 = 0.4
```

### MRR

Mean Reciprocal Rank emphasizes how early the first relevant result appears.

If the first relevant result is at rank 1:

```text
RR = 1 / 1 = 1.0
```

At rank 2:

```text
RR = 1 / 2 = 0.5
```

At rank 5:

```text
RR = 1 / 5 = 0.2
```

MRR averages that value across queries.

---

## 4. Answer metrics

Possible metrics include:

- exact match,
- normalized exact match,
- token-level F1,
- rubric-based grading,
- model-based grading.

The correct metric depends on the task.

A short factual answer may use exact match.

A synthesis task may require a rubric.

---

## 5. Agent metrics

For agents, final answer quality is not enough.

We may also measure:

- tool calls,
- retrieval rounds,
- repeated queries,
- latency,
- token use,
- cost,
- stopping behavior,
- failure to recover,
- loop frequency.

A system that gets the right answer after 30 unnecessary searches may be worse than one that gets it in 3.

---

## 6. Train / dev / test split

### Train set

Used to teach the system.

Examples:
- fine-tuning examples,
- RL trajectories.

### Development set

Used while making decisions.

Examples:
- prompt tuning,
- choosing top_k,
- selecting a reranker,
- deciding chunk size.

### Test set

Used for final unbiased evaluation.

The test set should remain untouched until the system design is largely fixed.

---

## 7. Why repeatedly tuning on the test set is dangerous

Suppose:

1. evaluate on test set,
2. inspect failures,
3. modify system,
4. evaluate on the same test set,
5. repeat 50 times.

Even if the test examples are never explicitly added to training data, design decisions are now influenced by them.

The system has indirectly adapted to the test set.

That is a form of evaluation leakage.

Eventually:

```text
test score ≠ honest estimate of generalization
```

The test set has effectively become another development set.

---

## 8. Leakage

Leakage means information that should be unavailable during model/system development affects the system or evaluation.

Examples:

- test answers included in training data,
- prompt written after reading test answers,
- chunking tuned specifically for test documents,
- benchmark examples accidentally appearing in few-shot prompts,
- using the final test score repeatedly to choose hyperparameters.

Leakage can make a weak system appear strong.

---

## 9. Fair comparison

Suppose we compare BM25 and dense retrieval.

To make the comparison fair, keep as much as possible fixed:

- same corpus,
- same queries,
- same relevance labels,
- same top_k,
- same evaluation code,
- same metric definitions.

Then the main changed variable is:

```text
retrieval method
```

That makes the result interpretable.

---

## 10. Variance

Agent systems can be stochastic.

Run 1:

```text
success
```

Run 2:

```text
failure
```

Run 3:

```text
success
```

A single run can therefore be misleading.

For stochastic systems, we may need:
- repeated trials,
- mean performance,
- variance / standard deviation,
- success rate across runs.

---

## 11. Phase 1 exercise review

### Question 1 — Why BM25?

Correct core idea:

Dense retrieval working on a tiny predictable corpus does not establish that dense retrieval is generally superior.

Refinement:

BM25 is valuable because it is a strong, simple lexical baseline, especially for exact-match queries.

### Question 2 — Why is 85% vs 82% insufficient?

Correct.

Answer accuracy is only one layer.

Also check:
- fair dataset/configuration,
- retrieval quality,
- efficiency,
- robustness,
- repeated-run stability.

### Question 3 — Why not tune repeatedly on the final test set?

The key issue is evaluation leakage.

Repeatedly changing the system based on final-test performance makes the final test set part of the development process.

The final score then becomes overly optimistic.

---

# Checkpoint

You should now be able to explain:

- baseline
- Recall@K
- Precision@K
- MRR
- train/dev/test split
- leakage
- variance
- fair comparison
