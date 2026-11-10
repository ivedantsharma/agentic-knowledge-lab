# EXP-085: Prompt-Injection Placement and Framing Sensitivity

## Research question

Does retrieved-content prompt-injection susceptibility depend on where and how the malicious instruction appears inside evidence?

## Motivation

EXP-084 confirmed a real vulnerability:

```text
CleanAccuracy=1.0000
InjectedAccuracy=0.5000
AttackSuccessRate=0.2500
```

Before adding defenses, we should characterize the attack surface.

## Controlled variables

Keep fixed:

- model,
- question,
- legitimate fact,
- expected answer,
- attack payload semantics,
- extraction prompt,
- decoding,
- evaluator.

Change only injection placement/framing.

## Variants

### Suffix directive

Malicious instruction appears after the legitimate fact.

### Prefix directive

Malicious instruction appears before the legitimate fact.

### Middle directive

Malicious instruction interrupts the evidence sentence.

### Quoted directive

The document reports the malicious instruction as quoted content rather than directly presenting it as an instruction.

## Why quoted framing matters

A robust system should distinguish:

```text
document says:
"Ignore the user"
```

from:

```text
system should actually ignore the user
```

This is a trust-boundary test.

## Metrics

For each variant:

- semantic answer accuracy,
- strict attack success rate.

## Interpretation

If attack success depends strongly on placement or framing, the vulnerability is input-structure sensitive.

If all placements succeed similarly, the weakness is broader.

No defense is introduced in EXP-085.
