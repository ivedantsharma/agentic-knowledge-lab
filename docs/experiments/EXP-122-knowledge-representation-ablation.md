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


## Gate B1 — Common source/evidence contract (implementation)

After Gate A identified incompatible historical tasks, Gate B starts by **reusing exactly one pre-existing source**: the Phase 6 branching claim graph and its four original graph traversal tasks. This is a development/reuse experiment, NOT a new independent heldout dataset.

- `knowledgebench/datasets/representation_bridge.py` derives flat evidence atoms and subject-grouped hierarchy sections from the **same** original `ClaimGraph.claims[].evidence[]` references, preserving each exact evidence string and source document ID. No new facts or task questions are written.
- Flat entries are keyed by a stable `claim_id#index` evidence atom ID with the claim relation as a retrieval header; hierarchical sections preserve the same relation header and original evidence text.
- Native graph uses the unmodified claims and graph edges. Structural navigation differs intentionally, and must be discussed as an information/inductive-bias distinction; comparable evidence text alone is not equal representation capacity.
- `scripts/run_phase13_common_representation_contract.py` validates parity and prints source SHA-256, task and evidence atom counts.
- `tests/test_phase13_representation_bridge.py` tests one-to-one source span preservation, references, task path continuity/terminal answer, and fail-closed malformed task gold. Task gold is only used for contract verification, never added to flat/hierarchical retrieval inputs.

**Gate B1 acceptance:** each source evidence reference maps one-to-one into flat and hierarchy; shared task question/answer list remains unchanged; validation rejects corrupt tasks. This makes future *paired queries possible*, but is not yet a fair model outcome comparison.

**Gate B2 still to do:** run the actual flat, hierarchy and graph systems on exactly the four same questions, with a clearly defined equal **evidence-unit/context budget** and per-action resource accounting. Gold claim evidence coverage can be measured after retrieval; answer correctness and search latency must not be inferred from coverage. If the existing hierarchical tool's document→section→chunk scoring makes a unit-equivalent comparison impossible, explicitly report the mismatch instead of claiming architecture superiority.

The native graph data and questions were designed together. Even with a valid paired dataset, this is a **development benchmark with graph-favorable inductive bias**; collect additional source-independent cases before external generalization claims.


## Gate B2 — preregistered system-level paired comparison (development-only)

Gate B1 source parity passed. For the first measured run, use the same four existing graph-derived questions and unchanged 15 evidence atoms for every method:

| System | Implementation | Search/output budget |
|---|---|---|
| Flat lexical retrieval | existing `BM25Retriever` on 15 source evidence atom texts | top **3 evidence atoms** |
| Hierarchical | existing `CoarseToFineHierarchicalRetriever`; all **11** parent documents available to avoid parent-beam exclusion, cross-encoder reranks all eligible sections; chunk-size large enough to retain each full single-evidence section | top **3 evidence sections/windows** |
| Native claim graph | existing `ClaimGraphQAEngine` + `SemanticGraphPathRanker`, explicit entity resolution and max_hops=3 | **one** chosen path with up to **3 claims/evidence atoms** |

Primary measured metric is **gold claim-evidence coverage at the common maximum of three source atoms** and fraction of fully covered tasks. Record actual output evidence atom count and output text word count for all methods, and candidate scoring counts/tool stages separately. The graph path may return only 2 atoms when the answer is two hops, so do not equate output K=3 with actual compute.

Secondary metric: native graph's independently evaluated *answer exact match*, claim-path match, and provenance; **not** a cross-system answer-accuracy comparison because flat/hierarchy provide evidence and have no matched answer generator. Report failures from missing entity resolution, missing evidence, incomplete windows, or excessive output.

**Critical scope:** Flat BM25, hierarchical Dense+CrossEncoder and graph semantic path ranker use different ranking methods and index schemas, so differences cannot be attributed *causally* to knowledge representation alone. Graph questions were authored for the graph substrate. This is a controlled **same-task, same-evidence, capped-output system comparison** and feasibility assessment; a pure architecture ablation requires fixed ranking/evidence selection and aligned reasoning and model access across variants.

Models are frozen `sentence-transformers/all-MiniLM-L6-v2` and `cross-encoder/ms-marco-MiniLM-L6-v2` (no finetuning), current installed revisions may vary. Golden task claims are held only by the scoring/evaluation module and not by the retriever. Gold claims are joined to evidence atoms *after* rankings are returned.

**Stop criteria:** fail if evidence atoms are duplicated/omitted, hierarchy returns partial evidence under the full-section setting, graph result cannot be mapped to source evidence, retrieved evidence exceeds the 3-atom output budget, or source SHA-256 drifts. If one variant cannot run within the contract, report the blocker rather than scoring an incomparable run.
