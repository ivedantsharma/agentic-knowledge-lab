# EXP-114 — Reward v2 Trajectory-Wide Counterfactual Sweep

## Question
Does Reward v2 treat incomplete forced timeouts consistently with explicit premature STOP across *every* legal increasing search prefix, rather than only a single example?

## Design
- Freeze original Cirrus `route-003` question, ranking and gold supporting document.
- Enumerate all 15 nonempty ordered increasing subsequences of K1, K2, K3, K5.
- For every prefix, compare v1 forced timeout, v2 forced timeout and v2 explicit STOP immediately after the same prefix.
- Evaluate one grounded case plus three **synthetic** support-label stress cases; do not aggregate them as benchmark performance.
- Gold labels remain evaluator-only.

## Metrics/invariants
Coverage, retrieved-document cost, conflicting exposure, total reward, incomplete versus complete termination, whether an explicit STOP occurred. An incomplete timeout must have the same v2 return as a premature STOP after an identical prefix. A complete timeout does not receive an explicit STOP bonus.

## Reproduce
```bash
uv run python scripts/run_phase12_reward_v2_trajectory_sweep.py
```
See `EXP-114-reward-v2-trajectory-sweep-result.md` for observed results.
