# Phase 9 Foundations: Adversarial Robustness and Failure Analysis

## Threat-model shift

Earlier phases mostly studied accidental failure:

- distractors,
- stale evidence,
- contradictions,
- ambiguity,
- planner errors.

Phase 9 introduces adversarial failure:

```text
retrieved content intentionally tries to manipulate the agent
```

## Main adversarial surfaces

### Retrieved-content prompt injection

A document contains instructions such as:

```text
ignore the user's task
return a different answer
stop searching
```

### Search-loop traps

Evidence encourages repeated or cyclic searches.

### Misleading but plausible evidence

Documents are topically relevant but crafted to bias answer selection.

### Long-context distraction

Correct evidence remains present but is surrounded by large amounts of competing material.

## Evaluation principle

Do not begin by adding defenses.

First establish:

```text
clean baseline
→ adversarial perturbation
→ measured behavior change
```

Then introduce one defense at a time.

## Why this matters

An agentic retrieval system crosses a trust boundary:

```text
external document
→ model context
→ agent action
```

The system must distinguish:

```text
content to reason about
from
instructions to execute
```

Phase 9 studies failures at that boundary.
