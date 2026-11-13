# ADR-016 — Retrieval RL Requires Observable Evidence, Fixed Evaluation Protocols, and Strong Baselines

## Status
Accepted (Phase 12 closeout, based on EXP-111–119).

## Context
Phase 12 showed that on-policy REINFORCE can optimize a frozen reward environment but that learned behavior can regress when the supporting evidence changes across families. The same question may need different top-k under BM25 versus Hybrid.

## Evidence
- EXP-117: five seeds, in-sample Cirrus gamma=0.9 return +1.5765 → +2.6722, gold oracle +2.7000. Seed 3 retrieved about 3.05 documents rather than about two.
- EXP-118: five-seed family-disjoint BM25 mean heldout return +1.6573 → +1.7540, delta SD 0.4797; completion 0.7753 → 0.7416. Three of five seeds regressed.
- The strongest fixed K3 scored +2.6000 and completion 1.0000 versus learned +1.7540 and 0.7416. Gold oracle scored +2.7500.
- EXP-119: Phase 11 SFT's `SEARCH_HYBRID_K*` + REFORMULATE and Phase 12 RL's `SEARCH_K*` + STOP are not a shared decision protocol; Phase 11 heldout family differs from Phase 12 heldout group.

## Decision
1. Never put hidden support IDs, oracle actions, reward-derived correctness, or benchmark labels into a policy observation.
2. Separate deterministic reward validation, synthetic stress cases, trained-policy on-policy rollouts, and genuinely held-out tasks in both code and reports.
3. Before any architecture comparison: freeze dataset version, retriever/ranking, action semantics (including STOP/reformulate), training families, evaluation families, metrics, seeds and budget.
4. Compare to fixed baselines and a label-aware diagnostic oracle, report all seeds and per-family outcomes; negative results remain first-class records.
5. Policy-visible question/evidence signals must be constructed **without labels** and audited for leakage. Prefer fresh families for future tests; EXP-118's five heldout families have already been inspected.
6. Do not equate retrieval coverage with answer correctness or convert classification accuracy directly into cumulative RL reward.

## Rejected alternatives
- Declaring a win because training reward improves: heldout failure disproves robust improvement.
- Treating gold-oracle trajectories as agent rollouts: off-policy leakage.
- Reusing synthetic changed labels as independent test tasks.
- Renaming Hybrid actions to BM25 actions to compare LoRA and REINFORCE: differing retriever and termination semantics.
- Scaling immediately to PPO/GRPO: our state and benchmark bottlenecks dominate.

## Consequences
Phase 13 needs a preregistered campaign matrix, task-family provenance, repeatable multi-seed trials and a new evaluation protocol before trying more complex policies. Phase 14 integration depends on these constraints.
