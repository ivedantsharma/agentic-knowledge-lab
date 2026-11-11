# Phase 9 High-Level Design

## Goal

Study how an agentic knowledge system behaves when retrieved content is intentionally adversarial.

The central Phase 9 question is:

> Can the system distinguish evidence to reason about from instructions embedded inside that evidence?

## Threat model

```text
external document
→ retriever
→ model context
→ agent action
```

The adversary controls document content, not system instructions.

Main attack surfaces:

- direct retrieved-content prompt injection,
- paraphrased instruction injection,
- quoted malicious instructions,
- placement sensitivity,
- sanitizer bypass,
- detector false positives.

## Experimental architecture

```text
clean evidence
      ↓
answer extractor
      ↓
clean baseline

adversarial evidence
      ↓
answer extractor
      ↓
attack susceptibility

adversarial evidence
      ↓
mitigation
      ↓
answer extractor
      ↓
robustness / collateral damage
```

## Evaluation dimensions

Phase 9 separates:

- answer accuracy,
- direct attack success,
- semantic behavior change,
- attack-span removal,
- benign fact preservation,
- instruction precision,
- instruction recall,
- DATA recall.

## Experiment progression

### EXP-083

Initial prompt-injection probe.

Found one direct attack success, but also exposed exact-string grader weakness.

### EXP-084

Repaired short-answer equivalence.

Final corrected result:

```text
CleanAccuracy=1.0000
InjectedAccuracy=0.5000
AttackSuccessRate=0.2500
SemanticBehaviorChangeRate=0.5000
```

### EXP-085

Varied placement/framing.

Result:

```text
Accuracy=0.5000
AttackSuccessRate=0.3750
```

Solstice remained robust.

Cirrus was vulnerable to prefix, middle, and quoted attacks.

### EXP-086

Prompt-only trust-boundary mitigation.

Result:

```text
baseline attack success=0.3750
hardened attack success=0.8750
```

Prompt hardening made the system worse.

### EXP-087

Keyword structural sanitization.

Result:

```text
baseline accuracy=0.5000
sanitized accuracy=0.8750

baseline attack success=0.3750
sanitized attack success=0.0000
```

This was the first successful mitigation on known attack strings.

### EXP-088

Paraphrase generalization.

Result:

```text
AdversarialAccuracy=0.0000
AttackSuccessRate=1.0000
AttackSpanRemovalRate=0.0000
```

The keyword sanitizer had no semantic generalization.

### EXP-089

Semantic instruction detector.

It removed all attack text but also all benign evidence.

```text
semantic attack success=0.0000
benign fact preservation=0.0000
```

### EXP-090

Isolated detector classification.

```text
InstructionRecall=1.0000
DATARecall=0.0000
```

The detector was effectively constant-positive.

### EXP-091

Prompt calibration on development probe.

```text
DATARecall=0.1667
InstructionRecall=1.0000
```

Small improvement only.

### EXP-092

Held-out generalization.

```text
DATARecall=0.2500
InstructionRecall=1.0000
Accuracy=0.5000
```

The gain generalized, but false-positive behavior remained unacceptable.

## Main architectural lessons

### 1. Retrieved evidence is a trust boundary

External text must not automatically inherit instruction authority.

### 2. Prompt hardening is not a security boundary

In this setup it increased attack success.

### 3. Structural filtering can help

Removing known instruction-like spans before model context can be effective.

### 4. Lexical filtering is narrow

Paraphrases bypassed it completely.

### 5. Semantic filtering introduces a classifier problem

A detector must balance:

```text
attack recall
vs
benign preservation
```

### 6. Attack recall alone is insufficient

A detector that removes everything is not robust.

### 7. Held-out evaluation is necessary

Mitigation prompts should not be tuned repeatedly on the same tiny adversarial probe.

## Limitations

- synthetic attacks,
- small datasets,
- two local Qwen models,
- sentence-like splitting,
- no tool-use attack propagation,
- no search-loop attack experiments,
- no long-context stress,
- no production-scale prompt-injection corpus,
- no calibrated probabilistic detector,
- no human annotation study.

Phase 9 validates failure-analysis methodology and architectural tradeoffs, not production security.
