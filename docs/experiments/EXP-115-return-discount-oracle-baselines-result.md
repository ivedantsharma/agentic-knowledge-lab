# EXP-115 Result — Discount, Fixed Retrieval and Gold Oracle

## Configuration
Frozen Cirrus hybrid ranking; one grounded case and three clearly synthetic stress cases. Six fixed policies, 16 legal default-horizon terminal paths, gold-aware diagnostic oracle, gamma 1.0 and 0.9.

## Validation
The user ran `uv run pytest` (**314 passed in 14.43s**), `uv run ruff check .` (passed), and `uv run python scripts/run_phase12_return_oracle_baselines.py` successfully.

## Results
| Case | Gold oracle actions | Oracle G gamma=1 | Oracle G gamma=.9 | Fixed K2 gamma=1 | Fixed K5 gamma=1 |
|---|---|---:|---:|---:|---:|
| Cirrus grounded | K2 → STOP | +2.80 | +2.70 | +2.80 | +2.50 |
| Synthetic two-support | K5 → STOP | +4.50 | +4.40 | +0.80 | +4.50 |
| Synthetic late-support | K5 → STOP | +2.50 | +2.40 | −1.20 | +2.50 |
| Synthetic rank-six | STOP | −1.00 | −1.00 | −1.20 | −1.50 |

Unreachable support cannot be recovered at K5. Discounting changes timing/credit assignment but is not measured wall-clock latency. The oracle reads hidden labels for evaluation **only**.

## Conclusion
A well-defined gold-aware upper bound and simple fixed baselines are available. Cirrus fixed K2 matches the oracle; adaptive RL must beat strong fixed strategies on valid heldout tasks to establish added value. Evidence coverage is not final answer correctness.
