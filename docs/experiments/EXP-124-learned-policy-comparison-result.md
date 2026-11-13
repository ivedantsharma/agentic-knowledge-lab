# EXP-124 Result — Gate A Policy Compatibility Feasibility

## Status
**Gate A source-level audit complete and CI-validated; direct SFT-versus-RL learned-policy comparison BLOCKED.** EXP-124 is **not** yet a completed generalization experiment. No retraining, Qwen model inference, REINFORCE policy inference, or fresh-family validation was performed.

## Reproducibility
GitHub Actions on `main`, run `43505656113`, commit `2a541c10ebd3fa5541706e110b31e16c2f0e19d6`: **439 tests passed in 17.72s**, Ruff **All checks passed**, EXP-120 provenance audit passed, EXP-122 common representation audit passed, and standalone EXP-124 driver **passed as an expected BLOCKED diagnostic**.

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_policy_feasibility_audit.py
```

### Observed input/source SHA-256

| Source file | SHA-256 |
|---|---|
| `data/processed/knowledgebench_v2_hard_documents_v0.json` | `9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be` |
| `data/processed/phase10_routing_pairs_v0.json` | `996514ff172e71756e300a9b43fc189603d14ba914da18e5c7cf12129d014ef2` |
| `data/processed/phase11_policy_dataset_v1.json` | `233e6d83a4607070d9937a3f302c27dd4a243b9373c4b692351a5f560bc3c549` |
| `scripts/run_phase11_class_balanced_lora_sft.py` | `70fe75da9f298407e75f69e5de511ce7a73c4396ffc6c7320a71699732a368b3` |
| `scripts/run_phase12_family_disjoint_transfer.py` | `a04c6763a2420b5a9aee3cbed191b1f225e2188050903a82c15044157c55b0bf` |

### Actual action spaces

Phase 11 SFT:
`SEARCH_HYBRID_K1`, `SEARCH_HYBRID_K2`, `SEARCH_HYBRID_K3`, `SEARCH_HYBRID_K5`, `REFORMULATE`.

Phase 12 RL:
`SEARCH_K1`, `SEARCH_K2`, `SEARCH_K3`, `SEARCH_K5`, `STOP`.

`REFORMULATE` has no RL equivalent and `STOP` has no SFT equivalent. The similarly numbered K actions are **not semantically interchangeable** because the baseline retriever, objective, episode horizon and stopping protocol differ.

### Data and label audit

- SFT examples: **17**; `train=11`, `dev=3`, `heldout=3`.
- Routing tasks: **12**; shared route questions with SFT examples: **12**.
- Supervised families/splits: `atlas_borealis:dev`, `cirrus:train`, `helios_solstice:train`, `nimbus:train`, `orion:train`, `security_meridian:heldout`.
- Among the 12 route labels, **9** SFT Hybrid budget targets happen to equal BM25's smallest sufficient budget, **3 do not**, **0 unmappable** in the route subset. These comparisons are **LABEL ALIGNMENT ONLY**—not learned policy predictions or performance.

### Hard Gate A readiness checks

| Gate | Audit |
|---|---|
| Identical action space | **False** |
| Shared retriever | **False** |
| Shared terminal/STOP protocol | **False** |
| Same heldout split | **False** |
| Genuinely independent new families available in these sources | **False** |
| Two inspected training scripts persist checkpoints | **False** |
| Ready for direct learned comparison | **False** |

The checkpoint persistence test is a **source-code inspection of two named experiment scripts only**. It does not prove that no checkpoints exist in the user's workspace, external storage, or other repository locations.

## Scientific conclusion

**Blocked feasibility gate, not negative trained-model performance.** A fair head-to-head model outcome cannot be inferred by comparing Phase 11 heldout action classification accuracy with Phase 12 on-policy discounted returns. The existing reported RL model also failed to beat fixed BM25 K3 on EXP-118's exposed heldout questions. No hypothesis test or generalization claim is justified.

**Required before Gate C:**
1. Define one frozen, evaluator-safe action/observation/retriever/termination/reward protocol for both policies, including STOP and query reformulation semantics.
2. Source and freeze genuinely new, independent evidence families and split them before training/tuning.
3. Implement checkpoint saving/loading and verified learned-policy inference under the shared protocol.
4. Reevaluate strong fixed baselines and policy controllers across independent training seeds and new families with separately measured answer quality (only when all arms have matched answer generation).

This gate should not be waved through by renaming Hybrid actions to BM25 names, relabeling existing OOD questions as new holdout, or reusing an oracle's evaluator labels as policy input.

## Implementation
- `scripts/run_phase13_policy_feasibility_audit.py` — source hashes, enum/split audit, source-level checkpoint persistence gate.
- `tests/test_phase13_policy_feasibility_audit.py` — real-data checks, duplicate/split leakage rejection, unsupported SFT action rejection, reproducibility and no-false-comparison assertions.
- `docs/experiments/EXP-124-learned-policy-comparison.md` — preregistered later gates.

## Campaign status
EXP-120–123 are finished as scoped research studies. **EXP-124 remains in progress** at Gate A, with unresolved genuine data and protocol prerequisites. EXP-125 is unstarted. Phase 13 core study count therefore remains **4/6 (~67%)**, with two studies plus the Phase 13 final review outstanding.

## Independent user-workspace reproduction

The user additionally ran `uv run python scripts/run_phase13_policy_feasibility_audit.py` and supplied the complete local stdout. **All five source SHA-256 values exactly matched the previously archived CI hashes**, with `17` SFT examples split `train=11/dev=3/heldout=3`, `12` shared routing tasks, `9` matching BM25 minimum-budget labels and `3` mismatches. The six gate checks are all `False`, including `ready_for_direct_learned_comparison=False`. This independently confirms the **comparability blocker** in the user's workspace. It is not evidence of trained-model performance or absence of checkpoints elsewhere.

## Gate B0 — New common BM25 episode protocol: verified

**CI-validated on `main`**: GitHub Actions run `43510455499`, commit `58d13714e9545927481230d2b6549fa6bdce4b80`: **458 tests passed in 20.56s**, Ruff clean, all previous audit steps and the new standalone `run_phase13_shared_policy_contract.py` **PASS**.

This is a **new common execution contract**, not a retroactive conversion of the old SFT policy:

- Identifier: `EXP-124-common-bm25-v0`.
- Reuses the existing BM25 ranking and `RetrievalEpisodeV2` reward semantics; action space `SEARCH_K1/K2/K3/K5` and `STOP`, no `REFORMULATE`; max 6 decisions, `gamma=0.9`.
- The new `ActionPolicy.choose_action(RetrievalObservation)` interface receives only `question, retrieved_ids, requested_k, steps_taken, done`. The hidden supporting IDs enter evaluator/reward logic only.
- Existing `legal_actions` ensures budgets strictly increase and terminal states do not accept actions. Tests reject old SFT action text, repeated K and incorrect action types.
- All fixed K baselines now execute through **the same runtime**; their scores below came from the actual CI driver, not inferred from fake models.

### Measured fixed-control contract smoke test (inspected development tasks only)

`uv run python scripts/run_phase13_shared_policy_contract.py` recomputed BM25 on the **12 existing Phase 10 route questions, 6 already inspected source families**, with frozen source hashes:

- Documents `9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be`
- Routing tasks `996514ff172e71756e300a9b43fc189603d14ba914da18e5c7cf12129d014ef2`

| Gold-blind fixed policy | Mean support recall | Complete support fraction | Mean discounted reward | Mean documents |
|---|---:|---:|---:|---:|
| Fixed K1 | 0.6667 | 0.6667 | +1.5333 | 1.0000 |
| Fixed K2 | 0.9167 | 0.9167 | +2.3833 | 2.0000 |
| **Fixed K3** | **1.0000** | **1.0000** | **+2.6000** | 3.0000 |
| Fixed K5 | 1.0000 | 1.0000 | +2.4000 | 5.0000 |

**Scientific interpretation:** the new mechanics now work, but fixed K3 already retrieves all labeled support at lower average context cost than K5 on these inspected questions. This makes a learned-policy win on the same dataset both difficult to demonstrate and uninformative for external generalization. These fixed policy numbers are consistent with EXP-118, **not a new result about SFT/RL learning**.

### Gate B0 decision / remaining blockers

**PASS: shared action/state/reward/STOP execution interface for future retrained models.**

**NOT DONE:** new SFT model trained on that action protocol, new RL policy trained and checkpointed using the same corpus/reward/splits, checkpoints reloaded for inference, fresh independently sourced test families, 5-seed trial evidence, final answer quality or generalization result.

**EXP-124 stays OPEN**; the six-study Phase 13 progress remains **5/6 (~83%)**, plus final research review. One must never claim the old Phase 11 Qwen policy is now comparable simply because a new shared interface exists.

Reproduce:
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_shared_policy_contract.py
```

