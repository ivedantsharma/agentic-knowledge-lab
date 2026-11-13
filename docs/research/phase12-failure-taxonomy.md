# Phase 12 Failure Taxonomy — Learning versus Transfer

## Reward and termination
- **Incomplete timeout loophole (EXP-112):** Reward v1 could avoid the premature STOP penalty through forced timeout. Reward v2 corrected this, tested by EXP-113/114.
- **Evidence-only proxy:** A supporting document can be retrieved alongside pending or contradictory information; full gold-document coverage alone does not prove a correct answer.
- **Unreachable evidence:** Rank-6 synthetic support cannot be retrieved under max K5; a reward oracle may prefer immediate STOP. Not a real unanswerable-detection result.

## Policy optimization
- **Local convergence (EXP-117):** seed 3 achieved complete evidence retrieval but used ~3.05 docs rather than ~2.04–2.10. Diverse reward-maximizing-ish behavior can emerge from different seeds.
- **State aliasing:** tabular state `(requested_k, steps_taken)` is identical across questions with different required retrieval depth; a policy cannot adapt using hidden question meaning.
- **Apparent training improvement without transfer:** EXP-118 train return rose for all seeds, but heldout reward fell for seeds 1, 3, 4 and completion fell on average.
- **Fixed-baseline domination:** fixed K3 achieved +2.6000 / 100% heldout completion; learned mean +1.7540 / 74.16% under the same BM25 protocol.

## Evaluation hazards
- **Retriever confound:** frozen Hybrid Cirrus support at rank 2 versus BM25 Cirrus support at rank 1.
- **Split mismatch:** Phase 11's heldout Meridian differs from Phase 12's non-Cirrus five-family heldout.
- **Action mismatch:** `REFORMULATE` in supervised action space, `STOP` in RL; raw action accuracy is not sequential discounted return.
- **Over-used benchmark:** EXP-118 families and target ranks were inspected, so iterative tuning on them invalidates untouched-test claims.
- **Small-sample uncertainty:** five seeds and ten heldout questions do not support broad significance or generalization claims.

## Corrective direction
Freeze tasks/protocols, use fresh family splits, add strictly policy-visible retrieval signals, audit independence, compare to fixed strategies, and measure grounded answer quality separately from support retrieval.
