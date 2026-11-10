# EXP-087: Structural Evidence Sanitization

## Research question

Can a structural pre-processing defense reduce retrieved-content prompt injection more reliably than prompt-only hardening?

## Motivation

EXP-086 showed that prompt-only trust-boundary instructions made the system worse:

```text
AttackSuccessRate
0.3750 → 0.8750
```

So the next experiment changes mitigation class.

## Defense

Before evidence reaches the model, remove sentence-like spans containing known assistant-directed instruction markers.

Examples include:

- assistant directive,
- system override,
- ignore the question,
- disregard the original question,
- answer exactly,
- output exactly,
- respond with.

## Controlled setup

Keep fixed:

- model,
- questions,
- adversarial cases,
- extraction prompt,
- decoding,
- evaluator.

Change only:

```text
raw evidence
→ sanitized evidence
```

## Why this is structurally different

Prompt hardening asks the model to ignore malicious instructions.

Sanitization attempts to prevent those instructions from entering model context at all.

## Metrics

Compare baseline vs sanitized:

- semantic accuracy,
- direct attack success rate,

overall and by placement.

## Important limitation

This sanitizer is intentionally simple and pattern-based.

It is not a production security solution.

It can:

- miss paraphrased attacks,
- remove legitimate text containing instruction-like language,
- fail on attacks embedded inside otherwise useful sentences.

The goal is to test whether changing the architecture boundary helps more than prompt wording.
