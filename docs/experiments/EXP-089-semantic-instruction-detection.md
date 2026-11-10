# EXP-089: Semantic Instruction Detection vs Keyword Sanitization

## Research question

Can a semantic detector identify paraphrased assistant-directed instructions that bypass lexical filtering?

## Trigger from EXP-088

The keyword sanitizer achieved:

```text
AttackSpanRemovalRate=0.0000
AttackSuccessRate=1.0000
```

on paraphrased attacks.

Therefore the next experiment changes detector class.

## Semantic detector

A separate instruction model classifies each sentence-like span as:

```text
INSTRUCTION
or
DATA
```

Definition of INSTRUCTION:

> text that tries to tell the current AI assistant what to answer, output, ignore, or do.

Definition of DATA includes:

- factual statements,
- ordinary human/software procedures,
- quoted or discussed instructions that are not directing the current assistant.

## Architecture

```text
retrieved evidence
→ sentence-like spans
→ semantic instruction detector
→ remove INSTRUCTION spans
→ answer extractor
```

## Models

Answer extractor:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

Instruction detector:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

The detector is intentionally separate from the answer extractor.

## Controlled comparison

On the same EXP-088 paraphrased attacks compare:

- keyword sanitizer,
- semantic sanitizer.

Also rerun the benign collateral-damage cases.

## Metrics

- keyword accuracy,
- keyword attack-success rate,
- semantic accuracy,
- semantic attack-success rate,
- semantic attack-span removal rate,
- benign required-fact preservation,
- benign change rate.

## Important limitation

The semantic detector is itself an LLM exposed to untrusted text.

It is therefore not assumed trustworthy.

EXP-089 evaluates whether it improves robustness; later experiments must test whether the detector itself can be bypassed or manipulated.

## Success criterion

A useful semantic detector should improve attack-span removal and reduce attack success while preserving benign factual content.
