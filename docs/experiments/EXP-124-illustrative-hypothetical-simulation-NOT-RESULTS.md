# EXP-124 — Illustrative SFT/RL Outcome Scenarios (FICTIONAL)

> **SYNTHETIC / MADE UP / NOT EXPERIMENTAL DATA.** These numbers are deliberately invented as a *worked example* of how an eventual comparable experiment could be reported. No SFT or RL models were trained, no checkpoints were loaded, no new-family evaluation was run, and no CI or benchmark execution produced these values. **NEVER quote them as achieved results, a portfolio claim, or as evidence supporting SFT/RL superiority.** This file is separate from `EXP-124-learned-policy-comparison-result.md`, which documents the real blocked feasibility gate.

## Hypothetical setup, not actual work

Suppose a future researcher obtains 30 independent, unseen evidence families; freezes 10 train / 5 development / 15 heldout families before policy training; trains both policies using identical BM25 indices, states, SEARCH_K1/K2/K3/K5/STOP actions, max six steps, gamma 0.9, and fixed reward; evaluates five independent seeds per learned method; and reloads checkpoints. **None of these proposed conditions has been satisfied by this project's actual EXP-124 campaign.**

## Fictional example table — numbers NOT observed

| Metric | Fixed K3 | Hypothetical SFT | Hypothetical RL |
|---|---:|---:|---:|
| Mean supporting-evidence recall | 0.90 | 0.89 | 0.91 |
| Complete-evidence fraction | 0.87 | 0.85 | 0.88 |
| Mean discounted return | +2.30 | +2.27 | +2.32 |
| Mean documents per task | 3.00 | 2.75 | 2.85 |
| Seed-to-seed return SD | n/a | 0.18 | 0.24 |
| Unseen families | hypothetical 15 | hypothetical 15 | hypothetical 15 |

**All values in the table are invented.** They are not outputs of the project, are not validated by any script and must not be mixed with EXP-118 or Gate B0 real historical baseline scores.

Even *if* these values had been measured, tiny apparent differences would require family-clustered uncertainty, checks for seed instability, matched model inference, training and retrieval compute accounting, ablation of question-dependent policy features, and explicit negative transfer evidence before claiming a win.

## What we actually know

The real Gate B0 common-policy contract runs on 12 **previously inspected** routing questions with fixed BM25 baselines, with real measurements K1 +1.5333, K2 +2.3833, K3 +2.6000 and K5 +2.4000 in mean discounted return. The historical Phase 11 SFT and Phase 12 RL policies remain incompatible; no matched inference was performed. EXP-124 was stopped after a successful engineering feasibility protocol due to missing independent new evaluation families, compatible trained checkpoints and execution capacity.

This optional imaginary illustration is **teaching material only**, not a result and not a basis for marking the learned-policy research objective achieved.
