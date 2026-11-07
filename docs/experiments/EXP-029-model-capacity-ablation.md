# EXP-029: Model-Capacity Ablation for Planner Capabilities

## Research question

Were the EXP-028 failures caused primarily by the planner architecture, or was FLAN-T5-small simply below the capability threshold?

## Controlled variable

We keep exactly the same:

- question,
- intermediate evidence,
- final evidence,
- five probe prompts,
- decoding settings,
- model family.

We change only:

```text
google/flan-t5-small
→ google/flan-t5-base
```

This is a model-capacity ablation.

## Why use the same model family?

Changing from FLAN-T5 to a completely different instruction model would alter several variables:

- architecture,
- training data,
- tokenizer,
- instruction tuning,
- model size.

Using a larger FLAN-T5 model gives a cleaner comparison.

## What would count as improvement?

The most important capabilities are:

### Query generation

Output should be an actual information-seeking query, for example:

```text
Which worker platform is owned by Developer Productivity?
```

and after intermediate evidence:

```text
Where are failed jobs sent after production Cirrus exhausts retries?
```

Exact wording is not required.

### Answerability

Expected:

```text
no evidence   → NO
final evidence → YES
```

### Extraction

Expected to contain:

```text
CIRRUS-DLQ
```

## Decision rule

If the larger model materially improves planner capabilities, model capacity is an important variable.

If it shows the same failure pattern, we should change the planner formulation rather than continue scaling this model family.
