# ADR-013: Treat Retrieved Content as Untrusted and Evaluate Defenses on Utility-Robustness Tradeoffs

## Status

Accepted.

## Context

Retrieved documents may contain instructions that conflict with the user task or system behavior.

Experiments showed:

- direct prompt-injection success,
- prompt-only hardening can increase attack success,
- keyword sanitization can block known attacks,
- paraphrases bypass lexical filters,
- semantic detectors can over-delete benign evidence.

## Decision

### 1. Retrieved text is untrusted input

Do not conceptually treat retrieved content as having instruction authority.

### 2. Prompt-only hardening is insufficient

Prompt wording may be used as one layer, but must not be treated as the security boundary.

### 3. Structural defenses must be evaluated on two axes

Always report:

```text
adversarial robustness
+
benign utility preservation
```

### 4. Detector evaluation precedes pipeline deployment

Instruction classifiers must be evaluated independently before being used to delete evidence.

### 5. Held-out evaluation is required

Do not repeatedly tune detection prompts against the same adversarial examples.

## Rationale

Security mitigations can fail in opposite directions:

```text
miss attacks
or
delete useful evidence
```

Both are system failures.

## Consequences

Positive:

- clearer trust model,
- measurable defense tradeoffs,
- reduced risk of misleading security claims,
- reusable evaluation pattern for future agent safety work.

Negative:

- more evaluation complexity,
- no single mitigation currently solves the problem,
- robust semantic filtering remains open.

## Rejected alternatives

### Trust prompt wording alone

Rejected after EXP-086.

### Expand keyword list indefinitely

Rejected because EXP-088 showed zero paraphrase generalization.

### Use semantic detector without calibration

Rejected because EXP-089/090 showed catastrophic false positives.

## Final decision

Subsequent phases should treat adversarial-content handling as a layered systems problem, not a single prompt-engineering trick.
