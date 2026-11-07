# EXP-028: FLAN-T5-Small Capability Probe

## Motivation

Few-shot planner output:

```text
STOP: No, no, no, ...
```

The result mixes several possible failure causes:

- bad stopping decision,
- weak query generation,
- poor grounding,
- repetition degeneration,
- prompt overload.

## Method

Keep the same model:

```text
google/flan-t5-small
```

and probe individual capabilities independently.

No retrieval is executed in this experiment.

The evidence is supplied directly so model behavior can be isolated from retriever behavior.

## Probes

- query generation without evidence,
- query generation after intermediate evidence,
- answer extraction from final evidence,
- answerability without evidence,
- answerability with final evidence.

## Interpretation guide

If query generation succeeds but answerability fails:

```text
use model as query generator,
do not trust it as stopping policy.
```

If answer extraction succeeds but planning fails:

```text
model understands evidence,
but planner prompt/action policy is too difficult.
```

If all probes fail:

```text
FLAN-T5-small is likely below the capability threshold
for this planner task.
```

This experiment should be completed before selecting a larger model or redesigning the planner.
