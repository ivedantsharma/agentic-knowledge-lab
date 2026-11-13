# Phase 11 Final Review

## Status

Complete.

## Central research question

> Can a model learn retrieval/search actions from oracle demonstrations instead of relying only on hand-written rules?

Within the controlled benchmark, yes—but only after fixing important data-design failures.

## EXP-101 — Frozen policy baseline

```text
format compliance=1.0000
action accuracy=0.0000
```

The frozen Qwen model produced valid action tokens but defaulted mostly to K3.

## EXP-102 — Dataset audit

Created a source-task-disjoint supervised seed dataset.

Later experiments showed that this split was not strict enough.

## EXP-103 — Target-only causal-LM loss

Validated:

```text
prompt_tokens=168
supervised_tokens=9
```

with only the assistant action suffix supervised.

## EXP-104 — First LoRA update

Only about:

```text
0.0547%
```

of parameters were trainable.

One-example target loss fell:

```text
0.204247 → 0.006459
```

proving optimization mechanics.

## EXP-105 — Initial train/dev/heldout SFT

```text
train   0.0833 → 0.5833
dev     0.0000 → 1.0000
heldout 0.3333 → 0.3333
```

Promising but inconclusive.

## EXP-106 — Class/source support audit

Only two of five classes were source-disjoint evaluable.

This exposed insufficient class/source coverage.

## EXP-107 — Existing-corpus policy mining

Measured 12 paired queries.

Key finding:

```text
paraphrases can change the oracle action
```

So inherited policy labels were invalid.

## EXP-108 — Measured dataset v1

Built a stricter dataset with:

- individually measured labels,
- evidence-family-disjoint splits,
- no family leakage.

## EXP-109 — Unbalanced v1 SFT

```text
train=0.6364
dev=0.6667
heldout=0.0000
```

but every prediction became K1.

This was a majority-class shortcut.

## EXP-110 — Balanced v1 SFT

Balanced effective training counts:

```text
K1=7
K2=7
K5=7
REFORMULATE=7
```

Results:

```text
train   0.1818 → 0.9091
dev     0.0000 → 1.0000
heldout 0.3333 → 0.6667
```

The single-class collapse disappeared.

## Final conclusion

Phase 11 demonstrates that retrieval-policy behavior can be learned with LoRA SFT in this controlled environment.

However, the more important research lesson is that policy-learning quality depends heavily on training-data construction.

The strongest principles established are:

```text
measured labels > inherited labels
evidence-family splits > random/example splits
prediction distribution > loss alone
balanced exposure > majority-class shortcuts
```

## Remaining limitations

- only 17 measured examples in v1,
- only six evidence families,
- K3 has no positive training example,
- REFORMULATE has one independent family,
- no multi-seed variance,
- no real-world corpus.

Therefore the correct claim is:

> We established a working supervised retrieval-policy learning pipeline and demonstrated partial evidence-family-disjoint generalization, while identifying data coverage and class balance as major constraints.

## Next phase

# Phase 12 — RL for Retrieval Policy

The next question is:

> Can trajectory-level rewards improve retrieval decisions beyond static imitation labels?

Phase 12 should introduce:

- rewards,
- trajectories,
- credit assignment,
- policy optimization,
- explicit retrieval-quality/cost tradeoffs,
- evaluation leakage controls.
