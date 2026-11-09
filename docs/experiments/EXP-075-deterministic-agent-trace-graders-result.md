# EXP-075 Result: Deterministic Agent Trace Grader Foundations

## Ideal trace

```text
search_steps=2
repeated_searches=0
required_evidence_coverage=1.0000
answer_correct=True
premature_stop=False
efficient_search=True
retrieved_required_evidence=True
```

## Premature-stop trace

```text
search_steps=1
required_evidence_coverage=0.5000
answer_correct=True
premature_stop=True
efficient_search=True
retrieved_required_evidence=False
```

This is the key result: answer correctness and process correctness are separable.

## Redundant-search trace

```text
search_steps=3
repeated_searches=1
required_evidence_coverage=1.0000
answer_correct=True
premature_stop=False
efficient_search=False
```

Full evidence and a correct answer do not imply efficient behavior.

## Wrong-evidence trace

```text
search_steps=2
required_evidence_coverage=0.5000
answer_correct=False
premature_stop=True
efficient_search=True
retrieved_required_evidence=False
```

## Conclusion

The deterministic grader contract distinguishes:

- outcome quality,
- evidence sufficiency,
- stopping quality,
- search efficiency.

EXP-076 moves from synthetic controlled traces to live Phase 4 planner executions.
