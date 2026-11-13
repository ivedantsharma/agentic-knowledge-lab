# EXP-124 — Learned Retrieval Policy Comparison: Compatibility and Generalization Gates

## Status
**Preregistered; protocol feasibility only. No new training, model inference or generalization scores have been generated.** This follows EXP-123's observed OOD first-action failure and EXP-118's negative transfer evidence.

## Research question
Under a *single fixed retrieval/control protocol* and truly uninspected source families, can SFT or RL retrieval policies improve quality/cost over strong static K3/K5 and simple adaptive baselines? How robustly across seeds and families?

## Prerequisites and evidence
- Phase 11 LoRA policy (Qwen2.5-0.5B-Instruct): `SEARCH_HYBRID_K1,K2,K3,K5` plus `REFORMULATE`; action classification on 17 examples, train/dev/heldout splits 11/3/3.
- Phase 12 REINFORCE policy: `SEARCH_K1,K2,K3,K5` plus `STOP`; sequential reward environment, `(requested_k,steps_taken)` policy state without semantic question features.
- EXP-119: retriever, action, horizon, stopping and heldout splits incompatible. Mapping K names doesn't make policies equivalent.
- EXP-118: fixed BM25 K3 heldout reward +2.6000, evidence completion 1.0000; five-seed learned RL mean +1.7540, completion .7416. Three of five seeds regress.
- EXP-123: handcrafted rule planner fails on `ood-001` before a search. This strengthens the need for a safe search fallback and an OOD family audit; **not** evidence for RL/SFT superiority.

## Gate A — Common data/control contract (must be passed before comparison)
1. Version and hash the existing source files and inspect exact action vocabularies, policy observation/state construction, checkpoint format, inference code, retrieval ranker, reward model, STOP/REFORMULATE semantics and split exposure.
2. Define one frozen **shared** retrieval engine and ranking (BM25 or Hybrid, not mixed); action set, allowed transitions, query/retrieval observations, total query/document budgets and terminal conditions. If STOP and REFORMULATE remain incomparable, replace both with a new shared policy interface and retrain; never quietly relabel old actions.
3. Gold support IDs/expected answers are evaluator-only. Policy-visible question text and evidence have provenance and a leakage audit.
4. Require **inference checkpoints** and the ability to execute each policy end-to-end on the same tasks. Do not mistake SFT training-label action accuracy for an online RL return.
5. Include identical fixed K1/K2/K3/K5, a simple query-independent budget policy, a rule/fallback baseline, and a gold-aware diagnostic oracle kept evaluator-only.

## Gate B — Actual independence of test families
- Cirrus is Phase 12 training; Borealis/Orion/Nimbus/Solstice/Meridian have been used or inspected in Phase 11–13. The Phase 4 OOD intent `ood-001` was also examined in EXP-123. These are **not** untouched test units.
- Create truly independent source-family groups with auditable source provenance, no reused facts/near-duplicate supporting documents, and a heldout split frozen **before** training or hyperparameter selection.
- If new evidence families cannot be sourced, EXP-124 **stops at feasibility**; descriptive development results may be reported but no generalization claim or training leaderboard can be promoted.

## Gate C — Measured comparison (only if A/B pass)
- Train/finetune policies to the same action/observation/reward and retriever contract, using comparable compute budgets where possible.
- Run >=5 independently seeded policy training trials. Save checkpoints/manifests, seed-specific task outcomes and all retrieval/STOP actions.
- Report full gold evidence coverage, mean discounted return, context/tool cost, explicit stop quality, unanswerable/abstention where task supports it, and **final-answer correctness only if a matched answer generator runs for all**.
- Compare per-family distributions and cluster-aware uncertainty. Never treat paraphrases as statistically independent.

## Stop conditions
- Different source rankers or reward models across evaluated policies.
- No usable checkpoints or policy inference implementation under a common action space.
- No independently sourced evaluation families.
- Gold-support shortcuts in policy state/inputs.
- Claiming Qwen SFT classification accuracy predicts RL return or that tabular RL generalizes from known-family reward.

## Initial implementation step
Audit the repo's real policy/checkpoint code and gather dataset provenance, then write the **actual gate-A measured feasibility result** in `docs/experiments/EXP-124-learned-policy-comparison-result.md`. Do not run new large-scale training or turn inspected families into fake heldout.

## Phase progress
EXP-120–123 complete (4/6 planned studies, roughly 67%). EXP-124 and EXP-125 remain, followed by Phase 13 final review. An honest blocked feasibility study is a useful research outcome, but it is not proof of learned-policy success.
