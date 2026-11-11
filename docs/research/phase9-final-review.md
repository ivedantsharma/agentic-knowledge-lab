# Phase 9 Final Review

## Status

Complete.

Phase 9 is closed as an adversarial robustness and failure-analysis phase.

## Central question

> What happens when retrieved evidence actively attempts to manipulate the agent?

The answer from the controlled experiments is:

> The model can follow malicious retrieved instructions, and naive defenses can either fail to generalize or destroy benign utility.

## What was learned

### Prompt injection is real in the current architecture

After evaluator repair:

```text
CleanAccuracy=1.0000
InjectedAccuracy=0.5000
AttackSuccessRate=0.2500
```

### Vulnerability is context-sensitive

Attack success varied by task family and placement.

### Quoted malicious text is not automatically inert

The model followed quoted attack text in the Cirrus family.

### Prompt-only defense can backfire

```text
AttackSuccessRate
0.3750 → 0.8750
```

### Structural removal can help on known patterns

```text
AttackSuccessRate
0.3750 → 0.0000
```

### Keyword defenses do not generalize semantically

Paraphrased attacks achieved:

```text
AttackSuccessRate=1.0000
```

### Semantic detection creates a calibration problem

Baseline semantic detector:

```text
InstructionRecall=1.0000
DATARecall=0.0000
```

Calibrated held-out detector:

```text
InstructionRecall=1.0000
DATARecall=0.2500
```

The improvement generalized slightly, but remained insufficient.

## Why Phase 9 stops here

The phase has established:

- a concrete retrieved-content threat model,
- attack-success metrics,
- semantic behavior-change metrics,
- mitigation comparisons,
- lexical generalization failure,
- semantic-detector false-positive analysis,
- development vs held-out classifier evaluation,
- utility-vs-robustness tradeoff reporting.

Further prompt tuning would add little scientific value.

The next major research question is no longer:

```text
Can we detect malicious evidence?
```

but:

```text
How should the system dynamically choose retrieval strategies for different query types?
```

That belongs to Phase 10.

## Next phase

# Phase 10 — Adaptive Retrieval & Query Understanding

Focus:

- query classification,
- BM25 vs dense vs hybrid vs graph routing,
- adaptive top-k,
- query transformation,
- retrieval policy design.
