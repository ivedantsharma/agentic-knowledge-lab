# ADR-020 — Do Not Optimize Retrieval Recall Without Tracking Evidence Risk

## Status
Accepted after measured Phase 13 EXP-125; applies to future knowledge engine design and portfolio claims.

## Problem
K-expanded retrieval can recover missing gold evidence yet simultaneously insert stale, misleading, contradictory or distracting documents into downstream context. Recall-only selection of K or a retrieval architecture can hide these tradeoffs.

## Evidence: EXP-125
Observed on 22 previously inspected documents, ten KnowledgeBench v2 hard tasks, six answerable, four unanswerable, three fixed methods at K1/K3/K5. Evidence labels were evaluator-only, MiniLM real inference was run by the user.

| Retriever | Mean Recall@3 | Mean Recall@5 | Fully supported at K5 |
|---|---:|---:|---:|
| BM25 | **0.7778** | 0.7778 | 4/6 |
| Dense MiniLM | 0.7500 | 0.8611 | 4/6 |
| Hybrid RRF | 0.6944 | **0.8889** | 5/6 |

At K5 Hybrid returned labeled distractors on **2/2 applicable tasks**, contradictions on **2/2**, and stale documents on **3/3**. BM25, Dense and Hybrid all retrieved documents for all unanswerable questions; **none attempted an abstention decision**. Four Phase 9 injection cases were inventoried but no paired model responses were measured.

## Decision
1. Keep *support coverage* and *misleading-source exposure* as separate core KPIs; K optimization must consider both.
2. Conditional risk denominators must be explicit; do not divide distractor, contradiction or stale rates by all tasks if only some are labeled.
3. Evaluate temporal status, conflicting claims, provenance trust, and ambiguity before a downstream controller treats retrieval as sufficient for answering.
4. Do not assume that returning more documents improves answer quality; measure answer-generation grounding, correctness and abstention with one matched answer system where possible.
5. For unanswerable questions, nonempty retrieval is NOT a failed abstention, and retrieving two ambiguity candidates is NOT successful disambiguation.
6. Prompt injection resilience requires paired clean/injected model inference, not a count of injection case files.
7. Research conclusions remain **development-only** until verified on genuinely independent evidence families, with proper experimental uncertainty.

## Rejected alternatives
- Promote Hybrid unconditionally: BM25 has better Recall@3; at K5 Hybrid has pervasive risk exposure.
- Use retrieval-only outcomes to assert better answer correctness, lower attack success, or safe refusals: these endpoints weren't evaluated.
- Maximize K without resource or evidence-quality constraints: cost and misleading-context effects are not controlled.
- Report population-level confidence from ten previously inspected related tasks: no independent-family sampling basis.

## Consequences
EXP-125 closes as a measured retrieval-only robustness study. EXP-124 remains independently blocked and is not satisfied by these results. Phase 14 should combine source-aware evidence verification, contradiction/temporal handling, explicit abstention and matched answer-quality evaluation with the frozen retrieval baselines. Results: `docs/experiments/EXP-125-hard-robustness-result.md`.
