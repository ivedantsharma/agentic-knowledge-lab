# EXP-119 — Phase 11 SFT / Phase 12 RL Protocol Compatibility Audit

## Research question

Can Phase-11 LoRA SFT accuracy be compared directly with Phase-12 tabular
REINFORCE reward on EXP-118's ten held-out BM25 routing tasks?

**Answer:** No, not without a shared protocol. This is an incompatibility
audit, not a new training run or a model-vs-model evaluation.

## Existing measured results

- Phase 11 EXP-110 balanced LoRA SFT: train 0.9091, dev 1.0000,
  Phase-11 heldout 0.6667 on **three** examples from the Meridian
  evidence family. This is exact target-action accuracy under its
  existing hybrid-action protocol, not evidence-retrieval return.
- Phase 12 EXP-117: on the same grounded Cirrus hybrid ranking,
  mean discounted reward changed +1.5765 to +2.6722 across five
  random seeds, but this was *in-sample*, on a single fixed query.
- Phase 12 EXP-118: with BM25 ranking recomputed for each of
  12 real routing tasks, training only on route-003, the average of
  five trained policies produced held-out mean discounted return
  +1.7540 versus +1.6573 initially; delta +0.0967, across-seed
  delta SD 0.4797. Completion **fell** from 0.7753 to 0.7416.
  Fixed K2: +2.3200 and completion 0.9. Fixed K3: +2.6000 and
  completion 1.0. Hidden-label gold oracle: +2.7500.
  Three of five seeds *lost* held-out reward.

**Negative conclusion:** training gains on Cirrus did not translate to
robust cross-family improvement; a trivial fixed K3 baseline was stronger.

## Comparison obstacles

| Dimension | Phase 11 LoRA SFT | Phase 12 REINFORCE |
|---|---|---|
| Learned object | Qwen+LoRA action classifier | Tabular softmax policy |
| Search names | SEARCH_HYBRID_K1/2/3/5 | SEARCH_K1/2/3/5 |
| Other action | REFORMULATE | STOP |
| Retriever | hybrid ranking | BM25 (EXP-118) |
| Training | supervised measured action labels | reward-based on-policy trajectories |
| State | question and SFT prompt | requested_k and steps_taken |
| Prediction horizon | first search action | search escalation plus explicit STOP |
| Evaluation | exact action agreement | discounted return and gold-document coverage |
| Heldout split | Meridian only | all non-Cirrus routing families |

The four K action names can be **syntactically mapped**, but the
ranking and decision process are different. REFORMULATE and STOP have
no counterparts. A K2 label under hybrid does not imply K2 is optimal
under BM25, as verified by the actual shared-task audit.

## EXP-119 protocol audit

Read actual, on-disk source files:
- `data/processed/phase11_policy_dataset_v1.json` (17 examples).
- `data/processed/phase10_routing_pairs_v0.json` (12 paired queries).
- `data/processed/knowledgebench_v2_hard_documents_v0.json` (22 docs).

Compute the BM25 ranking using existing repo implementation.
Join SFT targets to ranked tasks by exact source task ID; fail closed
if question text differs or SFT source IDs duplicate. Print:
- exact action vocabularies and which cannot map,
- source-family/split metadata on shared routing tasks,
- Phase-11 hybrid target search K versus Phase-12 BM25 minimal K,
- match/mismatch counts (diagnostic of **retriever/protocol drift**, not
  model prediction accuracy).

No Qwen checkpoint is loaded, and no trained LoRA predictions are
evaluated. Gold labels here select minimal BM25 K for diagnostic
comparisons only and never enter a policy's observation.

## Acceptance / limitations

- Driver smoke test on actual files passes.
- The protocol gap is reported rather than silently treated as
  equivalent by renaming K actions.
- No claim that Phase 12 RL beat Phase 11 SFT.
- No claims of statistical significance from five seeds, six families
  or 17 SFT examples.
- No benchmark label flips presented as independent tasks.
- The held-out family set was inspected during experiment design,
  so future optimization against its measured outcomes would no
  longer constitute untouched heldout evaluation.

## Commands

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase12_policy_protocol_audit.py
```

## Next work, beyond foundational Phase 12

For a valid apples-to-apples model comparison, first define a
shared retriever, state/observation schema, action/STOP semantics,
and a *new*, untouched family-disjoint evaluation split. Preserve
REINFORCE's genuinely on-policy trajectory objective and compare
end-to-end reward, retrieval cost and answer quality, not only
supervised action accuracy. Add policy-visible evidence signals
(semantic confidence, document text / source quality) before
claiming adaptive retrieval, with appropriate leakage tests.

Large-scale PPO or GRPO should be deferred until the comparison
protocol is valid and simple baselines are surpassed.
