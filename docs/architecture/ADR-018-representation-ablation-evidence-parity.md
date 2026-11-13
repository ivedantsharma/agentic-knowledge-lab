# ADR-018 — Source Parity Is Necessary but Not Sufficient for a Causal Representation Ablation

## Status
Accepted for Phase 13 after EXP-122. Revisit only with controlled cross-representation evaluation on new independent facts.

## Context
Phase 5 hierarchy and Phase 6 graph benchmarks originally used different questions, sources and grading criteria: three long-section evidence tasks versus four claim-path QA tasks. EXP-122 Gate A correctly rejected a comparison of their historical scores.

To remove that dataset confound for a development experiment, Gate B1 projected the 15 original Phase 6 claim evidence references losslessly into flat evidence units and 11 subject-grouped hierarchy documents containing 15 sections, preserving all evidence and original four questions. Gate B2 returned no more than three original evidence atoms per query for flat BM25, existing hierarchical Dense+CrossEncoder, and native graph QA.

## Measured evidence
User-reported full-model Gate B2 results:

| System | Mean gold claim coverage | Tasks fully supported | Mean atoms returned | Mean context words |
|---|---:|---:|---:|---:|
| Flat BM25 | 0.6250 | 1/4 | 3.0 | 34.75 |
| Hierarchical | 0.7500 | 2/4 | 3.0 | 38.75 |
| Native graph | 1.0000 | 4/4 | 2.5 | 35.00 |

Native graph separately produced correct answers and claim paths in 4/4 tasks. This is not matched answer generation because flat and hierarchy only return evidence.

## Decision
1. Treat EXP-122 as a reproducible **same-source, same-question, capped-output system-level comparison** and not a causal estimate of representation alone.
2. Preserve negative findings about unrelated historical tasks and explicit source/evidence mapping; do not compare mismatched benchmarks.
3. Track output budget and computational work separately. A graph-ranked-path count, BM25 scored-document count and hierarchy's aggregate parent/section/chunk scores are not equivalent units of compute; no latency superiority can be asserted.
4. Graph edges, model/ranker differences, and the graph-oriented questions are acknowledged confounds. In particular, graph performance on these existing tasks cannot establish external generalization.
5. A future representation-only ablation should use independently sourced facts and tasks; the same scorer or matched retrieval/reasoning budget wherever possible; provenance-preserving transforms; and separate answer-quality and evidence metrics.
6. Strong architecture claims require multiple independent evidence families, negative controls and uncertainty estimation based on real independent units.

## Rejected interpretations
- “Graph beats flat and hierarchy universally”: only four graph-derived development questions were evaluated.
- “The representation alone caused a 37.5-point gain”: ranking algorithms, edge navigation and downstream answer behavior differ.
- “Graph is cheapest”: candidates_scored are incomparable across system internals; no timed latency benchmark exists.
- “Graph has 100% versus other models' answer accuracy”: no flat/hierarchy answer generation was run.
- “The benchmark is heldout”: the source/tasks were already inspected and reused from Phase 6.

## Consequences
EXP-122 closes as a carefully scoped system-level result. EXP-123 must use a common search tool, consistent task sets and explicit call-budget controls to make static-vs-agentic search claims. See:
- `docs/experiments/EXP-122-knowledge-representation-ablation-result.md`
- `docs/experiments/EXP-123-static-vs-agentic-search.md`
- `docs/research/phase13-campaign-plan.md`
