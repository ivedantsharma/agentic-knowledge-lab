# EXP-108: Measured Policy Dataset v1 Audit

## Research question

Can we replace the inherited-label v0 dataset with a dataset containing only individually measured oracle actions while also preventing shared-evidence leakage across splits?

## Trigger from EXP-107

EXP-107 showed that paraphrases can change the optimal retrieval budget.

Examples:

```text
Cirrus:
  lexical  -> K2
  semantic -> K1

Solstice:
  lexical  -> K1
  semantic -> K2
```

Therefore policy labels must be query-specific.

## Dataset v1 rule

Every example must have an action supported by a completed oracle experiment.

No new paraphrase receives an inherited label.

## Evidence-family grouping

Queries that share supporting evidence belong to the same evidence family.

Examples:

```text
hard-001 + Borealis direct queries
→ atlas_borealis

hard-002 + hard-007 + Cirrus routes
→ cirrus

hard-005 + Solstice routes
→ helios_solstice

hard-006 + Meridian routes
→ security_meridian
```

All examples in one evidence family must remain in one split.

This is stricter than source-task disjointness and prevents the model from seeing the same underlying evidence relation during training and evaluation under a different task ID.

## Splits

Dataset v1 uses:

```text
train:
  cirrus
  helios_solstice
  nimbus
  orion

dev:
  atlas_borealis

heldout:
  security_meridian
```

## Limitations

- K3 still has zero positive examples.
- REFORMULATE still has one independently demonstrated source family.
- The dataset remains tiny and synthetic.

Therefore v1 improves label validity and leakage control but does not solve all class-coverage limitations.
