# EXP-122 — Knowledge Representation Ablation: Comparable Benchmark First

## Research question
Under the **same** queries, evidence sources, evaluation metrics and resource budget, how much do flat text, hierarchical navigation, and claim/evidence graph representations contribute to evidence retrieval and grounded answers?

## Motivation / critical feasibility gate
Phase 5's integrated hierarchical pipeline evaluates **three** long-section document tasks using evidence retention and returned window word count:
- `data/processed/phase5_long_section_documents_v0.json`
- `data/processed/phase5_long_section_tasks_v0.json`
- `scripts/run_phase5_final_hierarchical_benchmark.py`
- `knowledge_engine/retrieval/coarse_to_fine.py`

Phase 6's claim graph evaluates **different** graph traversal tasks using entity resolution, path/answer accuracy and provenance:
- `data/processed/phase6_branching_claim_graph_v0.json`
- `data/processed/phase6_graph_tasks_v0.json`
- `scripts/run_phase6_end_to_end_graph_qa.py`
- `knowledge_engine/graph/qa.py`

Their published metrics CANNOT be compared directly: the task populations, source representation, success definitions and model dependencies differ. Phase 5's reported 1.0 evidence retention over 3 tasks is **not** comparable to Phase 6's 1.0 on 4 explicit-entity QA cases or 0.5 on 6 harder stress cases.

## Preregistered stages

### Gate A — Auditable common substrate
1. Inventory exact document/task IDs, content hashes, label provenance and source families for the Phase 5 and Phase 6 experiments, with no invented crosswalks.
2. Verify which underlying facts can be expressed *without changing information content* in flat documents, document/section/chunk hierarchy, and claim graph.
3. Determine whether the existing datasets support a **paired** cross-representation experiment. If not, **STOP rather than compare unrelated scores**; create an independently sourced common evaluation set and frozen mapping first.
4. Track leakage if the same fact occurs in both training and evaluation; existing benchmark families are development material, not pristine heldout data.

### Gate B — Equal-budget controlled ablation (only if Gate A succeeds)
- Independent variable: representation (flat vs hierarchical vs claim graph).
- Controlled: same source facts, questions, gold evidence spans/claims, source provenance, retrieval budget definition, query resolution, encoder/re-ranker model revisions, and compute limits.
- Reuse exact existing retriever and graph modules rather than replacing them with bespoke scoring rules.
- Metrics: gold evidence success/coverage, end-to-end answer accuracy (where all systems support it), provenance correctness, context token/word counts, per-query latency when controlled, abstention and per-family failure mode.
- Where retrieval units differ, expose both **evidence coverage at matched context budget** and actual scorer/tool cost instead of equating K=2 windows to K=2 graph hops.
- Evaluate with multiple independent evidence families. Bootstrap/resample at family level and report the limited sample count.

## Hypotheses
1. Hierarchy may retain needed spans using fewer returned words than full-document retrieval, but parent-routing errors can reduce coverage.
2. A graph can improve explicitly relational multi-hop tasks if entity resolution succeeds, but errors in entity linking/abstention may dominate.
3. No single representation is guaranteed to win all task categories; knowledge transformation and evaluation parity may be the limiting factor.
4. The existing Phase 5/6 benchmark scores are not enough to estimate causal representation advantages.

## Controls / forbidden conclusions
No direct performance claim from Phase 5 vs Phase 6 historical percentages. No oracle entity identification for one variant while forcing automatic entity linking for another. No graph populated with gold task answers and then treated as independent evidence. No newly fabricated 'heldout' examples from paraphrased old facts.

## Initial next task
Implement the Gate A source/provenance/substrate audit, archive its actual output as `EXP-122-knowledge-representation-ablation-result.md`, then decide on a valid Gate B design. If a common substrate cannot be established, report the blocked comparison as a valid negative feasibility result rather than silently changing benchmarks.

## Phase 13 progress
EXP-120 completed; EXP-121 completed; EXP-122 protocol started. The six-gate Phase 13 campaign remains **2 of 6 completed (~33%)** until a justified EXP-122 evaluation is finished.
