# EXP-033: Extract-or-Abstain Stop Policy

## Failure addressed

The grounded-stop-v2 policy still stopped incorrectly because the model selected a real but irrelevant span:

```text
Developer Productivity
```

The span existed in evidence, so exact-span grounding passed.

## Hypothesis

A joint extract-or-abstain prompt will better distinguish:

- evidence that directly answers the question,
- evidence that is merely related.

## New policy

```text
If direct answer span exists:
    return exact span
else:
    return INSUFFICIENT
```

Then:

```text
INSUFFICIENT → SEARCH
grounded span → STOP
```

## Controlled variables

Unchanged:

- OOD task,
- corpus,
- MiniLM retriever,
- semantic bootstrap,
- Qwen2.5-0.5B-Instruct,
- deterministic decoding,
- max-step budget.

Changed:

- stopping formulation only.

## Expected intermediate behavior

On the organization document:

```text
candidate_answer=None
abstained=True
grounded=False
```

The planner should continue searching.

On the Cirrus manual:

```text
candidate_answer contains CIRRUS-DLQ
abstained=False
grounded=True
```

The planner should STOP.
