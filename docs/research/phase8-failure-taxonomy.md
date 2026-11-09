# Phase 8 Failure Taxonomy

## 1. Correct answer with insufficient evidence

A stopped answer can be correct while the agent has not retrieved all required evidence.

Detected by:

- AnswerCorrect=True
- PrematureStop=True
- EvidenceCoverage<1

Lesson:

```text
correct outcome != justified process
```

---

## 2. Correct answer with inefficient search

The agent can retrieve all evidence and answer correctly while repeating queries or exceeding the reasonable search budget.

Detected by:

- FullEvidence=True
- AnswerCorrect=True
- EfficientSearch=False

Lesson:

```text
correct != efficient
```

---

## 3. Full evidence but wrong answer

Semantic `ood-001` retrieved every required document but answered incorrectly.

Lesson:

```text
evidence availability != answer correctness
```

---

## 4. Grounded but wrong answer

The stopped answer appears in consumed evidence but does not answer the requested relation.

Lesson:

```text
grounded != correct
```

---

## 5. Grounded but relation-misaligned

Example:

Question asks for dead-letter destination.

Evidence contains both:

- retry count,
- destination.

Agent returns retry count.

Detected by deterministic relation alignment.

Lesson:

```text
grounded != relation aligned
```

---

## 6. Perfect path but wrong relation

Semantic OOD trace consumed the exact gold path in order but still selected the wrong fact.

Lesson:

```text
trajectory correctness != answer-selection correctness
```

---

## 7. Planner capability failure

Rule-based OOD case failed before issuing any search.

Detected by:

- PlannerFailed=True
- FullEvidence=False
- no trace actions.

Lesson:

An inability to formulate a query should be distinguished from retrieval failure.

---

## 8. Model-grader false negative

The Qwen grader rejected a valid Borealis answer.

This is a grader error, not an agent error.

Lesson:

```text
model judge output != ground truth
```

---

## 9. Model-grader input-form sensitivity

Meaning-preserving changes to Borealis evidence/question caused verdict flips.

Lesson:

Grader robustness must be measured under semantic-preserving perturbations.

---

## 10. Aggregate-accuracy blindness

Rule-based and semantic planners both had:

```text
AnswerAccuracy=0.8000
```

but failed for completely different reasons.

Rule-based:

```text
planner capability failure
```

Semantic:

```text
relation-selection failure after perfect retrieval
```

Lesson:

Single aggregate scores hide causal failure structure.

---

## Summary

The main Phase 8 principle is:

```text
evaluate the trajectory, not only the final answer
```

and when model graders are used:

```text
evaluate the grader too
```
