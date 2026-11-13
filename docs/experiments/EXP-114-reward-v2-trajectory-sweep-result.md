# EXP-114 Result — Reward v2 Trajectory-Wide Validation

## Validation observed in workspace
60 timeout/STOP counterfactual pairs validated: 15 prefixes × four cases. Full pytest and Ruff passed in the user-provided run (prior to EXP-115).

| Case | Kind | Prefixes | Incomplete | Complete | Partial coverage |
|---|---|---:|---:|---:|---:|
| cirrus_grounded | actual benchmark gold | 15 | 1 | 14 | 0 |
| synthetic_two_support | synthetic stress | 15 | 7 | 8 | 6 |
| synthetic_late_support | synthetic stress | 15 | 7 | 8 | 0 |
| synthetic_out_of_budget | synthetic stress | 15 | 15 | 0 | 0 |

All cases exposed the conflicting document in their tested nonempty prefixes.

## Invariants
- Incomplete Reward v2 timeout = explicit premature STOP after the **same** prefix.
- Complete Reward v2 timeout retains v1 return; complete STOP receives +1.
- With maximum search K5, rank-6 support is unreachable.

## Limits
Three synthetic configurations are not independently sampled benchmark evidence or learned RL behavior. The counterfactual sweep does not measure model answer quality or optimize policies.

## Reproduce
`uv run python scripts/run_phase12_reward_v2_trajectory_sweep.py`.