## Final disposition — stopped / inconclusive (2026-11-14)

**Status: CLOSED ADMINISTRATIVELY AS BLOCKED / INCONCLUSIVE, NOT COMPLETED AS A LEARNED-POLICY GENERALIZATION EXPERIMENT.** The project's Codespace became unavailable due to billing, and there are no compatible retrained SFT/RL inference checkpoints or genuinely new sealed evidence families. There is no scientific basis for replacing missing measurements with guessed values.

The actually completed Gate B0 common BM25 runtime passed GitHub Actions run `43510455499`: **458 tests passed in 20.56 seconds**, Ruff and source audits succeeded; the fixed-policy development outputs were K1 +1.5333, K2 +2.3833, K3 +2.6000, K5 +2.4000 mean discounted returns, using 12 exposed tasks. The shared `SEARCH_K1/K2/K3/K5/STOP` interface provides a future training contract, **not** valid cross-model comparison. Older SFT and RL policies remain incompatible with that protocol and with one another.

**Outstanding claims, explicitly NOT tested:** unseen-family SFT vs RL recall, advantage over fixed K3, reloaded model checkpoints, five-seed performance on new families, matched final-answer accuracy, training compute, confidence intervals on independent families. Mark these as *not measured*, not failures or successes.

A deliberately **fictional** scenario table for explanatory purposes is stored separately at `docs/experiments/EXP-124-illustrative-hypothetical-simulation-NOT-RESULTS.md`. **Its invented values are not observations, should never be entered in the real results, and must never be used in a resume or application.**

**Reopening conditions:** restore a suitable execution environment; collect genuinely new source families; pre-register sealed family-disjoint splits; train and checkpoint both policies on a single protocol; evaluate alongside strong fixed controls and publish all per-family/seed results. Until those conditions are met, this experiment remains an **inconclusive stopped study**.
