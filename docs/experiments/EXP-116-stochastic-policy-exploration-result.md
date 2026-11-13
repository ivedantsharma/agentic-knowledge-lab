# EXP-116 Result Record — Stochastic Exploration

## Configuration
Uniform legal-action sampling and epsilon=0.2 target-K2/K5; 400 seeded Monte Carlo episodes per policy × task × horizon, gamma=0.9. Grounded Cirrus and three explicitly synthetic support variants; max steps 2 vs 6.

## Verified checks
- GitHub Actions: **333 tests passed** and Ruff passed on the merged commit.
- Tests validate action masks, seeded reproducibility, hidden-gold isolation, policy/no-update control, and short-horizon timeout vs impossible default-horizon timeout.
- The user supplied a pytest listing showing the EXP-116 tests passing, but did **not** supply the script's numerical Monte Carlo table.

## Results availability
**Numerical EXP-116 rollout output: not archived / not independently user-confirmed.** No invented coverage, oracle gaps or seed variance figures should be inferred from successful unit tests.

## Reproduce
```bash
uv run python scripts/run_phase12_stochastic_policy_exploration.py
```
Archive the actual stdout before making numerical EXP-116 claims.

## Interpretation
This validates the **exploration infrastructure**, not policy learning. Parameter learning begins in EXP-117. Synthetic labels are stress tests, not heldout knowledge tasks.
