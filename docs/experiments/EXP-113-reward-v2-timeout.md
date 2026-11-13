# EXP-113: Repair Incomplete Timeout Rewards (v2)

## Research question
Can we eliminate the loophole where an agent avoids the -1 premature-STOP penalty by exhausting its step limit while missing required evidence?

## Controlled design
- Freeze the EXP-111 real-corpus Cirrus ranking.
- Use the same gold document and query.
- Compare reward v1 and v2 on identical predefined action sequences.
- No optimizer, language-model training, or changed retrieval ranking.

## Reward v1 (preserved)
- +2 per newly retrieved supporting document.
- -0.1 per newly retrieved document.
- +1 for explicit STOP with full evidence.
- -1 for explicit STOP with incomplete evidence.
- **No terminal penalty for incomplete forced timeout.**

## Reward v2 (single change)
If `max_steps` is reached on a **non-STOP** action and required support is incomplete, apply the same -1 terminal penalty as an explicit premature STOP.

Gold supporting IDs remain evaluator-only. The policy-visible observation does not expose them.

## Invariants
- Explicit STOP rewards unchanged.
- Complete retrieval trajectories unchanged.
- Complete forced timeout gets no incomplete penalty (and still no explicit STOP bonus).
- Conflicting evidence is counted in an independent diagnostic, not subtracted from reward yet.
- V1 remains selectable for reproducible EXP-111/112 comparisons.

## Interpretation
This fixes the specific timeout loophole but does **not** prove reward alignment with answer quality. It also does not resolve ambiguity, unanswerable tasks, stale evidence, or gaming through reward weights.

## Next
Formalize returns and credit assignment, then compare reward-aware policies against fixed baselines with source-family heldout evaluation. Do not claim a policy is learned from these hand-selected trajectories.
