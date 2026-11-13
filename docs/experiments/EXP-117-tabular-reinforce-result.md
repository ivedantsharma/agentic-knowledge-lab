# EXP-117 Result — First On-Policy Tabular REINFORCE Training

## Setup
Same single grounded Cirrus **frozen hybrid** question at train/evaluation time; 2500 REINFORCE episodes and 800 evaluation episodes per seed; seeds 0,1,2,3,4; gamma=.9; learning rate .08; baseline rate .05. Reward v2 and gold-support labels remain inside evaluator/environment only.

## Validation
The user executed `uv run python scripts/run_phase12_tabular_reinforce.py` and provided the full output. GitHub CI **356 tests passed**, Ruff passed, and the real-file driver smoke test passed.

## Results
Gold oracle +2.7000; fixed K2 +2.7000; EXP-116 epsilon-K2 baseline +2.4924.

| Seed | G before | G after | Delta | Completion after | Mean docs after | Initial P(K2) |
|---|---:|---:|---:|---:|---:|---:|
| 0 | +1.564 | +2.693 | +1.128 | 1.000 | 2.06 | .984 |
| 1 | +1.548 | +2.688 | +1.140 | 1.000 | 2.10 | .972 |
| 2 | +1.546 | +2.695 | +1.149 | 1.000 | 2.04 | .992 |
| 3 | +1.620 | +2.594 | +.974 | 1.000 | 3.05 | .010 |
| 4 | +1.605 | +2.692 | +1.087 | 1.000 | 2.06 | .986 |

Mean before **+1.5765**, after **+2.6722**; mean improvement **+1.0957**, across-seed delta population SD **0.0643**. Oracle gap +0.0278. Zero-learning-rate control delta **+0.0000**.

## Failure / transfer probes
Seed 3 learned a higher-cost retrieval strategy despite complete evidence coverage. Synthetic transfer of seed 0: two-support G +0.952, coverage .508, completion .016; late-support G −1.048, completion .016; rank-six G −1.103, completion 0. These are **synthetic label modifications**, not independently sampled task-family generalization.

## Conclusion
REINFORCE learns on-policy reward-driven action preferences in a fixed task; no robust, question-conditioned policy generalization or end-to-end answer correctness is established.
