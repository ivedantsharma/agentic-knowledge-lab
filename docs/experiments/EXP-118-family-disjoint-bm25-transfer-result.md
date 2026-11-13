# EXP-118 Result — Real-Family-Disjoint BM25 Transfer

## Setup
BM25 retrieval recomputed consistently from 22 KnowledgeBench documents for 12 routing questions in six evidence families. Train **route-003 only** from Cirrus; reserve route-004 as same-family diagnostic; evaluate ten questions in Borealis, Solstice, Meridian, Nimbus, Orion. Five seeds (0–4); 1600 training / 400 evaluation episodes per seed, gamma=.9. This is **not** the frozen EXP-117 hybrid ranking.

## Validation
The user executed `uv run python scripts/run_phase12_family_disjoint_transfer.py` and supplied the complete numerical result. GitHub CI **366 tests passed**, Ruff passed; ten new tests validated actual data and split.

## Evidence rank
Borealis (2,1); Cirrus (1,1); Solstice (1,3); Meridian (2,2); Nimbus (1,1); Orion (1,1). All reachable by K5.

## Heldout fixed baselines
| Strategy | Mean discounted G | Complete |
|---|---:|---:|
| STOP_NOW | −1.0000 | .0000 |
| FIXED_K1 | +1.2800 | .6000 |
| FIXED_K2 | +2.3200 | .9000 |
| FIXED_K3 | **+2.6000** | **1.0000** |
| FIXED_K5 | +2.4000 | 1.0000 |
| ESCALATE | +2.1413 | 1.0000 |
| Gold oracle (evaluator only) | +2.7500 | — |

## Five-seed transfer
| Seed | Train G before → after | Heldout G before → after | Heldout delta | Completion before → after |
|---|---|---|---:|---|
| 0 | +1.726 → +2.680 | +1.623 → +2.321 | +.698 | .769 → .906 |
| 1 | +1.866 → +2.779 | +1.727 → +1.341 | −.386 | .792 → .622 |
| 2 | +1.791 → +2.688 | +1.659 → +2.320 | +.661 | .774 → .903 |
| 3 | +1.872 → +2.752 | +1.730 → +1.440 | −.290 | .797 → .653 |
| 4 | +1.672 → +2.782 | +1.547 → +1.347 | −.200 | .744 → .623 |

Mean heldout G **+1.6573 → +1.7540**, mean delta **+0.0967**, across-seed delta population SD **0.4797**, completion **.7753 → .7416**; gold oracle gap **0.9960**. Three seeds regressed. For seed 0, Solstice completion was just .535, with mean G +.907.

## Conclusion / limitations
The policy learned training-task budget preferences but **did not robustly transfer** across source families or beat fixed K3. State `(requested_k, steps_taken)` does not encode query semantics or evidence sufficiency. Five seeds and ten related questions do not establish significance or general performance. The heldout families have now been inspected and cannot be reused as pristine test families after tuning.
